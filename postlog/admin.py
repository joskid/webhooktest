from django.contrib import admin

from postlog.models import Thread, Post

class PostInline(admin.TabularInline):
    model = Post
    extra = 0

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'alias', 'client_ip', 'target_url')
    search_fields = ('alias', 'uuid')
    list_filter = ('created', )
    inlines = (PostInline, )
admin.site.register(Thread, ThreadAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('remote_ip', 'number')
    search_fields = ('thread__alias', 'thread__uuid')
    list_filter = ('created',)
admin.site.register(Post, PostAdmin)
