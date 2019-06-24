from django.test import TestCase
from django.test import Client
from django.contrib import auth
from django.contrib.auth.models import User
import todo_app.views as my_views
from django.contrib.auth.forms import AuthenticationForm,  SetPasswordForm
import todo_app.models as my_models
from django.core import mail
from django.contrib.auth.hashers import check_password
from django.urls import reverse

# Create your tests here.
class TodoTestCase(TestCase):

    def test_can_open_login_page(self):
        my_rep = self.client.get('/todo_login/')
        self.assertEqual(my_rep.status_code, 200)

    def test_can_open_signup_page(self):
        my_rep = self.client.get('/todo_create_user/')
        self.assertEqual(my_rep.status_code, 200)

    def test_can_signup(self):
        username = 'test_user'
        password = 'test_pass_1'
        my_rep = self.client.post(
            '/todo_create_user/',
            {
                'username': username,
                'password1': password,
                'password2': password,
            }
        )
        self.assertEqual(my_rep.status_code, 302)

        self.assertEqual(
            my_rep.resolver_match.func.__name__,
            my_views.Todo_Create_User_View.as_view().__name__
        )
        self.assertTrue(
            User.objects.all().filter(username = username).exists()
        )

    def test_can_login(self):
        #create test user:
        my_user = User.objects.create_user(
            username = 'test_user_2',
            password = 'test_pass_1'
        )
        #check if it is created inside database:
        self.assertTrue(
            User.objects.all().filter(username = my_user.username).exists()
        )
        #check form validation:
        my_form = AuthenticationForm(
            data = {
                'username': 'test_user_2',
                'password': 'test_pass_1'
            }
        )
        self.assertTrue(my_form.is_valid())

        #post req with wrong username and password:
        my_rep = self.client.post(
            '/todo_login/',
            {
                'username': 'wrong_user_name',
                'password': 'wrong_password',
                'next': '/todo_view/',
            },
        )

        #print(my_rep)
        #check if gives the error
        self.assertFormError(
            my_rep,
            'form',
            None,
            'Please enter a correct username and password. ' +
            'Note that both fields may be case-sensitive.',
        )

        #make post req to login view with the new user:
        my_rep = self.client.post(
            '/todo_login/',
            {
                'username': 'test_user_2',
                'password': 'test_pass_1',
                'next': '/todo_view/',
            },
        )
        #check if its calling correct view:
        self.assertEqual(
            my_rep.resolver_match.func.__name__,
            my_views.Todo_Login_View.as_view().__name__
        )
        #check status code:
        self.assertEqual(my_rep.status_code, 302)
        #check whether successful login or not:
        my_user = auth.get_user(self.client)
        self.assertTrue(my_user.is_authenticated)

    def test_can_open_todo_view(self):
        #my_rep = self.client.get('/todo_view/')
        #print(my_rep)
        #'''create test user:'''
        my_user = User.objects.create_user(
            username = 'test_user',
            password = 'test_pass'
        )
        #'''check if it is created inside database:'''
        self.assertTrue(
            User.objects.all().filter(username = my_user.username).exists()
        )
        #'''login user'''
        self.client.login(username = 'test_user', password = 'test_pass')
        #'''check if we are logged in:'''
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        #'''make get request to todo_view:'''
        resp = self.client.get('/todo_view/')
        #'''check if its calling correct view:'''
        self.assertEqual(
            resp.resolver_match.func.__name__,
            my_views.Todo_View.as_view().__name__
        )
        #'''check status code:'''
        self.assertEqual(resp.status_code, 200)

    def test_can_logout(self):
        my_user = User.objects.create_user(
            username = 'test_user_2',
            password = 'test_pass_1'
        )
        #check if it is created inside database:
        self.assertTrue(
            User.objects.all().filter(username = my_user.username).exists()
        )
        self.client.login(username = 'test_user_2', password = 'test_pass_1')
        #check login
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        #make a get request for todo_logout_view
        resp = self.client.get('/todo_logout/', follow = True)
        #'''check if redirected to correct view:'''
        self.assertEqual(
            resp.resolver_match.func.__name__,
            my_views.Todo_Login_View.as_view().__name__
        )
        #'''check status code:'''
        self.assertEqual(resp.status_code, 200)
        # ''' check logout '''
        self.assertFalse(auth.get_user(self.client).is_authenticated)

    def test_reset_pass(self):
        #create user
        my_user = User.objects.create_user(
            username = 'test_user3',
            password = 'test_pass_1'
        )
        my_user.email = 'abc@xyz.com'
        my_user.save()
        #check if it is created inside database:
        self.assertTrue(
            User.objects.all().filter(username = my_user.username).exists()
        )
        # get request to reset pass view
        resp = self.client.post('/todo_reset_pass/', {'email': my_user.email})
        self.assertEqual(resp.status_code, 302)
        # check if mail is sent
        self.assertEqual(len(mail.outbox), 1)
        # simulate user following link sent in email
        resp = self.client.get(
            reverse(
                'todo_app:todo_confirm_pass',
                kwargs = {
                    'token': resp.context['token'],
                    'uidb64': resp.context['uid']
                },
            ),
        )
        self.assertEqual(resp.status_code, 302)
        # post request to change password to the url given by previous get req
        resp = self.client.post(
            resp.url,
            {
                'new_password1': 'zmalqp1029384756',
                'new_password2': 'zmalqp1029384756'
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/todo_login/')
        #reload user from DB and check if the password is changed
        my_user = User.objects.all().get(username = 'test_user3')
        self.assertTrue(check_password('zmalqp1029384756', my_user.password))

    def test_change_pass(self):
        #create a user:
        my_user = User.objects.create_user(
            username = 'change_pass',
            password = 'test_pass'
        )
        #check if it is created inside database:
        self.assertTrue(
            User.objects.all().filter(username = my_user.username).exists()
        )
        #login with the User:
        self.client.login(username = 'change_pass', password = 'test_pass')
        #'''check if we are logged in:'''
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        #get request to change pass:
        resp = self.client.get('/todo_change_pass/')
        self.assertEqual(resp.status_code, 200)
        #post request with form data:
        resp = self.client.post(
            '/todo_change_pass/',
            {
                'old_password': 'test_pass',
                'new_password1': 'zmalqp1029384756',
                'new_password2': 'zmalqp1029384756'
            }
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/todo_login/')
        #reload user from DB and check if the password has changed
        my_user = User.objects.all().get(username = 'change_pass')
        self.assertFalse(check_password('test_pass', my_user.password))
        self.assertTrue(check_password('zmalqp1029384756', my_user.password))

class TestWithFixtures(TestCase):
    fixtures = ['fix2.json']

    def test_todo_view(self):
        # '''login user'''
        self.client.login(username = 'fearMe', password = 'zmalqp1029384756')
        # '''check if we are logged in:'''
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        resp = self.client.get('/todo_view/')
        context_list = resp.context['todo_post_list']
        actual_list = my_models.Todo_Post.objects.all().filter(
            owner = auth.get_user(self.client)
        )
        #check if two list are same
        #print(set(context_list) - set(actual_list))
        self.assertFalse(set(context_list) - set(actual_list))

        #check if all user groups are displayed
        group_list = my_models.Todo_Group.objects.all()
        actual_list = []
        for g in group_list[:]:
            if auth.get_user(self.client).has_perm(
                'todo_app.' + 'group_su_' + str(g.id)
            ):
                actual_list.append(g)

        self.assertFalse(
            set(resp.context['user_groups_list']) - set(actual_list)
        )
