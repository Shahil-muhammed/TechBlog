from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from userpage.models import Blog, Comment

BLOGS_PER_PAGE = 5

def index(request):
    query = request.GET.get('q')
    no_results = False
    
    if query:
        featured_blog = Blog.objects.filter(
            Q(title__icontains=query) | Q(keywords__icontains=query)
        ).order_by('-created_at').first()
        no_results = featured_blog is None
    else:
        featured_blog = Blog.objects.order_by('-created_at').first()

    comments = Comment.objects.filter(blog=featured_blog).order_by('-created_at') if featured_blog else []

    other_blogs = Blog.objects.exclude(uid=featured_blog.uid) if featured_blog else Blog.objects.none()
    paginator = Paginator(other_blogs, BLOGS_PER_PAGE)
    page_obj = paginator.get_page(1)

    return render(request, 'index/index.html', {
        'featured_blog': featured_blog,
        'comments': comments,
        'page_blogs': page_obj.object_list,
        'has_next': page_obj.has_next(),
        'next_page': 2,
        'query': query,
        'no_results': no_results,
    })


def blog_detail(request, uid):
    featured_blog = get_object_or_404(Blog, uid=uid)
    comments = featured_blog.comments.all().order_by('-created_at')
    other_blogs = Blog.objects.exclude(uid=uid)
    paginator = Paginator(other_blogs, BLOGS_PER_PAGE)
    page_obj = paginator.get_page(1)

    return render(request, 'index/index.html', {
        'featured_blog': featured_blog,
        'comments': comments,
        'page_blogs': page_obj.object_list,
        'has_next': page_obj.has_next(),
        'next_page': 2,
    })

@login_required
def add_comment(request, uid):
    if request.method == "POST":
        blog = get_object_or_404(Blog, uid=uid)
        comment_text = request.POST.get('comment')

        if comment_text:
            Comment.objects.create(
                blog=blog,
                user=request.user,
                text=comment_text
            )
        return redirect('blog_detail', uid=uid)
    return redirect('index')

def blog_list_partial(request):
    page = int(request.GET.get('page', 1))
    blogs = Blog.objects.order_by('-created_at')
    paginator = Paginator(blogs, BLOGS_PER_PAGE)
    page_obj = paginator.get_page(page)

    return render(request, 'index/blog_list_partial.html', {
        'blogs': page_obj.object_list,
        'has_next': page_obj.has_next(),
        'next_page': page + 1,
    })
