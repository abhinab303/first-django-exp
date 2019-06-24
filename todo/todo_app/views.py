from django.shortcuts import render
from django.views import generic, View
from .models import Todo_Post, Todo_Group, Todo_Msg, Todo_Comment
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import TemplateView
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from .forms import InviteForm

class Todo_Login_View(auth_views.LoginView):
    template_name = 'todo_app/todo_login.html'
    extra_context = {'next':reverse_lazy('todo_app:todo_view')}

class Todo_Create_User_View(generic.edit.FormView):
    template_name = 'todo_app/create_user.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('todo_app:todo_login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class Change_Pass_view(auth_views.PasswordChangeView):
    template_name = 'todo_app/change_pass.html'
    success_url = reverse_lazy('todo_app:todo_login')

class Reset_Pass_View(auth_views.PasswordResetView):
    template_name = 'todo_app/reset_pass.html'
    email_template_name = 'todo_app/reset_pass_email.html'
    subject_template_name = 'todo_app/reset_pass_sub.html'
    success_url = reverse_lazy('todo_app:todo_login')
    from_email = "070bel303@pcampus.edu.np"

class Confirm_Pass_View(auth_views.PasswordResetConfirmView):
    template_name = 'todo_app/confirm_pass.html'
    success_url = reverse_lazy('todo_app:todo_login')

class Todo_Logout_View(LoginRequiredMixin, auth_views.LogoutView):
    login_url = reverse_lazy('todo_app:todo_login')
    next_page = login_url

