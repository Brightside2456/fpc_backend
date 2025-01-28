from rest_framework.decorators import api_view
from .models import CustomUserModel, AddressModel, TokenModel
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.db.models import Q
from django.conf.global_settings import EMAIL_HOST_USER
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from .serializers import TokenModelSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
import uuid

#Register Email
@api_view(['POST'])
def regster_customer(request):
    req_obj = request.data
    #custom User Data
    first_name = req_obj['first_name']
    last_name = req_obj['last_name']
    email = req_obj['email']
    password = req_obj['password']
    phone = req_obj['phone']
    referral_code = req_obj['referral_code']
    #Address Data
    street = req_obj['address']['street']
    city = req_obj['address']['city']
    state = req_obj['address']['state']
    postalCode = req_obj['address']['postalCode']
    country = req_obj['address']['country']

    if CustomUserModel.objects.get(email=email):
        return Response({ "error": "Email already exists"}, status=400)
    address_obj = AddressModel.objects.create(
        street=street,
        city=city,
        state=state,
        postalCode=postalCode,
        country=country
    )
    if not address_obj:
        return Response({"error": "Could not create address"}, status=400)
    #Get the pk of the Users address
    add_pk = address_obj
    user_create = CustomUserModel.objects.create(
        password=password,
        phone=phone,
        referral_code=referral_code,
        address=add_pk,
        first_name = first_name,
        last_name=last_name,
        email=email
    )
    if not user_create:
        return Response({"Error": "Could not create user"})
    return Response(
        {
  "message": "Account created successfully",
  "user": {
    "id": f"{user_create.pk}",
    "fullName": f"{first_name} {last_name}",
    "email": f"{email}",
    "phone": f"{phone}",
    "createdAt": f"{datetime.now()}"
  }
},
  status=201
)
    pass


# Validate email
@api_view(['POST'])
def validate_email(request):
    email = request.data['email']
    email_present = CustomUserModel.objects.filter(email=email).first()
    if email_present:
        return Response({
         "isAvailable": "true"
    }, status=404)
    return Response(
            {
                "isAvailable": "false",
                "error": "Email not registered"
            }
            ,
            status=404 )

#Verify Email
@api_view(['POST'])
def verify_email(request):
    subject = "Verify Email"
    sender = EMAIL_HOST_USER
    email = request.data['email']
    user_exists = CustomUserModel.objects.filter(email=email).first()
    if not user_exists:
        return Response(
            {
                "error": "User not found"
            }, status=404
        )
    reciever = [email]

    #Get template
    html_obj = get_template('confirm_email.html')
    link = 'http://127.0.0.1:8080/api/auth/signup/validate-email/'
    context = {'email': f'{email}', 'validate_email': f'{link}'}
    html_content = html_obj.render(context=context)
    email_message = EmailMultiAlternatives(subject=subject,from_email=sender, to=reciever, body="Verify from text")
    email_message.attach_alternative(html_content, 'text/html')
    email_message.send()
    return Response(
        {
            "message": "Verification email sent"
        }
    )
    pass


#Create token for verification
@api_view(['POST'])
def create_token(request):
    email = request.data['email']
    already_gen = TokenModel.objects.filter(Q(email=email) & Q(expired=False)).exists()
    if already_gen:
        return Response({'error': "Could not generate token, its already in the system"}, status=400)
    gen_token = uuid.uuid4()
    while TokenModel.objects.filter(token=gen_token).exists():
        gen_token = uuid.uuid4()
    
    email_exists = CustomUserModel.objects.get(email=email)
    if not email_exists:
        return  Response({"Error": "Email does not exist"}, status=404)
    
    token_created = TokenModel.objects.create(
        email=email,
        token=gen_token,
        use_count=1
    )
    if not token_created:
        return Response({"Error":"Token Could not be created"}, status=401)
    return Response({"message": f"Token Created succesfuly for {email}", "token": f"{gen_token}"})
    
    pass
##Verify email token

@api_view(['POST'])
def verify_email_token(request):
    obj = request.data
    token = obj['token']
    email = obj['email']
    token_valid = TokenModel.objects.filter(Q(expired=False) | Q(token=token))
    if not token_valid:
        return Response({ "error": "Invalid or expired token"}, status=200)
    valid = TokenModel.objects.filter(Q(email=email) & Q(token=token))
    if not valid:
        return Response({"Error": "Invalid Token"}, status=401)
    return Response({"message": "Email verified successfully"}, status=200)
    pass

@api_view(['POST'])
def resend_verification(request):
    subject = "Verify Email"
    sender = EMAIL_HOST_USER
    email = request.data['email']
    already_there = TokenModel.objects.filter(email=email).first()
    if not TokenModel.objects.filter(email=email).exists():
        return Response({ "error": "User not found"}, status=404)
    print(already_there)
    # already_there = TokenModelSerializer(already_there)
    # print(already_there)
    if already_there.use_count >= 5:
        already_there.expired = True
        already_there.save()
        return Response({"error": "Token Expired"}, status=401)
    already_there.use_count+=1
    already_there.save()
      #Get template
    html_obj = get_template('confirm_email.html')
    link = 'http://127.0.0.1:8080/api/auth/signup/validate-email/'
    context = {'email': f'{email}', 'validate_email': f'{link}'}
    html_content = html_obj.render(context=context)
    email_message = EmailMultiAlternatives(subject=subject,from_email=sender, to=[email], body="Verify from text")
    email_message.attach_alternative(html_content, 'text/html')
    email_message.send()
    return Response({"message": "Email resent successfully"}, status=200)
    pass


#Custom Login
class CustomTokenObtainnPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
       response = super().post(request, *args, **kwargs)
       if response.status_code == 200:
        access_token = response.data['access']
        refresh_token = response.data['refresh']
        # print(access_token)
        # print(refresh_token)

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='None'
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='None'
        )
        del response.data['access']
        del response.data['refresh']
        return response
    #    return Response({"access": access_token, "refesh": refresh_token}, status=200)
       return Response({"access": access_token, "refesh": refresh_token}, status=200)
    pass

# Refresh the token
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        if 'refresh_token' in request.COOKIES:
            request.data['refresh_token'] = request.COOKIES['refresh_token']

            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                access_token = response.data.get('access')

                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite='None'
                )
                del response.data['access']
                return response
            
#Logout
class CustomLogoutView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request, *args, **kwargs):
         # Optional: Blacklist the refresh token
         refresh_token = request.COOKIES.get('refresh_token')
         if refresh_token:
             try:
                 token = RefreshToken(refresh_token)
                 token.blacklist()  # Requires SimpleJWT's blacklist app to be installed
             except Exception as e:
                 # Handle invalid or expired token gracefully
                 print("Token invalid or already blacklisted", e)
 
         # Clear cookies by setting them to expire
         response = Response({"detail": "Successfully logged out."}, status=200)
         response.delete_cookie('access_token')
         response.delete_cookie('refresh_token')
         return response