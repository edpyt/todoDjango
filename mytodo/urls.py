from django.urls import path

from .views import UpdateUser, DetailUserView, ToDoList, CreateToDo, my_logout, LoginUser, RegisterUser, ToDoDelete

urlpatterns = [
    path('user/', DetailUserView.as_view(), name='user_profile'),
    path('user/edit', UpdateUser.as_view(), name='user_profile_edit'),

    path('', ToDoList.as_view(), name='todo_list'),
    path('todo/create/', CreateToDo.as_view(), name='todo_create'),
    path('todo/<int:pk>/delete/', ToDoDelete.as_view(), name='todo_delete'),

    path('registration/', RegisterUser.as_view(), name='register_myuser'),
    path('login/', LoginUser.as_view(), name='login_myuser'),
    path('logout/', my_logout, name='logout_myuser')
]
