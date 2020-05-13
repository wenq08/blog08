from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article

# Create your views here.
class IndexView(ListView):
    """主页视图"""
    # 获取数据库中文章列表
    model = Article
    # template_name指定模板
    template_name = 'Index.html'
    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'articles'

    def get_queryset(self, **kwargs):
        # 重写get_queryset来个性化定制数据
        queryset = super(IndexView, self).get_queryset()

