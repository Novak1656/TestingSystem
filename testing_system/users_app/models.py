from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    SECRET_WORD_TYPES = [
        ('Hometown', 'Родной город'),
        ('PetName', 'Имя домашнего питомца'),
        ('ChildDream', 'Кем вы хотели стать в детстве'),
        ('Hobby', 'Ваше хобби')
    ]

    type_secret_word = models.CharField(
        verbose_name='Тип секретного слова',
        choices=SECRET_WORD_TYPES,
        max_length=255,
        blank=True,
        null=True
    )
    secret_word = models.CharField(
        verbose_name='Секретное слово',
        max_length=255,
        blank=True,
        null=True
    )
    is_moder = models.BooleanField(
        verbose_name='Модератор',
        default=False
    )
