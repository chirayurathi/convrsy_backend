from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, CompanySerializer, UserReadSerializer
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Company, Form, Question, QuestionChoices
from django.contrib.auth import authenticate
import copy

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
            'company':{
                'name':user.company.name,
                'color':user.company.color
                }
            },
            'success':True
            # Add any other user data you want to include in the response
        }
        return Response(data)

class CompanyCreateView(APIView):

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            company = serializer.save()
            return Response({"data":serializer.data, "success":True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllCompanies(APIView):
    def get(self, request):
        queryset = Company.objects.all()
        if queryset.exists():
            serializer = CompanySerializer(queryset, many=True)
            return Response({'data':serializer.data,'success':True})
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateUserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        print(request.data["company"]["name"])
        user = request.user
        data = copy.deepcopy(request.data)
        data["company"] = data["company"]["name"]
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            comp = Company.objects.get(pk=data['company'])
            print(request.data["company"])
            compSerializer = CompanySerializer(comp, data=request.data["company"], partial = True)
            if compSerializer.is_valid():
                print(compSerializer.validated_data)
                serializer.save()
                compSerializer.save()
                return Response({'success':True,'data':UserReadSerializer(User.objects.get(pk=serializer.data.get("id"))).data}, status=status.HTTP_200_OK)
            else:
                return Response(compSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddFormView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        print(data)
        form = Form(title = data.get("title"), creator= request.user)
        form.save()
        for i in data["questions"]:
            question = Question(form = form, type=i["type"], text=i["text"])
            question.save()
            if(len(i["options"])>0 and i["type"] == "MCQ"):
                for j in i["options"]:
                    choice = QuestionChoices(text=j, question = question)
                    choice.save()
        return Response({"data":form.title,"success":True})