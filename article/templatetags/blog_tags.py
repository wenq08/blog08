# import sys
# sys.path.append('../')
from django import template
from ..models import BigCategory, Category

register = template.Library() # 注册自定义的过滤器与标签

@register.simple_tag
def get_BigCategory_list():
    """"返回大分类列表"""
    return BigCategory.objects.all()
    
@register.simple_tag
def get_Category_list(id):
    """返回分类"""
    return Category.objects.filter(big_category=id)