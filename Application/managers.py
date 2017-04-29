import os

from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save, post_delete, class_prepared

from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.index import create_in, open_dir, exists_in
from whoosh.qparser import QueryParser

try:
    STORAGE_DIR = settings.WHOOSH_STORAGE_DIR
except AttributeError:
    raise ImproperlyConfigured(u'Could not find WHOOSH_STORAGE_DIR setting. ' +
                               'Please make sure that you have added that setting.')

field_mapping = {
    'AutoField': ID(unique=True, stored=True),
    'BooleanField': STORED,
    'CharField': TEXT(stored=True),
    'CommaSeparatedIntegerField': STORED,
    'DateField': ID,
    'DateTimeField': ID,
    'DecimalField': STORED,
    'EmailField': ID,
    'FileField': ID,
    'FilePathField': ID,
    'FloatField': STORED,
    'ImageField': ID,
    'IntegerField': STORED,
    'IPAddressField': ID,
    'NullBooleanField': STORED,
    'PositiveIntegerField': STORED,
    'PositiveSmallIntegerField': STORED,
    'SlugField': KEYWORD,
    'SmallIntegerField': STORED,
    'TextField': TEXT(stored=True),
    'TimeField': ID,
    'URLField': ID,
}


class WhooshManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.default = kwargs.pop("default", None)
        self.fields = kwargs.pop('fields', []) + ['id']
        self.real_time = kwargs.pop('real_time', True)

        if not os.path.exists(STORAGE_DIR):
            os.mkdir(STORAGE_DIR)

        super().__init__()

    def contribute_to_class(self, model, name):
        super().contribute_to_class(model, name)
        class_prepared.connect(self.class_prepared_callback, sender=self.model)

    def class_prepared_callback(self, sender, **kwargs):
        if not exists_in(STORAGE_DIR):
            schema_dict = {}
            for field_name in self.fields:
                field_type = self.model._meta.get_field(field_name).get_internal_type()
                schema_dict[field_name] = field_mapping[field_type]
            schema = Schema(**schema_dict)

            create_in(STORAGE_DIR, schema)

        if self.real_time:
            post_save.connect(self.post_save_callback, sender=self.model)
            post_delete.connect(self.post_delete_callback, sender=self.model)

    def post_save_callback(self, sender, instance, created, **kwargs):
        dct = dict([(f, str(getattr(instance, f))) for f in self.fields])

        index = open_dir(STORAGE_DIR)
        writer = index.writer()

        if created:
            writer.add_document(**dct)
        else:
            writer.update_document(**dct)
        writer.commit()

        instance.on_save()

    def post_delete_callback(self, sender, instance, **kwargs):
        pass

    def query(self, field, query):
        results = self.__query_search(field, query)
        return self.filter(id__in=[r['id'] for r in results])

    def get_keywords(self,field, item_id, num_terms=20):
        results = self.__query_search('id', item_id)
        return [keyword for keyword, score in results.key_terms(field, numterms=num_terms)]

    def get_more_like_this(self, field, item_id):
        results = self.__query_search('id', item_id)
        first_hit = results[0]
        return self.filter(id__in=[r['id'] for r in first_hit.more_like_this(field)])

    @staticmethod
    def __query_search(field, search):
        index = open_dir(STORAGE_DIR)
        query = QueryParser(field, index.schema).parse(str(search))
        results = index.searcher().search(query)
        return results
