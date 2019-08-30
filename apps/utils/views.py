# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import commands
import datetime
import os

import subprocess as sub

from django.http import HttpResponse, FileResponse
from django.shortcuts import render

from ca_tassl.ca_tassl import ca_tassl

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your views here.
from rest_framework.utils import json


ca_tasslPath = os.getcwd() + "/apps/ca_tassl/public/"

def upload(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no file for upload!")

        destination = open(os.path.join(ca_tasslPath, myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()

        #解析csr判断结果
        csrout = commands.getstatusoutput('openssl_tassl req -noout -text -in '+ca_tasslPath+myFile.name)
        a = csrout[1].splitlines()

        certNum = 9

        if "rsaEncryption" in csrout[1]:
            certNum = 0
        elif "SM2" in csrout[1]:
            certNum = 1
        else:
            certNum = 2

        ca = ca_tassl()
        file_parse = ca.show_req_file(ca_tasslPath+myFile.name)
        print ('Path20 = ',file_parse[1])
        file_parse = file_parse[1].split('\n')
        file_parse = filter(lambda x: 'Subject:' in x, file_parse)
        file_parse = file_parse[0].split(',')
        file_parse_subject = {}
        for i in file_parse:
            t = i.split('=')
            m = i.replace(" ",'')
            if "C=" in m:
                file_parse_subject["countryCode"] = t[1].strip()
            elif "ST=" in m:
                file_parse_subject["province"] = t[1].strip()
            elif "L=" in m:
                file_parse_subject["city"] = t[1].strip()
            elif "O=" in m:
                file_parse_subject["organization"] = t[1].strip()
            elif "OU=" in m:
                file_parse_subject["organizationalUnit"] = t[1].strip()
            elif "CN=" in m:
                file_parse_subject["commonName"] = t[1].strip()

        file = open(ca_tasslPath+myFile.name,'rb')
        readcontent = file.read()
        file.close()

        context = {
            'flag':"Success",
            'csrfile':readcontent,
            'data': file_parse_subject,
            "num":certNum
            # 'path':myFile.name
        }
        return HttpResponse(json.dumps(context))


def sigin_cert(request):
    print "调用了"
    if request.method == "POST":
        body = json.loads(request.body)
        ca = ca_tassl()
        print body["num"]
        if body["num"]==0:
            ca.openssl_cmd = "/usr/bin/openssl"
        elif body["num"]==1:
            ca.openssl_cmd = "/usr/bin/openssl_sm2"
        elif body["num"] == 2:
            ca.openssl_cmd = "/usr/bin/openssl_ec"
        else:
            ca.openssl_cmd = "openssl_tassl"
        #如果是签名证书

        # if body['digestflag'] == false
        TEST_CLIENT_FILE=body['name']
        TEST_CLIENT_DN="/C={}/ST={}/L={}/O={}/OU={}/CN={}".format(body['countryCode'], body['province'], body['city'], body['organization'], body['organizationalUnit'], body['commonName'])

        timenow = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
        CURTIME = timenow.strftime('%y%m%d%H')

        CERTSTOTAL_DIR = os.getcwd() + "/apps/ca_tassl/userCerts"
        CERTS_DIR= CERTSTOTAL_DIR + "/" + TEST_CLIENT_FILE + "_" + CURTIME

        # 修改当前工作目录
        # os.chdir("./apps/ca_tassl/")

        #创建文件夹
        if os.path.exists(CERTS_DIR):
            # commands.getstatusoutput("rm -fr " + CERTS_DIR)
            import shutil
            shutil.rmtree(CERTS_DIR)

        os.mkdir(CERTS_DIR)

        outfile = CERTS_DIR + "/" + TEST_CLIENT_FILE + ".req.pem"
        keyout = CERTS_DIR + "/" + TEST_CLIENT_FILE + ".key.pem"
        if body.has_key("csrfile") and body["csrfile"] != '': #如果已经有csr文件则写入旧的
            with open(outfile,'w') as f:
                f.write(body["csrfile"])

        else:
            # 生成签名证书请求

            newkey = "SM2.pem"
            rv = ca.gen_cert_req(TEST_CLIENT_DN, keyout, newkey, outfile)

        reqfile = outfile


        #签署签名证书
        isca = False
        infile = reqfile
        extfile = ''
        cafile = "./caCerts/CA.cert.pem"
        cakeyfile = "./caCerts/CA.key.pem"
        outfile = CERTS_DIR + "/" + TEST_CLIENT_FILE + ".cert.pem"
        print ("目录修改成功 digestflag=%s" % body['digestflag'])
        extensions = "v3enc_req" if body['digestflag'] else "v3_req"

        rv = ca.sigin_cert( infile, None, cafile, cakeyfile, extensions, outfile)

        certfile = outfile
        keyfile = keyout

        # 显示签名证书
        rv = ca.show_cert(certfile)

        #签名证书合并
        outfile = CERTS_DIR + "/" + TEST_CLIENT_FILE +  ".pfx"
        rv = ca.common_file(certfile, keyfile, outfile)

        #压缩文件，下载文件
        ca_tasslPath =  "./apps/ca_tassl/userCerts/"
        output = commands.getstatusoutput("cd " + ca_tasslPath + ";" + "tar -zcf " + os.path.basename(CERTS_DIR) + ".tar " + os.path.basename(CERTS_DIR) + "; rm -fr " + os.path.basename(CERTS_DIR))

        context = {
            'flag':"Success",
            'file': os.path.basename(CERTS_DIR)+".tar",
        }
        return HttpResponse(json.dumps(context))



def download(request):

    file = os.getcwd() + "/apps/ca_tassl/userCerts/" + request.GET["0"]
    if os.path.exists(file):
        file=open(file,'rb')
        response =FileResponse(file)
        response['Content-Type']='application/octet-stream'
        response['Content-Disposition']='attachment;filename="' + request.GET["0"]
        return response