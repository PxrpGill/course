from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.AboutTemplateView.as_view(), name='about'),
    path('buyers/', views.BuyersTemplateView.as_view(), name='buyers'),
    path('contacts/', views.ContactsTemplateView.as_view(), name='contacts'),
]