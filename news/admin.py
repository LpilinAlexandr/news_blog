from django.contrib import admin
from .models import News, Comment, Image, ImageLink, PublicationDate, Links

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(ImageLink)
admin.site.register(PublicationDate)
admin.site.register(Links)



