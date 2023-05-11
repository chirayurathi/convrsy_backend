from rest_framework import serializers
from .models import User, Company, Form, Question, Response, QuestionChoices

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


class ResponseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Response
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    creator = serializers.StringRelatedField()

    class Meta:
        model = Form
        fields = '__all__'

class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoices
        fields= '__all__'
