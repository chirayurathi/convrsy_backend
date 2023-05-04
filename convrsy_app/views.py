from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, CompanySerializer
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Company


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                'data':serializer.validated_data,
                'success':True
            })
        return Response({
                'data':serializer.errors,
                'success':False,
                'message':serializer.error_messages[list(serializer.error_messages)][0]
            }, status=400)

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        refresh = RefreshToken.for_user(user)
        response_data = {
            'data':{
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
            },
            'success':True
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class UserDataView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class GetAllCompanies(APIView):
    def get(self, request):
        queryset = Company.objects.all()
        if queryset.exists():
            serializer = CompanySerializer(queryset, many=True)
            return Response({'data':serializer.data,'success':True})
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)