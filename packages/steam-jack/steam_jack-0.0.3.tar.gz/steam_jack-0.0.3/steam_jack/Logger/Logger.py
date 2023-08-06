###################################################################################
#	Author:			Bert Van Acker (bva.bmkr@gmail.com)
#	Version:		0.1.0
#	Lisence:		LGPL-3.0 (GNU Lesser General Public License version 3)
#
#	Description:	Logger class handling steam_jack logging functionality
###################################################################################

# imports
import logging

class Logger(object):

    def __init__(self,fileName ="tmp/steamjack.log"):
        logging.basicConfig(filename=fileName, filemode='w', format='%(asctime)s    %(message)s', level=logging.INFO)


    def log(self,msg,type):
        if type == 'INFO':
            logging.info(msg)
        elif type == 'DEBUG':
            logging.debug(msg)
        elif type == 'ERROR':
            logging.error(msg)
