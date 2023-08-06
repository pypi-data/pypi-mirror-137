# -*- coding: utf-8 -*-

"""
@Remark:登录视图
"""
import base64
import hashlib
import json
import logging
import traceback
import uuid

import requests
from captcha.views import CaptchaStore, captcha_image
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import SessionAuthentication
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_xml.parsers import XMLParser
from weixin import WXAPPAPI
from weixin.oauth2 import OAuth2AuthExchangeError
from xdj_utils.json_response import SuccessResponse, ErrorResponse, DetailResponse
from xdj_utils.serializers import CustomModelSerializer
from xdj_utils.viewset import CustomModelViewSet

from .models import OAuthModel, AuthCodeModel

logger = logging.getLogger('django')

user_model = get_user_model()


class CaptchaView(APIView):
    authentication_classes = []

    @swagger_auto_schema(
        responses={
            '200': openapi.Response('获取成功')
        },
        security=[],
        operation_id='captcha-get',
        operation_description='验证码获取',
    )
    def get(self, request):
        hashkey = CaptchaStore.generate_key()
        id = CaptchaStore.objects.filter(hashkey=hashkey).first().id
        imgage = captcha_image(request, hashkey)
        # 将图片转换为base64
        image_base = base64.b64encode(imgage.content)
        json_data = {"key": id, "image_base": "data:image/png;base64," + image_base.decode('utf-8')}
        return SuccessResponse(data=json_data)


class AuthTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(AuthTokenSerializer, cls).get_token(user)
        token['username'] = 'wx_{0}'.format(user.username)
        return token


class AuthSerializer(CustomModelSerializer):
    class Meta:
        model = OAuthModel
        fields = "__all__"


class AnonThrottle(AnonRateThrottle):
    THROTTLE_RATES = {'anon':'2/s'}
    scope = 'anon'


class UserThrottle(UserRateThrottle):
    THROTTLE_RATES = {'user':'2/m'}
    scope = 'user'


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class TextXMLParser(XMLParser):
    media_type = 'text/xml'


class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

import time
class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)


class BaseAuthViewSet(CustomModelViewSet):
    parser_classes = tuple(list(api_settings.DEFAULT_PARSER_CLASSES) + [TextXMLParser])
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = []
    throttle_classes = [AnonThrottle, UserRateThrottle]
    serializer_class = AuthSerializer
    queryset = OAuthModel.objects.all()


    @staticmethod
    def get_user_info(user):
        result = CustomModelViewSet.get_user_info(user)
        refresh = AuthTokenSerializer.get_token(user)
        result['refresh'] = str(refresh)
        result['access'] = str(refresh.access_token)
        return result

    def code(self,request):
        pass

    def auth(self,request):
        pass


class WXMiniAuthViewSet(BaseAuthViewSet):

    def auth(self, request):
        code = request.data.get('code',None)

        if code is None:
            return ErrorResponse(msg="code为空")

        api = WXAPPAPI(appid=settings.WX_APP_ID, app_secret=settings.WX_APP_SECRET)
        try:
            session_info = api.exchange_code_for_session_key(code=code)
        except OAuth2AuthExchangeError:
            pass
        else:
            openid = session_info.get('openid', None)
            if openid is None:
                return ErrorResponse(msg="openid获取失败")

            auth, created_ = OAuthModel.objects.get_or_create(openid=openid, type=1)
            user, created = user_model.objects.get_or_create(auth=auth)
            if user:
                return DetailResponse(self.get_user_info(user), status=HTTP_200_OK)


        return ErrorResponse(None,msg="微信小程序验证失败", status=HTTP_204_NO_CONTENT)


