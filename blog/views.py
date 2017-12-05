from django.shortcuts import render,get_object_or_404
from .models import Post,Category,Tag
import markdown
from comments.forms import CommentForm
#基于类的通用视图开发
from django.views.generic import ListView,DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
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
	paginate_by = 5


	def get_context_data(self,**kwargs):
		# 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
		# paginator 是 Paginator 的一个实例，
		# page_obj 是 Page 的一个实例，
		# is_paginated 是一个布尔变量，用于指示是否已分页。
		# 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
		# 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
		# 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
		context = super(IndexView, self).get_context_data(**kwargs)
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')

		# 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
		pagination_data = self.pagination_data(paginator,page,is_paginated)
		# 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
		# 注意此时 context 字典中已有了显示分页导航条所需的数据。
		context.update(pagination_data)
		return context

	def pagination_data(self,paginator,page,is_paginated):
		if not is_paginated :
			# 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
			return {}
		# 当前页左边连续的页码号，初始值为空
		left = []
		# 当前页右边连续的页码号，初始值为空
		right = []
		# 标示第 1 页页码后是否需要显示省略号
		left_has_more = False
		# 标示最后一页页码前是否需要显示省略号
		right_has_more = False
		# 标示是否需要显示第 1 页的页码号。
		# 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
		# 其它情况下第一页的页码是始终需要显示的。
		# 初始值为 False
		first = False
		# 标示是否需要显示最后一页的页码号。
		# 需要此指示变量的理由和上面相同。
		last = False
		# 获得用户当前请求的页码号
		page_number = page.number
		#总页数
		total_pages = paginator.num_pages
		# 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
		page_range = paginator.page_range

		if page_number == 1 :
			# 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
			# 此时只要获取当前页右边的连续页码号，
			# 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
			# 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。这里可能有越界问题
			right = page_range[page_number:page_number+2]
			# 如果最右边的页码号比最后一页的页码号减去 1 还要小，
			# 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示
			if right[-1] < total_pages -1:
				right_has_more = True
			#如果right部分页码号里面没有最后一页，就把最后一页显示出来
			if right[-1] < total_pages:
				last = True
		elif page_number == total_pages:
			# 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
			# 此时只要获取当前页左边的连续页码号。
			# 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
			# 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
		else:
			right = page_range[page_number:page_number+2]
			left = page_range[(page_number -3)if page_number - 3 > 0 else 0 :page_number -1]
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
			if right[-1] < total_pages -1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True


		data = {
			'first':first,
			'last':last,
			'right':right,
			'left':left,
			'left_has_more':left_has_more,
			'right_has_more':right_has_more
		}
		return data


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

class TagView(IndexView):
	def get_queryset(self):
		tag = get_object_or_404(Tag,pk = self.kwargs.get('pk'))
		return super(TagView, self).get_queryset().filter(tags = tag)


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
		md = markdown.Markdown(extensions=[
                                              'markdown.extensions.extra',
                                              'markdown.extensions.codehilite',
										 #'markdown.extensions.toc',
											#处理中文锚点
											  TocExtension(slugify = slugify)
                                ])
		post.body = md.convert(post.body)
		post.toc = md.toc
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


def search(request):
	q = request.GET.get('q')
	error_msg = ''

	if not q:
		error_msg = '请输入关键信息'
		return render(request,'blog/index.html',{'error_msg':error_msg})

	post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
	return  render(request,'blog/index.html',{'error_msg':error_msg,'post_list':post_list})


def contact(request):
	return render(request,'blog/contact.html')

def about(request):
	return render(request,'blog/about.html')




