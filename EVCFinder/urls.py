from django.contrib import admin
from django.urls import path
from polls.views import all_polls
from user.views import( add_polls, 
                        user_registration, 
                        user_login, 
                        user_logout, 
                        show_profile, 
                        search_user_view,
                        user_follow_view,
                        see_all_followings,
                        user_unfollow_view)

from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^allpolls/(?P<id>[0-9]*)', all_polls, name="allpolls"),

    path('signup/', user_registration, name="sign_up"),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add/', add_polls, name="add"),
    path('profile/', show_profile, name="profile"),

    path('search/', search_user_view, name="search"),
    path('follow/<int:id>', user_follow_view, name="follow"),
    path("unfollow/<int:id>/", user_unfollow_view, name="unfollow"),
    path("following/", see_all_followings, name="following"),
]
