from rest_framework import mixins, viewsets


class CreateListMixins(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    pass


class DestroyCreateMixin(mixins.DestroyModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    pass
