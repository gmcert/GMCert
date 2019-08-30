### <a href="#english">(Click here to view English README)</a>

## 关于 GMCert

![GMCert](https://github.com/gmcert/GMCert/image/raw/master/gmcert_640.jpg?raw=true "GMCert")

GMCert 是一个免费开源的SM2国密（以及RSA、ECC等）证书签发系统。您可以使用GMCert申请获得各种参数和格式的证书文件，并将该证书用于开发、测试、部署……等一切用途，没有任何限制。

在此之前，从事密码领域或其他信息安全行业的工作人员，想要签发一套指定密钥和参数的证书，需要自行搭建开源SSL或CA，研究学习签发命令或代码，自行生成根CA证书…… 将会遇到很多挑战且投入大量精力。有了GMCert，您需要做的只是点几下鼠标。
 
本工程基于django和vue.js框架.

## 关键服务功能

GMCert 提供多种证书服务内容和灵活参数设置：

* 通过CSR请求证书
* 在线生成密钥和证书
* 指定证书算法（国密/RSA/ECC）
* 支持生成国密签名证书或加密证书
* 指定证书扩展项
* 指定证书导出格式（PEM/DER/P12/JKS...）
* 指定HASH算法
* 支持生成PKCS7格式密码信封
* 选择指定CA或新建CA根证书
* 生成CRL证书吊销列表
* 查看证书、密钥、CSR、CRL等详情
* 提供常用证书工具
* 证书和密钥存储、托管
* CA/RA测试接口
* 用户登录后可保存和检索历史记录
* 提供国密SSL连接测试
* 提供自建CA技术支持
* ......

以上内容以及更多新功能会陆续推出。
  

## 关于 国密算法 与 国密证书

国密算法 是国家商用密码算法的简称。
自2012年以来，国家密码管理局以《中华人民共和国密码行业标准》的方式，陆续公布了SM2/SM3/SM4等密码算法标准及其应用规范。其中“SM”代表“商密”，即用于商用的、不涉及国家秘密的密码技术。其中SM2为基于椭圆曲线密码的公钥密码算法标准，包含数字签名、密钥交换和公钥加密，用于替换RSA/Diffie-Hellman/ECDSA/ECDH等国际算法；SM3为密码哈希算法，用于替代MD5/SHA-1/SHA-256等国际算法；SM4为分组密码，用于替代DES/AES等国际算法；SM9为基于身份的密码算法，可以替代基于数字证书的PKI/CA体系。
通过部署国密算法，可以降低由弱密码和错误实现带来的安全风险和部署PKI/CA带来的开销。
目前，国密算法已成为国际标准，并在OpenSSL 1.1.0开始支持。

国密证书 是使用国密算法进行公钥签名和HASH运算，并采用国密密钥封装的证书。国密证书同样符合X.509等国际标准证书规范。
在国内很多政企应用场景中，经常会使用“双国密证书”架构，即 每个节点同时部署两套证书：签名证书和加密证书。签名证书用于代表该节点身份，用于身份认证和对数据签名；加密证书用于交换密钥和对数据加密。



-----

#  <a name="english">English README</a>


GMCert is a open source system for providing free signing GM/RSA/ECC certificates. You can use this project to specify flexible parameters and generate multiple formats of certificates. 

This project based on django and vue.js.

Website: [www.gmcert.org](https://www.gmcert.org)
E-mail: [admin@gmcert.org](mailto:admin@gmcert.org)


