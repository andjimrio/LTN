# encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from math import log, floor

from Application.managers import WhooshManager


class UserProfile(models.Model):
    """Entidad UserProfile:
    Clase que contiene la información del usuario. Se relaciona con el
    User que define Django.
    """
    image = models.URLField()

    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username

    pass


class Section(models.Model):
    """Entidad Section:
    Representa la clasificación que hace el usuario de sus canales de
    noticias.
    """
    title = models.CharField(max_length=500)
    description = models.TextField()

    user = models.ForeignKey(UserProfile, related_name="sections")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)

    pass


class Feed(models.Model):
    """Entidad Feed:
    Representa al canal de noticias: al periódico. Contiene su
    información esencial y se relaciona con Section.
    """
    title = models.CharField(max_length=500)
    link_rss = models.URLField()
    link_web = models.URLField()
    description = models.TextField()
    language = models.CharField(max_length=50)
    logo = models.URLField()

    sections = models.ManyToManyField(Section, related_name="feeds")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title', )

    pass


class Item(models.Model):
    """Entidad Item:
    Representa a una noticia. Este se relaciona con el diario y por
    defecto se ordena por la fecha de publicación de manera descendente.
    """
    title = models.CharField(max_length=500)
    link = models.URLField()
    description = models.TextField()
    image = models.URLField()
    article = models.TextField()
    pubDate = models.DateTimeField()
    creator = models.CharField(max_length=500)

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE,
                             related_name="items")

    # The first argument is the default query field
    objects = WhooshManager('title', fields=['title', 'article'])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pubDate', )

    def get_key_number(self):
        return floor(log(len(self.article)))

    def __create_keywords(self):
        pass

    def __create_status(self):
        for section in self.feed.sections.all():
            Status.objects.get_or_create(user_id=section.user.id, item_id=self.id)
        pass

    def on_save(self):
        self.__create_status()
        self.__create_keywords()
        pass

    pass


class Status(models.Model):
    """Entidad Status:
    Contiene la información de un usuario con respecto a una noticia.
    Por defecto se inicializa a falso los tres atributos.
    """
    view = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    like = models.BooleanField(default=False)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                             related_name="statuses")
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name="statuses")

    def as_view(self):
        self.view = True
        self.save()
        pass

    def as_read(self):
        self.view = True
        self.read = True
        self.save()
        pass

    def as_like(self):
        self.like = True
        self.save()
        pass

    def as_unlike(self):
        self.like = False
        self.save()
        pass

    def get_score(self):
        if self.like:
            return 10
        elif self.read:
            return 1
        else:
            return 0

    def __str__(self):
        return "{}-{}: {}/{}/{}".format(self.item.id, self.user.user.username, self.view,
                                        self.read, self.like)
    pass


class Keyword(models.Model):
    """Entidad Keyword:
    Representa las palabras claves asociadas a un usuario. Estas servirán
    para el para el sistema de recomendación.
    """
    term = models.CharField(max_length=250)

    users = models.ManyToManyField(UserProfile, related_name="keywords")

    def __str__(self):
        return self.term

    pass


class Comment(models.Model):
    """Entidad Comment:
    Representa un comentario de un usuario en un Item."""
    description = models.TextField()
    pubDate = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                             related_name="comments")
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name="comments")

    def __str__(self):
        return "{}-{}".format(self.item.id, self.user.user.username)
    pass
