import __init
from Library.C5_RsaEncrypt.rsa_Wrap import RSA_Class
import datetime
import rsa #pip install rsa
#https://app.brevo.com/settings/keys/api
SIB_BIN_API_KEY  = b'j\xe1\xcba\xact\xec"5Uq\xdc\x84\xb3\xc2L\xd3Ub?"\x89+8\x1al\xdc\xe16=\xfah\x08\xdd\x17\xd3\x9aH\xdf\xea\x1dC\x83@2\r\xfa \xbc\x0b\xe5\xff/=\xf2\t1\xb5\x99!\x04\xa9\x9a\xd0\xb164\xaf5\x02fr\xc4\xf7>\x8e1\x0f\x05R\xf5\xfex\xf4\xe7\xeb\xdc\x04<,\xf9\xb0\xcf\x16>\xce0\xc8\xba<xx\xae\xd7\x83\x8f\x8d B\x03\x14\xfc\x1c\xdd\x8d\xaf\xa0\xd5\xe62\xe9\xf0\xac\x0f\xf7\x89c\xae\xc0&\xc7\x93\xb16\x04\x0f\xb8q\xea\xe2\xf3\xa1:\xcc9\x1c\x0e\xff\xa6(\xefF\xf2\\\xf7\x910\x01\xbf\xf5\n\xbc\x03\xf8\xec\xd3\x12\x1b\x83\xe5\xb8i\xb26Qv\xf4h]f\x0f\x0c\x93H\xcaMy\x0e<K\xf2\xd5\xd9\xe4s\xc1\xfb.\x9e\xa8\xf3\'\xb8\xb6qbF|\x96\x14\x88v\x13\x02\x0e\x97\xb3S\xc2\xfa\xb3\xcc\x15A\xb4x\x87=\xb9UId\xfd\x1f\\\x95\xf4\xed,!\xf5 /X\xdc\xce\xaay3\xe5\xda0\xa2a\xab\xe5'
RSA_SIB = RSA_Class(privateKeyPath="/AppDir/Library/A4_SendInBlue/Components/SIB_private.pem")
DEFAULT_API_KEY = RSA_SIB.decrypt(SIB_BIN_API_KEY) #decrypt data
# print("SIB_API_KEY:",DEFAULT_API_KEY)

DEFAULT_SENDER   = {"email":"wsn_system@cmengineering.com","name":"WSN System"}
DEFAULT_TO       = [{"email":'tran.dung@cmengineering.com.vn',"name":"Tran Dung"}]
DEFAULT_CC       = None # [{"email":"example2@example2.com","name":"Janice Doe"}]
DEFAULT_BCC      = None # [{"name":"John Doe","email":"example@example.com"}]
DEFAULT_REPLY_TO = None #{"email":"replyto@domain.com","name":"John Doe"}

DEFAULT_SUBJECT   = "Hello I'm test mail"

DEFAULT_TEXT_CONT = "Mail scheduled at: " + str(datetime.datetime.now())
DEFAULT_HTML_CONT = "<html><body><h1>This is testing mail. Please is ignore!</h1></body></html>"

# Pass the absolute URL (no local file) or the base64 content of the attachment along with the attachment name (Mandatory if attachment content is passed).
# For example, `[{\"url\":\"https://attachment.domain.com/myAttachmentFromUrl.jpg\", \"name\":\"myAttachmentFromUrl.jpg\"}, 
#                {\"content\":\"base64 example content\", \"name\":\"myAttachmentFromBase64.jpg\"}]`.
# Allowed extensions for attachment file: xlsx, xls, ods, docx, docm, doc, csv, pdf, txt, gif, jpg, jpeg, png, tif, tiff, rtf, bmp, cgm, css, shtml, html, htm, zip,
# xml, ppt, pptx, tar, ez, ics, mobi, msg, pub, eps, odt, mp3, m4a, m4v, wma, ogg, flac, wav, aif, aifc, aiff, mp4, mov, avi, mkv, mpeg, mpg, wmv, pkpass and xlsm
# ( If 'templateId' is passed and is in New Template Language format then both attachment url and content are accepted. If template is in Old template Language format, then 'attachment' is ignored )  # noqa: E501
# DEFAULT_ATTACHMENT = "https://www.dropbox.com/s/vfc36yzbqi7mogp/haha.PNG"
DEFAULT_ATTACHMENT = []