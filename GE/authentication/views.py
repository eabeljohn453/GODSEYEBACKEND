from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .models import CustomUser, ThreatMessage , DetectionHistory # Ensure CustomUser extends AbstractUser
import cv2
from .models import Detection, ThreatMessage 
from django.http import StreamingHttpResponse
from ultralytics import YOLO  # YOLOv8 Model

# Load YOLOv8 Model (Ensure it detects only knives and guns)
model = YOLO("yolov8n.pt")  # Load YOLOv8 model

# Set CCTV RTSP Stream (Change to actual stream if needed)
video_source = 0  


@login_required
def admin_dashboard(request):
    detection_history = DetectionHistory.objects.all().order_by('-detected_at')
    messages = ThreatMessage.objects.all().order_by('-created_at')

    return render(request, 'authentication/admin.html', {
        'detection_history': detection_history,
        'messages': messages,
        'user': request.user  # Pass the logged-in user
    })

def dashboard_view(request):
    # Fetch recent detections
    detection_history = Detection.objects.order_by('-detected_at')[:10]
    
    # Fetch messages only if there are detected threats
    messages = ThreatMessage.objects.filter(threat_detected=True) if detection_history else []

    context = {
        'detection_history': detection_history,
        'messages': messages
    }
    return render(request, 'admin_dashboard.html', context)

# Function to send alert and store message in session
def send_alert(threat_detected, request):
    threat_message = f"A {threat_detected} was detected in the CCTV feed. Please check immediately."

    # Append to threat messages list in session
    if 'threat_messages' not in request.session:
        request.session['threat_messages'] = []
    request.session['threat_messages'].append(threat_message)

    # Save to the database
    save_threat_message(threat_message)

    print(f"🚨 Threat detected: {threat_detected}, message saved.")

# Save Threat Message to Database
def save_threat_message(message):
    try:
        ThreatMessage.objects.create(message=message)
        print("✅ Threat message saved:", message)  # Debugging log
    except Exception as e:
        print(f"❌ Error saving message: {e}")

# Streaming Video with Object Detection (Knife & Gun Only)
def generate_frames(request):
    camera = cv2.VideoCapture(video_source)  # Connect to CCTV

    while True:
        success, frame = camera.read()
        if not success:
            break

        # Perform YOLO object detection
        results = model(frame)

        # Process detected objects
        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])  # Object Class ID
                conf = float(box.conf[0])  # Confidence Score
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding Box

                # Get class label
                class_label = model.names[cls]

                # Detect Only Knives & Guns
                if class_label in ["knife", "gun"]:
                    color = (0, 0, 255)  # Red for threats
                    label = f"{class_label} ({conf:.2f})"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                    # 🚨 Send Alert 🚨
                    send_alert(class_label, request)

        # Convert frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# History View
def history_view(request):
    detection_history = ThreatMessage.objects.all()
    return render(request, 'history.html', {'detection_history': detection_history})

# Fetch Latest Threat Message
def latest_threat_view(request):
    latest_threat_message = ThreatMessage.objects.order_by('-created_at').first()
    return render(request, 'your_template.html', {'latest_threat_message': latest_threat_message.message if latest_threat_message else None})

# Video Streaming Route
def video_feed(request):
    return StreamingHttpResponse(generate_frames(request), content_type='multipart/x-mixed-replace; boundary=frame')

# Login View
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')  # Fetch email from form
        password = request.POST.get('password')

        print(f"Attempting login for: {email}")  # Debugging
        user = authenticate(request, username=email, password=password)  # Change username → email

        if user is not None:
            print(f"Login successful for: {user.username}, Type: {user.user_type}")  # Debugging
            login(request, user)

            if user.user_type == 'admin':
                return redirect('/auth/admin/')
            else:
                return redirect('/auth/user/')
        else:
            print("Login failed: Invalid credentials")  # Debugging
            messages.error(request, "Invalid username or password")

    return render(request, 'authentication/login.html')

# Admin View
@login_required(login_url='login')  # Ensure only logged-in users can access
@never_cache
def admin_view(request):
    if request.user.user_type != 'admin':
        messages.error(request, "Access denied. Admins only.")
        return redirect('user_dashboard')

    threat_messages = ThreatMessage.objects.all()
    return render(request, 'authentication/admin.html', {'threat_messages': threat_messages})

# User Dashboard View
@login_required(login_url='login')
@never_cache
def user_view(request):
    if request.user.user_type != 'user':  
        return redirect('/auth/admin/')  
    return render(request, 'authentication/user.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')