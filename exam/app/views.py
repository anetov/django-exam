from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Post, Profile, Comment
from .forms import SignUpForm, UserLoginForm, PostForm, CommentForm
from django.views.generic import ListView, CreateView, TemplateView, View, UpdateView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
@login_required
def list_posts(request):
    posts = Post.objects.all()
    return render(request, 'post/list_posts.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts')
    else:
        form = PostForm()
    return render(request, 'post/create_post.html', {'form': form})

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class CommentListView(View):
    def get(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        comments = Comment.objects.filter(post=post_id)
        post = get_object_or_404(Post, id=post_id)
        print(post)
        return render(request, 'comments/comment_list.html', {'comments': comments, 'post': post})
    
class CommentCreateView(View):
    def get(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        comments = Comment.objects.filter(post=post_id)
        post = get_object_or_404(Post, id=post_id)
        
        return render(request, 'comments/comment_form.html', {'comments': comments, 'post': post})

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = self.kwargs.get('post_id')
            comment.author = request.user  
            comment.save()
            return redirect('comment_list', post_id=self.kwargs.get('post_id'))
        return render(request, 'comments/comment_form.html', {'form': form})

class Login(LoginView):
    template_name = 'auth/login.html'
    next_page = reverse_lazy('posts')

    def form_valid(self, form):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(reverse_lazy('login')+'?active=false')
        
class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('login')

class UserLogoutView(LogoutView):
    next_page = 'login'


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Проверка, что текущий пользователь - автор поста
    if post.author != request.user:
        # Обработка случая, когда пользователь не автор поста
        return redirect('posts')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            # Перенаправление на страницу поста или список постов
            return redirect('posts')
    else:
        form = PostForm(instance=post)

    return render(request, 'post/edit.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        # Обработка случая, когда пользователь не автор поста
        return redirect('posts')

    if request.method == 'POST':
        post.delete()
        return redirect('posts')

    return render(request, 'post/delete.html', {'post': post})

class VerificationSuccess(TemplateView):
    template_name = 'registration/verification_success.html'

    def get(self, request):
        return redirect('login')

class VerificationError(TemplateView):
    template_name = 'registration/verification_error.html'
    
class VerifyEmailView(View):
    def get(self, request, user_id, token):
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('verify_success')
        else:
            return redirect('verify_error')