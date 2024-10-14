from rest_framework import serializers
from .models import GroupMember, Notification, UserReport, CustomUser,UserProfile,TravelLeaderForm,Country,Trips,Place,Post,ArticlePost,Comment,Payment, Wallet,ChatMessages,Group,GroupChat
from django.db.models import Q

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'is_travel_leader', 'email', 'password','username','is_verified','is_block','user_preference','is_approve_leader','date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        
       
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.generate_otp()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password) 
        return super().update(instance, validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id','profile_image','address','bio','country_state','user','username']


class CountryField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        
        if isinstance(data, list):
            country_names = data
            countries = Country.objects.filter(name__in=country_names)
            if countries.count() != len(country_names):
                raise serializers.ValidationError("Some country names are invalid.")
            return countries
        return super().to_internal_value(data)
    

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country  
        fields = ['id','name']  


    

class FormSubmission(serializers.ModelSerializer):
    visited_countries = CountrySerializer(many=True, read_only=True)
    selectedCountries = CountryField(
        queryset=Country.objects.all(), 
        many=True, 
        required=False, 
        allow_empty=True,
        source='visited_countries'
    )
    user_id = UserSerializer()

    class Meta:
        model = TravelLeaderForm
        fields = ['id', 'visited_countries', 'firstname', 'lastname', 'cv', 'id_proof', 'is_approved', 'mobile', 'user_id','selectedCountries','bank_account_name','bank_account_number','bank_name','ifsc_code']

    def create(self, validated_data):
        selected_countries = validated_data.pop('visited_countries', [])
        instance = super().create(validated_data)
        instance.visited_countries.set(selected_countries)
        return instance

    def update(self, instance, validated_data):
        selected_countries = validated_data.pop('visited_countries', [])
        instance = super().update(instance, validated_data)
        instance.visited_countries.set(selected_countries)
        return instance
    

class PaymentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'trip',
            'amount',
            'status',
            'created_at',
            'payment_type',
            'user_username',
            'user_email',
        ]
    

