from modeltranslation.translator import translator, TranslationOptions
from .models import *

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'country', 'active_components', 'purpose', 'skin_type', 'how_to_use')

class WhySkinBlogTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(WhySkinBlog, WhySkinBlogTranslationOptions)