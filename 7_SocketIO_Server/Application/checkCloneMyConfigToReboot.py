import __init
############ IMPORT PARAMETER ############
import sys,os,time,threading

def checkUpdateMyConfigurationFileToRebootContainer():
  while True:
    if os.path.exists("/0_SHARE/myConfiguration.py") and os.path.exists("/AppDir/cloneMyConfig.py"):
      if os.path.getmtime("/0_SHARE/myConfiguration.py") > os.path.getmtime("/AppDir/cloneMyConfig.py"):
        print ("myConfiguration.py updated. Rebooting container...")
        os.system("reboot")
    time.sleep(5)
threading.Thread(target=checkUpdateMyConfigurationFileToRebootContainer).start()
