from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import User
from api.serializers.authSerializer import LoginSerializer, RegisterSerializer, UserSerializer, ForgotPasswordVerifySerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from api.utils.mail import sendMail
from api.utils.random import encrypt_dict, decrypt_dict
import os
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


class LoginViewset(viewsets.generics.CreateAPIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            norm_email = email.lower()
            user = authenticate(email = norm_email, password = password)
            if user is None:
                return Response({
                    'message': 'Invalid email or password',
                    # 'errors': serializer.errors,
                }, status=status.HTTP_401_UNAUTHORIZED)
            if not user.is_active:
                return Response({
                    'message': 'Your account is blocked, Please contact admin.',
                    # 'errors': serializer.errors,
                }, status=status.HTTP_401_UNAUTHORIZED)
            

            # invalidate all tokens
            try:
                tokens = OutstandingToken.objects.filter(user=user)
                for token in tokens:
                    token_ref = RefreshToken(token.token)
                    token_ref.blacklist()
            except:
                pass
            
            refresh = RefreshToken.for_user(user)
            
            # if user.role == 'company':
            #     user_serializer = UserCompanySerializer(user)
            # else:
            user_serializer = UserSerializer(user)
            return Response({
                'message': 'Login successful',
                'user': user_serializer.data,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, 200)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RegisterViewset(viewsets.generics.CreateAPIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'message': 'Invalid data',
                    'errors': serializer.errors,
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        serializer.save()
        # user = User.objects.get(email=serializer.data['email'])
        # send_email_verification(user)
        return Response({
            'message': 'Account created successfully',
            'success': True,
        })
    
class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        permissions = set()

        permissions.update(request.user.role.permissions.all().values_list("codename", flat=True))

        return Response({"permissions": permissions})
    

class ProfileViewset(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        try:
            user = request.user
            serializer = UserSerializer(user)
            return Response(serializer.data, 200)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh = request.data.get('refresh_token')
    if refresh is None:
        return Response({
            'message': 'Refresh token is required',
            'errors': {'refresh_token': ['Refresh token is required']}
        }, status=status.HTTP_400_BAD_REQUEST)

    
    token_obj = RefreshToken(refresh)
    token_obj.blacklist()

    return Response(
        {'message': 'Successfully logged out'}, 
        status=status.HTTP_200_OK
    )
        
@api_view(['POST'])
def forget_password_request(request):
    email = request.data.get('email', '').lower()

    # Validate email
    if not email:
        return Response({
            'message': 'Invalid data',
            'errors': {'email': ['Email is required']}
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    try:
        # Find user by email
        user = User.objects.get(email=email)

        # Prepare the reset link data
        data = {
            'email': user.email,
            'user_id': user.id,
            'time': timezone.now(),  # Use timezone-aware datetime
        }

        code = encrypt_dict(data)

        # Store the reset token
        user.remember_token = code
        user.save()

        # Build the reset password link
        base_url = os.getenv('BASE_URL', 'http://localhost:3000')
        reset_link = f'{base_url}/auth/reset-password/{user.id}/{code}'

        # Prepare email content
        content = {
            'full_name': user.fullName(),
            'title': 'Forget Password',
            'reset_link': reset_link,
        }

        # Send the email
        sendMail(
            user.email,
            'mail/forget_password.html',
            'Forget Password Request',
            content
        )

        return Response({
            'success': 'OK',
            'message': 'Reset password link sent to your email.',
        })

    except User.DoesNotExist:
        return Response({
            'message': 'Email is not registered.',
        }, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def forget_password_verify(request):
    serializer = ForgotPasswordVerifySerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'message': 'Invalid data.',
            'errors': serializer.errors,
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    token = serializer.validated_data['token']
    data = decrypt_dict(token)

    if data is None:
        return Response({
            'message': 'Invalid link, please request a new reset link.',
            'errors': {'url': ['Invalid link.']},
        }, status=status.HTTP_403_FORBIDDEN)

    # Check token expiration
    link_time = data['time']
    time_now = timezone.now()
    time_diff_mins = (time_now - link_time).total_seconds() / 60

    if time_diff_mins > 60:
        return Response({
            'message': 'Link expired, please request a new reset link.',
            'errors': {'url': ['Link expired.']},
        }, status=status.HTTP_403_FORBIDDEN)

    # Verify user
    email = data['email']
    user_id = data['user_id']
    user = User.objects.get(email=email)
    
    # If user doesn't exist or token is invalid, return an error
    if not user or user.remember_token != token or user.id != user_id:
        return Response({
            'message': 'Invalid link, please request a new reset link.',
            'errors': {'url': ['Invalid link.']},
        }, status=status.HTTP_403_FORBIDDEN)

    # Update password and reset token
    user.set_password(serializer.validated_data['password'])
    user.remember_token = None
    user.save()

    return Response({
        'success': 'OK',
        'message': 'Password changed successfully.',
    })

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def post(self, request):
        try:
            user = request.user
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if not serializer.is_valid():
                return Response({
                        'message' : 'Invalid data',
                        'errors' : serializer.errors
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            user.set_password(serializer.data['new_password'])
            user.remarks = ''
            user.save()
            return Response({
                'message' : 'Password changed successfully'
            }, 200)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    password = request.data.get('current_password')

    if not user.check_password(password):
        return Response({
            'message': 'Invalid password.',
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    if user.role == 'admin':
        return Response({
            'message': 'Admin account can not be deleted.',
        }, status=status.HTTP_403_FORBIDDEN)
    user.delete()
    return Response({
        'success': 'OK',
        'message': 'Account deleted successfully.',
    })

