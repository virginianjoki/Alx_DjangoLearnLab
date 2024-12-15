from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# Reference the custom user model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # Explicitly define the password field as a CharField with write-only behavior
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        # Using get_user_model().objects.create_user for proper password hashing
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        # Create a token for the new user
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    # Explicitly define username and password as CharFields
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(**data)
        if user and user.is_active:
            # Generate or retrieve the user's token
            token, _ = Token.objects.get_or_create(user=user)
            return {
                'token': token.key,
                'username': user.username,
                'email': user.email,
            }
        raise serializers.ValidationError("Invalid credentials")


