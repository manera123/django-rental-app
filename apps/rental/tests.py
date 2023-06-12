from django.test import TestCase
from .models import NewAdvt
from apps.accounts.models import User
# Create your tests here.


class RentalTestCase(TestCase):
    def setUp(self):
        user = User.objects.get(id='1')
        advt = NewAdvt.objects.create(host=user)
    def test_advt_host(self, advt, user):
        self.assertEqual(advt.host, user)