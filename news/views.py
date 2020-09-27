from django.shortcuts import render, redirect
from .models import News, Comment, Image, ImageLink, PublicationDate, Links
from django.db.models import Q
from .vkapi import get_request
import re


def sort_news(request):
    """
    Сортирует новости: либо старые вверх, либо новые
    """
    news = News.objects.all().order_by('-id')
    old_news = News.objects.all().order_by('id')

    if request.GET['category'] == 'Сначала новые':
        news = news
    elif request.GET['category'] == 'Сначала старые':
        news = old_news

    return news


def handle_link(text, news):
    """
    Ищет ссылки в тексте и вносит их в базу данных, привязывая к нужной статье
    """
    urls = re.findall(r"(https?://[\w\S]+)", text)
    for link in urls:
        Links.objects.get_or_create(news=news, link=link)


def make_news_from_vk():
    """
    Создаёт в базе данных новости, полученные из API Vk
    """
    # Получаем новости через API
    vk_news_list = get_request()
    # Обрабатываем каждую новость и вносим в базу данных
    for news in vk_news_list:
        pub_date = news[0].strftime("%d.%m.%Y %H:%M")
        text = news[1]
        img_url = news[2]
        slug = f'vk_{img_url[-40:-17]}_{img_url[-12:-6]}'
        # Если такая новость уже есть, то ничего не делаем
        if len(News.objects.filter(slug=slug)):
            pass
        # Если такой новости нет, вносим в БД
        else:
            vk_news = News.objects.get_or_create(name='Новость из Вконтакте',
                                                 text=text,
                                                 slug=slug)
            ImageLink.objects.get_or_create(news=vk_news[0], img_url=img_url)
            PublicationDate.objects.get_or_create(news=vk_news[0], date=pub_date)
            handle_link(text=text, news=vk_news[0])


def main(request):
    """
    Главная страница новостей
    """
    # Получаем новости из Vk через API
    make_news_from_vk()

    # Если пользователь что-то ищет - выдаём ему новости по поиску.
    search = request.GET.get('search', '')
    if search:
        news = News.objects.filter(Q(name__icontains=search.lower()) | Q(text__icontains=search.lower()))
    # Если ничего не ищет, выдаём в обычном порядке
    else:
        news = News.objects.all().order_by('-from_self', '-id')

    # Получаем все новости, картинки и даты публикаций
    images = Image.objects.all()
    image_links = ImageLink.objects.all()
    pub_date = PublicationDate.objects.all()

    # Показываем новости по категории: новые или старые
    if request.method == 'GET' and 'category' in request.GET:
        news = sort_news(request=request)


    context = {
        'news': news,
        'images': images,
        'image_links': image_links,
        'pub_date': pub_date
    }

    return render(request, 'news/main.html', context)


def get_news_page(request, slug):
    """
    Отдельная страница для каждой новости
    """
    # Получаем новость, комментарии к ней, картинку, дату публикации и ссылки из текста
    news = News.objects.get(slug__iexact=slug)
    comments = Comment.objects.filter(
        news=news).order_by('-id')
    images = Image.objects.filter(news=news)
    image_links = ImageLink.objects.all()
    pub_date = PublicationDate.objects.all()
    links = Links.objects.all()

    context = {
        'news': news,
        'comments': comments,
        'product_image': images,
        'image_links': image_links,
        'pub_date': pub_date,
        'links': links
    }

    # Если пользователь оставляет комментарий, вносим его в БД и редиректим на эту страницу
    if request.method == "GET":
        if 'name' in request.GET and 'text' in request.GET:
            name = request.GET['name']
            text = request.GET['text']
            Comment.objects.create(news=news, commentator=name, text=text)
            return redirect(request.path)

    return render(request, 'news/news_page.html', context)



