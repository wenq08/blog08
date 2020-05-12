from django.db import models
from django.contrib.auth.models import User 
from django.shortcuts import reverse
from blogpro.settings import base


import markdown
# Create your models here.


class BigCategory(models.Model):
    """大分类"""
    name = models.CharField(max_length=20, verbose_name='大分类')
    slug = models.SlugField(unique=True, verbose_name='编号')
    description = models.TextField(verbose_name='说明', max_length=200, default=base.SITE_DESCRIPTION)
    keyword = models.TextField(verbose_name='关键字', max_length=200, default=base.SITE_KEYWORD)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '大分类'
        verbose_name_plural = verbose_name
       
    def __str__(self):
        return self.name 


class Category(models.Model):
    """分类"""
    name = models.CharField(max_length=20, verbose_name='大分类')

    slug = models.SlugField(unique=True, verbose_name='编号')
    description = models.TextField(verbose_name='说明', max_length=200, default=base.SITE_DESCRIPTION)
    bigcategory = models.ForeignKey(BigCategory, verbose_name='大分类', on_delete=models.CASCADE)
    keyword = models.TextField(verbose_name='关键字', max_length=200, default=base.SITE_KEYWORD)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
       
    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

    def get_Article_list(self):
        return Article.objects.filter(category=self)


class Tag(models.Model):
    """标签"""
    name = models.CharField(max_length=20, verbose_name='标签')
    slug = models.SlugField(unique=True, verbose_name='编号')
    description = models.TextField(verbose_name='说明', max_length=200, default=base.SITE_DESCRIPTION)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['name']
       
    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'tag': self.name})

    def get_Article_list(self):
        """返回当前标签下所有发表的文章列表"""
        return Article.objects.filter(tags=self)


class KeyWord(models.Model):
    """关键词"""
    name = models.CharField(max_length=20, verbose_name='关键词')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name
        ordering = ['name']
       
    def __str__(self):
        return self.name 


class Article(models.Model):
    """文章"""
    IMG_LINK = '/image/'
    title = models.CharField(max_length=100, verbose_name='标题')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    description = models.TextField(max_length=300, verbose_name='摘要')
    body = models.TextField(verbose_name='文章内容')
    img_link = models.CharField('图片地址', default=IMG_LINK, max_length=255)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    views = models.IntegerField('阅览量', default=0)
    loves = models.IntegerField('喜爱量', default=0)
    slug = models.SlugField(unique=True, verbose_name='编号') # 用作文章的访问路径，每篇文章有独一无二的标识，下同
    category = models.ForeignKey(Category, verbose_name='文章分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    keywords = models.ManyToManyField(KeyWord, verbose_name='文章关键词', 
                                    help_text='文章关键词，用来作为SEO中keywords，最好使用长尾词，3-4个足够')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article', kwargs={'slug': self.slug})

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])


