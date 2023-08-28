# -*- coding: utf-8 -*-
# source: https://www.smartfile.com/blog/what-is-good-logging-in-python/
import __init
import logging
from Application.parameter import *
import datetime
import platform
import os
from logging.handlers import RotatingFileHandler

################################################################################################
################################ USER DEFINE CODE ##############################################
################################################################################################
LOGFILE_LOGGING_ENABLED    = True   #Enable Logfile logging (No ANSI color)
ROTATELOG_LOGGING_ENABLED  = False  #Enable Rotate logging for ShowLog purpose (ANSI color)
CONSOLE_LOGGING_ENABLED    = False   #Enable Console logging (ANSI color)
HTML_LOGGING_ENABLED       = False  #Enable HTML logging
MQTT_LOGGING_ENABLED       = False  #Enable MQTT logging (ANSI color)
MQTT_SERVER_ALIVE_CHECKING = False  #Enable MQTT server alive checking (lastRcvTimestamp is updated everytime MQTT message is received)


if MQTT_LOGGING_ENABLED == True:
  from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt
  import threading
  MQTT = mqttClass(broker, port, client_id, username, password)
  if MQTT_SERVER_ALIVE_CHECKING == True:
    MQTT.subscribe(MQTT_TOPIC) #Subscribe to MQTT_TOPIC to check if MQTT is working in diagnostic operation.
    threading.Thread(target=MQTT.listen).start()

#1. Set level of logfile and console print out
#   a. DEBUG   : Thông tin chi tiết, thường là thông tin để tìm lỗi.
#   b. INFO    : Là các thông báo thông thường, các thông tin in ra khi chương trình chạy theo đúng kịch bản.
#   c. WARNING : Thông báo khi nghi vấn bất thường hoặc lỗi có thể xảy ra, tuy nhiên chương trình vẫn có thể hoạt động.
#   d. ERROR   : Lỗi. Chương trình có thể không hoạt động được một số chức năng. Thường thì nên dùng khi bắt được exception.
#   e. CRITICAL: Lỗi nghiêm trọng. Chương trình khi gặp lỗi nghiêm trọng không thể giải quyết được và bắt buộc phải dừng lại.
LEVEL_LOGFILE_LOGGING = logging.DEBUG
LEVEL_CONSOLE_LOGGING = logging.DEBUG
LEVEL_HTML_LOGGING    = logging.DEBUG
LEVEL_MQTT_LOGGING    = logging.DEBUG

#2. Set file name for output file
curDay  = datetime.datetime.now()
osName = platform.uname()[0]
nodeName = platform.uname()[1]
LOG_FILE_NAME = 'Logs/Logfile_'+str(nodeName)+'_'+str(curDay.day)+str(curDay.strftime("%b"))+'_'+str(curDay.strftime("%H.%M.%S"))+".txt"
LOG_APPEND_FILE_NAME = "Logs/RotateLogs/Logfile.log"
HTML_LOG_DIR = "Logs/RotateLogs"

#3. Define output format display
printTime          = "[%(asctime)s]"
printLevel         = "[%(levelname)s]"
printMessage       = "%(message)s"
printFileLine      = " - %(filename)s: %(lineno)d"
NEW_FORMAT         = '[%(asctime)s][%(levelname)-8s] %(message)-50s - File:%(filename)s:%(lineno)d'
APPEND_FILE_FORMAT = '[%(asctime)s][%(levelname)-8s] %(message)-50s - File:%(filename)s:%(lineno)d'

if MQTT_LOGGING_ENABLED == True:
  class MQTTHandler(logging.Handler):
      """
      A handler class which writes logging records, appropriately formatted,
      to a MQTT server to a topic.
      """
      def __init__(self,topic:str="TOPIC"):
          logging.Handler.__init__(self)
          self.topic = topic

      def emit(self, record):
          """
          Publish a single formatted logging record to a broker, then disconnect
          cleanly.
          """
          msg = self.format(record)
          MQTT.publish(self.topic, msg)
  
