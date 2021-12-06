from django.contrib import admin
from tweets.models import Tweet

#admin码差不多
@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    data_hierarchy = 'created_at'
    #表格列出来
    list_display = (
        'created_at',
        'user',
        'content',
    )
# Register your models here.
