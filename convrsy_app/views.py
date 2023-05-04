from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, CompanySerializer, UserReadSerializer
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Company
from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            serializer = UserReadSerializer(user)
            print(serializer)
            data = {
                'data':{
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user': serializer.data
                },
                "success":True
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials', "success":False}, status=status.HTTP_401_UNAUTHORIZED)

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


class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request)
        user = request.user
        data = {
            'data':{
            'id': user.id,
            'company': user.company.name,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            },
            'success':True
            # Add any other user data you want to include in the response
        }
        return Response(data)

class GetAllCompanies(APIView):
    def get(self, request):
        queryset = Company.objects.all()
        if queryset.exists():
            serializer = CompanySerializer(queryset, many=True)
            return Response({'data':serializer.data,'success':True})
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)