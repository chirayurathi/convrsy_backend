from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-user/', UserDataView.as_view(), name='user_data'),
    path('create-company/', CompanyCreateView.as_view(), name="create-company"),
    path('get-companies/', GetAllCompanies.as_view(), name='companies_view'),
    path('update-user/',UpdateUserDataView.as_view(), name="user_update"),
    path('create-form/', AddFormView.as_view(), name="add-form"),
    path('get-user-forms/', GetUserForms.as_view(), name="get-user-forms"),
    path('form/<int:form_id>/', FormDetailAPIView.as_view(), name='form-detail'),

]
