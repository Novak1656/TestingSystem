from django.test import TestCase
from ..models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.model_meta = User._meta

    def test_type_secret_word_field(self):
        field = self.model_meta.get_field('type_secret_word')
        self.assertEqual(field.verbose_name, 'Тип секретного слова')
        self.assertEqual(field.max_length, 255)
        field_choices = [('Hometown', 'Родной город'), ('PetName', 'Имя домашнего питомца'),
                         ('ChildDream', 'Кем вы хотели стать в детстве'), ('Hobby', 'Ваше хобби')]
        self.assertEqual(field.choices, field_choices)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_secret_word_field(self):
        field = self.model_meta.get_field('secret_word')
        self.assertEqual(field.verbose_name, 'Секретное слово')
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_is_moder_field(self):
        field = self.model_meta.get_field('is_moder')
        self.assertEqual(field.verbose_name, 'Модератор')
        self.assertFalse(field.default)
