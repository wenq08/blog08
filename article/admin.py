from django.contrib import admin
from .models import Article, Tag, KeyWord, BigCategory, Category
# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
   
    list_display = ('id', 'title', 'author', 'category', 'create_date', 'update_date')  # 要展示的字段
   
    list_display_links = ('title', 'category')  # 配置作为链接的字段

    fields = ('title', 'author', 'description', 'body', 'img_link', 'slug', 'category', 'tags', 'keywords') # 控制创建、编辑页面出现的字段

    list_filter = ('author', 'category') # 配置页面过滤器

    search_fields = ('title', 'author') # 配置搜索字段

    list_per_page = 50  # 控制每页显示的对象数量，默认是100

    filter_horizontal = ('tags', 'keywords')  # 给多选增加一个左右添加的框

    # 限制用户权限
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(ArticleAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date')
