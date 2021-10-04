from socket import *
import time
from time import strftime, localtime
import numpy as np


serverName = "127.0.0.1"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

#settimeout(seconds) will raise a timeout exception if the timeout period value has elapsed before the operation has completed
#source: https://docs.python.org/3/library/socket.html#socket.socket.settimeout

clientSocket.settimeout(1.0)

RTT = {"response_time":[], "packet_loss": 0, "delivered": 0}

for sequence_number in range(0,10):
    start = time.time() 
    message = f"Ping: {sequence_number} Datetime: {strftime('%a, %d %b %Y %H:%M:%S %Z', localtime())}"
    clientSocket.sendto(message.encode(), (serverName, serverPort))

    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        end = time.time()
        roundTrip = end - start
        RTT["response_time"].append(roundTrip)
        RTT["delivered"] += 1
        print(f"\nresponse: {modifiedMessage.decode()}")
        print(f"RTT: {roundTrip} seconds")
    except timeout:
        RTT["packet_loss"] += 1
        print("\nRequest timed out")

clientSocket.close()

minimum = np.min(RTT["response_time"]) if len(RTT["response_time"]) > 0 else 'NA'
maximum = np.max(RTT["response_time"]) if len(RTT["response_time"]) > 0 else 'NA'
average = np.mean(RTT["response_time"]) if len(RTT["response_time"]) > 0 else 'NA'
totalMessages = RTT["packet_loss"] + RTT["delivered"]

print(f"""
RTT report
minimum: {round(minimum,5)}
maximum: {round(maximum,5)}
average: {round(average,5)}
packet loss: {round((RTT["packet_loss"] / totalMessages * 100),2)}%
""")