from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('register/', views.RegisterationApi.as_view(),name="register"),
    path('otpverify/',views.VerifyOtp.as_view(),name = 'verify_otp'),
    path('selectingrole/',views.SelectinTravelleader.as_view(),name = 'selecting-role'),
    path('userpreference/',views.Userpreference.as_view(),name = 'preference1'),
    path('login/',views.CustomTokenObtainPairView.as_view(),name = 'login'),           
    path('send/',views.SendOTPView.as_view(),name = 'send'),
    path('formsubmission/',views.FormSubmissionView.as_view(),name = 'form'),
    path('formview/',views.TravelLeaderListView.as_view(),name = 'formview'),
    path('details/<int:id>/',views.TravelLeaderDetailView.as_view(),name = 'details'),
    path('accept/<int:pk>/', views.AcceptTravelLeaderView.as_view(), name='accept_travel_leader'),
    path('reject/<int:pk>/', views.RejectTravelLeaderView.as_view(), name='reject_travel_leader'),
    path('travellers/', views.TravellersView.as_view(), name='travellers'),
    path('block/<int:pk>/', views.is_Block.as_view(), name='block'),
    path('travellerprofile/', views.TravellerProfile.as_view(), name='travellerprofile'),
    path('editprofile/', views.UserProfileEdit.as_view(), name='editprofile'),
    path('profile/', views.UserProfileCreate.as_view(), name='udateprofile'),
    path('createtrip/', views.CreateTrip.as_view(), name='createtrip'),
    path('viewtrip/', views.ViewTrips.as_view(), name='viewtrip'),
    path('updatetrip/', views.EditTrips.as_view(), name='updatetrip'),
    path('addplaces/', views.AddPlaces.as_view(), name='addplaces'),
    path('viewplaces/<int:id>/', views.ViewPlaces.as_view(), name='viewplaces'),
    path('editplaces/<int:id>/', views.EditPlace.as_view(), name='editplaces'),
    path('deleteplaces/<int:id>', views.DeleteItem.as_view(), name='delete'),
    path('viewalltrips/', views.ViewAllTrips.as_view(), name='view_all_trips'),
    path('viewonetrip/<int:id>/', views.TripDetails.as_view(), name='view_one_trips'),
    path('placedetails/<int:id>/', views.PlaceDetails.as_view(), name='view_places_details'),
    path('posts/', views.PostCreation.as_view(), name='posts'),
    path('article/', views.ArticlePosts.as_view(), name='article'),
    path('viewposts/', views.ViewPosts.as_view(), name='viewposts'),
    path('viewusers/', views.ViewUser.as_view(), name='viewposts'),
    path('viewarticle/', views.ViewArticle.as_view(), name='viewarticle'),
    path('likeposts/<int:id>/', views.LikeTravelPostAPIView.as_view(), name='like_travel_post'),
    path('likearticle/<int:id>/', views.LikeArticleView.as_view(), name='like_travel_article'),
    path('commentcreate/', views.CommentCreateView.as_view(), name='comment_create'),
    path('commentview/', views.CommentListView.as_view(), name='comment_view'),
    path('create-checkout-session/' , views.CreateStripeSessionAPIView.as_view(),name='checkout'),  
    path('adminviewtrip/<int:id>/' , views.TripsByLeaderView.as_view(),name='tripbyleaderview'),  
    path('follow/<int:id>', views.FollowUserView.as_view(), name='follow_user'),
    path('showbookedtrip/', views.ShowBookedTrip.as_view(), name='show_booked_trip'),
    path('confirm-payment/', views.ConfirmPaymentAPIView.as_view(), name='confirm_payment'),
    path('canceltrip/', views.CancelTrip.as_view(), name='canceltrip'),
    path('showwallet/', views.ShowWallet.as_view(), name='wallet'),
    path('wallet_payment/', views.WalletPayment.as_view(), name='wallet_pay'),
    path('chat-partners/', views.ChatPartnersView.as_view(), name='chat-partners'),
    path('messages/<int:receiver_id>/', views.MessageListView.as_view(), name='message-list'),
    path('trip_details/', views.TripDetailsTravelLeaders.as_view(), name='trip-details'),
    path('trip_cancel/<int:id>', views.CancelTripLeader.as_view(), name='trip-cancel'),
    path('mark-all-messages-as-read/', views.mark_all_messages_as_read, name='mark_all_messages_as_read'),
    path('refund/<int:id>', views.RefundAPIView.as_view(), name='refund'),
    path('following-leaders/', views.Followviewtravellers.as_view(), name='following'),
    path('fetchposts/', views.ViewPostsTravelleader.as_view(), name='posts'),
    path(
        "notification/",
        views.NotificationViewSet.as_view({"get": "list"}),
        name="notification",
    ),
    path(
        "notification/<int:id>",
        views.NotificationViewSet.as_view({"delete": "destroy"}),
        name="notification",
    ),
    path("mark_as_read/<int:id>",views.NotificationViewSet.as_view({"post": "mark_as_read"}), name="mark_as_read"),
    path("mark_all_as_read", views.NotificationViewSet.as_view({"post": "mark_all_as_read"}), name="mark_all_as_read"),
    path("forgot-password/", views.PasswordResetRequestView.as_view(), name="forgot_password"),
    path("password-reset/", views.PasswordResetConfirmView.as_view(), name="password_confirm"),
    path("edit-post-view/<int:id>/", views.EditPostAPIView.as_view(), name="edit-post"),
    path('groups/', views.CreateGroupView.as_view(), name='create_group'),
    path('report/<int:id>/', views.ReportAPIView.as_view(), name='report-user'),
    path('reports/', views.UserReportListAPIView.as_view(), name='user-report-list'),

    # path('token/refresh/', views.RefreshTokenAPIView.as_view(), name='token_refresh'),







   
    

 



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)