###################################################################################
#	Author:			Bert Van Acker (bva.bmkr@gmail.com)
#	Version:		0.1.0
#	Lisence:		LGPL-3.0 (GNU Lesser General Public License version 3)
#
#	Description:	Communicator class handling the generic communication patterns
###################################################################################

#imports
import socket
import serial
from .Communicator_Constants import *

class Communicator():
    """
        Communicator: Class representing the generic communication handler

         :param bool DEBUG: setting the verbose
         :param string UDP_IP: IP address of the target device
         :param int UDP_PORT: UDP port of the target device
         :param int COM_PORT: COM port of the target device
         :param int COM_BAUD: Baud rate of the target device
         :param object Logger: Logger object for uniform logging
    """
    def __init__(self,UDP_IP='192.168.0.110',UDP_PORT=6789,COM_PORT=4,COM_BAUD=SJ_DefaultBaud,DEBUG=True,LOGGER=None):

        #verbose and logging
        self.DEBUG = DEBUG
        self.LOGGER = LOGGER

        #UDP interface
        self.UDP_IP = UDP_IP
        self.UDP_PORT = UDP_PORT
        self.udp_socket_out = None
        self.udp_socket_in = None

        #serial (USB) interface
        self.COM_PORT = COM_PORT
        self.COM_BAUD = COM_BAUD
        self.Serial_socket = None

        #active communcation
        self.activeCOMM = "UDP" #UDP connection [UDP] / UBSserial [Serial]

    def activateSerial(self):
        """
              Function to activate the serial communication method
        """
        self.activeCOMM = "Serial"
        self.Serial_socket = serial.Serial(self.COM_PORT, self.COM_BAUD)
        self.Serial_socket.timeout = SJ_Timeout / 1000  #in sec

    def activateUDP(self):
        """
              Function to activate the UDP communication method
        """
        self.activeCOMM = "UDP"
        #activate an outgoing UDP
        self.udp_socket_out = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # UDP
        # activate an ingoing UDP
        self.udp_socket_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self.udp_socket_in.bind((socket.gethostname(), SJ_DefaultPortIn))


    def genericWrite(self,id,cmd,parameter=None):
        """
              Function to compose & write a steam_jack command to the communcation bus

              :param string id: Name identifier of the targetted device
              :param string cmd: Command identifier
              :param list parameters: parameterList

              :return bool writeSuccess: successfull bus write identification (-1 = error)
        """
        #compose the message - independent from active communication
        if parameter is not None:
            MESSAGE = (SJ_CommandStart + str(id) + cmd + str(parameter) + SJ_CommandEnd).encode('utf-8')
        else:
            MESSAGE = ("#" + str(id) + cmd + "\r").encode('utf-8')

        if self.activeCOMM == "UDP":
            try:
                self.udp_socket.sendto(MESSAGE, (self.UDP_IP, self.UDP_PORT))
                self.LOGGER.log(msg="UPD send: "+MESSAGE,type="INFO")
            except:
                if self.DEBUG:print("UDP communication failed.")
                self.LOGGER.log(msg="UPD failed: " + MESSAGE, type="ERROR")

        elif self.activeCOMM == "Serial":
            try:
                self.Serial_socket.write(MESSAGE)
                self.LOGGER.log(msg="Serial send:" + MESSAGE, type="INFO")
            except:
                if self.DEBUG:print("Serial communication failed.")
                self.LOGGER.log(msg="Serial failed: " + MESSAGE, type="ERROR")