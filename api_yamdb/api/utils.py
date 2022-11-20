from rest_framework import mixins, viewsets


class ListEditViewSet(viewsets.GenericViewSet,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin):
    """Миксин для просмотра отдельной записи и её изменения"""
    pass