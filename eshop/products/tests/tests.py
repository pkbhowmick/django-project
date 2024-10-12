from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from products.models import Product

class ProductAPITests(APITestCase):
    def setUp(self):
        # Create users
        self.admin_user = User.objects.create_user('admin', password='adminpass', is_staff=True, is_superuser=True)
        self.staff_user = User.objects.create_user('staff', password='staffpass', is_staff=True)
        self.general_user = User.objects.create_user('user', password='userpass')

        # Create a test product
        self.product = Product.objects.create(name='Product 1', price=10.0, description='A test product', stock= 10)

    def authenticate(self, user):
        # Authenticate user using JWT token
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    # Test cases

    def test_admin_can_create_product(self):
        self.authenticate(self.admin_user)
        response = self.client.post('/api/v1/products/', {'name': 'New Product', 'price': 20.0, 'description': 'New test product', 'stock': 10})
        self.assertEqual(response.status_code, 200)

    def test_staff_can_create_product(self):
        self.authenticate(self.staff_user)
        response = self.client.post('/api/v1/products/', {'name': 'New Product', 'price': 20.0, 'description': 'New test product', 'stock': 10})
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_create_product(self):
        self.authenticate(self.general_user)
        response = self.client.post('/api/v1/products/', {'name': 'New Product', 'price': 20.0, 'description': 'New test product', 'stock': 10})
        self.assertEqual(response.status_code, 403)

    def test_anonymous_cannot_create_product(self):
        response = self.client.post('/api/v1/products/', {'name': 'New Product', 'price': 20.0, 'description': 'New test product', 'stock': 10})
        self.assertEqual(response.status_code, 401)
