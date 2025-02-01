from django.urls import path
from admin_soft import views
from . import views
from home import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('billing/', views.billing, name='billing'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chat_with_gemini/', views.chat_with_gemini, name='chat_with_gemini'),
    path('tables/', views.tables, name='tables'),
    path('vr/', views.vr, name='vr'),
    path('rtl/', views.rtl, name='rtl'),
    path('profile/', views.profile, name='profile'),
    path('payment/',views.payment,name='payment'),
    path('eco-friendly/', views.eco_friendly_view, name='eco_friendly'),  # Map to the view
    path('ecostore/', views.product_list, name='ecostore'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),


    # Urls
    path('recommend/', views.get_clothing_recommendation, name='recommend'),
    path('passItOver/', views.item_view, name='passItOver'),
    path('resellItem/', views.resellItem, name='resellItem'),
    path('donateItem/', views.donateItem, name='donateItem'),


    path('mirror/', views.mirror, name='mirror'),

    path('wardrobe/', views.wardrobe, name='wardrobe'),
    path('add_dress/', views.add_dress, name='add_dress'),
    path('view_model/', views.viewModel, name='view_model'),


    path('worn_today/<str:key>/', views.worn_today, name='worn_today'),


    path('stream/', views.video_feed, name='video_feed'),
    path('sponsor-selfie/', views.video_feed_with_banner, name='sponsor_selfie'),

     path('create/', views.create_post, name='createPost'),
    path('feed/', views.feed, name='communityFeed'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.comment_post, name='comment_post'),
    path('toggle-event-status/<str:event_name>/', views.toggle_event_status, name='toggle_event_status'),
    path('basicItem/', views.basic_item_view, name='basicItem'),
    path('advanceItem/', views.advance_item_view, name='advanceItem'),
    path('premiumItem/', views.premium_item_view, name='premiumItem'),
    path('addItem/', views.addItem, name='add_item'),
    path('fixtures/', views.generate_fixtures, name='generate_fixtures'),
    path('judge_fixtures/<str:sport>/', views.judge_fixtures, name='judge_fixtures'),
    path('view_fixtures/', views.view_fixtures, name='view_fixtures'),
    path('certificate/', views.certificate_view, name='certificate_view'),
    path('certificate/download/<str:recipient_name>/', views.download_certificate, name='download_certificate'),
    path('get-img-url/', views.get_all_image_urls, name='get_img_url'),
    path('leaderboard/', views.view_leaderboard, name='leaderboard'),
    path('track-image-click/', views.track_image_click, name='track_image_click'),


    # Authentication
    
    path('accounts/logout/', views.logout_view, name='logout'),
    path('admin/logout/', views.logout_view, name='logout'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),



    path('accounts/login/', views.login, name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/admin-login/', views.admin_login, name='admin_login'),
    path('accounts/admin-register/', views.admin_register, name='admin_register'),

    path('accounts/create-event/', views.create_event, name='create_event'),
    path('accounts/add-leader/', views.add_leader, name='add_leader'),
    path('accounts/add-judge/', views.add_judge, name='add_judge'),
    path('accounts/add-sponsor/', views.add_sponsor, name='add_sponsor'),
    path('accounts/additional_register/', views.additional_register, name='add_register'),
    path('accounts/view-events/', views.get_events, name='view_events'),
    path('accounts/register-team/', views.register_team, name='register_teams'),
]
