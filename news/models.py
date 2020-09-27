from django.db import models
from django.shortcuts import reverse


class News(models.Model):
    """
    Модель новости
    """
    name = models.CharField(max_length=100, verbose_name='Название новости')
    text = models.TextField(verbose_name='Текст новости')
    slug = models.SlugField(max_length=150, unique=True, null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    from_self = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('news_page', kwargs={'slug': self.slug})


class PublicationDate(models.Model):
    """
    Модель даты публикации новости в Vk
    """
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=100, verbose_name='Дата публикации в Вк')

    def __str__(self):
        return f'{self.news}'


class Links(models.Model):
    """
    Модель ссылки, привязано к новости
    """
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True)
    link = models.URLField(verbose_name='Ссылка')

    def __str__(self):
        return f'{self.news}'


class Image(models.Model):
    """
    Модель картинки, загружаемой из админки
    """
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True)
    img = models.ImageField(default='no-image.png', upload_to='product_image')

    def __str__(self):
        return f'{self.news}'


class ImageLink(models.Model):
    """
    Модель ссылки на картинку, получаемой из Vk API
    """
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True)
    img_url = models.URLField(verbose_name='Ссылка на картинку')

    def __str__(self):
        return f'{self.news}'


class Comment(models.Model):
    """
    Модель комментариев к новости
    """
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True, verbose_name='Новость')
    commentator = models.CharField(max_length=100, verbose_name='Имя комментатора', null=True)
    text = models.TextField(null=True, verbose_name='Текст комментария')
    date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата комментария')

    def __str__(self):
        return f'{self.news}'