import __init
from Library.B1_jsonFileControl.jsonFileControl import jsonFileRecord
import os

#############################################################
# APPLIATION CONFIGURATION                                  #
# Mananage all the configuration by using json file         #
#############################################################
# USAGE:
# 1. A json file (JSON_STORE_FILE)is created to store the configuration of all members (profiles as dict{}).
# 2. At the beginning of the application, a variable (profileManager) is created and load load all json file's content.
# 3. When a new member is added, the new member (with dict{} structure.Ex: profileTemplate{}) is added to the profileManager and also the json file is updated.
# 4. When a member is removed, the member is removed from the profileManager and also the json file is updated.
# 5. When a member is updated, User can call syncToJsonFile to update the json file with the latest changes in the profileManager.
# 6. User can call syncToJsonFile anytime to update the json file with the latest changes in the profileManager.
#############################################################
  
JSON_STORE_FILE = "Library/B1_jsonFileControl/Example/EX1_nodeManagement.json"

profileTemplate = {
    "name": "JUBEI",
    "rollno": 56,
    "cgpa": 8.6,
    "phonenumber": "9976770500"
}

###########################
JSON = jsonFileRecord()
nodeManager = JSON.loadFromJsonFile(JSON_STORE_FILE)
JSON.registerNewMember(fileName=JSON_STORE_FILE, newMember="AAA",profileTemplate=profileTemplate,profileManager=nodeManager)
JSON.registerNewMember(fileName=JSON_STORE_FILE, newMember="BBB",profileTemplate=profileTemplate,profileManager=nodeManager)
JSON.registerNewMember(fileName=JSON_STORE_FILE, newMember="CCC",profileTemplate=profileTemplate,profileManager=nodeManager)
JSON.removeMember(fileName=JSON_STORE_FILE, removeMember="AAA",profileManager=nodeManager)

