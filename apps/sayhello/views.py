# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import commands
import datetime
import os

from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_filters import rest_framework as filters
from rest_framework import viewsets

from ca_tassl.ca_tassl import ca_tassl
from .serializers import UserSerializer, GroupSerializer

cwd = os.getcwd()

class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'email', ]

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = UserFilter

class GroupViewSet(viewsets.ModelViewSet):
    """
    允许组查看或编辑的API路径。
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

def sayHello(request):
    ca = ca_tassl()

    os.chdir(cwd + "/apps/ca_tassl/")

    TEST_CLIENT_FILE="104@192.168.1.9"
    TEST_CLIENT_DN="/C=CN/ST=BJ/L=HaiDian/O=SSL TEST ORG/OU=DEV UNIT/CN=" + TEST_CLIENT_FILE
    TEST_CLIENT_ENC_FILE=TEST_CLIENT_FILE + "_enc"
    TEST_CLIENT_ENC_DN="/C=CN/ST=BJ/L=HaiDian/O=SSL TEST ORG/OU=DEV UNIT/CN=" + TEST_CLIENT_ENC_FILE

    timenow = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    CURTIME = timenow.strftime('%y%m%d%H')


    CERTSTOTAL_DIR = "./userCerts"
    CERTS_DIR= CERTSTOTAL_DIR + "/" + TEST_CLIENT_FILE + "_" + CURTIME

    #创建文件夹
    if os.path.exists(CERTS_DIR):
        # commands.getstatusoutput("rm -fr " + CERTS_DIR)
        import shutil
        shutil.rmtree(CERTS_DIR)

    os.mkdir(CERTS_DIR)

    # 生成签名证书请求
    keyout = CERTS_DIR + "/" + TEST_CLIENT_FILE + ".key.pem"
    newkey = "SM2.pem"
    outfile = CERTS_DIR + "/" + TEST_CLIENT_FILE + ".req.pem"
    rv = ca.gen_cert_req(TEST_CLIENT_DN, keyout, newkey, outfile)
    reqfile = outfile

    #签署签名证书
    isca = False
    infile = reqfile
    extfile = ''
    cafile = "./caCerts/CA.cert.pem"
    cakeyfile = "./caCerts/CA.key.pem"
    outfile = CERTS_DIR + "/" + TEST_CLIENT_FILE + ".cert.pem"
    extensions = "v3_req"
    rv = ca.sigin_cert( infile, None, cafile, cakeyfile, extensions, outfile)

    certfile = outfile
    keyfile = keyout

    # 显示签名证书
    rv = ca.show_cert(certfile)

    #签名证书合并
    outfile = CERTS_DIR + "/" + TEST_CLIENT_FILE +  ".pfx"
    rv = ca.common_file(certfile, keyfile, outfile)

    # 删除签名证书请求文件
    #rv = ca.remove_file(reqfile)
    rv = ca.show_req_file(reqfile)

    # 生成加密证书请求
    keyout = CERTS_DIR + "/" + TEST_CLIENT_ENC_FILE + ".key.pem"
    newkey = "SM2.pem"
    outfile = CERTS_DIR + "/" + TEST_CLIENT_ENC_FILE + ".req.pem"
    rv = ca.gen_cert_req(TEST_CLIENT_ENC_DN, keyout, newkey, outfile)
    reqfile = outfile

    #签署加密证书
    isca = False
    infile = reqfile
    extfile = ''
    cafile = "./caCerts/CA.cert.pem"
    cakeyfile = "./caCerts/CA.key.pem"
    outfile = CERTS_DIR + "/" + TEST_CLIENT_ENC_FILE + ".cert.pem"
    extensions = "v3_req"
    rv = ca.sigin_cert( infile, None, cafile, cakeyfile, extensions, outfile)

    certfile = outfile
    keyfile = keyout

    # 显示加密证书
    rv = ca.show_cert(certfile)

    # 加密证书合并
    outfile = CERTS_DIR + "/" + TEST_CLIENT_ENC_FILE +  ".pfx"
    rv = ca.common_file(certfile, keyfile, outfile)

    # 删除加密证书请求文件
    #rv = ca.remove_file(reqfile)
    rv = ca.show_req_file(reqfile)

    s = 'Hello World!'
    current_time = datetime.datetime.now()
    html = '<html><head></head><body><h1> %s 圣诞快乐减肥</h1><p> %s </p></body></html>' % (s, current_time)
    return HttpResponse(html)