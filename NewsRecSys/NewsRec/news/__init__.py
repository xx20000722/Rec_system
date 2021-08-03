# -*-coding: utf-8 -*-
from django.apps import AppConfig

default_app_config = 'news.PrimaryIndexConfig'

class PrimaryIndexConfig(AppConfig):
    name = "news"
    verbose_name = u"新闻"