class Todo_View(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('todo_app:todo_login')
    model = Todo_Post
    template_name = 'todo_app/todo_temp.html'
    context_object_name = 'todo_post_list'

    def get_queryset(self):
        return Todo_Post.objects.filter(owner = self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #get groups in which the current user is the superuser
        my_groups = self.request.user.todo_group_set.all()
        su_group_list = []
        for each_group in my_groups:
            if(self.request.user.has_perm('todo_app.' + 'group_su_' + str(each_group.id))):
                su_group_list.append(each_group)
        context['user_groups_list'] = su_group_list
        return context

class Add_View(LoginRequiredMixin, generic.edit.CreateView):
    login_url = reverse_lazy('todo_app:todo_login')
    model = Todo_Post
    template_name = 'todo_app/todo_add.html'
    fields = ['post_text', 'image']

    def get_success_url(self, **kwargs):
        self.object.post_group = Todo_Group.objects.get(id=self.kwargs['passed_group_id'])
        self.object.add_date = timezone.now()
        self.object.owner = self.request.user
        self.object.post_slug = 'post_' + str(self.object.id)

        content_type = ContentType.objects.get_for_model(Todo_Post)
        perm_edit = Permission.objects.create(
            codename = 'can_edit_post_' + str(self.object.id),
            name = 'can_edit_post_' + str(self.object.id),
            content_type = content_type,
        )
        perm_delete = Permission.objects.create(
            codename = 'can_delete_post_' + str(self.object.id),
            name = 'can_delete_post_' + str(self.object.id),
            content_type = content_type,
        )
        self.request.user.user_permissions.add(perm_edit, perm_delete)


        self.object.save()

        return reverse(
            'todo_app:todo_enter_group',
            kwargs = {'passed_group_id' : self.kwargs['passed_group_id']},
        )

class Del_View(LoginRequiredMixin, generic.edit.DeleteView):
    login_url = reverse_lazy('todo_app:todo_login')
    model = Todo_Post
    #template_name = 'todo_app/del_temp.html'
    #success_url = reverse_lazy('todo_app:todo_enter_group')
    def get_success_url(self, **kwargs):
        return reverse(
            'todo_app:todo_enter_group',
            kwargs = {'passed_group_id' : self.kwargs['passed_group_id']},
        )

class Display_Group_View(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('todo_app:todo_login')
    model = Todo_Group
    template_name = 'todo_app/todo_group_list.html'
    context_object_name = 'todo_group_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_groups_list'] = self.request.user.todo_group_set.all()
        #to check whether the user has requested to join the group or not
        usr_msgs = Todo_Msg.objects.filter(msg_from_user_id = self.request.user.id)
        user_msg_group_list = []
        for each_msg in usr_msgs:
            user_msg_group_list.append(each_msg.msg_group)
        context['user_msg_group_list'] = user_msg_group_list
        return context


class Create_Group_View(LoginRequiredMixin, generic.edit.CreateView):
    login_url = reverse_lazy('todo_app:todo_login')
    model = Todo_Group
    template_name = 'todo_app/todo_group.html'
    fields = ['group_name', 'group_type']

    def get_success_url(self):
        content_type = ContentType.objects.get_for_model(Todo_Group)
        group_su_perm = Permission.objects.create(
            codename = 'group_su_' + str(self.object.id),
            name = 'group_su_' + str(self.object.id),
            content_type = content_type,
        )
        self.request.user.user_permissions.add(group_su_perm)
        self.object.group_slug = 'group_' + str(self.object.id)
        self.object.save()
        self.object.group_users.add(self.request.user)
        self.object.save()
        return reverse('todo_app:todo_display_group')

class Enter_Group_view(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('todo_app:todo_login')
    template_name = 'todo_app/inside_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_post_list'] = Todo_Post.objects.filter(post_group_id = context['passed_group_id'])
        context['todo_group'] = Todo_Group.objects.get(id = context['passed_group_id'])

        del_perm = []
        edit_perm = []
        for post in context['todo_post_list']:
            if(self.request.user.has_perm('todo_app.can_delete_post_' + str(post.id))or \
                self.request.user.has_perm('todo_app.group_su_' \
                + str(self.kwargs['passed_group_id']))):
                del_perm.append(post.id)
            if(self.request.user.has_perm('todo_app.can_edit_post_' + str(post.id))):
                edit_perm.append(post.id)
        context['del_perm'] = del_perm
        context['edit_perm'] = edit_perm
        if(self.request.user.has_perm('todo_app.group_su_' + str(self.kwargs['passed_group_id']))):
            context['can_delete_group'] = True

        return context

class Edit_Post_View(LoginRequiredMixin, generic.edit.UpdateView):
    model = Todo_Post
    fields = ['post_text']
    template_name = 'todo_app/edit_post.html'

    def get_success_url(self, **kwargs):
        return reverse(
            'todo_app:todo_enter_group',
            kwargs = {'passed_group_id' : self.kwargs['passed_group_id']},
        )

class Display_Msg_View(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('todo_app:todo_login')
    model = Todo_Msg
    template_name = 'todo_app/disp_msg.html'
    context_object_name = 'todo_msg_list'

    def get_queryset(self):
        return Todo_Msg.objects.filter(msg_to_user = self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_groups_list'] = self.request.user.todo_group_set.all()
        return context



class Req_Group_View(LoginRequiredMixin, generic.edit.CreateView):
    login_url = reverse_lazy('todo_app:todo_login')
    model = Todo_Msg
    template_name = 'todo_app/req_msg.html'
    fields = ['msg_text']

    def get_success_url(self, **kwargs):
        perm = Permission.objects.get(codename = 'group_su_' + str(self.kwargs['passed_group_id']))
        related_users = perm.user_set.all()
        self.object.msg_from_user_id = self.request.user.id
        self.object.msg_group = Todo_Group.objects.get(id = self.kwargs['passed_group_id'])
        self.object.save()

        for each_user in related_users:
            self.object.msg_to_user.add(each_user)

        return reverse('todo_app:todo_display_group')


class Accept_Request_View(LoginRequiredMixin, generic.edit.DeleteView):
    login_url = reverse_lazy('todo_app:todo_login')
    model = Todo_Msg
    #template_name = 'todo_app/del_temp.html'
    #success_url = reverse_lazy('todo_app:todo_enter_group')
    def get_success_url(self, **kwargs):
        req_user = User.objects.get(id = self.object.msg_from_user_id)
        self.object.msg_group.group_users.add(req_user)
        return reverse( 'todo_app:todo_display_msg')

class Join_Group_View(LoginRequiredMixin, View):
    login_url = reverse_lazy('todo_app:todo_login')

    def post(self, request, *args, **kwargs):
        my_group = Todo_Group.objects.get(id = self.kwargs['passed_group_id'])
        my_group.group_users.add(self.request.user)
        redirect_url = reverse(
            'todo_app:todo_enter_group',
            kwargs = {'passed_group_id' : self.kwargs['passed_group_id']},
        )
        return HttpResponseRedirect(redirect_url)

class Invite_User_View(LoginRequiredMixin, generic.edit.FormView):
    login_url = reverse_lazy('todo_app:todo_login')
    template_name = 'todo_app/invite_user.html'
    form_class = InviteForm

    def form_valid(self, form):
        user_id = form.cleaned_data['user_id']
        my_group = Todo_Group.objects.get(id = self.kwargs['passed_group_id'])
        my_user = User.objects.get(id = user_id)
        my_group.group_users.add(my_user)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse(
            'todo_app:todo_enter_group',
            kwargs = {'passed_group_id' : self.kwargs['passed_group_id']},
        )

class View_Group_Users(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('todo_app:todo_login')
    template_name = 'todo_app/list_users.html'
    model = User
    context_object_name = 'user_list'

    def get_queryset(self):
        return Todo_Group.objects.get(id = self.kwargs['passed_group_id']).group_users.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['passed_group_id'] = self.kwargs['passed_group_id']
        my_perm = Permission.objects.get(codename = 'group_su_' + str(self.kwargs['passed_group_id']))
        context['already_su_list'] = my_perm.user_set.all()
        return context

class Make_Su_View(LoginRequiredMixin, View):
    login_url = reverse_lazy('todo_app:todo_login')


    def post(self, request, *args, **kwargs):
        my_group = Todo_Group.objects.get(id = self.kwargs['passed_group_id'])
        my_user = User.objects.get(id = self.kwargs['passed_user_id'])
        my_perm = Permission.objects.get(codename = 'group_su_' + str(self.kwargs['passed_group_id']))
        my_user.user_permissions.add(my_perm)
        redirect_url = reverse(
            'todo_app:todo_list_user',
            kwargs = {'passed_group_id' : self.kwargs['passed_group_id']},
        )
        return HttpResponseRedirect(redirect_url)

class Delete_Group_View(LoginRequiredMixin, generic.edit.DeleteView):
    login_url = reverse_lazy('todo_app:todo_login')
    model = Todo_Group
    success_url = reverse_lazy('todo_app:todo_display_group')

class Add_Comment_View(LoginRequiredMixin, generic.edit.CreateView):
    login_url = reverse_lazy('todo_app:todo_login')
    model = Todo_Comment
    template_name = 'todo_app/add_cmnt.html'
    fields = ['text']

    def get_success_url(self, **kwargs):
        self.object.post = Todo_Post.objects.get(id=self.kwargs['post_pk'])
        self.object.date = timezone.now()
        self.object.owner = self.request.user
        self.object.vote = 0

        content_type = ContentType.objects.get_for_model(Todo_Post)
        perm_edit = Permission.objects.create(
            codename = 'can_edit_cmnt_' + str(self.object.id),
            name = 'can_edit_cmnt_' + str(self.object.id),
            content_type = content_type,
        )
        perm_delete = Permission.objects.create(
            codename = 'can_delete_cmnt_' + str(self.object.id),
            name = 'can_delete_cmnt_' + str(self.object.id),
            content_type = content_type,
        )
        self.request.user.user_permissions.add(perm_edit, perm_delete)


        self.object.save()

        return reverse(
            'todo_app:todo_inside_post',
            kwargs = {'pk' : self.kwargs['post_pk']},
        )

class Inside_Post_View(LoginRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('todo_app:todo_login')
    model = Todo_Post
    template_name = 'todo_app/inside_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_post = Todo_Post.objects.get(pk = self.kwargs['pk'])
        context['comment_list'] = Todo_Comment.objects.filter(post = my_post)

        del_perm = []
        edit_perm = []
        for comment in context['comment_list']:
            if(self.request.user.has_perm('todo_app.can_delete_cmnt_' + str(comment.id))or \
                self.request.user.has_perm('todo_app.group_su_' \
                + str(my_post.post_group.id)) or self.request.user == my_post.owner):
                del_perm.append(comment.id)
            if(self.request.user.has_perm('todo_app.can_edit_cmnt_' + str(comment.id))):
                edit_perm.append(comment.id)
        context['del_perm'] = del_perm
        context['edit_perm'] = edit_perm

        return context

class Edit_Cmnt_View(LoginRequiredMixin, generic.edit.UpdateView):
    model = Todo_Comment
    fields = ['text']
    template_name = 'todo_app/edit_post.html'

    def get_success_url(self, **kwargs):
        return reverse(
            'todo_app:todo_inside_post',
            kwargs = {'pk' : self.kwargs['post_pk']},
        )

class Del_Cmnt_View(LoginRequiredMixin, generic.edit.DeleteView):
    login_url = reverse_lazy('todo_app:todo_login')
    model = Todo_Comment
    #template_name = 'todo_app/del_temp.html'
    #success_url = reverse_lazy('todo_app:todo_enter_group')
    def get_success_url(self, **kwargs):
        return reverse(
            'todo_app:todo_inside_post',
            kwargs = {'pk' : self.kwargs['post_pk']},
        )