class TripSerializer(serializers.ModelSerializer):
    travelead_username = serializers.CharField(source='travelead.username', read_only=True)
    travelead_email = serializers.CharField(source='travelead.email', read_only=True)
   
    booked_customers = PaymentSerializer(many=True, read_only=True, source='payment_set')
    travelead_profile_image = serializers.SerializerMethodField()
    travelead_bio = serializers.SerializerMethodField()
    travelead_address = serializers.SerializerMethodField()
    class Meta:
        model = Trips
        fields = [
            'id',
            'travelead_username',
            'travelead_email',
            'Trip_image', 
            'location', 
            'trip_type',  
            'start_date', 
            'end_date',    
            'duration', 
            'description', 
            'accomodation', 
            'transportation', 
            'amount', 
            'participant_limit' ,
            'travelead_profile_image' ,
            'booked_customers',
            'is_completed',
            'travelead',
            'travelead_bio',
            'travelead_address',
            'is_refund',
            'is_group'
        ]
        extra_kwargs = {
            'travelead': {'read_only': True}  
        }
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        
        trip = Trips.objects.create(travelead=user, **validated_data)
        return trip
    
    def get_travelead_profile_image(self, obj):
        try:
            user_profile = UserProfile.objects.get(user=obj.travelead)
            
            if user_profile.profile_image:
                request = self.context.get('request')
                
                
                if request:
                    return request.build_absolute_uri(user_profile.profile_image.url)
            return None
        except UserProfile.DoesNotExist:
            return None
    
    def get_travelead_bio(self, obj):
        try:
            user_profile = UserProfile.objects.get(user=obj.travelead)
            return user_profile.bio if user_profile.bio else None
        except UserProfile.DoesNotExist:
            return None
    
    def get_travelead_address(self, obj):
        try:
            user_profile = UserProfile.objects.get(user=obj.travelead)
            return user_profile.address if user_profile.address else None
        except UserProfile.DoesNotExist:
            return None


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'trip', 'place_name', 'description', 'accomodation','Transportation','place_image']
    
    
    
    
class PostSerializer(serializers.ModelSerializer):
    travelead_username = serializers.CharField(source='travel_leader.username', read_only=True)
    total_likes = serializers.IntegerField( read_only=True)
    travelead_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','travel_leader','post_image','description','created_at','travelead_profile_image',"travelead_username",'likes',"total_likes"]
        read_only_fields = ['id', 'travel_leader', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        print(request)
        user = request.user

        validated_data['travel_leader'] = user
        likes_data = validated_data.pop('likes', None)
    
        # post = Post.objects.create(**validated_data)
    
        if likes_data:
            post.likes.set(likes_data)  

        post = Post.objects.create(**validated_data)
        return post
    
    # def create(self, validated_data):
    #     likes_data = validated_data.pop('likes', None)
    
    #     post = Post.objects.create(**validated_data)
    
    #     if likes_data:
    #         post.likes.set(likes_data)  
    #     return post
    
   
    def get_travelead_profile_image(self,obj):
        try:
            print(obj)
            user_profile = UserProfile.objects.get(user=obj.travel_leader)
            if user_profile.profile_image:
                request = self.context.get('request')
                
                
                if request:
                    return request.build_absolute_uri(user_profile.profile_image.url)
            return None
        except UserProfile.DoesNotExist:
            return None



class ArticleSerilizer(serializers.ModelSerializer):
    travelead_username = serializers.CharField(source='travel_leader.username', read_only=True)

    travelead_profile_image = serializers.SerializerMethodField()
    class Meta:
        model = ArticlePost
        fields = '__all__'
        read_only_fields = ['id', 'travel_leader', 'created_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        validated_data['travel_leader'] = user
        likes_data = validated_data.pop('likes', None)
    
        # post = ArticlePost.objects.create(**validated_data)
    
        if likes_data:
            post.likes.set(likes_data)  

        post = ArticlePost.objects.create(**validated_data)
        return post
    def get_travelead_profile_image(self,obj):
        try:
            print(obj)
            user_profile = UserProfile.objects.get(user=obj.travel_leader)
            if user_profile.profile_image:
                request = self.context.get('request')
                
                
                if request:
                    return request.build_absolute_uri(user_profile.profile_image.url)
            return None
        except UserProfile.DoesNotExist:
            return None

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at', 'content_type', 'object_id','profile_image']

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if hasattr(obj.user, 'profile_image') and obj.user.profile_image:
            return request.build_absolute_uri(obj.user.profile_image.url)
        return None
    
    def create(self, validated_data):
        request = self.context.get('request')
        content_object = validated_data.get('content_object')
        return Comment.objects.create(
            user=request.user,
            content_object=content_object,
            text=validated_data.get('text')
        )

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user', 'wallet'] 


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessages
        fields = ['sender', 'receiver', 'content', 'timestamp','is_read']




class ChatPartnerSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()


    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'last_message','unread_count']

    def get_last_message(self, obj):
        user = self.context['request'].user 
        last_message = ChatMessages.objects.filter(
            (Q(sender=user.id) & Q(receiver=obj.id)) | (Q(sender=obj.id) & Q(receiver=user.id))
        ).order_by('-timestamp').first() 

        if last_message:
            return ChatMessageSerializer(last_message).data  
        return None 
    
    def get_unread_count(self, obj):
        user = self.context['request'].user
        # Count unread messages sent from the partner to the current user
        unread_count = ChatMessages.objects.filter(
            receiver=user.id,
            sender=obj.id,
            is_read=False
        ).count()
        return unread_count 
    

class NotificationSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Notification
        fields = [
            "id",
            "sender",
            "text",
            "link",
            "is_read",
            "created_at",
            "notification_type",
        ]




class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GroupMember
        fields = ['user', 'joined_at']

class GroupSerializer(serializers.ModelSerializer):
    members = GroupMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'trip', 'members', 'created_at']

    def create(self, validated_data):
        members_data = self.context['request'].data.get('members', [])
        group = Group.objects.create(**validated_data)
        for member_data in members_data:
            GroupMember.objects.create(group=group, **member_data)
        return group


class GroupChatSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = GroupChat
        fields = ['id', 'group', 'sender', 'content', 'timestamp']

    def create(self, validated_data):
        group_chat = GroupChat.objects.create(**validated_data)
        return group_chat




class UserReportSerializer(serializers.ModelSerializer):
    reporter_name = serializers.CharField(source='reporter.username', read_only=True)  
    reported_user_name = serializers.CharField(source='reported_user.username', read_only=True)  
    reporter_email = serializers.EmailField(source='reporter.email', read_only=True)  
    reported_user_email = serializers.EmailField(source='reported_user.email', read_only=True) 

    class Meta:
        model = UserReport
        fields = ['reporter', 'reported_user', 'reason','reporter_email','reported_user_email','reporter_name','reported_user_name']



        


