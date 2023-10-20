import logging
import logging.handlers
import socket
from flask import render_template


def getHistory(title, media_type):
    hostname = socket.gethostname()
    client_ip = socket.gethostbyname(hostname)
    
    logging.basicConfig(filename="history.log",
                    format='%(asctime)s - %(name)s - %(message)s',
                    filemode='w')
    logger = logging.getLogger()
 
    logger.setLevel(logging.INFO)
    
    logger.info(f"{client_ip} has downloaded the {media_type} named {title}") 



def loadHistory():
    data = []
    with open('history.log', 'r') as fp:
    # read all lines in a list
        lines = fp.readlines()
        for line in lines:
            # check if string present on a current line
            if line.find("root") != -1:
                data.append(line)

    return render_template("history.html", history_list=data)
       

 


    
        
    