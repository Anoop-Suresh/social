from rest_framework import serializers
from django.contrib.auth.models import User
from .models import NewsFeedItem
from chat.models import Profile
from friendship.models import FriendshipRequest,Friend
from django.contrib.auth import get_user_model
from . import services as likes_services
# from django_private_chat.models import Dialog,Message
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
        'id','username','email','password')

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""

        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model= Profile
        fields='__all__'





class NewsFeedItemSerializer(serializers.ModelSerializer):
    """A serializer for profile feed items."""

    class Meta:
        model = NewsFeedItem
        fields = ('id', 'user_profile', 'cover','status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}





class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendshipRequest
        fields = ('id', 'from_user', 'to_user')
        extra_kwargs = {'from_user': {'read_only': True}}


#
# class FriendAcceptSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Friend
#         fields = ('id', 'from_user', 'to_user')
#         extra_kwargs = {'to_user': {'read_only': True}}



class FriendshipRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendshipRequest
        fields = ('id', 'from_user', 'to_user', 'message', 'created', 'rejected', 'viewed')






from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class FanSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'full_name',
        )

    def get_full_name(self, obj):
        return obj.get_full_name()



class FeedSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = NewsFeedItem
        fields = (
            'id',
            'user_profile', 'cover','status_text', 'created_on',
            'is_fan',
            'total_likes',
        )
        extra_kwargs = {'user_profile': {'read_only': True}}

    def get_is_fan(self, obj) -> bool:
        """Check if a `request.user` has liked this tweet (`obj`).
        """
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)



# class DialogSerializer(serializers.ModelSerializer):
#     """A serializer for profile feed items."""
#     # opponent = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
#     def create(self, validated_data):
#         # opponent=validated_data.get('opponent',None)
#         dialog, created = Dialog.objects.get_or_create(**validated_data)
#         return dialog
#     class Meta:
#         model = Dialog
#         fields = ('id', 'owner','opponent')
#         extra_kwargs = {'owner': {'read_only': True}}
#
#
# class MessageSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model=Message
#         fields=('id','sender','dialog','text')
#




# class ContactSerializer(serializers.StringRelatedField):
#     def to_internal_value(self, value):
#         return value
#
#
# class ChatSerializer(serializers.ModelSerializer):
#     participants = ContactSerializer(many=True)
#
#     class Meta:
#         model = Chat
#         fields = ('id', 'messages', 'participants')
#         read_only = ('id')
#
#     def create(self, validated_data):
#         print(validated_data)
#         participants = validated_data.pop('participants')
#         chat = Chat()
#         chat.save()
#         for username in participants:
#             contact = get_user_contact(username)
#             chat.participants.add(contact)
#         chat.save()
#         return chat
