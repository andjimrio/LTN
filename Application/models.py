#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User


#   Clase que contiene la información del usuario. Se relaciona con el
# User que define Django.
class UserProfile(models.Model):
    image = models.URLField()

    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username

    pass


#   Representa la clasificación que hace el usuario de sus canales de
# noticias.
class Section(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                             related_name="sections")

    def __str__(self):
        return self.title


    class Meta:
        ordering = ('title',)

    pass


#   Representa al canal de noticias: al periódico. Contiene su
# información esencial y se relaciona con Section
class Feed(models.Model):
    title = models.CharField(max_length=500)
    link_rss = models.URLField()
    link_web = models.URLField()
    description = models.TextField()
    language = models.CharField(max_length=50)
    logo = models.URLField()

    section = models.ManyToManyField(Section, on_delete=models.CASCADE,
                                related_name="feeds")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title', )

    pass


#   Representa a una noticia. Este se relaciona con el diario y por
# defecto se ordena por la fecha de publicación de manera descendente.
class Item(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField()
    description = models.TextField()
    image = models.URLField()
    article = models.TextField()
    pubDate = models.DateTimeField()
    creator = models.CharField(max_length=500)

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE,
                             related_name="items")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pubDate', )

    pass


#   Contiene la información de un usuario con respecto a una noticia.
# Por defecto se inicializa a falso los tres atributos.
class Status(models.Model):
    view = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    like = models.BooleanField(default=False)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                             related_name="statuses")
    item = models.OneToOneField(Item)

    def __str__(self):
        return "{}: {}/{}/{}".format(self.user.username,self.view,
                                     self.read,self.like)
    pass


#   Término más representantivo tanto para el usuario como para una
# noticia.
class Keyword(models.Model):
    term = models.CharField(max_length=250)

    users = models.ManyToManyField(UserProfile, related_name="keywords")
    items = models.ManyToManyField(Item, related_name="keywords")

    def __str__(self):
        return self.term

    pass
