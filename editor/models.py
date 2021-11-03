from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.text import slugify
import random
import string
from account.models import CustomUser


def id_generator():
    return ''.join(random.choices(
        string.ascii_letters + string.digits, k=24))


class Document(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    document_id = models.CharField(max_length=24, default=id_generator)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    document = models.ForeignKey(Document, on_delete=CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(default='')
    slug = models.SlugField(max_length=110)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Chapter, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Section(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    slug = models.SlugField(max_length=110)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Section, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
