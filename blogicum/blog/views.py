from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import CommentForm, CustomUserChangeForm, PostForm
from .models import Category, Comment, Post
from .utils import paginator_func

User = get_user_model()


def index(request):
    template = 'blog/index.html'
    post_list = Post.filtered_objects.filter(
        category__is_published=True,
    )
    page_obj = paginator_func(request, post_list)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = Post.filtered_objects.filter(
        category_id=category.id,
    )
    page_obj = paginator_func(request, post_list)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, template, context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'id'
    queryset = Post.objects.select_related('author', 'category', 'location')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    posts = None
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.posts = get_object_or_404(Post, pk=kwargs['pk'])
        if self.posts.author != request.user:
            return redirect('blog:post_detail', id=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'id': self.posts.id})


def edit_profile(request):
    template = 'blog/user.html'
    instance = get_object_or_404(User, username=request.user)
    form = CustomUserChangeForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, template, context)


def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(User, username=username)
    profile_posts = (
        Post.objects.select_related('category', 'location', 'author')
        .filter(author=profile.id)
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
        )
    page_obj = paginator_func(request, profile_posts)
    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, template, context)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', id=pk)


@login_required
def edit_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    form = CommentForm(request.POST or None, instance=comment)
    context = {'form': form, 'comment': comment}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', id=pk)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    context = {'comment': comment}
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id=pk)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_post(request, pk):
    instance = get_object_or_404(Post, id=pk, author=request.user)
    form = CommentForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:profile', username=request.user)
    return render(request, 'blog/create.html', context)
