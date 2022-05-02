from django.urls import path
from .views import AgendaDelete, AgendaList, AgendaDetail, AgendaCreate, AgendaUpdate, AgendaLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', AgendaLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', AgendaList.as_view(), name='agenda-list'),
    path('agenda/<int:pk>/', AgendaDetail.as_view(), name='agenda'),
    path('agenda-create', AgendaCreate.as_view(), name='agenda-create'),
    path('agenda-update/<int:pk>/', AgendaUpdate.as_view(), name='agenda-update'),
    path('agenda-delete/<int:pk>/', AgendaDelete.as_view(), name='agenda-delete'),
]
