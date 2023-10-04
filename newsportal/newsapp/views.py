from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter
from .forms import PostForm
from .models import Post


class PostsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


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


class NWCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'nw_post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)


class NWUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'nw_post_edit.html'

    def get_queryset(self):
        queryset = super(NWUpdate, self).get_queryset()
        return queryset.filter(categoryType='NW')


class NWDelete(DeleteView):
    model = Post
    template_name = 'nw_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        queryset = super(NWDelete, self).get_queryset()
        return queryset.filter(categoryType='NW')


class ARCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'ar_post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)


class ARUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'ar_post_edit.html'

    def get_queryset(self):
        queryset = super(ARUpdate, self).get_queryset()
        return queryset.filter(categoryType='AR')


class ARDelete(DeleteView):
    model = Post
    template_name = 'ar_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        queryset = super(ARDelete, self).get_queryset()
        return queryset.filter(categoryType='AR')
