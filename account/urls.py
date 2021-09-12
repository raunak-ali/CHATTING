from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import  (
 
    register_view,
    login_view,
    logout_view,
    account_views,
    search_view,
    edit_account_view
)
app_name='account'
urlpatterns = [

    path('register/',register_view, name='register'),

    

    path('login/',login_view, name='login'),
    path('logout/',logout_view, name='logout'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),name='password_reset_complete'),
    path('<user_id>/',account_views, name='view'),
    path('?q',search_view, name='search'),
    path('<user_id>/edit/',edit_account_view, name='edit'),
    


]