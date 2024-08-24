from datetime import datetime, timezone,timedelta
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver



class Usermodels(AbstractUser):
    username = models.CharField(max_length=800,null=True)
    email = models.EmailField(max_length=254,unique=True,null = True)
    is_travel_leader = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_block = models.BooleanField(default=True)
    otp = models.CharField(max_length=254,null = True)
    is_verified = models.BooleanField(default=False)
    is_approve_leader = models.BooleanField(default=False)
    user_preference = models.CharField(max_length=254,null = True)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    def __str__(self):
        return self.username

    def generate_otp(self):
        otp = get_random_string(length=6, allowed_chars="1234567890")
        now = datetime.now(timezone.utc)
        # self.otp_expiration = now + timedelta(seconds=60)
        self.otp = otp
        self.save()
        self.send_otp_email()
    
    def is_otpexperied(self):
        now = datetime.now(timezone.utc)
        self.otp_expiration = now + timedelta(seconds=60)
        return datetime.now(timezone.utc) > now + timedelta(seconds=60)
    

    
    def send_otp_email(self):
        subject = "Your OTP for Signup"
        message = f"Your OTP is {self.otp}. Enter this code to complete your signup."
        from_email = "worldmagical491@gmail.com" 
        to_email = [self.email]
        send_mail(subject, message, from_email, to_email)

   

@receiver(post_save, sender=Usermodels)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.generate_otp()


class UserProfile(models.Model):
    user = models.ForeignKey(Usermodels,on_delete=models.CASCADE,related_name='userprofile')
    profile_image = models.ImageField(upload_to='media', blank=True, null=True)
    address = models.TextField(max_length=345)
    bio = models.CharField(max_length=234,null=True)
    country_state = models.CharField(max_length=234,null=True)
    
    def __str__(self):
        return f"{self.user.username} - Profile"
    
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class TravelLeaderForm(models.Model):
    user_id = models.ForeignKey(Usermodels,on_delete=models.CASCADE)
    email = models.EmailField(max_length=254,unique=True,null = True)
    visited_countries = models.ManyToManyField(Country, related_name='visited_by')
    firstname = models.CharField(max_length=255,null = True)
    lastname = models.CharField(max_length=255,null= True)
    mobile = models.BigIntegerField()
    cv = models.FileField(upload_to='cv', blank=True, null=True)
    id_proof = models.FileField(upload_to='id_proof', blank=True, null=True)
    is_approved = models.CharField(max_length=254,default="pending") 
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

    

