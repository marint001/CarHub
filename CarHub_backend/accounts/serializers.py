from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CustomerProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CustomerRegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    id_card = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'phone',
            'address',
            'gender',
            'id_card'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        phone = validated_data.pop('phone', '')
        address = validated_data.pop('address', '')
        gender = validated_data.pop('gender', '')
        id_card = validated_data.pop('id_card', '')

        user = User.objects.create_user(**validated_data)

        CustomerProfile.objects.create(
            user=user,
            phone=phone,
            address=address,
            gender=gender,
            id_card=id_card
        )

        return user