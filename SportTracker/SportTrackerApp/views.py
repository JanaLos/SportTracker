from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Activity
from .forms import ActivityForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post
from django.http import Http404
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import views as auth_views


class LoginUserView(auth_views.LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')

class ActivityListView(ListView):
    model = Activity
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(name__icontains=query)
        else:
            object_list = self.model.objects.all()
        return object_list


class ActivityDetailView(DetailView):
    model = Activity


@method_decorator(staff_member_required, name='dispatch')
class ActivityCreate(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('activities:list')


@method_decorator(staff_member_required, name='dispatch')
class ActivityUpdate(UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('activities:list')

    # def get_success_url(self):
    #     return reverse_lazy('activities:update', args=(self.object.id, )) + '?ok'


@method_decorator(staff_member_required, name='dispatch')
class ActivityDelete(DeleteView):
    model = Activity
    success_url = reverse_lazy('activities:list')

class PostListView(ListView):
    model = Post
    template_name = 'home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,
                     UserPassesTestMixin,
                     UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.author == self.request.user:
            raise Http404
        return obj

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    return render(request, 'about.html', {'title': 'About'})


def privacy_policy(request):
    return render(request, 'privacy_policy.html', {})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')


    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


def home(request):
    context = {
        'posts': Post.objects.all(),
        'activities': Activity.objects.all()
    }
    return render(request, 'home.html', context)