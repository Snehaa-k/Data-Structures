from datetime import datetime, timezone
import json
from tokenize import TokenError
from django.shortcuts import render
from .models import Usermodels,UserProfile,TravelLeaderForm,Country
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions,generics
from .serializer import UserSerializer,ProfileSerializer,FormSubmission
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import update_last_login
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

# Create your views here.

class RegisterationApi(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return Response({"message": "User created successfully. OTP sent.",
                             "user": user_data }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class VerifyOtp(APIView):
    def post(self,request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        print(email,"hiii")
        
        print(otp)
        try:
            user = Usermodels.objects.get(email= email)
            print(user)
            print(user.otp)
        except Usermodels.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        now = datetime.now(timezone.utc)
        if user.is_otpexperied() and now > user.is_otpexperied():
            user.otp = '' 
            # user.otp_expiration = None 
            user.save()
            return Response({"error": "OTP has expired. Please request a new OTP."}, status=status.HTTP_400_BAD_REQUEST)
        
    
        if user.otp == otp:
            user.is_verified = True
            user.otp = ''
            # user.otp_expiration = None  
            user.save()
            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        
        else: 
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


class SelectinTravelleader(APIView):
    def post(self,request):
        email = request.data.get('email')
        role = request.data.get('role')
        roles = "traveller"
        print(email,"hiii")
        print(role)
        try:
            user = Usermodels.objects.get(email= email)
            print(user)
        except Usermodels.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
        if role == "traveller":
            user.is_travel_leader = False
        elif role == "travel_leader":
            user.is_travel_leader = True
        else:
            return Response({"error": "Invalid role selection."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        user_data = UserSerializer(user).data
        return Response({"message": "Role selected successfully.","user": user_data }, status=status.HTTP_200_OK)

class Userpreference(APIView):
    def post(self,request):
        email = request.data.get('email')
        preference = request.data.get('selectedPreference')
       
        print(email,"hiii")
        print(preference)
        try:
            user = Usermodels.objects.get(email= email)
            print(user)
        except Usermodels.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
        if preference:
            user.user_preference = preference
       
        else:
            return Response({"error": "Invalid role selection."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        user_data = UserSerializer(user).data
        return Response({"message": "preference selected successfully.","user": user_data }, status=status.HTTP_200_OK)


class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = Usermodels.objects.get(email=email)
            if not user.is_verified:
                user.generate_otp()  
                return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User is already verified."}, status=status.HTTP_400_BAD_REQUEST)
        except Usermodels.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        


# class resendOtp(APIView):
#     def post(self,request):
#         email = request.data.get('email')
#         try:
#             user = Usermodels.objects.get(email = email)
#             user.generate_otp()
#             return Response({"messege":"OTP sent successfully."},status = status.HTTP_200_OK)
#         except Usermodels.DoesNotExist:
#             return Response({"messege":"User not found."},status=status.HTTP_404_NOT_FOUND)





class CustomTokenObtainPairView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        print(f"emailfail{email}")
        try:
            user = Usermodels.objects.get(email=email)
        except Usermodels.DoesNotExist:
            return Response({'error': 'User not found or invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        
        if not check_password(password, user.password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
       

        
        
        if user.is_superuser == False:

        
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
               
               
            })
        else:
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'admin': UserSerializer(user).data
            })


class FormSubmissionView(APIView):
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request):
        user = request.data.get('email')
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        visited_countries = request.data.getlist('selectedCountries[]') 
        # email = request.data.get('email')
        mobile = request.data.get('mobile')
        cv_file = request.FILES.get('cvFile')
        id_file = request.FILES.get('idFile')
        
        try:
            user_id = Usermodels.objects.get(email=user)
            print(user)
        except Usermodels.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if not all([firstname, lastname, user, mobile]):
            return Response({"error": "Missing required fields"}, status=400)
        
        
        form_submission = TravelLeaderForm.objects.create(
            user_id = user_id,
            firstname=firstname,
            lastname=lastname,
            email=user,
            mobile=mobile,
            cv=cv_file,
            id_proof=id_file

        )
        for country_name in visited_countries:
            country, created = Country.objects.get_or_create(name=country_name)
            form_submission.visited_countries.add(country)
        form_submission.save()
        
        # Return a success response
        return Response({"message": "Form submitted successfully."}, status=200)


class TravelLeaderListView(generics.ListAPIView):
    queryset = TravelLeaderForm.objects.select_related('user_id')
    serializer_class = FormSubmission




class TravelLeaderDetailView(generics.RetrieveAPIView):
    queryset = TravelLeaderForm.objects.select_related('user_id').prefetch_related('visited_countries')
    serializer_class = FormSubmission
    lookup_field = 'id'
    def get(self, request, *args, **kwargs):
        print(f"Requested ID: {kwargs.get('id')}")
        return super().get(request, *args, **kwargs)


class AcceptTravelLeaderView(APIView):
  
    # permission_classes = [IsAuthenticated]
    def post(self, request, pk, *args, **kwargs):
        
       
        try:
            form = TravelLeaderForm.objects.get(id=pk)
            user = Usermodels.objects.get(email = form.user_id.email)
        except TravelLeaderForm.DoesNotExist:
            return Response({'error': 'Travel Leader Form not found'}, status=status.HTTP_404_NOT_FOUND)
        
        form.is_approved = "accepted"
        form.save()
        user.is_approve_leader=True
        user.save()
        
        return Response({'status': 'Accepted'}, status=status.HTTP_200_OK)


class RejectTravelLeaderView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, pk, *args, **kwargs):
       
        try:
            form = TravelLeaderForm.objects.get(id=pk)
            user = Usermodels.objects.get(email = form.user_id.email)
            
        except TravelLeaderForm.DoesNotExist:
            return Response({'error': 'Travel Leader Form not found'}, status=status.HTTP_404_NOT_FOUND)
        
        form.is_approved = "rejected"
        form.save()
        user.is_approve_leader=True
        user.save()
      
        return Response({'status': 'Rejected'}, status=status.HTTP_200_OK)


class TravellersView(generics.ListAPIView):
    queryset = Usermodels.objects.filter(~Q(is_superuser=True) & ~Q(is_travel_leader=True))
    serializer_class = UserSerializer



class is_Block(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, pk, *args, **kwargs):
       
        try:
           user = Usermodels.objects.get(id = pk)  
        except Usermodels.DoesNotExist:
            return Response({'error': 'Travel Leader Form not found'}, status=status.HTTP_404_NOT_FOUND)
        user.is_block = not user.is_block
        user.save()
        return Response({'status': 'Rejected'}, status=status.HTTP_200_OK)


class TravellerProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Get the user model
            user = Usermodels.objects.get(id=request.user.id)

            # Attempt to get the user's profile
            try:
                detail = UserProfile.objects.get(user=request.user.id)
                user_serializer = UserSerializer(user)

                profile_serializer = ProfileSerializer(detail)
                return Response({"profile":profile_serializer.data,"user":user_serializer.data}, status=status.HTTP_200_OK)
            except UserProfile.DoesNotExist:
                # If UserProfile does not exist, return the user model data
                user_serializer = UserSerializer(user)
                return Response(user_serializer.data, status=status.HTTP_200_OK)

        except Usermodels.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    

        


    

class UserProfileEdit(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        print(user_id)
        try:
            profile = Usermodels.objects.get(id=user_id)

            print(profile)
            
        except Usermodels.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(profile)
        return Response(serializer.data)
    

    

class UserProfileCreate(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        print(request.data)
        
        
        userprofile, created = UserProfile.objects.get_or_create(user_id=user_id)
        
        address = request.data.get('address')
        bio = request.data.get('bio')
        country_state = request.data.get('country_state')
        image_file = request.FILES.get('profile_image') 
        
        if image_file:
            userprofile.profile_image = image_file
        
        userprofile.address = address
        userprofile.bio = bio
        userprofile.country_state = country_state
        userprofile.save()
        
        if created:
            message = "Profile created successfully"
        else:
            message = "Profile updated successfully"
        
        return Response({"message": message}, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        print(user_id)
        try:
            profile = UserProfile.objects.get(user=user_id)

            print(profile)
            
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)