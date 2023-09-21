import datetime
#https://app.brevo.com/settings/keys/api
DEFAULT_API_KEY  = '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'
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