from django.conf.urls import url
from . import views
#定义命名空间
app_name = 'blog'
urlpatterns = [
	#url(r'^$',views.index,name='index'),
	#url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),
	#url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',views.archives,name = 'archives'),
	#url(r'^category/(?P<pk>[0-9]+)/$',views.category,name='category')
	#使用通用类视图处理
	url(r'^$',views.IndexView.as_view(),name='index'),
	url(r'^post/(?P<pk>[0-9]+)/$',views.PostDetailView.as_view(),name='detail'),
	url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchiveView.as_view(),name = 'archives'),
	url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(),name='category')
]