class CustomFormatter(logging.Formatter):
    RESET = "\x1b[0m"
    printTime = "[%(asctime)s]"
    printLevel = "[%(levelname)-8s]"
    printMessage = " %(message)s"
    printFileLine = " - %(filename)s: %(lineno)d"
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    formatDebug    = "\x1b[38;5;245m" + printTime +RESET+                   printLevel +RESET+                   printMessage +RESET
    formatInfo     = "\x1b[38;5;245m" + printTime +RESET+ "\x1b[48;5;51m" + printLevel +RESET+ "\x1b[38;5;51m" + printMessage +RESET
    formatWarining = "\x1b[38;5;245m" + printTime +RESET+ "\x1b[48;5;3m"  + printLevel +RESET+ "\x1b[38;5;3m"  + printMessage +RESET + "\x1b[38;5;245m" + printFileLine +RESET
    formatError    = "\x1b[38;5;245m" + printTime +RESET+ "\x1b[48;5;1m"  + printLevel +RESET+ "\x1b[38;5;1m"  + printMessage +RESET + "\x1b[38;5;245m" + printFileLine +RESET
    # formatCritical = "\x1b[38;5;245m" + printTime +RESET+ "\x1b[48;5;5m"  + printLevel +RESET+ "\x1b[38;5;5m"  + printMessage +RESET + "\x1b[38;5;245m" + printFileLine +RESET
    formatCritical = "\x1b[38;5;245m" + "HTML: "+printMessage +RESET
    FORMATS = {
        logging.DEBUG:    formatDebug,
        logging.INFO:     formatInfo,
        logging.WARNING:  formatWarining,
        logging.ERROR:    formatError,
        logging.CRITICAL: formatCritical
    }
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Tạo thư mục Logs
if os.path.exists("Logs") == False:
  os.mkdir("Logs")
if os.path.exists("Logs/RotateLogs") == False:
  os.mkdir("Logs/RotateLogs")
if os.path.exists("Logs/RotateLogs/data") == False:
  os.mkdir("Logs/RotateLogs/data")


class CustomFormatterHtml(logging.Formatter):
    printTime      = "<span style='color:#B2B2B2'>" + "[%(asctime)s]"               + "</span>"
    printLevelD    = "<span style='color:#000000'>" + "[%(levelname)-8s]"           + "</span>"
    printLevelI    = "<span style='background-color:#008FF0'>" + "[%(levelname)-8s]"           + "</span>"
    printLevelW    = "<span style='background-color:#FFB700'>" + "[%(levelname)-8s]"           + "</span>"
    printLevelE    = "<span style='background-color:#FF0000'>" + "[%(levelname)-8s]"           + "</span>"
    printLevelC    = "<span style='background-color:#FF00FF'>" + "[%(levelname)-8s]"           + "</span>"
    printMessageD  = "<span style='color:#000000'>" + " %(message)s"                + "</span>"
    printMessageI  = "<span style='color:#008FF0'>" + " %(message)s"                + "</span>"
    printMessageW  = "<span style='color:#FFB700'>" + " %(message)s"                + "</span>"
    printMessageE  = "<span style='color:#FF0000'>" + " %(message)s"                + "</span>"
    printMessageC  = "<span style='color:#FF00FF'>" + " %(message)s"                + "</span>"
    printFileLine  = "<span style='color:#B2B2B2'>" + " - %(filename)s: %(lineno)d" + "</span>"
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    formatDebug    = "<p>" + printTime                + printMessageD                 + "</p>"
    formatInfo     = "<h3>" + printTime + printLevelI + printMessageI                 + "</h3>"
    formatWarining = "<h3>" + printTime + printLevelW + printMessageW + printFileLine + "</h3>"
    formatError    = "<h2>" + printTime + printLevelE + printMessageE + printFileLine + "</h2>"
    # formatCritical = "<h1>" + printTime + printLevelC + printMessageC + printFileLine + "</h1>"
    formatCritical = "%(message)s"
    FORMATS = {
        logging.DEBUG:    formatDebug,
        logging.INFO:     formatInfo,
        logging.WARNING:  formatWarining,
        logging.ERROR:    formatError,
        logging.CRITICAL: formatCritical
    }
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

