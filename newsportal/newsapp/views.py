from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.db.models import Exists, OuterRef
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author, Category, Subscription


class PostsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name="authors").exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            return obj


class PostsSearch(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NWCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('newsapp.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'nw_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        post.author = self.request.user.author
        return super().form_valid(form)


class NWUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('newsapp.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'nw_edit.html'

    def get_queryset(self):
        queryset = super(NWUpdate, self).get_queryset()
        return queryset.filter(categoryType='NW')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_author'] = Post.objects.get(pk=self.kwargs.get('pk')).author
        return context


class NWDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('newsapp.delete_post',)
    model = Post
    template_name = 'nw_delete.html'
    success_url = reverse_lazy('posts_list')

    def get_queryset(self):
        queryset = super(NWDelete, self).get_queryset()
        return queryset.filter(categoryType='NW')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_author'] = Post.objects.get(pk=self.kwargs.get('pk')).author
        return context


class ARCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('newsapp.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'ar_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        post.author = self.request.user.author
        return super().form_valid(form)


class ARUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('newsapp.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'ar_edit.html'

    def get_queryset(self):
        queryset = super(ARUpdate, self).get_queryset()
        return queryset.filter(categoryType='AR')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_author'] = Post.objects.get(pk=self.kwargs.get('pk')).author
        return context


class ARDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('newsapp.delete_post',)
    model = Post
    template_name = 'ar_delete.html'
    success_url = reverse_lazy('posts_list')

    def get_queryset(self):
        queryset = super(ARDelete, self).get_queryset()
        return queryset.filter(categoryType='AR')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_author'] = Post.objects.get(pk=self.kwargs.get('pk')).author
        return context


def author_now(request):
    user = request.user
    author_group = Group.objects.get(name="authors")
    if not user.groups.filter(name='authors').exists():
        user.groups.add(author_group)
        Author.objects.create(authorUser=user)
    return redirect("posts_list")


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
