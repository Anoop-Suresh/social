from .serializers import FanSerializer
from rest_framework.response import Response
from . import services
from rest_framework.decorators import action


class LikedMixin:

    @action(methods=['GET'],detail=True)
    def like(self, request, pk=None):
        """Like a model instance.
        """
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(methods=['GET'],detail=True)
    def unlike(self, request, pk=None):
        """Unlike a model instance.
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()

    @action(methods=['GET'],detail=True)
    def fans(self, request, pk=None):
        """Get the users which liked a model instance.
        """
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data)