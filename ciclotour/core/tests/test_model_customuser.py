import os

from ciclotour.core.models.custom_user import CustomUser, _user_profile_directory_path, CustomUserManager
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings


class CustomUserModelTest(TestCase):
    @override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
    def setUp(self):
        TINY_GIF = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;'
        profile_picture = SimpleUploadedFile('test.jpg', TINY_GIF)

        self.user = CustomUser.objects.create(
            name='Guilherme',
            last_name='Hübner',
            email='guilherme_hubner@msn.com',
            password='123456',
            profile_picture=profile_picture
        )

    def test_create(self):
        self.assertTrue(CustomUser.objects.exists())

    def test_user_directory_path(self):
        self.assertEqual(_user_profile_directory_path(self.user, 'test.png'),
                         'users_profile/user_{}/profile.png'.format(self.user.email))

    def test_required_fields(self):
        required_fields = ['email', 'name', 'last_name']

        with self.subTest():
            for field in required_fields:
                field = CustomUser._meta.get_field(field)
                self.assertFalse(field.blank and field.null)

    def test_email_unique(self):
        field = CustomUser._meta.get_field('email')
        self.assertTrue(field.unique)

    def test_profile_picture(self):
        self.assertEqual(self.user.profile_picture.path,
                         '{}/users_profile/user_{}/profile.jpg'.format(settings.MEDIA_ROOT,
                                                                       self.user.email))

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'Guilherme Hübner')

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), 'Guilherme')

    def test_str(self):
        self.assertEqual(str(self.user), 'Guilherme Hübner')

class CustomUserManagerTest(TestCase):
    def setUp(self):
        self.regular_user = CustomUser.objects.create_user(
            name='Guilherme',
            last_name='Hübner',
            email='guilherme_hubner@msn.com',
            password='123456'
        )
        self.super_user = CustomUser.objects.create_superuser(
            name='Guilherme',
            last_name='Hübner',
            email='guilherme_hubner@immortalopus.com',
            password='123456'
        )

    def test_manager(self):
        self.assertIsInstance(CustomUser.objects, CustomUserManager)

    def test_create_user(self):
        self.assertFalse(self.regular_user.is_staff or self.regular_user.is_superuser)

    def test_create_superuser(self):
        self.assertTrue(self.super_user.is_staff and self.super_user.is_superuser)
