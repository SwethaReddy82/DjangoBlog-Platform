from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import UserRegisterForm
from .models import Post


def sidebar_context():
    latest_posts = Post.objects.select_related('author').order_by('-date_posted')[:5]
    return {
        'latest_posts': latest_posts,
        'announcements': [
            'Welcome to BlogForge',
            'Registered users can publish posts',
            'Authors can edit or delete only their own posts',
        ],
        'quick_links': [
            {'label': 'All Posts', 'url_name': 'blog-home'},
            {'label': 'About', 'url_name': 'blog-about'},
            {'label': 'Create Post', 'url_name': 'post-create'},
        ],
    }


class PostListView(ListView):
    model = Post
    template_name = 'sweblog/home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(sidebar_context())
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'sweblog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(sidebar_context())
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'sweblog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been published.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(sidebar_context())
        context['form_title'] = 'Create New Post'
        context['submit_label'] = 'Publish'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'sweblog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated.')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(sidebar_context())
        context['form_title'] = 'Update Post'
        context['submit_label'] = 'Save Changes'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'sweblog/post_confirm_delete.html'
    success_url = reverse_lazy('blog-home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your post has been deleted.')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(sidebar_context())
        return context


def about(request):
    context = {'title': 'About'}
    context.update(sidebar_context())
    return render(request, 'sweblog/about.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('blog-home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {'title': 'Register', 'form': form}
    context.update(sidebar_context())
    return render(request, 'registration/register.html', context)
