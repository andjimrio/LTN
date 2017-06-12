# LT-News
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/699f99831bef456cabe256133876a03d)](https://www.codacy.com/app/andjimrio/LTN?utm_source=github.com&utm_medium=referral&utm_content=andjimrio/LTN&utm_campaign=badger)
[![Stories in Ready](https://badge.waffle.io/andjimrio/LTN.svg?label=ready&title=Ready)](http://waffle.io/andjimrio/LTN)

[LT-News](http://lt-news.mooo.com/) es mi Trabajo de Fin de Grado. Consiste en un lector RSS enriquecido con: búsqueda y sistema de recomendación.


## Resumen
¿Por qué LT-News? Surge de la necesidad de todos de informarse, pero la enormidad de medios y el poquísimo tiempo nos hace excusarnos de la gran tarea de leer y formarse una opinión propia de lo que ocurre a nuestro alrededor.
Este trabajo se propone ser un lector RSS. Pero no uno típico, no, sino uno que te acabe conociendo tanto, que te averigüe tus gustos, te muestre las noticias en las que estés realmente interesado. Además, poseerá funcionalidades tan útiles como la de buscar noticias en los periódicos que sigas, o hacer un análisis diario de las noticias más importantes de tus secciones.
Además, podrás ir viendo gráficas en bases a tu uso de la aplicación o de la evolución de la aparición de una determinada noticia a lo largo del tiempo.


## Herramientas
* [Django 1.11](https://www.djangoproject.com/): framework back-end
* [Feedparser 5.2](http://pythonhosted.org/feedparser/): RSS parser
* [Whoosh 2.7](http://whoosh.readthedocs.io/en/latest/index.html): sistema de recuperación de información
* [Newspaper 0.1.2](http://newspaper.readthedocs.io/en/latest/): web scrapping de noticias
* [Materialize 0.98](http://materializecss.com/): framework front-end
* [Django_cron 0.5](http://django-cron.readthedocs.io/en/latest/): cliente de cron para Django
* [Django_whoosh](https://github.com/JoeGermuska/django-whoosh): capa de abstracción entre Django y Whoosh

## Licencia
Este proyecto posee la MIT License - ver el archivo [LICENSE](LICENSE) para más detalles.
