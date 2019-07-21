# -- coding: utf-8 --
import rsa

(publickey,privatekey) = rsa.newkeys(1000)
pub = publickey.save_pkcs1()  # 获取公钥
# ...将公钥保存到本地...
filepub = open("public.pem", "w")
filepub.write(pub.encode('utf-8'))
filepub.close()

pri = privatekey.save_pkcs1()  # 获取私钥
# .....将私钥保存到本地...
filepri = open("private.pem", "w")
filepri.write(pri.encode("utf-8"))
filepri.close()

string = "ControllerA123"  # 待加密的字符串

# 取出公钥
with open("public.pem", "r") as file_pub:
    f_pub = file_pub.read()
    pubkey = rsa.PublicKey.load_pkcs1(f_pub)


# 取出私钥
with open("private.pem", "r") as file_pri:
    f_pri = file_pri.read()
    prikey = rsa.PrivateKey.load_pkcs1(f_pri)

# 使用公钥加密
crpt = rsa.encrypt(string.encode('utf-8'), pubkey)


# 使用私钥解密
de_crpt = rsa.decrypt(crpt, prikey)
