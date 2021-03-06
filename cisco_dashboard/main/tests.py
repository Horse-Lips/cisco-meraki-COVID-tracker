"""Django Unit Tests"""
import meraki
from django.contrib.auth import authenticate
from django.test import TestCase
from django.contrib.auth.models import User
from main.models import UserProfile
from main.models import Organisation

# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

# Create your tests here.
class RegisterLoginTest(TestCase):
    """Tests registration and login functionality"""

    def test_register_and_login(self):
        """
         * Test registration functionality by registering a test account
         * Also test login functionality by logging in to the registered user account
        """
        user_creds = {
            'username': 'aa',
            'email': '549956326@qq.com',
            'password': 'secret',
            'apikey': 'customerday1'
        }

        response = self.client.post(
            '/register/',
            user_creds,
            follow=True
        )

        self.assertTrue(response.status_code == 200)  # Check registration was successful
        assert User.objects.get(username="aa")  # Ensure user exists

        user = authenticate(username='aa', password='secret')  # Login with register details
        self.assertTrue((user is not None) and user.is_authenticated)  # Assert login was successful


class TestUsername(TestCase):
    """Tests username """
    def test_username(self):
        """ Tests username """
        user_creds = {
            'username': 'testuser',
            'email': 'user@test.com',
            'password': 'secret',
            'apikey': 'customerday1'
        }

        self.client.post(
            '/register/',
            user_creds,
            follow=True
        )
        user_name = 'testuser'
        user = User.objects.get(username=user_name)
        assert user


class TestEmail(TestCase):
    """Tests user email"""
    def test_email(self):
        """ Tests emails """
        user_creds = {
            'username': 'testuser',
            'email': 'user@test.com',
            'password': 'secret',
            'apikey': 'customerday1'
        }

        self.client.post(
            '/register/',
            user_creds,
            follow=True
        )
        user_email = 'user@test.com'
        user = User.objects.get(email=user_email)
        assert user


class TestAPI(TestCase):
    """Simple API Test.
     *  Retrieves DevNet Sandbox organisation using the test API key
     *  Creates a db object for the organisation
     *  Checks that creation was successful
    """

    def test_api_call_and_model(self):
        """
         * This function retrieves the DevNet Sandbox organisation and stores it in the db
         * The organisation will then be retrieved and checked
        """
        api_key = "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"  # Test API keys
        dash = meraki.DashboardAPI(api_key)  # Set up dash using API keys

        try:
            devnet = dash.organizations.getOrganization("549236")

            test_org = Organisation.objects.create(
                org_id=devnet['id'],
                org_name=devnet['name'],
                org_url=devnet['url'],
                apikey=api_key
            )
            test_org.save()

        except meraki.exceptions.APIError:
            assert False

        try:
            get_org = Organisation.objects.get(org_id="549236")
            self.assertEqual(get_org, test_org)

        except Organisation.DoesNotExist:
            assert False


class ChangeAPIKeyTest(TestCase):
    """ Tests changing the api key for a user """
    def test_change_api_key(self):
        """ Tests changing the api key for a user """
        testdata = {
            'username': 'testuseralpha',
            'email': 'testuser@test.com',
            'password': 'testuser',
            'apikey': 'testcase1'
        }

        self.client.post('/register/', testdata, follow=True)
        self.client.login(username=testdata['username'], password=testdata['password'])
        testdatabeta = {'apikey': 'testcase2'}
        self.client.post('/editapikey', testdatabeta, follow=True)
        user = User.objects.get(username=testdata['username'])
        userprofile = UserProfile.objects.get(user=user)
        assert userprofile.apikey == testdatabeta['apikey']

class UseDemoKeyTest(TestCase):
    """ Tests if using the demo key works """
    def test_demo_key(self):
        """ Tests if using the demo key works """
        testprofile = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'secret',
            'apikey': 'testcase1'
        }
        self.client.post('/register/', testprofile, follow=True)
        self.client.login(username=testprofile['username'], password=testprofile['password'])
        self.client.post('/usedemokey', follow=True)
        user = User.objects.get(username=testprofile['username'])
        userprofile = UserProfile.objects.get(user=user)
        testdatabeta = {'apikey': 'demo'}
        self.assertEqual(userprofile.apikey, testdatabeta['apikey'])

class AlertsTest(TestCase):
    """ Tests alerts """
    def test_alerts(self):
        """ Tests alerts """
        testprofile = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'secret',
            'apikey': 'testcase1'
        }
        self.client.post('/register/', testprofile, follow=True)
        self.client.login(username=testprofile['username'], password=testprofile['password'])
        res = self.client.post('/alerts', follow=True)
        self.assertTrue(res.status_code == 200)


class OverviewTest(TestCase):
    """ Tests overview """
    def test_overview(self):
        """ Tests overview """
        testprofile = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'secret',
            'apikey': 'demo'
        }
        self.client.post('/register/', testprofile, follow=True)
        self.client.login(username=testprofile['username'], password=testprofile['password'])
        res = self.client.get('/overview', follow=True)
        self.assertTrue(res.status_code, 200)
