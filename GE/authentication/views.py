from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import JsonResponse, StreamingHttpResponse
from django.contrib.auth.hashers import make_password
from .models import CustomUser, ThreatMessage, DetectionHistory, Detection
import cv2
from ultralytics import YOLO  # YOLOv8 Model

# Load YOLOv8 Model (Ensure it detects only knives and guns)
model = YOLO("yolov8n.pt")  # Load YOLOv8 model
video_source = 0  # Set CCTV RTSP Stream (Change to actual stream if needed)


def add_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Ensure no duplicate users
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"error": "User with this email already exists"}, status=400)

        # Create user
        user = CustomUser.objects.create(
            username=email,  # Use email as username
            email=email,
            password=make_password(password),  # Hash password for security
            user_type="user"  # Ensure it's a regular user, not admin
        )

        return JsonResponse({"message": "User added successfully"})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

# 🔹 Fetch and return the list of users in JSON format


def users_list(request):
    users = CustomUser.objects.filter(user_type="user").values("id", "username", "email")  # Exclude admins
    return JsonResponse({"users": list(users)})


@login_required
def admin_dashboard(request):
    detection_history = DetectionHistory.objects.all().order_by('-detected_at')
    messages = ThreatMessage.objects.all().order_by('-created_at')
    return render(request, 'authentication/admin.html', {
        'detection_history': detection_history,
        'messages': messages,
        'user': request.user
    })

def dashboard_view(request):
    detection_history = Detection.objects.order_by('-detected_at')[:10]
    messages = ThreatMessage.objects.filter(threat_detected=True) if detection_history else []
    return render(request, 'admin_dashboard.html', {'detection_history': detection_history, 'messages': messages})

def send_alert(threat_detected, request):
    threat_message = f"A {threat_detected} was detected in the CCTV feed. Please check immediately."
    ThreatMessage.objects.create(message=threat_message)
    print(f"🚨 Threat detected: {threat_detected}, message saved.")

def generate_frames(request):
    camera = cv2.VideoCapture(video_source)
    while True:
        success, frame = camera.read()
        if not success:
            break

        results = model(frame)
        for result in results:
            for box in result.boxes:
                cls = int(box.cls.item())
                conf = float(box.conf.item())
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                class_label = model.names[cls]
                if class_label in ["knife", "gun"]:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, f"{class_label} ({conf:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    send_alert(class_label, request)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
def manage_users(request):
    users = CustomUser.objects.all()  # Fetch users from CustomUser model
    return render(request, 'manage_users.html', {'users': users})
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delete_users(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_ids = data.get("users", [])
        CustomUser.objects.filter(id__in=user_ids).delete()
        return JsonResponse({"success": "Users deleted successfully"})

def history_view(request):
    detection_history = ThreatMessage.objects.all()
    return render(request, 'history.html', {'detection_history': detection_history})

def latest_threat_view(request):
    latest_threat_message = ThreatMessage.objects.order_by('-created_at').first()
    return render(request, 'your_template.html', {'latest_threat_message': latest_threat_message.message if latest_threat_message else None})

def video_feed(request):
    return StreamingHttpResponse(generate_frames(request), content_type='multipart/x-mixed-replace; boundary=frame')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/auth/admin/' if user.user_type == "admin" else '/auth/user/')
        messages.error(request, "Invalid email or password")
    return render(request, 'authentication/login.html')

@login_required(login_url='login')
@never_cache
def admin_view(request):
    if request.user.user_type != 'admin':
        messages.error(request, "Access denied. Admins only.")
        return redirect('user_dashboard')
    return render(request, 'authentication/admin.html', {'threat_messages': ThreatMessage.objects.all()})



@login_required(login_url='login')
@never_cache
def user_view(request):
    if request.user.user_type != 'user':  
        return redirect('/auth/admin/')  
    return render(request, 'authentication/user.html')

def logout_view(request):
    logout(request)
    return redirect('login')
