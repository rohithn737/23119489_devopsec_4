
from django.contrib import admin
from django.urls import path,include 

from django.conf import settings #Importing all the configurations from settings.py file

from django.conf.urls.static import static #Importing the static function

urlpatterns = [

    path("admin/", admin.site.urls),

    path('',include('journal.urls')), #to combine urls of our app with urls.py file of the project
     #Generate a unique URL to access our media files
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
#This will help in uploading our own media files