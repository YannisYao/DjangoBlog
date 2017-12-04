from ..models import Post,Category,Tag
from django import template
from django.db.models.aggregates import Count
#自定义最新文章的模板标签 最大数量5
register = template.Library()
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_time')[:num]

#归档模板标签
@register.simple_tag
def archives():
    return Post.objects.dates('create_time','month',order='DESC')

#分类模板标签
@register.simple_tag
def get_categories():
    #return Category.objects.all()
    """这个 Category.objects.annotate 方法和 Category.objects.all 有点类似，它会返回数据库中全部 Category 的记录，但同时它还会做一些额外的事情，在这里我们希望它做的额外事情就是去统计返回的 Category 记录的集合中每条记录下的文章数。代码中的 Count 方法为我们做了这个事，它接收一个和 Categoty 相关联的模型参数名（这里是 Post，通过 ForeignKey 关联的），然后它便会统计 Category 记录的集合中每条记录下的与之关联的 Post 记录的行数，也就是文章数，最后把这个值保存到 num_posts 属性中。
此外，我们还对结果集做了一个过滤，使用 filter 方法把 num_posts 的值小于 1 的分类过滤掉。因为 num_posts 的值小于 1 表示该分类下没有文章，没有文章的分类我们不希望它在页面中显示"""
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts = Count('post')).filter(num_posts__gt=0)
