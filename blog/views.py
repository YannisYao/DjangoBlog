from django.shortcuts import render,get_object_or_404
from .models import Post,Category
import markdown
from comments.forms import CommentForm
#from django.http import HttpResponse
# Create your views here.

def index(request):
	#return HttpResponse("欢迎来到我的博客首页！");
	# -create_time 前面加'-' 表示逆序返回
	post_list = Post.objects.all()
	return render(request,'blog/index.html',context={'post_list': post_list})


def detail(request, pk):
	post = get_object_or_404(Post,pk=pk)
	#增加阅读量
	post.increase_views()
	# 记得载入markdown模块
	post.body = markdown.markdown(post.body,
                                      extensions=[
                                              'markdown.extensions.extra',
                                              'markdown.extensions.codehilite',
                                              'markdown.extensions.toc',
                                ])
	# 记得在顶部导入 CommentForm
	form = CommentForm()
	# 获取这篇 post 下的全部评论
	comment_list = post.comment_set.all()

	# 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
	context = {'post':post,
				'form':form,
				'comment_list':comment_list,
				}
	#return render(request,'blog/detail.html',context={'post':post})
	return render(request,'blog/detail.html',context = context)


def archives(request, year, month):
	post_list = Post.objects.filter(create_time__year = year,create_time__month = month)
	return render(request,'blog/index.html',context={'post_list':post_list})


def category(request,pk):
	#category = Category.objects.get('pk' = pk)
	#首先获取Category分类对象
	cate = get_object_or_404(Category,pk = pk)
	#获取特定Category文章列表
	post_list = Post.objects.filter(category = cate)
	return render(request,'blog/index.html',context={'post_list':post_list})

