from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, CharField, Value, Max
from django.db.models.functions import Cast, Concat
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, )

from .forms import PostForm, CommentForm
from .models import Post, Comment, Author
from .filters import PostFilter


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'app/posts.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetailView(DetailView):
    template_name = 'app/post.html'
    form_class = CommentForm
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = (
            Comment.objects
            .filter(linkedPost__id=self.kwargs['pk'])
            .order_by('familyTree')
        )
        if self.request.user.is_authenticated:
            context['form'] = self.form_class
        return context

    def post(self, request, *args, **kwargs):
        c = Comment.objects.create(
            commentText=request.POST.get('commentText'),
            linkedUser=self.request.user,
            linkedPost=Post.objects.get(id=self.kwargs['pk'])
        )
        c.familyTree = f"{self.kwargs['pk']:09}-{c.id:09}"
        c.save(update_fields=["familyTree"])
        context = {
            'post': Post.objects.get(pk=self.kwargs['pk']),
            'comments': Comment.objects.filter(linkedPost__id=self.kwargs['pk']),
            'form': self.form_class,
        }
        return render(request, self.template_name, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'app/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)

        if not Author.objects.filter(user=self.request.user).exists():
            Author.objects.create(user=self.request.user)

        post.linkedAuthor = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'app/post_edit.html'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'app/post_delete.html'
    success_url = reverse_lazy('home')


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'app/comment_edit.html'

    def form_valid(self, form):
        probably_id = Comment.objects.aggregate(Max('id'))['id__max']
        f = form.save(commit=False)
        f.parent = Comment.objects.get(id=self.request.GET['pk'])
        f.linkedPost = f.parent.linkedPost
        f.linkedUser = self.request.user
        f.familyTree = f"{f.parent.familyTree}-{probably_id:09}"
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('post', kwargs={'pk': Comment.objects.get(id=self.request.GET['pk']).linkedPost.id})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CommentForm
    model = Comment
    template_name = 'app/comment_edit.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('post', kwargs={'pk': Comment.objects.get(id=self.kwargs['pk']).linkedPost.id})