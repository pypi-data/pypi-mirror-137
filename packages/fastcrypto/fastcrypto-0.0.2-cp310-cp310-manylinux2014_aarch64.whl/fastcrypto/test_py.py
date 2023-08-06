# -*- coding: utf-8 -*-
import sys
#from fastcrypto import fastcrypto
import fastcrypto

data = bytes([125,2,3,4])
#,key,iv  length must 16
key = bytes([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
iv = bytes([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

ret = fastcrypto.aes_encode(data,key,iv)
print(ret)
if ret[0] == 0:
    crypt_data = ret[1]
    ret = fastcrypto.aes_decode(crypt_data,key,iv)
    print(ret)
