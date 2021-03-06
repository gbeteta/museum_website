from django.db import models
from model_utils.managers import InheritanceManager

CONDITION_CHOICES = [
    (1, ("Preserved"),),
    (2, ("Fair"),),
    (3, ("Damaged"),)
]

CONDITION_CHOICES_ORGANISM = [
    (1, ("Live"),),
    (2, ("Taxidermied"),)
]

class Gallery(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Galleries"

class Exhibition(models.Model):
    name = models.CharField(max_length=100)
    sponsor = models.CharField(max_length=100)
    start_date = models.DateField('Date exhibition starts')
    end_date = models.DateField('Date exhibition ends')
    active = models.BooleanField()
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField('Item description')
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE)

    # Manage inheritance (one-to-one Item types)
    objects = InheritanceManager()

    def __str__(self):
        return self.name

class Artifact(Item):
    country_origin = models.CharField(max_length=100)
    excavation_site = models.CharField(max_length=150)
    discovery_year = models.IntegerField('Year artifact was discovered')
    condition = models.IntegerField(choices=CONDITION_CHOICES)
    material = models.CharField(max_length=50)

class Organism(Item):
    scientific_name = models.CharField(max_length=100)
    condition = models.IntegerField(choices=CONDITION_CHOICES_ORGANISM)

class Fossil(Item):
    country_origin = models.CharField(max_length=100)
    excavation_site = models.CharField(max_length=150)
    discovery_year = models.IntegerField('Year fossil was discovered')
    period = models.CharField(max_length=50)

class Artwork(Item):
    art_type = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    year = models.IntegerField()

class Staff(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    shift = models.CharField('Day or Night shift', max_length=50)

    works_in = models.ManyToManyField(Gallery)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Staff"
