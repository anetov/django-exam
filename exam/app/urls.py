from django.urls import re_path, path
from .views import  UserLogoutView, UserProfileView, list_posts, Login, SignUpView, edit_post, delete_post, create_post, VerifyEmailView, VerificationSuccess, VerificationError, CommentListView, CommentCreateView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetView, LogoutView


urlpatterns = [
    #  Пути для авторизации
    path('', Login.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name = 'signup'),
    path('logout/', UserLogoutView.as_view(), name = 'logout'),
    # 
    path('profile/', UserProfileView.as_view(), name='profile'),
    #  Пути для восстановления пароля
    path('reset_password/',PasswordResetView.as_view(template_name = "registration/password_reset.html"), name='reset'),
    path('reset/<uidb64>/<str:token>',PasswordResetConfirmView.as_view(template_name = "registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/',PasswordResetDoneView.as_view(template_name='registration/reset_done.html'), name='password_reset_done'),
    path('reset/complete/',PasswordResetCompleteView.as_view(template_name='registration/reset_complete.html'), name='password_reset_complete'),
    #  Пути для подтверждения почты
    path('verify/<int:user_id>/<str:token>', VerifyEmailView.as_view(), name='verify'),
    path('verify/success', VerificationSuccess.as_view(), name='verify_success'),
    path('verify/error', VerificationError.as_view(), name='verify_error'),
    #  Пути для работы с публикациями
    re_path(r'^posts/$', list_posts, name='posts'),
    re_path(r'^posts/create/$', create_post, name='create_post'),
    path('posts/edit/<int:post_id>/', edit_post, name='edit_post'),
    path('posts/delete/<int:post_id>/', delete_post, name='delete_post'),
    #  Пути для работы с комментариями
    re_path(r'^posts/(?P<post_id>\d+)/comments/$', CommentListView.as_view(), name='comment_list'),
    re_path(r'^posts/(?P<post_id>\d+)/comments/create/$', CommentCreateView.as_view(), name='create_comment'),
]