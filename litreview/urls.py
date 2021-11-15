"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth.views import LoginView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# imports
import authentication.views
import app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup, name='signup'),
    path('home/create_ticket', app.views.create_ticket, name='create_ticket'),
    path('home/create_review', app.views.create_review, name='create_review'),
    path('home/<int:review_id>', app.views.view_review, name='view_review'),
    path('home/<int:review_id>/edit', app.views.edit_review,
         name='edit_review'),
    path('home/subsriptions', app.views.sub, name='sub'),
    path('feed', app.views.feed, name='feed'),
    path('home/', app.views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