class WXAcAuthViewSet(BaseAuthViewSet):

    #认证
    def auth(self, request):
        code = request.data.get('code',None)

        if code is None:
            return ErrorResponse(msg="code为空")

        try:acode = AuthCodeModel.objects.get(code=code)
        except AuthCodeModel.DoesNotExist:return ErrorResponse(msg=f'还没有acode:{code}')
        else:
            if acode.auth is None:return DetailResponse(msg='等待扫码中')
            user = acode.auth.user
            if user is None:
                user = user_model()
                user.save()
                acode.auth.user = user
                acode.auth.save()
            acode.delete()
            cache.set(self.get_ident(request),'')
            return DetailResponse(self.get_user_info(user),status=HTTP_200_OK)




    #发验证码
    def code(self,request):
        expire = 2 * 60 * 60
        code_ = str(uuid.uuid4())
        create = False
        ident = self.get_ident(request)
        if cache.has_key(ident) and cache.get(ident) != '':
            res = cache.get(ident)
            res = json.loads(res)
        else:
            while create is False:
                auth, create = AuthCodeModel.objects.get_or_create(code=code_, expire=expire)
                if create is False:
                    code_ = str(uuid.uuid4())
                else:
                    auth.ident = ident
                    auth.save()
            ticket = self.get_qr_ticket(auth.code, expire)
            url = f"https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}"
            res = {
                "code": auth.code,
                "ticket": ticket,
                "url": url,
                "expire":expire,
                "create_datetime": auth.create_datetime.timestamp()
            }
            cache.set(ident,json.dumps(res),expire - 1)
        return DetailResponse(res)

    #微信配置，get请求
    def auth_check(self,request):
        wechat_data = request.GET


        if not self.wx_ac_match(wechat_data):
            return HttpResponse("")

        if request.method.upper() == 'GET':
            echostr = wechat_data['echostr']
            return HttpResponse(echostr)

        parser = self.parse_xml(request)
        print('auth_check:parser:',parser)
        if parser.get('MsgType', '') != 'event':
            return HttpResponse(self.autoreply(request))

        if parser.get('Event', '') == 'SCAN' or parser.get('Event','') == 'subscribe':
            code = parser.get('EventKey','qrscene_')
            code = code.lstrip('qrscene_')
            try:
                acode = AuthCodeModel.objects.get(code=code)
            except AuthCodeModel.DoesNotExist:
                raise Exception(f'微信扫码后，acode不存在，code为：{code}')
            else:
                openid = parser.get('FromUserName',None)
                auth,created = OAuthModel.objects.get_or_create(openid=openid,type=1)
                if auth.user is None:
                    user = user_model()
                    user.save()
                    auth.user = user
                    auth.save()
                acode.auth = auth
                acode.save()
            return HttpResponse(TextMsg(parser.get('FromUserName'), parser.get('ToUserName'), '').send())

        return HttpResponse(TextMsg(parser.get('FromUserName'), parser.get('ToUserName'), '...').send())


    def wx_ac_match(self,wechat_data):
        signature = wechat_data['signature']
        timestamp = wechat_data['timestamp']
        nonce = wechat_data['nonce']
        token = settings.WX_AC_TOKEN

        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        sha1.update(''.join(list).encode('utf-8'))
        hashcode = sha1.hexdigest()
        return hashcode == signature

    def parse_xml(self,request):
        import xml.etree.ElementTree as ET
        data = {}
        try:
            webData = request.body
            print('parse_xml:webData:',webData)
            xmlData = ET.fromstring(webData)
            data.setdefault('ToUserName',xmlData.find('ToUserName'))
            data.setdefault('FromUserName',xmlData.find('FromUserName'))
            data.setdefault('CreateTime',xmlData.find('CreateTime'))
            data.setdefault('MsgType',xmlData.find('MsgType'))
            data.setdefault('Event',xmlData.find('Event'))
            data.setdefault('EventKey',xmlData.find('EventKey'))
            data.setdefault('Ticket',xmlData.find('Ticket'))
            data.setdefault('MsgId',xmlData.find('MsgId'))
            data.setdefault('Content',xmlData.find('Content'))
            res = {}
            for k,v in data.items():
                v = v.text if v is not None else ''
                v = v.replace('\n','') if v is not None else ''
                v = v.strip()
                res.setdefault(k,v)

        except Exception:
            res = {}
            traceback.print_exc()
        return res

    def autoreply(self, request):
        import xml.etree.ElementTree as ET
        try:
            webData = request.body
            xmlData = ET.fromstring(webData)

            msg_type = xmlData.find('MsgType').text
            ToUserName = xmlData.find('ToUserName').text
            FromUserName = xmlData.find('FromUserName').text
            CreateTime = xmlData.find('CreateTime').text
            MsgType = xmlData.find('MsgType').text
            MsgId = xmlData.find('MsgId').text

            toUser = FromUserName
            fromUser = ToUserName

            if msg_type == 'text':
                content = "您好,欢迎来到Innobase!"
                replyMsg = TextMsg(toUser, fromUser, content)
                return replyMsg.send()

            elif msg_type == 'image':
                content = "图片已收到,谢谢"
                replyMsg = TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            elif msg_type == 'voice':
                content = "语音已收到,谢谢"
                replyMsg = TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            elif msg_type == 'video':
                content = "视频已收到,谢谢"
                replyMsg = TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            elif msg_type == 'shortvideo':
                content = "小视频已收到,谢谢"
                replyMsg = TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            elif msg_type == 'location':
                content = "位置已收到,谢谢"
                replyMsg = TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            elif msg_type == 'link':
                content = "链接已收到,谢谢"
                replyMsg = TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                replyMsg = TextMsg(toUser, fromUser, f'其他类型:{MsgType}')
                return replyMsg.send()

        except Exception as Argment:
            return "出错了"

    def get_access_token(self):
        access_token = ''
        try:
            if cache.has_key('access_token') and cache.get('access_token') != '':
                access_token = cache.get('access_token')
                logger.critical('cache access_token:' + access_token)
            else:
                appId = "wx28118b45eede9c27"
                appSecret = "cc1ccdf7116681162f1c835c7ae95a09"
                postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
                appId, appSecret))
                logger.debug(postUrl)
                urlResp = requests.get(url=postUrl)
                urlResp = json.loads(urlResp.text)
                access_token = urlResp.get('access_token',None)
                cache.set('access_token', access_token, 1.5 * 60 * 60)#1.5小时
        except Exception as e:
            traceback.print_exc()
        return access_token

    def get_qr_ticket(self,code,expire):
        ticket = ''
        try:
            #         if cache.has_key('ticket') and cache.get('ticket') != '':
            #             ticket = cache.get('ticket')
            #             logging.critical('cache ticket:'+ticket)
            #         else:
            token = self.get_access_token()
            logger.critical(f'code:{code}, ticket:{token}')
            data = {
                'expire_seconds': expire,
                'action_name': 'QR_STR_SCENE',
                'action_info': {
                    'scene': {
                        'scene_str': code
                    }
                }}

            import requests as reqs
            params = json.dumps(data)
            # params = urllib.parse.urlencode(data).encode(encoding='UTF8')
            # headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json'}
            if token != '':
                ticket_url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={}".format(token)
                response = reqs.post(url=ticket_url, data=params)
                # response = reqs.urlopen(req).read()
                # get_qr_ticket = urllib.urlopen(ticket_url)
                # urlResp = get_qr_ticket.read().decode("utf-8")
                logger.critical(response.content)
                js_ticket = json.loads(response.content)
                ticket = js_ticket.get("ticket")
                # cache.set('ticket', ticket, 60 * 100)
            # r.setex('wx:ticket', ticket, 7200)
        except Exception as e:
            return ''
        return ticket

    def get_ident(self, request):
        """
        Identify the machine making the request by parsing HTTP_X_FORWARDED_FOR
        if present and number of proxies is > 0. If not use all of
        HTTP_X_FORWARDED_FOR if it is available, if not use REMOTE_ADDR.
        """
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        remote_addr = request.META.get('REMOTE_ADDR')
        num_proxies = api_settings.NUM_PROXIES

        if num_proxies is not None:
            if num_proxies == 0 or xff is None:
                return remote_addr
            addrs = xff.split(',')
            client_addr = addrs[-min(num_proxies, len(addrs))]
            return client_addr.strip()
        ident = (''.join(xff.split()) if xff else remote_addr)
        return ident

class BasicAuthViewSet(BaseAuthViewSet):
    def auth(self,request):
        username = request.data.get('username',None)
        password = request.data.get('password',None)

        if username is None or password is None:
            return ErrorResponse(msg="用户名或密码为空")

        user = user_model.objects.filter(username=username).first()
        if user and user.check_password(password):  # check_password() 对明文进行加密,并验证
            result = self.get_user_info(user)
        else:
            result = {
                "code": 4000,
                "msg": "账号/密码不正确",
                "data": None
            }
        return result