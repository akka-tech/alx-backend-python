from django.urls import path, include,routers.DefaultRouter()


urlpatterns = [
    path('api/', include('messaging_app.chats.urls')),