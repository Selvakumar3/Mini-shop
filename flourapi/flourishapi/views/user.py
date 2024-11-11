from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import traceback
from flourishapi.models import *
from flourishapi.serializers.user import *
from flourishapi.mail_functions import *
from flourishapi.utils import *
from flourishapi.bulk_creations import *
from django.contrib.auth import authenticate

# ---------------- Forgot password ---------------------
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.conf import settings

from datetime import datetime
now = datetime.now()
current_hour = now.hour
current_minute = now.minute
import pywhatkit as kit

#--------------- Mail Urls ----------------------------
FRONTEND_URL = settings.FRONTEND_URL
Backend_url = settings.BACKEND_URL
forget_mail = settings.FORGET_MAIL_URL


# Call function for bulk creations ::
def callbulkCreation():
    if Menu.objects.all().exists() == False:
        MenuCreation()
    if BillType.objects.all().exists() == False:
        BillTypeCreation()


def send_whatsapp_msg():
    phone_number = "+91913682383006"
    message = "Hello! This is a message sent from Python using pywhatkit."
    try:
        kit.sendwhatmsg_instantly(phone_number, message, wait_time=5)  # waits for 5 seconds
        print("Message sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")




# Login function
class LoginAPI(APIView):

    def post(self, request, *args, **kwargs):
        
        try:
            existing_user = getAllObjectWithFilter(User,{'username':request.data.get('username')})
            user_active = getAllObjectWithFilter(User,{'username':request.data.get('username'),'is_active':True})

            if existing_user.exists():
                if user_active.exists():

                    serializer_class = LoginSerializer(data=request.data, context={'request': request})
                    if serializer_class.is_valid():
                        callbulkCreation()
                        user = serializer_class.validated_data['user']
                        username = serializer_class.validated_data['username']
                        password = serializer_class.validated_data['password']
                        user_data = getObject(User,{'username':user})
                    
                        if user_data.username == username and user_data.check_password(password):
                            refresh = RefreshToken.for_user(user)
                            user_active.update(last_login=date_time)
                            # Check if profile_image has a file associated with it
                            if user_data.profile_image and user_data.profile_image.name:
                                profile_image = request.build_absolute_uri(user_data.profile_image.url)
                            else:
                                profile_image = '/static/images/spear-logo.jpg'  # Default image
                        
                            data = {
                                "status": status.HTTP_202_ACCEPTED,
                                'refresh_token': str(refresh),
                                'token': str(refresh.access_token),
                                'user_id': user_data.id,
                                'username': username,
                                'is_super_admin': user_data.is_super_admin,
                                'is_admin': user_data.is_admin,
                                'profile_image': profile_image,
                                'email': user_data.email,
                                'display_name': user_data.username,
                                "message": " User logged in Successfully"
                            }
                            return Response(data=data, status=status.HTTP_202_ACCEPTED)
                        else:
                            return Response({'message': 'Password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
                        
                    else:
                        return error_response.serializer_error(
                            self.__class__.__name__, request, serializer_class
                        )
                else:
                    return Response({'message': 'This account is inactive.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'Enter valid username.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

# Logout function 
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            refresh_token= request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)



# User Forgot PassWord Functions ::
class ResetPasswordRequestEmailAPI(APIView):
    """
    send forgot password Link
    data: email str(),url str()
    Returns:
        (json):Success failure Response
    """
    def post(self, request):

        try:
            serializer_class = ResetPasswordEmailRequestSerializer(data=request.data)
            email = request.data.get('email')
           
            if serializer_class.is_valid():
                data = {}

                if getAllObjectWithFilter(User,{'email':email}).exists():
                    User_data = getObject(User,{'email':email})
                    uidb64 = urlsafe_base64_encode(smart_bytes(User_data.id))
                    token = PasswordResetTokenGenerator().make_token(User_data)

                    relativeLink = reverse(
                        'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
                    
                    absurl = f"{Backend_url}{relativeLink}?redirect_url={forget_mail}?emailid={email}"
                    kwargs = {
                        "to_address":email,
                        "absurl":absurl,
                    }
                    """
                    Password reset email with link will be sent to the requested user
                    """
                    respone = send_email(VelanEmailType.PASSWORD_RESET_LINK,VelanEmailSettingsType.NOREPLY,**kwargs)
                    respone_data={}

                    if respone == True:
                        respone_data['message'] = 'Reset link sent your email successfully'
                        respone_data['status'] = status.HTTP_201_CREATED
                        return Response(respone_data, status=status.HTTP_201_CREATED)
                    else:
                        respone_data['message'] = 'Email sent failed.'
                        respone_data['status'] = status.HTTP_400_BAD_REQUEST
                        return Response(respone_data, status=status.HTTP_400_BAD_REQUEST)
                else:
                    data['status'] = status.HTTP_404_NOT_FOUND
                    data['message'] = 'Email is invalid !'
                    return Response(data=data, status=status.HTTP_404_NOT_FOUND)
            else:
               return error_response.serializer_error(
                    self.__class__.__name__, request, serializer_class
                )
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)


    def put(self, request):

        try:
            serializer_class = SetNewPasswordSerializer(data=request.data)
            if serializer_class.is_valid():
                data = {}
                data['message'] = 'Password has been reset, redirecting to login page ...'
                data['status'] = status.HTTP_200_OK
                return Response(data=data,status=status.HTTP_200_OK)
            else:
                return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('---resetpass error ',e)
            return error_response.exception_error(self.__class__.__name__, request, e)


# REDIRECT RESPONSE URL :
class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [FRONTEND_URL, 'http', 'https']

# GENERATE TOKEN FOR RESET PASSWORD ::
class PasswordTokenCheckAPI(APIView):
    """
    user token checking 
    params: redirect_url str(), token ,uidb64 int()
    Returns:
        (json):Success failure Response
    """

    def get(self, request, uidb64, token):
        
        try:
            redirect_url = request.GET.get('redirect_url')
            try:
                id = smart_str(urlsafe_base64_decode(uidb64))
                user =  getObject(User,{'id':id})
                if not PasswordResetTokenGenerator().check_token(user, token):
                    return CustomRedirect(FRONTEND_URL + redirect_url+'&token_valid=False')
                else:
                    return CustomRedirect(FRONTEND_URL + redirect_url + '&token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            except (DjangoUnicodeDecodeError, ValueError) as identifier:
                return CustomRedirect(FRONTEND_URL + redirect_url+'&token_valid=False')

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)


# User Profile Get and Update ::
class UserProfileUpdate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')
            query_set = getObject(User,{'id':user_id})
            serializer_class = GetUserProfileSerializer(query_set, context={"request":request})
            return Response(serializer_class.data, status=status.HTTP_202_ACCEPTED)
        
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
    
    def put(self, request):
        try:

            user_id = request.query_params.get('user_id')
            queryset = getObject(User,{'id':user_id})
            serializer_class = UpdateUserProfileSerializer(queryset, data=request.data, context={'request':request}, partial=True)
            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_202_ACCEPTED)
            else:
               return error_response.serializer_error(self.__class__.__name__, request, serializer_class)
        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
            

# User Password Update :::
class UserPasswordUpdateAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            user_id = request.query_params.get('user_id')
            userData = getObject(User,{'id':user_id})
            oldpassword = request.data.get('old_password')
            newpassword = request.data.get('new_password')

            user = authenticate(username=userData.username, password=oldpassword)
            if user is not None:
                userData.set_password(newpassword)
                userData.save()
                return Response({'error_message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error_message': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'userId': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        

class UserProfileImgeUpdateAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
       
        try:
            user_id = request.query_params.get('user_id')
            queryset = getObject(User,{'id':user_id})
            serializer_class = GetUserDetailsSerializer(queryset, context={'request': request})
            return Response(serializer_class.data, status=status.HTTP_200_OK)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)

    def put(self, request):
        try:
            user_id = request.query_params.get('user_id')
            queryset = getObject(User,{'id':user_id})

            serializer_class = UserProfileImageUpdateSerializer(queryset, data=request.data,context={'request':request})
            if serializer_class.is_valid():
                serializer_class.save()
                data={}
                profile_image =serializer_class.data.get('profile_image')
                display_name =serializer_class.data.get('display_name')
                profile_image = request.build_absolute_uri(profile_image)
                data['profile_image']=profile_image
                data['display_name']=display_name
                return Response(data, status=status.HTTP_200_OK)
            
            else:
                return error_response.serializer_error(self.__class__.__name__, request, serializer_class)

        except Exception as e:
            return error_response.exception_error(self.__class__.__name__, request, e)
        
        
