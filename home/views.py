from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import filters
from .serializers import UserSerializer,FriendRequestSerializer,FriendshipRequestSerializer,FeedSerializer,ProfileSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets,status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from . import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .models import NewsFeedItem
from chat.models import Profile
from .pagination import PostPageNumberPagination
from django.apps import apps
from friendship.models import Friend,FriendshipRequest
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from .mixins import LikedMixin
from django.db.models import Q
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)






# Create your views here.
config = apps.get_app_config('home')

#Register API view
class Usercreate1(viewsets.ModelViewSet):
    """Handles creating, creating and updating profiles."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields=('username',)


#Login API
class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)




# Edit Profile API

class EditProfileView(viewsets.ModelViewSet):

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)





class FriendRequestViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = FriendRequestSerializer
    # queryset = FriendshipRequest.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user=self.request.user
        return FriendshipRequest.objects.filter(from_user=user)




    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""

        serializer.save(from_user=self.request.user)

    @action(methods=['get'],detail=True)

    def cancel(self, request, pk=None):
         friendship_request = get_object_or_404(FriendshipRequest, pk=pk, from_user=request.user)
         friendship_request.cancel()
         return Response(
             FriendshipRequestSerializer(friendship_request).data,
             status.HTTP_201_CREATED
         )




class FriendshipRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for FriendshipRequest model
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = FriendshipRequestSerializer

    def get_queryset(self):
        user=self.request.user
        return FriendshipRequest.objects.filter(to_user=user)


    @action(methods=['get'],detail=True)
    def accept(self, request, pk=None):
        friendship_request = get_object_or_404(FriendshipRequest, pk=pk, to_user=request.user)
        friendship_request.accept()
        return Response(
            FriendshipRequestSerializer(friendship_request).data,
            status.HTTP_201_CREATED
        )

    @action(methods=['get'],detail=True)
    def reject(self, request, pk=None):
        friendship_request = get_object_or_404(FriendshipRequest, pk=pk, to_user=request.user)
        friendship_request.reject()
        return Response(
            FriendshipRequestSerializer(friendship_request).data,
            status.HTTP_201_CREATED
        )



class FeedViewSet(LikedMixin,
                   viewsets.ModelViewSet):

        queryset = NewsFeedItem.objects.all()
        serializer_class = FeedSerializer
        permission_classes = (permissions.PostOwnStatus,IsAuthenticated )
        pagination_class = PostPageNumberPagination

        def perform_create(self, serializer):
            """Sets the user profile to the logged in user."""

            serializer.save(user_profile=self.request.user)



# class DialogueViewSet(viewsets.ModelViewSet):
#
#     serializer_class = DialogSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#
#
#         user=self.request.user
#
#         return Dialog.objects.filter(Q(owner=user) | Q(opponent=user))
#
#     def perform_create(self, serializer):
#         """Sets the user profile to the logged in user."""
#
#         serializer.save(owner=self.request.user)
#     # def create(self,**kwargs):
#
#
# class MessageViewSet(viewsets.ModelViewSet):
#
#     serializer_class = MessageSerializer
#     permission_classes = (IsAuthenticated,)
#
#
#
#
#     def get_queryset(self):
#
#
#         user=self.request.user
#
#         return Message.objects.filter(sender=user)





#
#
#
#
# class ChatListView(ListAPIView):
#     serializer_class = ChatSerializer
#     permission_classes = (IsAuthenticated, )
#
#     def get_queryset(self):
#         queryset = Chat.objects.all()
#         username = self.request.user
#         if username is not None:
#             contact = get_user_contact(username)
#             queryset = contact.chats.all()
#         return queryset
#
#
# class ChatDetailView(RetrieveAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (IsAuthenticated, )
#
#
# class ChatCreateView(CreateAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (IsAuthenticated, )
#
#
# class ChatUpdateView(UpdateAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (IsAuthenticated, )
#
#
# class ChatDeleteView(DestroyAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (IsAuthenticated, )



