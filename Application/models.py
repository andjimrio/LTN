# encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

from Application.utilities.python_utilities import floor_log
from Application.managers import WhooshManager


class UserProfile(models.Model):
    """Entidad UserProfile:
    Clase que contiene la información del usuario. Se relaciona con el
    User que define Django.
    """
    image = models.URLField(max_length=500, blank=True)

    user = models.OneToOneField(User, related_name="profile")

    def __str__(self):
        return self.user.username


class Section(models.Model):
    """Entidad Section:
    Representa la clasificación que hace el usuario de sus canales de
    noticias.
    """
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)

    user = models.ForeignKey(UserProfile, related_name="sections")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Feed(models.Model):
    """Entidad Feed:
    Representa al canal de noticias: al periódico. Contiene su
    información esencial y se relaciona con Section.
    """
    title = models.CharField(max_length=500)
    link_rss = models.URLField(max_length=500)
    link_web = models.URLField(max_length=500)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, blank=True)
    logo = models.URLField(blank=True)

    sections = models.ManyToManyField(Section, related_name="feeds")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title', )


class Item(models.Model):
    """Entidad Item:
    Representa a una noticia. Este se relaciona con el diario y por
    defecto se ordena por la fecha de publicación de manera descendente.
    """
    title = models.CharField(max_length=500)
    link = models.URLField(max_length=500)
    description = models.TextField()
    image = models.URLField(max_length=500)
    article = models.TextField()
    pubDate = models.DateTimeField()
    creator = models.CharField(max_length=500)

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE,
                             related_name="items")

    # The first argument is the default query field
    objects = WhooshManager('article', fields=['title', 'article', 'description', 'creator', 'feed'])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pubDate', )

    def get_key_number(self):
        return floor_log(len(self.article))

    def __create_keywords(self):
        for keyword in Item.objects.get_keywords('article', self.id, self.get_key_number()):
            keyword = Keyword.objects.get_or_create(term=keyword)[0]
            keyword.items.add(self)
            keyword.save()

    def __create_status(self):
        for section in self.feed.sections.all():
            Status.objects.get_or_create(user_id=section.user.id, item_id=self.id)

    def on_save(self):
        self.__create_status()
        self.__create_keywords()


class Status(models.Model):
    """Entidad Status:
    Contiene la información de un usuario con respecto a una noticia.
    Por defecto se inicializa a falso los tres atributos.
    """
    view = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    web = models.BooleanField(default=False)
    like = models.BooleanField(default=False)
    saves = models.BooleanField(default=False)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                             related_name="statuses")
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name="statuses")

    def as_view(self):
        self.view = True
        self.save()

    def as_read(self):
        self.view = True
        self.read = True
        self.save()

    def as_web(self):
        self.web = True
        self.save()

    def as_like(self):
        self.like = True
        self.save()

    def as_unlike(self):
        self.like = False
        self.save()

    def as_save(self):
        self.saves = True
        self.save()

    def as_unsave(self):
        self.saves = False
        self.save()

    def get_score(self):
        if self.like:
            return 10
        elif self.web:
            return 5
        elif self.read:
            return 1
        else:
            return 0

    def __str__(self):
        return "{}-{}: {}/{}/{}/{}/{}".format(self.item.id, self.user.user.username, self.view,
                                              self.read, self.web, self.like, self.saves)


class Keyword(models.Model):
    """Entidad Keyword:
    Representa las palabras claves asociadas a un usuario. Estas servirán
    para el para el sistema de recomendación.
    """
    term = models.CharField(max_length=250)

    users = models.ManyToManyField(UserProfile, related_name="keywords")
    items = models.ManyToManyField(Item, related_name="keywords")

    def __str__(self):
        return self.term


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
