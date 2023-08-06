from django.db import models
from djangoldp.models import Model
from djangoldp_circle.models import Circle


class SpaceCategory(object):
    Etablissement = 'Etablissement'
    Evenement = 'Evenement'
    Thematique = 'Thematique'

    @classmethod
    def choices(cls):
        return (
            (cls.Etablissement, 'Etablissement'),
            (cls.Evenement, 'Evénement'),
            (cls.Thematique, 'Thématique'),
        )


class FCPESpace(Model):
    coverImage = models.URLField(blank=True, null=True)
    circle = models.OneToOneField(Circle, null=True, blank=True, related_name="space", on_delete=models.CASCADE)
    category = models.CharField(max_length=16, choices=SpaceCategory.choices(), default=SpaceCategory.Etablissement)

    class Meta(Model.Meta):
        pass


class EstablishmentSpaceInfo(Model):
    space = models.OneToOneField(FCPESpace, null=True, blank=True, related_name="establishment_info", on_delete=models.CASCADE)

    class Meta(Model.Meta):
        pass


class EventSpaceInfo(Model):
    space = models.OneToOneField(FCPESpace, null=True, blank=True, related_name="event_info", on_delete=models.CASCADE)

    class Meta(Model.Meta):
        pass


class ThemeSpaceInfo(Model):
    space = models.OneToOneField(FCPESpace, null=True, blank=True, related_name="theme_info", on_delete=models.CASCADE)

    class Meta(Model.Meta):
        pass
