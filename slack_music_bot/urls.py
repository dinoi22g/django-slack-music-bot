"""
URL configuration for slack_music_bot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from events.views import slack_events, slack_interactions
from favorite_list.views import favorite_list_command

urlpatterns = [
    path('admin/', admin.site.urls),
    path('slack/events/', slack_events, name='slack_events'),
    path('slack/interactions/', slack_interactions, name='slack_interactions'),
    path('command/favorite_list/', favorite_list_command, name='favorite_list_command')
]
