from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *


varDict = {
    'bestUsers': Profile.objects.best(),
    'popularTags': Tag.objects.popular()
}


def paginate(request, object_list, obj=None):
    paginator = Paginator(object_list, 10)
    if obj is not None:
        for i in paginator.page_range:
            if obj in paginator.get_page(i).object_list:
                return paginator.get_page(i)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    return objects


def index(request):
    questions = paginate(request, Question.objects.newest())
    varDict['subCategory'] = 'hot'
    varDict['questions'] = questions
    varDict['title'] = 'New questions'
    varDict['subTitle'] = 'Hot questions'
    return render(request, 'index.html', varDict)


def tag(request, tag_name):
    questions = paginate(request, Question.objects.tagged(tag_name))
    varDict['subCategory'] = ''
    varDict['questions'] = questions
    varDict['title'] = 'Tag: ' + tag_name
    varDict['subTitle'] = ''
    return render(request, 'index.html', varDict)


def hot(request):
    questions = paginate(request, Question.objects.hottest())
    varDict['subCategory'] = ''
    varDict['questions'] = questions
    varDict['title'] = 'HOT questions'
    varDict['subTitle'] = ''
    return render(request, 'index.html', varDict)


def question(request, question_id=0):
    form = AnswerForm(request.POST)
    quest = Question.objects.get(pk=question_id)
    if request.POST:
        if form.is_valid():
            answer = Answer.objects.create(question=quest,
                                           text=form.cleaned_data.get('textarea'),
                                           author=request.user.profile)
            page_num = int(quest.answer_set.count() / 4) + 1
        return redirect(request.path + '?page=' + str(page_num) + '#' + str(answer.id))
    answers = paginate(request, quest.answer_set.all())
    varDict.update({'question': quest,
                    'answers': answers,
                    'form': form})
    return render(request, 'one-question.html', varDict)


def login(request):
    next_page = request.GET.get('next', '/')
    form = LoginForm(request.POST)
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get('login'),
                                     password=form.cleaned_data.get('password'))
            if user is not None:
                auth.login(request, user)
                return redirect(next_page)
            else:
                form.add_error(None, 'Wrong login or password')
    varDict.update({'form': form})
    return render(request, 'login.html', varDict)


def logout(request):
    auth.logout(request)
    next_page = request.GET.get('stay', '/')
    return redirect(next_page)


def signup(request):
    form = RegisterForm(request.POST)
    if request.POST:
        if form.is_valid():
            name = form.cleaned_data.get('login')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('password2')
            if password != password2:
                form.add_error(None, 'Passwords do not match')
            elif Profile.objects.is_exist(name, email):
                form.add_error(None, 'User with this login already exist')
            else:
                user = User.objects.create_user(name, email, password)
                Profile.objects.create(user=user)
                auth.login(request, user)
                return redirect('/')
    varDict.update({'form': form})
    return render(request, 'signup.html', varDict)


@login_required(login_url='/login')
def ask(request):
    form = AskForm(request.POST)
    if request.POST:
        if form.is_valid():
            tags = form.cleaned_data.get('tags')
            tags_id = []
            if tags:
                tags = tags.split()
                tags_id = Tag.objects.add_tag(tags).copy()
            quest = Question.objects.create(title=form.cleaned_data.get('title'),
                                            text=form.cleaned_data.get('text'),
                                            author=request.user.profile)
            quest.add_tags(tags_id)
            return redirect(reverse('askqa_question', args=[quest.id]))
    varDict.update({'form': form})
    return render(request, 'ask.html', varDict)


@login_required(login_url='/login')
def profile(request):
    init_data = {'login': request.user.username,
                 'email': request.user.email}
    prof = Profile.objects.filter(user=request.user)[0]
    form = ProfileEditForm(init_data, initial=init_data)
    changed = False

    if request.POST:
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('login')
            email = form.cleaned_data.get('email')

            if name != request.user.username:
                if not prof.new_name(name):
                    form.add_error(None, 'This username is already exist')
                else:
                    changed = True

            if email != request.user.email:
                if not prof.new_email(email):
                    form.add_error(None, 'This email is already taken')
                else:
                    form.add_error(None, 'OK')
                    changed = True

            if changed:
                auth.logout(request)
                auth.login(request, prof.user)

    varDict.update({'form': form})
    return render(request, 'profile.html', varDict)
