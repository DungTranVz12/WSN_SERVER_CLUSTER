import __init
from Application.parameter import *
from Conf.loggingSetup import *
import json
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
  
JSON_STORE_FILE = "nodeManagement.json"

profileTemplate = {
    "name": "USER1",
    "rollno": 56,
    "cgpa": 8.6,
    "phonenumber": "9976770500"
}

class jsonFileRecord():
  '''
  APPLIATION CONFIGURATION\\
  Mananage all the configuration by using json file.\\
  ==========================================================\\
  USAGE:
  1. A json file (JSON_STORE_FILE)is created to store the configuration of all members (profiles as dict{}).
  2. At the beginning of the application, a variable (profileManager) is created and load load all json file's content.
  3. When a new member is added, the new member (with dict{} structure.Ex: profileTemplate{}) is added to the profileManager and also the json file is updated.
  4. When a member is removed, the member is removed from the profileManager and also the json file is updated.
  5. When a member is updated, User can call syncToJsonFile to update the json file with the latest changes in the profileManager.
  6. User can call syncToJsonFile anytime to update the json file with the latest changes in the profileManager.
  '''
  ###########################################
  # Read node                               #
  ###########################################
  def __init__(self):
    os.system("mkdir -p "+PROFILE_MANAGER)
    os.system("mkdir -p "+TRANS_DATA_DIR)
    
  def loadFromJsonFile(self,jsonFile:str= JSON_STORE_FILE):
    '''
    Load the json file and return the content as a dict{}.
    Ex: nodeManager = JSON.loadFromJsonFile()
    '''
    if not os.path.exists(jsonFile):
      logger.error("File \""+jsonFile+"\" does not exist. Create new file")
      #create new file
      with open(jsonFile, 'w') as f:
        f.write('{}')
      return dict()

    # Opening JSON file
    with open(jsonFile, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
        # logger.debug("Node Manager:"+str(json_object))
    return json_object

  ###########################################
  # update JSON file                        #
  ###########################################
  def syncToJsonFile(self,fileName:str=JSON_STORE_FILE,profileManager:dict={}):
    '''
    Sync the profileManager to the json file.
    Ex: JSON.syncToJsonFile(fileName=JSON_STORE_FILE,profileManager=nodeManager)
    '''
    # Serializing json
    json_object = json.dumps(profileManager, indent=4)
    # Writing to sample.json
    retryCnt = 0
    while True:
      if not os.path.exists(fileName+".lock") or retryCnt >= 30: #If the file is not used by other process or retryCnt >= 30
        os.system("touch "+fileName+".lock") #Lock the file
        with open(fileName, 'w') as outfile:
            # Reading from json file
            outfile.write(json_object)
        os.system("rm -f "+fileName+".lock") #Unlock the file
        return json_object
      else:
        retryCnt = retryCnt + 1
        time.sleep(0.1)

  ###########################################
  # Register node                           #
  ###########################################
  def registerNewMember(self,fileName:str=JSON_STORE_FILE, newMember:str="node1",profileTemplate:dict={},profileManager:dict={}):
    '''
    Register a new member to the profileManager and also update the json file.
    Ex: JSON.registerNewMember(fileName=JSON_STORE_FILE, newMember=newObject,profileTemplate=profileTemplate,profileManager=nodeManager)
    '''
    if newMember in profileManager:
      logger.debug("Node already exists")
      return
    else:
      profileManager[newMember] = profileTemplate
      self.syncToJsonFile(fileName,profileManager)

  ###########################################
  # Remove node                             #
  ###########################################
  def removeMember(self,fileName:str=JSON_STORE_FILE, removeMember:str="node1",profileManager:dict={}):
    '''
    Remove a member from the profileManager and also update the json file.
    Ex: JSON.removeMember(fileName=JSON_STORE_FILE, removeMember=removeMember,profileManager=nodeManager)
    '''
    if removeMember in profileManager:
      del profileManager[removeMember]
      self.syncToJsonFile(fileName,profileManager)
    else:
      logger.warning("Node does not exist")
      return

  ###########################################
  # Update profileManager not sync          #
  ###########################################
  def updateKeyValue(self,parentPath:str="",key:str="keyName",value="Value",profileManager:dict={}):
    '''
    Update key value in the profileManager under the parentPath.
    Ex: JSON.updateProfileManager(parentPath="node1",key="name",value="USER1",profileManager=nodeManager)
    '''
    path = parentPath.split("/")
    for i in range(len(path)):
      if path[i].isdigit():
        profileManager = profileManager[int(path[i])]
      else:
        if path[i] not in profileManager:
          logger.debug("\"%s\"" %path[i], "NOT existed -> Create new dict()")
          profileManager[path[i]]= dict()
          profileManager = profileManager[path[i]]
        else:
          profileManager = profileManager[path[i]]
    profileManager[key] = value

      
###########################
# JSON = jsonFileRecord()
# nodeManager = JSON.loadFromJsonFile()
# JSON.registerNewMember(fileName=JSON_STORE_FILE, newMember="ABC",profileTemplate=profileTemplate,profileManager=nodeManager)

# print("Node Manager Name:"+str(nodeManager["ABC"]["name"]))