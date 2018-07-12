from django.db import models

class Gallery(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Galleries"

class Exhibition(models.Model):
    name = models.CharField(max_length=100)
    sponsor = models.CharField(max_length=100)
    start_date = models.DateField('Date exhibition starts')
    end_date = models.DateField('Date exhibition ends')
    active = models.BooleanField()
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField('Item description')
    item_type = models.CharField(max_length=10)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE)

class Artifact(Item):
    country_origin = models.CharField(max_length=100)
    excavation_site = models.CharField(max_length=150)
    discovery_date = models.DateField('Date artifact was discovered')
    condition = models.CharField(max_length=50)
    material = models.CharField(max_length=50)

class Organism(Item):
    scientific_name = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)

class Fossil(Item):
    country_origin = models.CharField(max_length=100)
    excavation_site = models.CharField(max_length=150)
    discovery_date = models.DateField('Date artifact was discovered')
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

    class Meta:
        verbose_name_plural = "Staff"