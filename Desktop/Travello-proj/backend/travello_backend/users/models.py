from datetime import datetime, timezone,timedelta
from django.db import models
from datetime import timedelta
import uuid
# Create your models here.
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



class CustomUser(AbstractUser):
    username = models.CharField(max_length=800,null=True)
    email = models.EmailField(max_length=254,unique=True,null = True)
    is_travel_leader = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    is_block = models.BooleanField(default=False)
    otp = models.CharField(max_length=254,null = True)
    is_verified = models.BooleanField(default=False)
    is_approve_leader = models.BooleanField(default=False)
    user_preference = models.CharField(max_length=254,null = True)
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    token_expiration = models.DateTimeField(blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    def __str__(self):
        return self.username

    def generate_otp(self):
        otp = get_random_string(length=6, allowed_chars="1234567890")
        # self.otp_expiration = now + timedelta(seconds=60)
        self.otp = otp
        self.save()
        self.otp_expiration = timezone.now() + timedelta(seconds=60) 
        self.send_otp_email()
    
    def is_otp_expired(self):
        now = timezone.now()  
        return now > self.otp_expiration
    

    
    def send_otp_email(self):
        subject = "Your OTP for Signup"
        message = f"Your OTP is {self.otp}. Enter this code to complete your signup."
        from_email = "worldmagical491@gmail.com" 
        to_email = [self.email]
        send_mail(subject, message, from_email, to_email)
    
    def create_reset_token(self):
        """Generates a reset token and expiration time."""
        self.reset_token = uuid.uuid4().hex
        self.token_expiration = timezone.now() + timedelta(hours=1)  
        self.save()

   

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.generate_otp()


class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='userprofile')
    profile_image = models.ImageField(upload_to='media', blank=True, null=True)
    address = models.TextField(max_length=345)
    bio = models.CharField(max_length=234,null=True)
    country_state = models.CharField(max_length=234,null=True)
    followers = models.ManyToManyField(CustomUser, related_name='following', blank=True)
    
    def __str__(self):
        return f"{self.user.username} - Profile"
    
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class TravelLeaderForm(models.Model):
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    email = models.EmailField(max_length=254,unique=True,null = True)
    visited_countries = models.ManyToManyField(Country, related_name='visited_by')
    firstname = models.CharField(max_length=255,null = True)
    lastname = models.CharField(max_length=255,null= True)
    mobile = models.BigIntegerField()
    cv = models.FileField(upload_to='cv', blank=True, null=True)
    id_proof = models.FileField(upload_to='id_proof', blank=True, null=True)
    is_approved = models.CharField(max_length=254,default="pending") 
    bank_account_name = models.CharField(max_length=255, null=True, blank=True)  
    bank_account_number = models.CharField(max_length=50, null=True, blank=True)  
    bank_name = models.CharField(max_length=255, null=True, blank=True)  
    ifsc_code = models.CharField(max_length=20, null=True, blank=True)  
    def __str__(self):
        return f"{self.user_id.username}'s Travel Leader Profile"

    def approve(self):
        self.is_approved = "accepted"
        self.save()
       
    def reject(self):
        self.is_approved = "rejected"
        self.save()


@receiver(post_save, sender=TravelLeaderForm)
def handle_travel_leader_form_save(sender, instance, created, **kwargs):
    
    if not created:
        if instance.is_approved == "accepted":
            send_mail(
                'Application Approved',
                'Congratulations! Your application has been approved.',
                'worldmagical491@gmail.com', 
                [instance.email],  
                fail_silently=False,
            )
        elif instance.is_approved == "rejected":
            send_mail(
                'Application Rejected',
                'Sorry, your application has been rejected.',
                'worldmagical491@gmail.com',  
                [instance.email], 
                fail_silently=False,
            )


class Trips(models.Model):
    travelead = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Trip_image  =    models.ImageField(upload_to='media', blank=True, null=True)
    location =   models.CharField(max_length=250,null=True)
    trip_type = models.CharField(max_length=250,null=True)
    start_date =  models.DateField()
    end_date = models.DateField()
    duration = models.IntegerField(null=True,blank=True)
    description= models.TextField(max_length=345,null=True,blank=True)
    accomodation = models.CharField(max_length=250,null=True)
    transportation =  models.CharField(max_length=345)
    amount =  models.IntegerField()
    participant_limit = models.IntegerField()
    is_completed = models.CharField(max_length=254,default="pending")
    is_refund = models.CharField(default="false")
    is_group = models.CharField(default="false")
    def __str__(self):
        return f"{self.location} - {self.trip_type} by {self.travelead.username}"


class Place(models.Model):
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)
    place_image = models.ImageField(upload_to='media', blank=True, null=True)

    place_name = models.CharField(max_length=250)
    description = models.TextField(max_length=1000, null=True, blank=True)
    accomodation = models.TextField(max_length=234,null= True,blank = True)
    Transportation = models.TextField(max_length=234,null=True,blank=True)


class Post(models.Model):
    travel_leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='media', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type_of_trip = models.CharField(blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(CustomUser, related_name='liked_travel_posts', blank=True)
    def __str__(self):
        return f'Post by {self.travel_leader.username} at {self.created_at}'
    @property
    def like_count(self):
        return self.likes.count()
    
class ArticlePost(models.Model):
    travel_leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    article = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_travel_articles', blank=True)
    
    @property
    def like_count(self):
        return self.likes.count()

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.content_type} ID: {self.object_id}"



class Payment(models.Model):
    
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=355, default='Ongoing')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=255)


    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} for {self.trip.location} - {self.status}"
    

class ChatMessages(models.Model):
    sender = models.IntegerField(null=True,blank= True)
    receiver = models.IntegerField(null=True,blank= True)
    content = models.TextField()
    thread_name = models.CharField(max_length=30,null= True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class Wallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    wallet = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user.username}'s Wallet: {self.wallet}"
    



class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ("message", "Message"),
        ("trip_edited", "Trip is Edited"),
        ("new_trip_created", "New Trip is Created"),
        ("follow", "Follow"),
        ("user_is_booked", "User is Booked"),
       
    )
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sent_notifications", null=True
    )
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notifications", null=True
    )
    notification_type = models.CharField(
        max_length=50, choices=NOTIFICATION_TYPES, null=True
    )
    text = models.TextField(null=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Notification for {self.receiver.username} from {self.sender.username}: {self.text}"
    


class Group(models.Model):
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE) 
    members = models.ManyToManyField(CustomUser, through='GroupMember') 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Group for {self.trip.title}"

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    joined_at = models.DateTimeField(auto_now_add=True)  
    class Meta:
        unique_together = (('group', 'user'),)  

    def __str__(self):
        return f"{self.user.username} in {self.group.trip.title}"
    

class GroupChat(models.Model):
    group =  models.ForeignKey(Group, on_delete=models.CASCADE) 
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)  
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    content = models.TextField()  
    timestamp = models.DateTimeField(auto_now_add=True)  


class UserReport(models.Model):
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reports_made")
    reported_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reports_received")
    reason = models.TextField()  

    def __str__(self):
        return f"Report by {self.reporter} on {self.reported_user}"

