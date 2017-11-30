from django.shortcuts import render, redirect
from accounts.forms import RegisterationForm, EditProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView
from .forms import GetFeedBack, MakePost, CommentsForm
from django.contrib.auth.models import User
from .models import Friend, Post, MyComments


def index(request):
    name = 'The Portal'
    return render(request, 'accounts/index.html', {'name': name})


def home(request):
    post = Post.objects.all()
    return render(request, 'accounts/home.html', {'post': post})


def register(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/logout')
    else:
        form = RegisterationForm

        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)


def profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)


def other_profile(request, pk):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'accounts/profile.html', args)


def friends(request):
    users = User.objects.exclude(id=request.user.id)
    friend = Friend.objects.get(current_user=request.user)
    friends = friend.users.all()
    return render(request, 'accounts/friends.html', {'users': users, 'friends': friends})


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    else:
        form = EditProfile(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
        else:
            return redirect('/accounts/change-password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


class FeedBack(TemplateView):
    template_name = 'accounts/feedback.html'

    def get(self, request):
        form = GetFeedBack()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = GetFeedBack(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')

        else:
            form = GetFeedBack()
            return render(request, self.template_name, {'form': form})


class MyPost(TemplateView):
    template_name = 'accounts/post.html'

    def get(self, request):
        form = MakePost()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = MakePost(request.POST)

        if form.is_valid():
            var = form.save(commit=False)
            var.user = request.user
            var.save()
            return redirect('/accounts/profile')

        else:
            form = MakePost()
            return render(request, self.template_name, {'form': form})


def connect(request, op, pk):
    new_friend = User.objects.get(pk=pk)
    if op == 'add':
        Friend.make_friend(request.user, new_friend)
    if op == 'remove':
        Friend.lose_friend(request.user, new_friend)
    return redirect('accounts:friends')


def make_comment(request, pk):

    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.user = request.user
            var.post_associated = Post.objects.get(pk=pk)
            form.save()
            form = CommentsForm
            l = []
            for item in MyComments.objects.all():
                if int(item.post_associated.pk) == int(pk):
                    l.append(item)
            l = tuple(l)
            args = {'form': form, 'l': l}
            return render(request, 'accounts/comment.html', args)

    else:
        form = CommentsForm
    l = []
    for item in MyComments.objects.all():
        if int(item.post_associated.pk) == int(pk):
            l.append(item)
    l = tuple(l)
    args = {'form': form, 'l': l}
    return render(request, 'accounts/comment.html', args)


