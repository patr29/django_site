# -*- coding:UTF-8 -*-

from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
class tags(models.Model):
    tag = models.CharField(max_length=100, unique = True)
    def __unicode__(self):
        return self.tag
    class Meta:
        verbose_name_plural = "tags"

class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name = u'Имя катогории', unique = True)
    OnTop = models.BooleanField(verbose_name = u'Показывать на главной')
    url = models.CharField(max_length=250, verbose_name = u'url суффикс для категории', unique = True)
    def __unicode__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name = u'Имя пользователя')
    date = models.DateTimeField(auto_now_add=True, verbose_name = u'Дата комментария')
    text = models.TextField(verbose_name = u'Текст комментария')

class content(models.Model):
    title = models.CharField(max_length=30, verbose_name = u'Заголовок')
    preview = models.TextField(unique = True, verbose_name = u'Превью', blank = True)
    text = models.TextField(unique = True, verbose_name = u'Текст')
    tags = models.ManyToManyField('tags', verbose_name = u'Теги')
    description = models.CharField(blank=True, max_length=250, verbose_name = u'Тег описания записи')
    category = models.ForeignKey(Category, verbose_name = u'Категория')
    date = models.DateTimeField(auto_now_add=True, verbose_name = u'Дата публикации')
    comment = models.ManyToManyField(Comment, blank = True, verbose_name = u'Комментарии')
    published = models.BooleanField(default = False, verbose_name = u'Публикация')
    def get_absolute_url(self):
        return "/%s/" % self.title
    class Meta:
        verbose_name_plural = u'контент'
        verbose_name = u'контент'

class site_setting(models.Model):
    title = models.CharField(max_length = 250)
    description = models.CharField(max_length = 200)
    url = models.CharField(max_length = 250)

class Login_form(forms.Form):
    username = forms.CharField(label = u'Логин')
    password = forms.CharField(label = u'Пароль', widget = forms.PasswordInput)
    OpenID = forms.CharField(label = u'или OpenID')

class Comment_form(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label = u'Текст комментария')




class AuthForm(forms.Form): 
    username = forms.CharField(label = u'Логин', required = False)
    password = forms.CharField(label = u'Пароль', widget = forms.PasswordInput, required = False)
    openid_url = forms.CharField(label='OpenID', max_length=200, required = False)

    def __init__(self, session, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        self.session = session

    def clean(self):
        if self.data['openid_url'].count('') > 1 and self.data['username'].count('') == 1:
            from tst.main.openidbase import create_request, OpenIdError, absolute_url
            try:
                self.request = create_request(self.cleaned_data['openid_url'], self.session)
            except OpenIdError, e:
                raise ValidationError(e)
            return self.cleaned_data['openid_url']
        else:
            if self.data['username'].count('') and self.data['password'].count('') > 1:
                return self.cleaned_data['username'] and self.cleaned_data['password']
            raise forms.ValidationError('Не верно введены данные')

    def auth_redirect(self, target, view_name, acquire=None, args=[], kwargs={}):
        trust_url = 'http://'+view_name
        return_to = 'http://'+view_name+'/loginopenid'
        self.request.return_to_args['redirect'] = target
        if acquire:
            self.request.return_to_args['acquire_article'] = str(acquire.id)
        return self.request.redirectURL(trust_url, return_to)
