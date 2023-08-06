###################################################################################
#	Author:			Bert Van Acker (bva.bmkr@gmail.com)
#	Version:		0.1.0
#	Lisence:		LGPL-3.0 (GNU Lesser General Public License version 3)
#
#	Description:	Device class representing the emlid navio 2
#
#   Note:           Emlid firmware under Firmware/00_PiBased/Navio2
###################################################################################
from steam_jack.Communicator import Communicator,Communicator_Constants
from steam_jack.Logger import Logger

class Emlid_navio():
    """
        Emlid_navio: Class representing emlid navio 2 device, interfaced via UDP

         :param bool DEBUG: setting the verbose
         :param string UDP_IP: IP address of the target device
         :param int UDP_PORT: UDP port of the target device
    """
    def __init__(self,UDP_IP='192.168.0.110',UDP_PORT=6789,DEBUG=False):
        self.logger = Logger.Logger(fileName="logs/Emlid-navio.log")
        self.communicator = Communicator.Communicator(UDP_IP=UDP_IP, UDP_PORT=UDP_PORT, LOGGER=self.logger,DEBUG=DEBUG)

        #activating the UDP communication method
        self.communicator.activateUDP()

    def deactivate(self):
        """
              Function deactivate the device
        """
        self.communicator.deactivateUDP()

    def buildinLED(self, color):
        """
              Function to set the color of the buildin LED- Non-blocking

              :param string color: predefined color - see communcation protocol
        """
        self.communicator.genericWrite(id=1, cmd=Communicator_Constants.SJ_ActionLED,parameter=color)


