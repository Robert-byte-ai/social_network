from rest_framework import mixins, viewsets


class CreateListMixins(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    pass


class DestroyCreateMixins(mixins.DestroyModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    pass
