from django.http import HttpResponseForbidden
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from .forms import *
from django.shortcuts import render, redirect
from .forms import RegisterUserForm, LoginUserForm
from .models import *
from django.views.generic import CreateView, ListView, DetailView

# Create your views here.

nav = [{'title': "Главная страница", 'url_name': 'home'},
        {'title': "Варианты ЕГЭ", 'url_name': 'options'},
        {'title': "Задания ЕГЭ", 'url_name': 'tasks'},
        {'title': "Теория", 'url_name': 'themes'}
]

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def forbidden_403(request):
    return HttpResponseForbidden()

class Home(ListView):
    model = Task
    template_name = 'tasks/index.html'
    extra_context = {'title': 'Главная страница'}


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        context['home'] = 'Главная страница'
        context['options'] = 'Варианты ЕГЭ'
        context['tasks'] = 'Задания ЕГЭ'
        context['theory'] = 'Теория'
        return context

class Tasks(ListView):
    model = Category_Tasks
    template_name = 'tasks/tasks.html'
    context_object_name = 'categorie'
    extra_context = {'title': 'Задания ЕГЭ'}


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        count_tasks = Category_Tasks.objects.all()
        context['categories'] = {}
        for i in range(1,len(count_tasks) + 1):
            context['categories'][Category_Tasks_Filter.objects.filter(cat__id=i)] = count_tasks[i-1]

        return context

class Task_Object(DetailView):
    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'post'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        context['title'] = f"Задача №{self.kwargs['task_id']}"
        context['title_task'] = self.kwargs['task_id']
        context['comments'] = Comment.objects.filter(post = self.kwargs['task_id'], is_published = True)
        form = AddCommentForm()
        context['form'] = form
        context['theme'] = Task.objects.get(id = self.kwargs['task_id']).filter
        return context

    def get_object(self, **kwargs):
        return Task.objects.get(id=self.kwargs['task_id'])

    def post(self, request,  *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'POST':
                form = AddCommentForm(request.POST)
                if form.is_valid():
                    form.user = request.POST.get("user", "")
                    form.post = request.POST.get("post", "")
                    form.save()
                    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
        return render(request, "tasks/index.html")




class Options(ListView):
    model = Category_Options
    template_name = 'tasks/options.html'
    context_object_name = 'options'
    extra_context = {'title': 'Варианты ЕГЭ'}


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav

        return context

class Catalog_tasks(ListView):
    model = Task
    template_name = 'tasks/list_tasks.html'
    context_object_name = 'posts'
    paginate_by = 10


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        context['title'] = f"Задание {self.kwargs['cat_id']}"
        context['task_cat'] = self.kwargs['cat_id']

        return context

    def get_queryset(self):
        return Task.objects.filter(cat_id=self.kwargs['cat_id'])



class Catalog_tasks_filter(ListView):
    model = Category_Tasks_Filter
    template_name = 'tasks/list_tasks.html'
    context_object_name = 'posts'
    paginate_by = 10




    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        context['task_cat'] = self.kwargs['filter_slug'].split('-')[2]
        context['title'] = f"Задание {context['task_cat']}"

        return context

    def get_queryset(self):
        lst = Category_Tasks_Filter.objects.filter(slug = self.kwargs['filter_slug'])
        posts = Task.objects.filter(filter__id=lst.values('id')[0]['id'], is_published=True)
        return posts


class Catalog_option_tasks(ListView):
    model = Category_Options
    template_name = 'tasks/list_option.html'
    context_object_name = 'tasks'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        context['title'] = f"Вариант {self.kwargs['opt_id']}"


        return context

    def get_queryset(self):
        option = Category_Options.objects.filter(id=self.kwargs['opt_id'], is_published=True)
        lst = list(option.values()[0].items())[7:]
        lst = [
            Task.objects.get(id=i) for i in [int(x[1]) for x in lst]
        ]
        tasks = {}
        for i in range(1,18+1):
            tasks[i] = lst[i-1]
        return tasks

class Themes(ListView):
    model = Theory_category
    template_name = 'tasks/themes.html'
    extra_context = {'title': 'Теория'}
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        lst_id = [i['id'] for i in Theory_category.objects.all().values('id')]
        lst_cats = [i['category'] for i in Theory_category.objects.all().values('category')]
        context['content'] = []
        for i in lst_id:
            context['content'].append([item for item in Theory_item.objects.filter(cat__id=i, is_published=True)])
        context['dct'] = {}
        for i in range(0,len(lst_id)):
            context['dct'][lst_cats[i]] = context['content'][i]

        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'nav': nav, 'title': 'Регистрация'}
        return dict(list(context.items()) + list(c_def.items()))


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'nav': nav, 'title': 'Войти'}
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

