from haystack import indexes
from .models import Post
#建立全文索引工具类

class PostIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self,using = None):
        return self.get_model().objects.all()
