from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, data):
        # Validar que el nombre de usuario no esté ya registrado
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Este nombre de usuario ya está registrado.'})
        
        # Validar que el correo electrónico no esté ya registrado
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Este correo electrónico ya está registrado.'})

        return data

class VerifyEmailSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        # Se pueden agregar validaciones adicionales si es necesario
        return data

class CreatePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        # Validar que el usuario esté activo y exista
        try:
            user = User.objects.get(username=data['username'], is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError({'username': 'El usuario no existe'})

        # Validar que la contraseña tenga al menos 8 caracteres
        if len(data['password']) < 8:
            raise serializers.ValidationError({'password': 'La contraseña debe tener al menos 8 caracteres.'})

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
