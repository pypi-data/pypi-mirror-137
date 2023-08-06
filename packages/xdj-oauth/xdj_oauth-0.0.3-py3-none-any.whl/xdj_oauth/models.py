from django.db import models

from xdj_utils.models import CoreModel, table_prefix
from django.conf import settings

class OAuthModel(CoreModel):
    types = (
        (1,'weixin'),
        (3,'qq'),
        (4,'weibo'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='auth',on_delete=models.CASCADE,verbose_name='用户资料', help_text="用户资料",blank=True,null=True)
    openid = models.CharField(max_length=100, default='',verbose_name='授权opeind', help_text="授权opeind",blank=True,null=True)
    type = models.IntegerField(choices=types,verbose_name='认证类型', help_text="认证类型",blank=True,null=True)

    class Meta:
        db_table = table_prefix + 'auth'
        verbose_name = '认证表'
        verbose_name_plural = verbose_name
        ordering = ('user',)


class AuthCodeModel(CoreModel):
    code = models.CharField(max_length=100, default='',verbose_name='验证code', help_text="验证code",blank=True,null=True)
    ident = models.CharField(max_length=100, default='',verbose_name='请求者身份', help_text="请求者身份",blank=True,null=True)
    expire = models.IntegerField(default=0,verbose_name="过期时间",help_text="过期时间(秒)",blank=True,null=True)
    auth = models.ForeignKey('xdj_oauth.OAuthModel',related_name='auth_code',on_delete=models.SET_NULL ,verbose_name='认证模型', help_text="认证模型",blank=True,null=True)

    class Meta:
        db_table = table_prefix + 'auth_code'
        verbose_name = '认证验证表'
        verbose_name_plural = verbose_name
        ordering = ('code',)