from django.db import models
from django.contrib.auth.models import User


class Collection(models.Model):
    subject = models.CharField(max_length=300, blank=True)
    owner = models.CharField(max_length=300, blank=True)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(User,
        related_name="collections", blank=True, null=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.id)


class CollectionTitle(models.Model):
    """
    A Class for Collection titles.

    """
    collection = models.ForeignKey(Collection,
        related_name="has_titles", on_delete=models.CASCADE)
    name = models.CharField(max_length=500, verbose_name="Title")
    language = models.CharField(max_length=3)


class CollectionTitleChild(models.Model):
    """
    A Class for Collection title children.

    """
    collection_title = models.ForeignKey(CollectionTitle,
        related_name="has_children", on_delete=models.CASCADE)
    name = models.CharField(max_length=500, verbose_name="Child")
    language = models.CharField(max_length=3)

