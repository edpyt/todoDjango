from datetime import datetime

from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.forms import ValidationError

from .models import MyUser, ToDoModel
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _

from .forms import ToDoUser, LoginUserForm, RegistrationCustomUserForm, UpdateCustomUserForm


# Create your views here.
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
            not_solved = str(_('Not solved task'))
            for todo in todo_list:
                if todo.date_ending <= datetime.now(todo.date_ending.tzinfo) \
                        and todo.title != not_solved:
                    todo.title = not_solved
                    todo.is_done = True
                    todo.save()

            return todo_list
        return None

    def post(self, request, *args, **kwargs):
        check_list = request.POST.getlist('checkbox_list')

        done_list = [ToDoModel.objects.get(pk=todo_pk) for todo_pk in check_list]
        active_done_list = [todo for todo in done_list if not todo.is_done]

        if request.POST.get('Delete') and done_list:
            for todo in done_list:
                todo.delete()
        elif active_done_list:
            for todo in active_done_list:
                todo.is_done = True
                todo.save()
        else:
            messages.error(request, _('Select at least one active task'), extra_tags='danger')

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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = _('Registration')
        return data

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('todo_list')

    def get_template_names(self):
        return 'user/registration.html'


class DetailUserView(DetailView):
    model = MyUser
    template_name = 'user/user_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = _('User')
        return data

    def get_object(self, **kwargs):
        return MyUser.objects.get(pk=self.request.user.pk)


class UpdateUser(LoginRequiredMixin, UpdateView):
    form_class = UpdateCustomUserForm
    model = MyUser

    template_name = 'user/user_update.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = _('Redact User')
        return data

    def get_object(self, **kwargs):
        return MyUser.objects.get(pk=self.request.user.pk)


@login_required
def my_logout(request):
    logout(request)
    return redirect('todo_list')
