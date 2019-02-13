from django.urls import path
from . import views


app_name = 'mycollections'

urlpatterns = [
	path('', views.HomepageView.as_view(), name='homepage'),
	path('collection/<int:pk>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    path('collection/create/', views.CollectionCreate.as_view(), name='collection_create'),
    path('collection/update/<int:pk>/', views.CollectionUpdate.as_view(), name='collection_update'),
    path('collection/delete/<int:pk>/', views.CollectionDelete.as_view(), name='collection_delete'),
	]
