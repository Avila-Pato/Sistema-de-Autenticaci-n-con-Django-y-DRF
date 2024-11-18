from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from server.serializers import RegisterSerializer, VerifyEmailSerializer, CreatePasswordSerializer, LoginSerializer
from django.http import JsonResponse
import random
from server.serializers import UserSerializer



# Función para enviar un ramdon winner

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_winner(request):
    if not request.user.is_staff:
        return Response({'error': 'No tienes permiso para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)

    users = User.objects.filter(is_active=True)
    if not users.exists():
        return Response({'message': 'No hay usuarios inscritos para el sorteo.'}, status=status.HTTP_404_NOT_FOUND)

    winner = random.choice(users)
    
    try:
        send_mail(
            '¡Felicidades, eres el ganador!',
            'Has ganado una estadía de 2 noches para dos personas en nuestro hotel en San Valentín.',
            'noreply@mywebsite.com',
            [winner.email],
            fail_silently=False,
        )
        return Response({'message': f'El ganador es {winner.username}. Se ha enviado un correo.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Error al enviar el correo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Función para enviar un correo de prueba
def enviar_correo(request):
    send_mail(
        'Asunto del correo',  # Asunto
        'Cuerpo del correo',  # Cuerpo
        'tu_correo@gmail.com',  # Correo desde el cual se envía
        ['destinatario@dominio.com'],  # Correo destinatario
        fail_silently=False,  # Lanza un error si algo falla
    )
    return JsonResponse({'mensaje': 'Correo enviado con éxito'})

# Vista de registro
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Verificar si el correo ya está registrado
        if User.objects.filter(email=email).exists():
            return Response({'message': 'Este correo electrónico ya está registrado. Por favor, verifique su correo para activar su cuenta.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear el usuario si el correo no está registrado
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Generar el enlace de verificación y enviarlo por correo
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
        domain = get_current_site(request).domain
        link = f'http://{domain}/verify-email/{uid}/{token}/'

        try:
            send_mail(
                'Activa tu cuenta',
                f'Por favor verifica tu dirección de correo electrónico haciendo clic en el siguiente enlace: {link}',
                'noreply@mywebsite.com',
                [email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({'error': f'Error al enviar el correo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Usuario creado exitosamente, por favor verifica tu correo electrónico.'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Endpoint para verificar el correo electrónico
@api_view(['GET'])
def verify_email(request, uidb64, token):
    serializer = VerifyEmailSerializer(data={'uidb64': uidb64, 'token': token})
    if serializer.is_valid():
        try:
            uid = urlsafe_base64_decode(uidb64).decode('utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Enlace no válido'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Correo verificado exitosamente!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token no válido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Endpoint para crear la contraseña después de la verificación
@api_view(['POST'])
def create_password(request):
    serializer = CreatePasswordSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(username=username, is_active=True)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado o correo no verificado.'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(password)
        user.save()
        return Response({'message': 'Contraseña creada exitosamente.'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista de login
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(username=username)
            if user.is_active:
                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)

                    return Response({
                        'access_token': access_token,
                        'refresh_token': str(refresh),
                        'username': user.username,
                        'email': user.email
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Contraseña incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Cuenta no activa.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Endpoint para ver el perfil del usuario
@api_view(['GET'])
def profile(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Cambiar a IsAuthenticated para permitir acceso a cualquier usuario
def get_all_users(request):
    users = User.objects.all()
    user_data = [
        {'username': user.username, 'email': user.email} for user in users
    ]
    return Response(user_data)
