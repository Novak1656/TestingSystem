from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils.timezone import now
from django_unique_slugify import slugify, unique_slugify
from unidecode import unidecode


def question_image_path(instance, filename):
    return f'img/{instance.test}/questions_img/{filename}'


class Category(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=255,
        unique=True
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлен',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Категория теста'
        verbose_name_plural = 'Категории тестов'
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(unidecode(self.title))
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=255,
        unique=True
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлен',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Тег теста'
        verbose_name_plural = 'Теги тестов'
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(unidecode(self.title))
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class TestAnswers(models.Model):
    question = models.ForeignKey(
        verbose_name='Вопрос',
        to='TestQuestions',
        on_delete=models.CASCADE,
        related_name='answers'
    )
    answer = models.TextField(
        verbose_name='Ответ'
    )
    is_right = models.BooleanField(
        verbose_name='Правильный',
        default=False
    )

    class Meta:
        verbose_name = 'Ответ теста'
        verbose_name_plural = 'Ответы тестов'

    def __str__(self):
        return f'Answer #{self.pk}'


class TestQuestions(models.Model):
    ANSWERS_TYPES = [('Expanded', 'Развёрнутый ответ'), ('Variable', 'С вариантами ответа')]

    test = models.ForeignKey(
        verbose_name='Тест',
        to='Test',
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question = models.TextField(
        verbose_name='Вопрос',
        max_length=500
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=question_image_path,
        blank=True,
        null=True
    )
    answers_type = models.CharField(
        verbose_name='Тип ответа',
        max_length=255,
        choices=ANSWERS_TYPES,
        default='Variable'
    )

    class Meta:
        verbose_name = 'Вопрос теста'
        verbose_name_plural = 'Вопросы тестов'

    def __str__(self):
        return f'{self.test} quest: #{self.pk}'


class Test(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    author = models.ForeignKey(
        verbose_name='Автор',
        to='users_app.User',
        on_delete=models.CASCADE,
        related_name='tests'
    )
    category = models.ForeignKey(
        verbose_name='Категория',
        to=Category,
        on_delete=models.CASCADE,
        related_name='tests'
    )
    tags = models.ManyToManyField(
        verbose_name='Теги',
        to=Tag,
        related_name='tests',
        blank=True,
    )
    passed_times = models.PositiveIntegerField(
        verbose_name='Раз пройдено',
        default=0
    )
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=False
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    published_at = models.DateTimeField(
        verbose_name='Дата публикации',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, slugify(unidecode(self.title)))
        if self.is_published:
            self.published_at = now()
        super(Test, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class TestResults(models.Model):
    test = models.ForeignKey(
        verbose_name='Тест',
        to=Test,
        on_delete=models.CASCADE,
        related_name='results'
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='users_app.User',
        on_delete=models.CASCADE,
        related_name='results'
    )
    score = models.PositiveIntegerField(
        verbose_name='Результат',
        validators=[MaxLengthValidator(100), MinLengthValidator(0)]
    )
    right_answers = models.ManyToManyField(
        verbose_name='Правильные ответы',
        to=TestQuestions,
        related_name='results'
    )
    completed_at = models.DateTimeField(
        verbose_name='Пройден',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'
        ordering = ['-completed_at']

    def __str__(self):
        return f'{self.user}: Test-{self.test}'
