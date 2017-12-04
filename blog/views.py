from django.shortcuts import render,get_object_or_404
from .models import Post,Category
import markdown
from comments.forms import CommentForm
#基于类的通用视图开发
from django.views.generic import ListView,DetailView
#from django.http import HttpResponse
# Create your views here.

"""
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
"""
class IndexView(ListView):
	#model。将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。
	#template_name。指定这个视图渲染的模板。
	#context_object_name。指定获取的模型列表数据保存的变量名。这个变量会被传递给模板j即模板变量名。
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'


class CategoryView(IndexView):
	#ListView通过get_queryset()获取列表数据
	def get_queryset(self):
		#命名参数组都存放在kwargs中通过get方法获取
		cate  = get_object_or_404(Category,pk = self.kwargs.get('pk'))
		return super(CategoryView,self).get_queryset().filter(category=cate)


class ArchiveView(IndexView):
	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		return super(ArchiveView,self).get_queryset().filter(create_time__year = year,create_time__month = month)


class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/detail.html'
	context_object_name = 'post'

	def get(self,request,*args,**kwargs):
		# 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
		# get 方法返回的是一个 HttpResponse 实例
		# 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
		# 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
		response = super(PostDetailView,self).get(request,*args,**kwargs)
		# 将文章阅读量 +1
		# 注意 self.object 的值就是被访问的文章 post
		self.object.increase_views();
		# 视图必须返回一个 HttpResponse 对象
		return response;

	def get_object(self,queryset=None):
		#获取父类通过pk从数据库找到的Post对象
		post = super(PostDetailView,self).get_object(queryset=None)
		# 记得载入markdown模块，进行markdown渲染
		post.body = markdown.markdown(post.body,
                                      extensions=[
                                              'markdown.extensions.extra',
                                              'markdown.extensions.codehilite',
                                              'markdown.extensions.toc',
                                ])
		return post

	def get_context_data(self,**kwargs):
		# 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
		context = super(PostDetailView,self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all();
		context.update({
			'form':form,
			'comment_list':comment_list
			})
		return context




