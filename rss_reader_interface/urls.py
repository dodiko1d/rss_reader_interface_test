from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:item_index>', views.show_more_about_item, name='full_item_info'),
    path('return_to_index', views.return_to_index, name='return_to_index')
]