from socket import *


#Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ('smtp.gmail.com', 587) #("mail.smtp2go.com", 2525) 

print('Your GMAIL account must allow "Less secure apps')

enterUsername = input('Username: ')
enterPassword = input('Password: ')

username = bytes(enterUsername, encoding='utf-8')
password = bytes(enterPassword, encoding='utf-8')

emailFrom = enterUsername
emailTo = input('Send email to: ')

enterMsg = input('What would you like to say? ')
msg = f"\r\n {enterMsg}"
endmsg = "\r\n.\r\n"

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024)
print(recv)

if recv[:3] != b'220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
print(recv1)

if recv1[:3] != b'250':
    print('250 reply not received from server.')

# Attending Google requirements
TLS = b'STARTTLS\r\n'
clientSocket.send(TLS)
tlsRecv = clientSocket.recv(1024)
print(tlsRecv)
if tlsRecv[:3] != b'220':
    print('220 reply not received from server')
    
securedSocket = ssl.wrap_socket(clientSocket,      
                ssl_version=ssl.PROTOCOL_TLSv1_2,     
                ciphers="HIGH:-aNULL:-eNULL:-PSK:RC4-SHA:RC4-MD5")

# Seding AUTH LOGIN command
authCommand = b'AUTH LOGIN\r\n'
securedSocket.write(authCommand)
authRecv = securedSocket.read(1024)
print(authRecv)
if authRecv[:3] != b'334':
    print('334 reply not received from server')
    
# Sending username
encodedUsername = base64.b64encode(username) + b'\r\n'
securedSocket.write(encodedUsername)
encodedUsernameRecv = securedSocket.read(1024)
print(encodedUsernameRecv)
if encodedUsernameRecv[:3] != b'334':
    print('334 reply not received from server')
    
# Sending password
encodedPassword = base64.b64encode(password) + b'\r\n'
securedSocket.write(encodedPassword)
encodedPasswordRecv = securedSocket.read(1024)
print(encodedPasswordRecv)
if encodedPasswordRecv[:3] != b'235':
    print('235 reply not received from server')

# Send MAIL FROM command and print server response.
mailFromCommand = bytes(f"MAIL FROM: <{emailFrom}>\r\n", encoding='utf-8') 

securedSocket.write(mailFromCommand)
mailFromCommandRecv = securedSocket.read(1024)
print(mailFromCommandRecv)
if mailFromCommandRecv[:3] != b'250':
    print('250 reply not received from server.') 

# Send RCPT TO command and print server response.
rcptToCommand = bytes(f"RCPT TO: <{emailTo}>\r\n", encoding='utf-8') 

securedSocket.write(rcptToCommand)
rcptToCommandRecv = securedSocket.read(1024)
print(rcptToCommandRecv)
if rcptToCommandRecv[:3] != b'250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
dataCommand = bytes(f"DATA\r\n", encoding='utf-8') 

securedSocket.write(dataCommand)
dataCommandRecv = securedSocket.read(1024)
print(dataCommandRecv)
if dataCommandRecv[:3] != b'354':
    print('354 reply not received from server.')

# Send message data.
msgCommand = bytes(msg, encoding='utf-8') 
securedSocket.write(msgCommand)

# Message ends with a single period.
endCommand = bytes(endmsg, encoding='utf-8')

securedSocket.write(endCommand)
endCommandRecv = securedSocket.read(1024)
print(endCommandRecv)
if endCommandRecv[:3] != b'250':
    print('250 reply not received from server.')

# Send QUIT command and get server response
quitCommand = bytes(f"QUIT\r\n", encoding='utf-8')

securedSocket.write(quitCommand)
quitCommandRecv = securedSocket.read(1024)
print(quitCommandRecv)
if quitCommandRecv[:3] != b'221':
    print('221 reply not received from server.')

clientSocket.close()