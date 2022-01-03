from django.contrib import admin
from tweets.models import Tweet, TweetPhoto


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
@admin.register(TweetPhoto)
class TweetPhotoAdmin(admin.ModelAdmin):
    list_display = (
        'tweet',
        'user',
        'file',
        'status',
        'has_deleted',
        'created_at',
    )
    list_filter = ('status', 'has_deleted')
    date_hierarchy = 'created_at'