#4. Tạo file log mới và ghi đề lên ở mỗi lần chạy ghi 1, ghi nối tiếp file cũ ghi 0
OVER_WRITE_LOG_FILE = 1

################################################################################################
################################ TEXT LOG HANDLER ##############################################
################################################################################################
if LOGFILE_LOGGING_ENABLED == True:
  # create the logging instance for logging to file only
  logger = logging.getLogger('SmartfileTest')
  if HTML_LOGGING_ENABLED == True:
    def html(msg, *args, **kws):
      logger.critical(msg, *args, **kws)
    logger.html = html #Replace logger.critical with logger.html

  # create the handler for the main logger
  if OVER_WRITE_LOG_FILE == 1:
    configuration = logging.FileHandler(LOG_FILE_NAME,'w','utf-8') #logging method
  else:
    configuration = logging.FileHandler(LOG_FILE_NAME,'a','utf-8') #logging method
  configuration.setFormatter(logging.Formatter(NEW_FORMAT)) #logging format

  # finally, add the handler to the base logger
  logger.addHandler(configuration)
  logger.setLevel(LEVEL_LOGFILE_LOGGING) #Thiết lập mức độ in ra console

################################################################################################
############################# ROTATE LOG HANDLER (FOR SHOWLOG) #################################
################################################################################################
if ROTATELOG_LOGGING_ENABLED == True:
  rotatLog = logging.getLogger('SmartfileTest')
  appendFile = RotatingFileHandler(LOG_APPEND_FILE_NAME,maxBytes=5000000, backupCount=20)
  appendFile.setFormatter(CustomFormatter())
  rotatLog.addHandler(appendFile)

################################################################################################
################################ HTML LOG HANDLER ##############################################
################################################################################################
if HTML_LOGGING_ENABLED == True:
  htmlLogger = logging.getLogger('SmartfileTest')
  # appendFile = RotatingFileHandler(HTML_LOG_DIR+"/Logfile.html",maxBytes=5000000, backupCount=20).setFormatter(CustomFormatterHtml())
  configuration = logging.FileHandler(HTML_LOG_DIR+"/Logfile.html",'w','utf-8')
  configuration.setFormatter(CustomFormatterHtml()) #loggin method & format
  htmlLogger.addHandler(configuration)
  htmlLogger.setLevel(LEVEL_HTML_LOGGING) #Thiết lập mức độ in ra console

################################################################################################
################################ CONSOLE HANDLER ###############################################
################################################################################################
if CONSOLE_LOGGING_ENABLED == True:
  consoleLogger = logging.getLogger('SmartfileTest')
  # source: https://www.smartfile.com/blog/what-is-good-logging-in-python/
  configuration = logging.StreamHandler() #logging method
  configuration.setFormatter(CustomFormatter()) #logging format
  consoleLogger.addHandler(configuration)
  consoleLogger.setLevel(LEVEL_CONSOLE_LOGGING) #Thiết lập mức độ in ra console

################################################################################################
################################ MQTT LOGGING HANDLER ##########################################
################################################################################################
if MQTT_LOGGING_ENABLED == True:
  mqttLogger = logging.getLogger('SmartfileTest')
  configuration = MQTTHandler(topic=MQTT_TOPIC) #logging method
  configuration.setFormatter(CustomFormatter()) #logging format
  mqttLogger.addHandler(configuration)
  mqttLogger.setLevel(LEVEL_MQTT_LOGGING)

############################################
# log some stuff!
# logger.debug("This is a debug message!")
# logger.info("This is an info message!")
# logger.warning("This is a warning message!")
# logger.error("This is an error message!")
# logger.critical("This is a critical message!")
# logger.debug('<img src="https://picsum.photos/200/300" alt="Image">')
# logger.debug('<img src="TestHtmlLogging.jpg" alt="Image">')

