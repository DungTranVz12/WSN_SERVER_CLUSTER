import __init
from Library.C5_RsaEncrypt.rsa_Wrap import RSA_Class

#1. Create RSA object
RSA = RSA_Class(privateKeyPath="Library/C5_RsaEncrypt/Example/key_private.pem")
ENCRYPT_DATA = b'f9\x16v\xf0Yi}\x04\x9b\x9b\xdfE\xf2\x1b;$\x1f{R"\x93\x8d\x1e\x05\xbd\x87\xc9L\xbe\xbd|YV\x02\xa8\xb5\x90\xb9\x01.t\xe4\x8a#\xbd?~\xaf\xddS%]|\xd4Dw^\x92N\xf7\'\x02h'
print("1. Encrypted data:", ENCRYPT_DATA)
#4. Decrypt message
decryptData = RSA.decrypt(ENCRYPT_DATA) #decrypt data
print("2. Decrypt message:",decryptData)