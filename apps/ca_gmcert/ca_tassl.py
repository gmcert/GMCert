
# -*- coding: utf-8 -*-
import os
import commands

ca_tasslPath = os.getcwd() + "/apps/ca_tassl/"

class ca_tassl(object):

    def __init__(self):
        self.openssl_cmd =  'openssl_tassl'
        self.openssl_cnf =  'openssl.cnf'
        self.days = 1500
        self.precommand = "cd " + ca_tasslPath + ";"

    # 生成CA
    def gen_seilf_signed_ca_cert(self, TEST_CA_CURVE):
        return  commands.getstatusoutput(self.precommand + self.openssl_cmd + " ecparam -name " + TEST_CA_CURVE + " -out " + ca_tasslPath+ TEST_CA_CURVE + ".pem")

    # 生成证书请求
    # 参数：配置文件、主题、输出密钥、新密钥、输出
    # 输出：请求证书结果
    def gen_cert_req(self, subj, keyout, newkey, outfile):

        #执行命令
        output = commands.getstatusoutput(self.precommand + self.openssl_cmd + " req -config " + self.openssl_cnf + " -nodes -subj \"" + subj + "\" -keyout " + keyout + " -newkey ec:" + newkey + " -new -out " + outfile)
        return  output


    # 解析证书请求
    # 参数： csrfile
    # 输出： 查看证书请求结果
    def show_req_file(self, csrfile):

        #执行命令
        output = commands.getstatusoutput(self.precommand + self.openssl_cmd + " req -in " + csrfile + " -noout -text ")
        return  output

    # 签署证书请求
    # 参数： isca ：是否是签署ca
    #       infile ： 输入请求文件
    #       signkey : 签名密钥
    #       CA ： 输入ca文件
    #       CAKey ： 输入cakey文件
    #       outfile ： 输出文件
    # 输出：签署证书结果
    def sigin_cert(self, infile, signkey , ca, cakey, extensions,outfile):

        if extensions == 'v3_ca':
            #执行命令
            output = commands.getstatusoutput(self.precommand + self.openssl_cmd + " x509 -req -days " + str(self.days) + " -in " + infile + " -extfile " + self.openssl_cnf + " -extensions v3_ca -signkey " + signkey + " -out " + outfile)
        else:
            #执行命令
            output = commands.getstatusoutput(self.precommand + self.openssl_cmd + " x509 -req -days " + str(self.days) + " -in " + infile + " -CA " + ca + " -CAkey " + cakey + " -extfile " + self.openssl_cnf + " -extensions "+ extensions + " -out " + outfile)

        return  output


    # 证书显示
    def show_cert(self, certfile):
        #执行命令
        output = commands.getstatusoutput(self.precommand + self.openssl_cmd + " x509 -in " + certfile + " -text")
        return  output


    # 合并证书和密钥
    def common_file(self, certfile, keyfile, outfile):
        #执行命令
        output = commands.getstatusoutput(self.precommand + self.openssl_cmd + " x509 -in " + certfile + " -issuer -subject > " + outfile)
        output += commands.getstatusoutput(self.precommand + "/bin/cat " + keyfile + " >> " + outfile)
        return  output

    # 删除请求证书
    def remove_file(self, file):
        output = commands.getstatusoutput(self.precommand + "/bin/rm " +file)
        return output











