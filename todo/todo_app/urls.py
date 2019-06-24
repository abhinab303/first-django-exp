from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'todo_app'
urlpatterns = [
    path('todo_view/', views.Todo_View.as_view(), name = 'todo_view'),
    path('add_view/<slug:passed_group_id>/', views.Add_View.as_view(), name = 'add_view'),
    path('del_view/<pk>/<slug:passed_group_id>/', views.Del_View.as_view(), name = 'del_view'),
    path('todo_login/', views.Todo_Login_View.as_view(), name = 'todo_login'),
    #path('todo_logout/', views.todo_logout_view, name = 'todo_logout'),
    path('todo_logout/', views.Todo_Logout_View.as_view(), name = 'todo_logout'),
    path('todo_create_user/', views.Todo_Create_User_View.as_view(), name = 'todo_create_user'),
    path('todo_change_pass/', views.Change_Pass_view.as_view(), name = 'todo_change_pass'),
    path('todo_reset_pass/', views.Reset_Pass_View.as_view(), name = 'todo_reset_pass'),
    path('todo_confirm_pass/<slug:uidb64>/<slug:token>/', views.Confirm_Pass_View.as_view(), name = 'todo_confirm_pass'),
    path('todo_create_group/', views.Create_Group_View.as_view(), name = 'todo_create_group'),
    path('todo_display_group/', views.Display_Group_View.as_view(), name = 'todo_display_group'),
    path('todo_enter_group/<slug:passed_group_id>/', views.Enter_Group_view.as_view(), name = 'todo_enter_group'),
    path('todo_edit_post/<pk>/<slug:passed_group_id>/', views.Edit_Post_View.as_view(), name = 'todo_edit_post'),
    path('todo_req_group/<slug:passed_group_id>/', views.Req_Group_View.as_view(), name = 'todo_req_group'),
    path('todo_display_msg/', views.Display_Msg_View.as_view(), name = 'todo_display_msg'),
    path('todo_accept_req/<pk>/', views.Accept_Request_View.as_view(), name = 'todo_accept_req'),
    path('todo_join_group/<slug:passed_group_id>/', views.Join_Group_View.as_view(), name = 'todo_join_group'),
    path('todo_invite_group/<slug:passed_group_id>/', views.Invite_User_View.as_view(), name = 'todo_invite_group'),
    path('todo_list_user/<slug:passed_group_id>/', views.View_Group_Users.as_view(), name = 'todo_list_user'),
    path('todo_make_su/<slug:passed_group_id>/<slug:passed_user_id>/', views.Make_Su_View.as_view(), name = 'todo_make_su'),
    path('todo_delete_group/<pk>/', views.Delete_Group_View.as_view(), name = 'todo_delete_group'),
    path('todo_inside_post/<pk>/', views.Inside_Post_View.as_view(), name = 'todo_inside_post'),
    path('todo_add_cmnt/<slug:post_pk>/', views.Add_Comment_View.as_view(), name = 'todo_add_cmnt'),
    path('todo_edit_cmnt/<pk>/<slug:post_pk>/', views.Edit_Cmnt_View.as_view(), name = 'todo_edit_cmnt'),
    path('todo_del_cmnt/<pk>/<slug:post_pk>/', views.Del_Cmnt_View.as_view(), name = 'todo_del_cmnt'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
