from django.urls import path
from juntagrico_webdav import views

app_name = 'webdav'
urlpatterns = [
    path('wd/list/<int:id>/', views.list),
    path('wd/get/<int:id>/<str:file>/', views.get_item, name='get-file')
]
