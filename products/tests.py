from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse

from products.models import Category, Products


class TestApiProduct(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', email='', password='admin-pass')
        self.normal_user = User.objects.create_user(username='user', email='user@email.com', password='user-pass')
        self.product = Products.objects.create(name='Product',
                                              description='Description',
                                              price=100, stock=10,
                                              category=Category.objects.create(name='Category'))

        self.url = reverse('products-list')

    def test_get_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['name'], self.product.name)


    def test_unauthorized_update_product(self):
        response = self.client.put(self.url, {'name': 'Updated Product'})
        self.assertEqual(response.status_code, 401)

