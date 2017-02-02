from haystack import indexes
from Application.models import Item

class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    article = indexes.CharField(model_attr='article')
    pubDate = indexes.DateTimeField(model_attr='pubDate')
    creator =  indexes.CharField(model_attr='creator')
    newspaper = indexes.CharField()

    def get_model(self):
        return Item

    def index_queryset(self, using=None):
        return self.get_model().objects.all().order_by('pubDate')

    def prepare_newspaper(self, obj):
        return obj.feed.title
