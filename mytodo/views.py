from datetime import timedelta, datetime

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .models import MyUser, ToDoModel
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from .forms import ToDoUser, LoginUserForm, RegistrationCustomUserForm


# Create your views here.
class MyUserDetail(DetailView):
    model = MyUser
    template_name = 'user/user_detail.html'
    context_object_name = 'user_details'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = _('Profile')
        return data


class ToDoList(ListView):
    model = ToDoModel
    template_name = 'todo/todo_list.html'
    context_object_name = 'todo_list'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = _('Task list')
        return data

    def get_queryset(self):
        if self.request.user.id:
            todo_list = self.model.objects.filter(user=self.request.user)
            not_solved = str(_('Task not solved'))
            for todo in todo_list:
                if todo.date_ending <= datetime.now(todo.date_ending.tzinfo)\
                        and todo.title != not_solved:
                    todo.title = not_solved
                    todo.save()
            return todo_list
        return None

    def post(self, request, *args, **kwargs):
        done_list = [ToDoModel.objects.get(pk=todo_pk) for todo_pk in request.POST.getlist('checkbox_list')]

        for todo in done_list:
            if todo.is_done:
                todo.is_done = False
            else:
                todo.is_done = True

            todo.save()

        return redirect('todo_list')


class ToDoDelete(LoginRequiredMixin, DeleteView):
    model = ToDoModel
    template_name = 'todo/todo_delete.html'
    context_object_name = 'todo'

    success_url = reverse_lazy('todo_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = _('Delete todo')
        return data


class CreateToDo(LoginRequiredMixin, CreateView):
    form_class = ToDoUser
    model = ToDoModel
    template_name = 'todo/todo_create.html'

    success_url = reverse_lazy('todo_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['input_value'] = _('Send')
        return data

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        return redirect('todo_list')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse_lazy('todo_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = _('Login')
        return data


class RegisterUser(CreateView):
    form_class = RegistrationCustomUserForm
    template_name = 'user/register.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = _('Registrate')
        return data

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('todo_list')


@login_required
def my_logout(request):
    logout(request)
    return redirect('todo_list')
