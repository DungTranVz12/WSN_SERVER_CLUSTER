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

JSON_INPUT_FILE  = "Library/B1_jsonFileControl/Example/EX2_Input.json"
JSON_OUTPUT_FILE = "Library/B1_jsonFileControl/Example/EX2_Output.json"

profileTemplate = {
    "name": "JUBEI",
    "rollno": 56,
    "cgpa": 8.6,
    "phonenumber": "9976770500"
}

###########################
JSON = jsonFileRecord()
nodeManager = JSON.loadFromJsonFile(JSON_INPUT_FILE)
JSON.updateKeyValue(parentPath="B0/B1",key="New Key",value="ADD NEW KEY!!!",profileManager=nodeManager) # Library/B1_jsonFileControl/Components/PIC/EX2_Output.png (1)
JSON.updateKeyValue(parentPath="B0/B1/B2",key="New Branch KEY",value="NEW BRANCH & NEW KEY",profileManager=nodeManager) # Library/B1_jsonFileControl/Components/PIC/EX2_Output.png (2)
JSON.updateKeyValue(parentPath="B0/B2",key="name",value="MODIFIED NAME!!!",profileManager=nodeManager) # Library/B1_jsonFileControl/Components/PIC/EX2_Output.png (3)
JSON.updateKeyValue(parentPath="C0/1",key="name",value="MODIFIED IN ARRAY[1]!!!",profileManager=nodeManager) # Library/B1_jsonFileControl/Components/PIC/EX2_Output.png (4)

JSON.syncToJsonFile(fileName=JSON_OUTPUT_FILE,profileManager=nodeManager)
