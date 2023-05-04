from rest_framework import serializers
from .models import User, Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'company')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'],
            validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            company=validated_data['company']
        )
        return user

class UserReadSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'company')
        extra_kwargs = {'password': {'write_only': True}}
