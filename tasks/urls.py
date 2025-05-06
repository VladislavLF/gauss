from django.conf import settings
from django.conf.urls.static import static
from tasks.views import *
from django.urls import path, include
from django.contrib.auth import views


urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('tasks/', Tasks.as_view(), name="tasks"), # Список заданий ЕГЭ
    path('options/', Options.as_view(), name="options"), # Список вариантов ЕГЭ
    path('options/option-num-<int:opt_id>/', Catalog_option_tasks.as_view(), name='option'), # Каталог вариантов ЕГЭ
    path('tasks/task-num-<int:cat_id>/', Catalog_tasks.as_view(), name='category'), # Категория заданий ЕГЭ
    path('tasks/<slug:filter_slug>/', Catalog_tasks_filter.as_view(), name='filter_category'),  # Категория с фильтром заданий ЕГЭ
    path('themes/', Themes.as_view(), name="themes"),  # Теория
    path('accounts/register/', RegisterUser.as_view(), name='register'),
    path('accounts/login/', LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('task/<int:task_id>/', Task_Object.as_view(), name='task_object'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
