from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from .serialisers import CustomUserSerializer
from rest_framework.authentication import get_authorization_header

token_generator = PasswordResetTokenGenerator()

# function for registering the user with help of email , username , password
@api_view(['POST'])
@permission_classes([])
def register_user(request):
    data = request.data
    try:
        user = CustomUser.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email']
        )

        role = 'admin' if data['email'] == 'admin@gmail.com' else 'user'

        return Response({"message": "User created successfully", "role": role}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# function for login user with the help of the email and password , and generates the token if the user is valid(register itself) and send the login mail 
@api_view(['POST'])
@permission_classes([])
def login_user(request):
    data = request.data
    email = data.get('email') 
    password = data.get('password') 

    if not email or not password:
        return Response({"message": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = authenticate(email=email, password=password)  
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            role = 'admin' if email == 'admin@gmail.com' else 'user'
            subject = 'Login Notification'
            html_message = render_to_string('login_notification_email.html', {
                'user': user,
                'login_time': timezone.now().strftime('%d-%m-%Y'),
            })
            plain_message = strip_tags(html_message)

            send_mail(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
                html_message=html_message,
            )

            return Response({"username": user.username, "token": token.key,"role":role}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# function for reset password with the help of the email , sends the password reset mail, this is done when the user is logged in and remember it old password and needs to create the new password
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    data = request.data

    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not user.check_password(old_password):
        return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

    if not new_password:
        return Response({'error': 'New password cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user.set_password(new_password)
        user.save()
        login_url = "http://127.0.0.1:8000/api/login-user"
        subject = 'Password Changed Successfully'
        html_message = render_to_string('password_changed_notification_email.html', {
            'login_link': login_url
        })
        plain_message = strip_tags(html_message)
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
            html_message=html_message,
        )
        return Response({'message': 'Password changed successfully. A notification email has been sent.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# function for sending the mail to reset the passwod this takes inputs email as an input and checks if its registered then only sends mails
@api_view(['POST'])
@permission_classes([])
def request_password_reset(request):
    email = request.data.get('email')
    try:
        user = CustomUser.objects.get(email=email)
        token = token_generator.make_token(user)
        
        # Encode the email to make it safe for URLs
        encoded_email = user.email
        
        # Include email in the reset link
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}&email={encoded_email}"

        subject = 'Password Reset Request'
        html_message = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
            html_message=html_message,
        )
        return Response({'message': 'Password reset link sent successfully.'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# this is the function which takes the new password as an input and sets the new password for the users and sends mail that the password  has been successfully changed
@api_view(['POST'])
@permission_classes([])
def reset_password(request):
    token = request.query_params.get('token')
    email = request.query_params.get('email')

    if not token or not email:
        return Response({'error': 'Token and email are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the user by email
        user = CustomUser.objects.get(email=email)

        # Check the token validity
        if token_generator.check_token(user, token):
            new_password = request.data.get('password')
            if not new_password:
                return Response({'error': 'New password cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password and save the user
            user.set_password(new_password)
            user.save()

            subject = "Password Changed Successfully"
            html_message = render_to_string('password_reset_successfully.html')
            plain_message = strip_tags(html_message)

            send_mail(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
                html_message=html_message,
            )

            return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# this is the function which is used to logout the user when the user will be loggout then the token from the auth token will be deleted
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        auth_header = get_authorization_header(request).split()
        
        if not auth_header or len(auth_header) != 2 or auth_header[0].lower() != b'token':
            return Response({"error": "Invalid token header."}, status=status.HTTP_400_BAD_REQUEST)
        
        token_key = auth_header[1].decode('utf-8')

        token = Token.objects.get(key=token_key)
        user = token.user
        
        if request.user != user:
            return Response({"error": "Token does not match the authenticated user."}, status=status.HTTP_403_FORBIDDEN)

        token.delete()
        return Response({"message": "Logout successful. Token deleted."}, status=status.HTTP_200_OK)

    except Token.DoesNotExist:
        return Response({"error": "Token not found."}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# this is the function which get the user detials its only work when the user is authenticated and if the authenticated user is the admin then it will give all the user's list else it will return the authenticated user data
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_detail(request, user_id=None):
    try:
        if request.user.is_staff or request.user.is_superuser:
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                serializer = CustomUserSerializer(user)
            else:
                users = CustomUser.objects.all()
                serializer = CustomUserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            if user_id and int(user_id) != request.user.id:
                return Response({'error': 'You are not authorized to view this user'}, status=status.HTTP_403_FORBIDDEN)
            user = CustomUser.objects.get(id=request.user.id)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# this is the function in which admin can update the any user but the user can only update his account
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    try:
        if request.user.is_staff or request.user.is_superuser:
            user = CustomUser.objects.get(id=user_id)
        else:
            if int(user_id) != request.user.id:
                return Response({'error': 'You are not authorized to update this user'}, status=status.HTTP_403_FORBIDDEN)
            user = CustomUser.objects.get(id=request.user.id)

        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# this is the function in which admin can delete the any user but the user can only delete his account
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    try:
        if request.user.is_staff or request.user.is_superuser:
            user = CustomUser.objects.get(id=user_id)
        else:
            if int(user_id) != request.user.id:
                return Response({'error': 'You are not authorized to delete this user'}, status=status.HTTP_403_FORBIDDEN)
            user = CustomUser.objects.get(id=request.user.id)

        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)