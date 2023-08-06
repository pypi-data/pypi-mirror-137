from django.db import models
from djangoldp.models import Model
from djangoldp_circle.models import Circle


class FCPESpace(Model):
    coverImage = models.URLField(blank=True, null=True)

    class Meta(Model.Meta):
        abstract = True


class EstablishmentSpace(FCPESpace):
    circle = models.ForeignKey(Circle, null=True, blank=True, related_name="spaces_establishments", on_delete=models.CASCADE)

    class Meta(FCPESpace.Meta):
        pass


class EventSpace(FCPESpace):
    circle = models.ForeignKey(Circle, null=True, blank=True, related_name="spaces_events", on_delete=models.CASCADE)

    class Meta(FCPESpace.Meta):
        pass


class ThemeSpace(FCPESpace):
    circle = models.ForeignKey(Circle, null=True, blank=True, related_name="spaces_themed", on_delete=models.CASCADE)

    class Meta(FCPESpace.Meta):
        pass
