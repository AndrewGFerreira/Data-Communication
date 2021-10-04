"""
Class: CSC 321 Data Communication
Name: Andrew Gessinger Ferreira
Program 2.1 - WebServer
"""

#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
serverPort = 80
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('Serve is ready to receive')

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr =  serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]                 
        f = open(filename[1:])                        
        outputdata = f.read() 
        #Send one HTTP header line into socket
        connectionSocket.send('\nHTTP/1.1 200 OK\r\n'.encode())

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):           
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:
        #Send response message for file not found
        connectionSocket.send('\nHTTP/1.1 404 Not Found\r\n'.encode())
        #Close client socket
        connectionSocket.close()
        #Fill in start
        #Fill in end
serverSocket.close()


sys.exit()#Terminate the program after sending the corresponding data