# serializers.py
from rest_framework import serializers

# from dja import User
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name',
                  "mobile_number",
                  )
        extra_kwargs = {
            "id": {"read_only": True},
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class GoogleLoginSerializer(serializers.Serializer):
    google_key = serializers.CharField()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    full_name = serializers.CharField()
    mobile_number = serializers.CharField()

    def save(self, **kwargs):
        user = User.objects.create_user(
            email=self.validated_data['email'],
            password=self.validated_data['password'],
            full_name=self.validated_data['full_name'],
            mobile_number=self.validated_data['mobile_number'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_mobile_number(self, value):
        # Check if User with the given mobile number already exists
        if User.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Mobile Number already exists")
        # Remove any spaces from the mobile number
        value = value.replace(" ", "")
        # Check if the mobile number starts with +91, if not, add it
        if not value.startswith("+91"):
            # Remove any spaces between +91 and the number
            value = "+91" + value

        # Validate that the mobile number is exactly 13 digits long
        if len(value) != 13:
            raise serializers.ValidationError("Mobile Number must be 13 digits long")

        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long")
        elif not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least 1 digit")
        elif not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least 1 uppercase letter")
        elif not any(char.islower() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least 1 lowercase letter")
        elif not any(char in ['$', '#', '@', '&', '!', '%', '^', '*', '(', ')'] for char in value):
            raise serializers.ValidationError(
                "Password must contain at least 1 special character")
        return value


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
