from datetime import datetime, timedelta, timezone
import json
from tokenize import TokenError
from urllib import response
from django.shortcuts import render
from .models import Notification, Post, UserReport, CustomUser,UserProfile,TravelLeaderForm,Country,Trips,Place,ArticlePost,Comment,Payment,Wallet,ChatMessages,Group,GroupChat,GroupMember
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions,generics
from .serializer import GroupSerializer, NotificationSerializer, UserReportSerializer, UserSerializer,ProfileSerializer,FormSubmission,TripSerializer,PlaceSerializer,PostSerializer,ArticleSerilizer,CommentSerializer,WalletSerializer,ChatPartnerSerializer,ChatMessageSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import update_last_login
from django.contrib.contenttypes.models import ContentType
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db.models import Case, When
from datetime import timedelta
import datetime
from django.utils.dateparse import parse_date
from django.conf import settings
import stripe
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework import generics, response, status, views, viewsets
from rest_framework.decorators import action
from channels.layers import get_channel_layer
from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode
from asgiref.sync import async_to_sync
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache

# stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.

class RegisterationApi(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            Wallet.objects.create(user=user, wallet=0)
            user_data = UserSerializer(user).data
            return Response({"message": "User created successfully. OTP sent.",
                             "user": user_data }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class VerifyOtp(APIView):
    def post(self,request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        try:
            user = CustomUser.objects.get(email= email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        
        
    
        if user.otp == otp:
            user.is_verified = True
            user.otp = ''
            user.save()
            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        
        else: 
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


class SelectinTravelleader(APIView):
    def post(self,request):
        email = request.data.get('email')
        role = request.data.get('role')
        roles = "traveller"
        try:
            user = CustomUser.objects.get(email= email)
        except CustomUser.DoesNotExist:
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
        try:
            user = CustomUser.objects.get(email= email)
        except CustomUser.DoesNotExist:
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
            user = CustomUser.objects.get(email=email)
            if not user.is_verified:
                user.generate_otp()  
                return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User is already verified."}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        






class CustomTokenObtainPairView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': ' Invalid email Address'}, status=status.HTTP_401_UNAUTHORIZED)
        if not check_password(password, user.password):
            return Response({'error': 'Invalid Password'}, status=status.HTTP_401_UNAUTHORIZED)
        
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
        mobile = request.data.get('mobile')
        cv_file = request.FILES.get('cvFile')
        id_file = request.FILES.get('idFile')
        accountHolder = request.data.get('accountHolder')
        accountNumber = request.data.get('accountNumber')
        bankName = request.data.get('bankName')
        ifscCode = request.data.get('ifscCode')

         
        
        try:
            user_id = CustomUser.objects.get(email=user)
        except CustomUser.DoesNotExist:
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
            id_proof=id_file,
            bank_account_name = accountHolder,
            bank_account_number = accountNumber,
            bank_name = bankName,
            ifsc_code = ifscCode

        )
        for country_name in visited_countries:
            country, created = Country.objects.get_or_create(name=country_name)
            form_submission.visited_countries.add(country)
        form_submission.save()
        
        # Return a success response
        return Response({"message": "Form submitted successfully."}, status=200)


class TravelLeaderListView(generics.ListAPIView):
    serializer_class = FormSubmission

    def get_queryset(self):
        queryset = TravelLeaderForm.objects.select_related('user_id')
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(is_approved=status_filter)

        
        ordering = Case(
            When(is_approved='pending', then=0),
            When(is_approved='accepted', then=1),
            When(is_approved='rejected', then=2),
        )

        return queryset.order_by(ordering)




class TravelLeaderDetailView(generics.RetrieveAPIView):
    queryset = TravelLeaderForm.objects.select_related('user_id').prefetch_related('visited_countries')
    serializer_class = FormSubmission
    lookup_field = 'id'
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AcceptTravelLeaderView(APIView):
  
    # permission_classes = [IsAuthenticated]
    def post(self, request, pk, *args, **kwargs):
        
        try:
            form = TravelLeaderForm.objects.get(id=pk)
            user = CustomUser.objects.get(email = form.user_id.email)
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
            user = CustomUser.objects.get(email = form.user_id.email)
            
        except TravelLeaderForm.DoesNotExist:
            return Response({'error': 'Travel Leader Form not found'}, status=status.HTTP_404_NOT_FOUND)
        
        form.is_approved = "rejected"
        form.save()
        user.is_approve_leader=False
        user.save()
      
        return Response({'status': 'Rejected'}, status=status.HTTP_200_OK)



class TravellersView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(~Q(is_superuser=True) & ~Q(is_travel_leader=True))
    serializer_class = UserSerializer



class is_Block(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, pk, *args, **kwargs):
       
        try:
           user = CustomUser.objects.get(id = pk)  
        except CustomUser.DoesNotExist:
            return Response({'error': 'Travel Leader Form not found'}, status=status.HTTP_404_NOT_FOUND)
        user.is_block = not user.is_block
        user.save()
        return Response({'status': 'Rejected'}, status=status.HTTP_200_OK)



class TravellerProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        cached_profile = cache.get(f'user_profile_{user_id}')
        if cached_profile:
            return Response(cached_profile, status=status.HTTP_200_OK)

        
        try:
            
            user = CustomUser.objects.get(id=request.user.id)

            
            try:
                detail = UserProfile.objects.get(user=request.user.id)
                user_serializer = UserSerializer(user)

                profile_serializer = ProfileSerializer(detail)
                response_data = {
                    "profile": profile_serializer.data,
                    "user": user_serializer.data,
                }

                cache.set(f'user_profile_{user_id}', response_data, timeout=600)
                return Response({"profile":profile_serializer.data,"user":user_serializer.data}, status=status.HTTP_200_OK)
            
            except UserProfile.DoesNotExist:
                
                user_serializer = UserSerializer(user)
                response_data = {
                    "user": user_serializer.data,
                }

                cache.set(f'user_profile_{user_id}', response_data, timeout=600)
                return Response({"user":user_serializer.data}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    

        


    

class UserProfileEdit(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            profile = CustomUser.objects.get(id=user_id)

            
        except CustomUser.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(profile)
        return Response(serializer.data)
    

    

class UserProfileCreate(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
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
        try:
            profile = UserProfile.objects.get(user=user_id)

            
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class CreateTrip(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        
        try:
            user = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        new_trip_start_date = parse_date(request.data.get('start_date'))

        existing_trips = Trips.objects.filter(travelead=user).order_by('-end_date')
        if existing_trips.exists():
            last_trip = existing_trips.first()
            if new_trip_start_date <= last_trip.end_date:
                return Response({'error': 'New trip start date must be after the last trip\'s end date'},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = TripSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            trip = serializer.save()
            trip_data = TripSerializer(trip).data

            user_profile = UserProfile.objects.get(user=user)
            followers = user_profile.followers.all()  

            for follower in followers:
                notification_type = "new_trip"
                text = f"{user.username} has created a new trip."
                link = f"/viewdestination/{trip.id}" 

                Notification.objects.create(
                    receiver=follower,
                    sender=user,
                    notification_type=notification_type,
                    text=text,
                    link=link,
                    is_read=False,
                )

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"notification_{follower.id}",
                    {
                        "type": "send_notification",
                        "data": {
                            "type": notification_type,
                            "sender": user.username,
                            "text": text,
                            "link": link,
                        },
                    },
                )

            return Response({"message": "Trip created successfully", "trip": trip_data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewTrips(APIView):
     def get(self, request, *args, **kwargs):
        user_id = request.user.id
        today = timezone.now().date()
        try:
            trip = Trips.objects.filter(travelead=user_id,end_date__gt = today)

            
        except Trips.DoesNotExist:
            return Response({'error': 'trip not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TripSerializer(trip,many=True,context={'request': request})
        return Response({'trip':serializer.data}, status=status.HTTP_201_CREATED)
     


class EditTrips(APIView):
    
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        trip_id = request.data.get('id')
        try:
            trips, created = Trips.objects.get_or_create(id = trip_id)
        except Trips.DoesNotExist:
            return Response({'error': 'trip not found'}, status=status.HTTP_404_NOT_FOUND)

        


        
        accommodation = request.data.get('accommodation')
        transportation = request.data.get('transportation')
        participant = request.data.get('participant_limit')
        amount = request.data.get('amount')
        duration = request.data.get('duration') 
        start_date = request.data.get('start_date')
        trips.accomodation = accommodation
        trips.transportation = transportation
        trips.participant_limit = participant
        trips.duration = duration
        trips.start_date = start_date
        trips.amount = amount

        if start_date and duration:
            try:
                start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                
                end_date = start_date_obj + timedelta(days=int(duration))
                
                trips.start_date = start_date_obj
                trips.end_date = end_date
            except ValueError:
                return Response({"error": "Invalid date or duration format"}, status=status.HTTP_400_BAD_REQUEST)        
       

        image_file = request.FILES.get('Trip_image', None)
        if image_file:
            trips.Trip_image = image_file

        trips.save()

        
        if created:
            message = "trip created successfully"
        else:
            message = "trip updated successfully"
        
        return Response({"message": message}, status=status.HTTP_200_OK)


class AddPlaces(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        trip_id = request.data.get('tripId')

        try:
            trip = Trips.objects.get(id=trip_id)
        except Trips.DoesNotExist:
            return Response({'error': 'Trip not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PlaceSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            place = serializer.save()
            place_data = PlaceSerializer(place).data
            return Response({"message": "Place added successfully", "place": place_data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewPlaces(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request,id, *args, **kwargs):
        
        user = CustomUser.objects.get(id = request.user.id)
        if user:
        
            try:
                trip_obj = Trips.objects.get(id = id)
                trip = Place.objects.filter(trip = trip_obj)
            except Trips.DoesNotExist:
                return Response({'error': 'trip not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = PlaceSerializer(trip,many=True)

            return Response({'trip':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)



class EditPlace(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        user_id = request.user.id
        place_name = request.data.get('place_name')
        accommodation = request.data.get('accomodation')
        transportation = request.data.get('transportation')
        description = request.data.get('description')
        image = request.FILES.get('image')  

        try:
            place = Place.objects.get(id=id)
        except Place.DoesNotExist:
            return Response({'error': 'Place not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            trip = Trips.objects.get(id=request.data.get('trip_id'), travelead=user_id)
        except Trips.DoesNotExist:
            return Response({'error': 'Trip not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)

        place.trip = trip  
        place.place_name = place_name
        place.accomodation = accommodation
        place.Transportation = transportation
        place.description = description

        if image:
            
            place.place_image = image  

        place.save()

        return Response({"message": "Place updated successfully"}, status=status.HTTP_200_OK)

class DeleteItem(APIView):
    def delete(self, request, id, *args, **kwargs):
        try:
            item = Place.objects.get(id=id)
            item.delete()
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)
        except Place.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)   


class ViewAllTrips(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            user = CustomUser.objects.get(id = user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        if user:
            today = timezone.now().date()
            tomorrow = today + timedelta(days=1)

            try:
                trip = Trips.objects.select_related('travelead').filter(end_date__gt = today,start_date__gt=tomorrow)
                
            except Trips.DoesNotExist:
                return Response({'error': 'trip not found'},status=status.HTTP_404_NOT_FOUND)
            
        

        
        serializer = TripSerializer(trip,many=True,context={'request': request})
        return Response({'trip':serializer.data,'user':user.id}, status=status.HTTP_201_CREATED)


class TripDetails(APIView):
    def get(self, request,id, *args, **kwargs):
        user_id = request.user.id
        try:
            user = CustomUser.objects.get(id = user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        if user:
            try:
                trip = Trips.objects.select_related('travelead').get(id = id)
                
            except Trips.DoesNotExist:
                return Response({'error': 'trip not found'},status=status.HTTP_404_NOT_FOUND)
            is_booked = False  
        try:
            payment = Payment.objects.get(user=user, trip=trip)
            is_booked = payment.status == 'completed'  
        except Payment.DoesNotExist:
            pass
        serializer = TripSerializer(trip,context={'request': request})
        return Response({'trip':serializer.data,'userId':user_id,'is_booked': is_booked}, status=status.HTTP_201_CREATED)

    
class PlaceDetails(APIView):
    def get(self, request,id, *args, **kwargs):
        user_id = request.user.id
        try:
            user = CustomUser.objects.get(id = user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        if user:

            try:
                trip = Place.objects.select_related('trip').filter( trip = id)
                
            except Place.DoesNotExist:
                return Response({'error': 'trip not found'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = PlaceSerializer(trip,many=True)
        return Response({'trip':serializer.data}, status=status.HTTP_201_CREATED)



class PostCreation(APIView):
    def post(self, request):
        try:
            user = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(data=request.data, context={'request': request})


        if serializer.is_valid():
            post = serializer.save()
            post_data = PostSerializer(post).data
            return Response({"message": "Post created successfully.", "posts": post_data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ArticlePosts(APIView):
    def post(self, request):
        try:
            user = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerilizer(data=request.data, context={'request': request})


        if serializer.is_valid():
            post = serializer.save()
            post_data = ArticleSerilizer(post).data
            return Response({"message": "Post created successfully.", "posts": post_data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class ViewPosts(APIView):
    def get(self, request, *args, **kwargs):
        try:
            
            user = CustomUser.objects.get(id=request.user.id)
            
            try:
                posts = Post.objects.select_related('travel_leader')
                article = ArticlePost.objects.select_related('travel_leader')
                

                posts_serializer = PostSerializer(posts,many=True,context={'request': request})
                article_serilizer = ArticleSerilizer(article,many=True)

                return Response({"posts":posts_serializer.data,"article":article_serilizer.data}, status=status.HTTP_200_OK)
            except Post.DoesNotExist:
                
                return Response({"message":"no posts"}, status=status.HTTP_404_NOT_FOUND)

        except CustomUser.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)



class ViewArticle(APIView):
    def get(self, request, *args, **kwargs):
        try:
            
            user = CustomUser.objects.get(id=request.user.id)
            
            try:
                article = ArticlePost.objects.select_related('travel_leader')
                

                article_serilizer = ArticleSerilizer(article,many=True,context={'request': request})
                return Response({"article":article_serilizer.data,}, status=status.HTTP_200_OK)
            except Post.DoesNotExist:
                
                return Response({"message":"no posts"}, status=status.HTTP_404_NOT_FOUND)

        except CustomUser.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        



class ViewUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            user = CustomUser.objects.get(id = user_id)
            profile_img = UserProfile.objects.get(user = user)
        except CustomUser.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user_serializer = UserSerializer(user)
        profile = ProfileSerializer(profile_img)
        return Response({"user":user_serializer.data,"profile":profile.data}, status=status.HTTP_200_OK)
    




# comment and likes section..................
class LikeTravelPostAPIView(APIView):
    def post(self, request, id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            message = "Like removed"
        else:
            post.likes.add(request.user)
            message = "Like added"

        serializer = PostSerializer(post, context={'request': request})
        likes_count = post.likes.count()
        return Response({'message': message, 'data': serializer.data,'likes':likes_count}, status=status.HTTP_200_OK)




class LikeArticleView(APIView):
    def post(self, request, id):
        try:
            article = ArticlePost.objects.get(id=id)
        except ArticlePost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
            message = "Like removed"
        else:
            article.likes.add(request.user)
            message = "Like added"

        serializer = PostSerializer(article, context={'request': request})
        likes_count = article.likes.count()
        return Response({'message': message, 'data': serializer.data,'likes':likes_count}, status=status.HTTP_200_OK)



# comment section.................
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  

    def create(self, request, *args, **kwargs):
        content_type = request.data.get('content_type')
        object_id = request.data.get('object_id')
        text = request.data.get('text')

        try:
            content_type_obj = ContentType.objects.get(id=content_type)
        except ContentType.DoesNotExist:
            return Response({"error": "Invalid content type"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            user=request.user,
            content_type=content_type_obj,
            object_id=object_id,
            text=text,
        )

        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')

        try:
            content_type_obj = ContentType.objects.get(id=content_type)
        except ContentType.DoesNotExist:
            return Comment.objects.none()

        return Comment.objects.filter(content_type=content_type_obj, object_id=object_id)



class CreateStripeSessionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user:
                return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
            
            user_id = CustomUser.objects.get(id=user.id)
            trip_id = request.data.get('trip_id')
            if not trip_id:
                return Response({'error': 'trip_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            

            
            trip = Trips.objects.get(id=trip_id)
            amount = int(trip.amount * 100)  
            
            if trip.participant_limit <=0: 
                return Response({'error': 'No available spots for this trip'}, status=status.HTTP_400_BAD_REQUEST)
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': f'Advance Payment for {trip.location}',
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                customer_email=user_id.email,
                success_url=f'http://localhost:5173/success?session_id={{CHECKOUT_SESSION_ID}}&trip_id={trip_id}',
                cancel_url='http://localhost:5173/cancel',
            )
            
        


            return Response({'sessionId': session.id}, status=status.HTTP_200_OK)

        except Trips.DoesNotExist:
            return Response({'error': 'Trip not found'}, status=status.HTTP_404_NOT_FOUND)

        except stripe.error.StripeError as e:
            return Response({'error': f'Stripe error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error': f'Internal server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#confirmation payment
class ConfirmPaymentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        session_id = request.data.get('session_id')
        trip_id = request.data.get('trip_id')

        if not session_id:
            return Response({'error': 'session_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session:
                trip = Trips.objects.get(id=trip_id)
                user = request.user

                Payment.objects.create(
                    user=user,
                    trip=trip,
                    amount=session.amount_total / 100,  
                    status='completed',
                    payment_type='stripe'
                )

                trip.participant_limit -= 1
                trip.save()

                user_profile = CustomUser.objects.get(user=user)

                notification_type = "user_is_booked"
                text = f"{user_profile.username} has booked your trip."
                link = "/dashboard/" 

                Notification.objects.create(
                    receiver=trip.travelead,  
                    sender=user,
                    notification_type=notification_type,
                    text=text,
                    link=link,
                    is_read=False,
                )

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"notification_{trip.travelead}", 
                    {
                        "type": "send_notification",
                        "data": {
                            "type": notification_type,
                            "sender": user_profile.username,
                            "text": text,
                            "link": link,
                        },
                    },
                )

                return Response({'success': True}, status=status.HTTP_200_OK)

            return Response({'error': 'Payment not successful'}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            return Response({'error': f'Stripe error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class TripsByLeaderView(generics.ListAPIView):
    serializer_class = TripSerializer

    def get_queryset(self):
        leader_id = self.kwargs['id']
        return Trips.objects.filter(travelead=leader_id)   



class FollowUserView(APIView):
    
    def post(self, request,id):
        user = request.user
        try:
            users = CustomUser.objects.get(id = request.user.id)
            profile = UserProfile.objects.get(user = id)
            
            if profile.followers.filter(id=request.user.id).exists():
                profile.followers.remove(request.user)
                return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
            else:
                profile.followers.add(request.user)
                receiver = CustomUser.objects.get(id=id)

                notification_type = "follow"
                text = f"{users.username} started following you"
                link = f"/travellerprofile"
                sender = user

                Notification.objects.create(
                    receiver=receiver,
                    sender=sender,
                    notification_type=notification_type,
                    text=text,
                    link=link,
                    is_read=False,
                )

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"notification_{id}",
                    {
                        "type": "send_notification",
                        "data": {
                            "type": notification_type,
                            "sender": profile.user.username,
                            "text": text,
                            "link": link,
                        },
                    },
                )
                return Response({'message': 'Followed successfully'}, status=status.HTTP_200_OK)
            
        
        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request,id):
        user = request.user.id
        try:
            profile = UserProfile.objects.get(user=id)
            
            
            is_following = profile.followers.filter(id=user).exists()
            
            total_followers = profile.followers.count()
            
            return Response({
                'is_following': is_following,
                'total_followers': total_followers,
            }, status=status.HTTP_200_OK)
        
        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)

class Followviewtravellers(APIView):
    def get(self, request):
        user = request.user.id
        try:
            user_profile = CustomUser.objects.get(id=user)
            total_completed_trip = Payment.objects.filter(user = user,trip__is_completed = 'completed').count()
            
            followed_travel_leaders = UserProfile.objects.filter(followers=user_profile)
            
            travel_leader_data = ProfileSerializer(followed_travel_leaders, many=True).data
            
            total_followed_leaders = followed_travel_leaders.count()
            
            return Response({
                'total_followed_leaders': total_followed_leaders,
                'travel_leaders': travel_leader_data,
                'total_completed_trip':total_completed_trip,
            }, status=status.HTTP_200_OK)
        
        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)



class ShowBookedTrip(APIView):
    
    def get(self, request):
        user = request.user  

        payments = Payment.objects.filter(user=user)

        if payments.exists():
            booked_trips = []

            for payment in payments:
                trip = payment.trip
                image_url = trip.Trip_image.url if trip.Trip_image else ''

                booked_trips.append({
                    'id': trip.id,
                    'name': trip.location,
                    'destination': trip.location,
                    'start_date': trip.start_date,
                    'end_date': trip.end_date,
                    'status': payment.status,
                    'image_url':image_url,
                })

            return Response({'booked_trips': booked_trips}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No booked trips found'}, status=status.HTTP_404_NOT_FOUND)
        


class CancelTrip(APIView):
    def post(self, request):
        user = request.user
        trip_id = request.data.get('trip_id')
        try:
            cancel = Payment.objects.get(user = user,trip=trip_id)
            trip = Trips.objects.get(id = trip_id)
            wallet = Wallet.objects.get(user = user)
            end_datetime = datetime.datetime.combine(trip.end_date, datetime.datetime.min.time())
            end_datetime = timezone.make_aware(end_datetime) 
            if timezone.now() >= end_datetime - timedelta(days=2):
                return Response({'message': 'You can only cancel the trip at least 2 days before the end date.'}, status=status.HTTP_400_BAD_REQUEST)
            trip.participant_limit = trip.participant_limit+1
            wallet.wallet = trip.amount
            wallet.save()
            trip.save()
             
            cancel.status = "cancelled"
           
            cancel.save()
            return Response({'message': 'Trip cancelled successfully.'}, status=status.HTTP_200_OK)
            
            
        
        except Payment.DoesNotExist:
            return Response({'error': 'payement not found'}, status=status.HTTP_404_NOT_FOUND)


class ShowWallet(APIView):
    def get(self, request):
        user = request.user
        try:
            
            wallet = Wallet.objects.get(user=user)
            user_profile = CustomUser.objects.get(id=request.user.id)
            total_completed_trip = Payment.objects.filter(user = user,trip__is_completed = 'completed').count()
            
            followed_travel_leaders = UserProfile.objects.filter(followers=user_profile)
            
            
            total_followed_leaders = followed_travel_leaders.count()

        except Wallet.DoesNotExist:
            return Response({'error': 'wallet not found'}, status=status.HTTP_404_NOT_FOUND)
        user_serializer = WalletSerializer(wallet)
        return Response({"wallet":user_serializer.data,"total_followed_leaders":total_followed_leaders}, status=status.HTTP_200_OK)



class WalletPayment(APIView):
    def post(self, request, *args, **kwargs):
        trip_id = request.data.get('trip_id')
        
        if not trip_id:
            return Response({'error': 'trip_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trip = Trips.objects.get(id=trip_id)
            user = request.user

            wallet = Wallet.objects.get(user=user)
            trip_cost = trip.amount

            existing_payment = Payment.objects.filter(user=user, trip=trip).first()

            if existing_payment:
                existing_payment.status = 'completed'  
                existing_payment.payment_type = 'wallet'  
                existing_payment.save()

                if wallet.wallet < trip_cost:
                    return Response({'error': 'Insufficient wallet balance'}, status=status.HTTP_400_BAD_REQUEST)

                wallet.wallet -= trip_cost
                wallet.save()

            else:
                if wallet.wallet >= trip_cost:
                    wallet.wallet -= trip_cost
                    wallet.save()

                    Payment.objects.create(
                        user=user,
                        trip=trip,
                        amount=trip_cost,  
                        status='completed',
                        payment_type='wallet'
                    )
                else:
                    return Response({'error': 'Insufficient wallet balance'}, status=status.HTTP_400_BAD_REQUEST)

            trip.participant_limit -= 1
            trip.save()

            return Response({'success': True, 'message': 'Payment completed using wallet'}, status=status.HTTP_200_OK)

        except Trips.DoesNotExist:
            return Response({'error': 'Trip not found'}, status=status.HTTP_404_NOT_FOUND)

        except Wallet.DoesNotExist:
            return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ChatPartnersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatPartnerSerializer

    def get_queryset(self):
        user = self.request.user
        sender_ids = ChatMessages.objects.filter(sender=user.id).values_list('receiver', flat=True)
        receiver_ids = ChatMessages.objects.filter(receiver=user.id).values_list('sender', flat=True)

        chat_partners_ids = set(sender_ids) | set(receiver_ids) 

        return CustomUser.objects.filter(id__in=chat_partners_ids) 


class MessageListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user.id
        receiver_id = self.kwargs['receiver_id']
        return ChatMessages.objects.filter(
            (Q(sender=current_user) & Q(receiver=receiver_id)) |
            (Q(receiver=current_user) & Q(sender=receiver_id))
        ).order_by('timestamp')


class TripDetailsTravelLeaders(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            trip = Trips.objects.prefetch_related('payment_set').filter(travelead=user.id)  
            serializer = TripSerializer(trip,many=True,context={'request': request})
           
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Trips.DoesNotExist:
            return Response({'error': 'Trip not found'}, status=status.HTTP_404_NOT_FOUND)
        
class CancelTripLeader(APIView):
    def post(self, request, id, *args, **kwargs):
        try:
            trip = Trips.objects.filter(id=id).first()

            if not trip:
                return Response({"error": "Trip not found"}, status=status.HTTP_404_NOT_FOUND)

            trip.is_completed = "cancelled"
            trip.save()

            trip_amount = trip.amount

            booked_customers = Payment.objects.filter(trip=id)

            if not booked_customers.exists():
                return Response({"message": "No customers booked for this trip"}, status=status.HTTP_200_OK)

            for payment in booked_customers:
                
                payment.status = "trip_cancelled"
                payment.save()

                
                wallet = Wallet.objects.get(user=payment.user)

                if wallet:
                    wallet.wallet += trip_amount  
                    wallet.save()

                    
                    send_mail(
                        subject='Trip Cancellation Notice',
                        message=f'Dear {payment.user.username},\n\nThe trip you booked has been cancelled due to unforeseen circumstances. '
                                f'We apologize for any inconvenience caused. The amount has been refunded to your wallet.\n\nBest regards,\nYour Travel Team',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[payment.user.email],
                        fail_silently=False,
                    )
                else:
                    return Response({"message": f"Wallet not found for user {payment.user.email}"}, status=status.HTTP_200_OK)

            return Response({"message": "Trip marked as cancelled, funds returned to wallets, and emails sent"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def mark_all_messages_as_read(request):
  
    partner_id = request.data.get('partner_id')
    current_user_id = request.user.id  

    if not partner_id:
        return Response({'error': 'Partner ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ChatMessages.objects.filter(
            sender=partner_id,  
            receiver=current_user_id,  
            is_read=False 
        ).update(is_read=True)

        return Response({'message': 'All unread messages marked as read.'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Refund.................
class RefundAPIView(APIView):
    def post(self, request, id):
        try:
           
            trip = Trips.objects.get(id = id)
            if trip.is_refund == True:
                return Response({"message": "Trip has already been refunded."}, status=status.HTTP_400_BAD_REQUEST)

            
            booked_customers = Payment.objects.filter(trip=id)
            sum = 0
            for i in booked_customers:
                sum = sum+1
            refund_amount = trip.amount * sum

           

            trip.is_refund = True
            trip.save()

            return Response({
                "message": "Refund successful.",
                "refunded_amount": refund_amount
            }, status=status.HTTP_200_OK)

        except Trips.DoesNotExist:
            return Response({"error": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class ViewPostsTravelleader(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=request.user.id)
            
            try:
                posts = Post.objects.filter(travel_leader=user).select_related('travel_leader')
                articles = ArticlePost.objects.filter(travel_leader=user).select_related('travel_leader')
                post_content_type = ContentType.objects.get_for_model(Post)
                post_ids = posts.values_list('id', flat=True)

                posts_serializer = PostSerializer(posts, many=True, context={'request': request})
                article_serializer = ArticleSerilizer(articles, many=True)
                post_comments = Comment.objects.filter(
                    content_type=post_content_type, object_id__in=post_ids, user=request.user
                )
                notification_count = Notification.objects.filter(receiver=request.user.id,is_read = False).count()
                post_comments_serializer = CommentSerializer(post_comments, many=True)
                
                return Response({
                    "posts": posts_serializer.data,
                    "articles": article_serializer.data,
                    "post_comments": post_comments_serializer.data,
                    "notification_count":notification_count
                }, status=status.HTTP_200_OK)

            except Post.DoesNotExist:
                return Response({"message": "no posts"}, status=status.HTTP_404_NOT_FOUND)

        except CustomUser.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        


class NotificationViewSet(viewsets.ModelViewSet):
  
    serializer_class = NotificationSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_as_read(self, request, id=None):
      
        notification = Notification.objects.get(id=id)
        notification.is_read = True
        notification.save()
        return response.Response(data="notification", status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def mark_all_as_read(self, request):
       
        notification = self.get_queryset()
        notification.update(is_read=True)
        return response.Response(
            data="All notification marked as read", status=status.HTTP_200_OK
        )

    def destroy(self, request, id):
       
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
    


class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

       
        user.create_reset_token()

        reset_url = f"http://localhost:5173/password-reset-confirm/{user.id}/{user.reset_token}"
        
        send_mail(
                        subject='PassWord Reset',
                        message=f'Click the link to reset your password: {reset_url} ',
                                
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email],
                        fail_silently=False,
                    )
       

        return Response({"message": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)





class PasswordResetConfirmView(APIView):
    def post(self, request):
        user_id = request.data.get('userid')
        password = request.data.get("password")
        token = request.data.get('token')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.reset_token != token:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.token_expiration < timezone.now():
            return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, data={'password': password}, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EditPostAPIView(APIView):
    def put(self, request, id):
        try:
            user = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if post.travel_leader != user:
            return Response({'error': 'You do not have permission to edit this post'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            post = serializer.save()
            post_data = PostSerializer(post).data
            return Response({"message": "Post updated successfully.", "post": post_data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateGroupView(APIView):
    def post(self, request, *args, **kwargs):
        trip_id = request.data.get('trip')
        members = request.data.get('members', [])
      

        try:
            trip = Trips.objects.get(id=trip_id)          
            if Group.objects.filter(trip=trip).exists():
                return Response({"message": "Group already created for this trip."}, status=status.HTTP_400_BAD_REQUEST)

            group = Group.objects.create(trip=trip)

            for member in members:
                user_id = member['user']  
                user = CustomUser.objects.get(id=user_id) 
                
                GroupMember.objects.create(group=group, user=user) 

            serializer = GroupSerializer(group)

           

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Trips.DoesNotExist:
            return Response({"message": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)


class ReportAPIView(APIView):
    """
    API View for submitting a report against a travel leader.
    """

    def post(self, request, id):
        try:
            travel_leader = CustomUser.objects.get(id=id)

            report_data = {
                "reporter": travel_leader.id, 
                "reported_user": request.user.id,  
                "reason": request.data.get("reason")  
            }
            serializer = UserReportSerializer(data=report_data)
            if serializer.is_valid():
                user_report = serializer.save()
                report_data = UserReportSerializer(user_report).data

                return Response({
                    "message": "Report submitted successfully.",
                    "report": report_data
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({"error": "Travel leader not found."}, status=status.HTTP_404_NOT_FOUND)



class UserReportListAPIView(APIView):
    """
    API View to retrieve all user reports.
    """

    def get(self, request):
        reports = UserReport.objects.all()  
        serializer = UserReportSerializer(reports, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    
    
    
    
