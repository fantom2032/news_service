from rest_framework import serializers
from .models import User, ActivationCode


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
            activation = user.activation_code
        except (User.DoesNotExist, ActivationCode.DoesNotExist):
            raise serializers.ValidationError("Неверные данные")

        if activation.code != data["code"]:
            raise serializers.ValidationError("Неверный код")
        return data

    def save(self, **kwargs):
        user = User.objects.get(email=self.validated_data["email"])
        user.is_active = True
        user.save()
        user.activation_code.delete()
        return user