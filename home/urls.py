from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Resgister',views.Usercreate1)#mension path in space given between''
router.register('Login', views.LoginViewSet, base_name='login')
router.register('Profile',views.EditProfileView, base_name='editprofile')
router.register('Newsfeed', views.FeedViewSet)


router.register("SendFriendRequest",views.FriendRequestViewSet,base_name='SendFriendRequest')

router.register('friendrequests',views.FriendshipRequestViewSet, base_name='friendrequests')


# router.register('chat',views.DialogueViewSet,base_name='chat')
# router.register('message',views.MessageViewSet,base_name='message')







urlpatterns=[
    path('', include(router.urls)),
    # path('chat/', views.ChatListView.as_view()),
    # path('chat/create/', views.ChatCreateView.as_view()),
    # path('chat/<pk>/', views.ChatDetailView.as_view()),
    # path('chat/<pk>/update/', views.ChatUpdateView.as_view()),
    # path('chat/<pk>/delete/', views.ChatDeleteView.as_view())

    # path('messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    # path('messages', views.message_list, name='message-list'),

    # path('login',views.login,name="login"),
    # path('register1', views.Usercreate1.as_view(), name='account-create1'),
]