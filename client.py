import socket
import threading
import random
import sys
import ssl
def extract_string_after_pattern(input_string):
    pattern = "sended->FILE:"
    index = input_string.find(pattern)
    if index != -1:
        index += len(pattern)
        extracted_string = input_string[index:].strip()
        return extracted_string
    else:
        return None
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.bind(("localhost" , random.randint(8000,9000)))

ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_verify_locations("server.crt")

global name
name = input("Nickname :")

        


def receive():
    global cond
    while cond:
        try:
            message, _ = client.recvfrom(1024)
            sys.stdout.write('\r')
            s=message.decode()
            if message.decode().startswith("Kicked:"):
                print(message.decode()[message.decode().index(" ")+1 :])
                cond = False
                client.close()
                sys.exit()
            elif message.decode().startswith("Taken"):
                print(message.decode()[message.decode().find(":") + 2 :])
                cond = False
                client.close()
                print("Exiting....\n Press Enter \n")
                sys.exit()
            elif message.decode().startswith("List:"):
                mes = (message.decode()[message.decode().find(":") + 1 : ]).split()
                print("The list of Clients are:-")
                for clients in mes:
                    print(clients)
            elif message.decode().startswith("sended->FILE:"):

                    print("filecontent")
                    output_f =extract_string_after_pattern(s)
                    print("+",output_f)
                    k = r"C:\Users\LEN0VO\Documents\client\sender\\" + output_f   
                    with open(k,"w") as file:
                      message, _ = client.recvfrom(1024)

                      file.write(message.decode())
                      file.flush()
                      file.close()

    
            else:
                print(message.decode())
        except:
            pass


cond = True
t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode() , ("localhost",9999))

while True:
    try:
        message=input()
        output_f=""
        if message == "Exit":
            client.sendto(f"exit:{name}".encode(),("localhost",9999))
            cond = False
            client.close()
            sys.exit()
        elif message[0:5] == "Kick:":
            message = message + " " + name
            client.sendto(message.encode(),("localhost", 9999))
        elif message.startswith("Direct:"):
            message = message + " " + name 
            client.sendto(message.encode(),("localhost",9999))
        elif message.startswith("Leave:"):
            message = message + " " + name 
            client.sendto(message.encode(),("localhost",9999))
        elif message.startswith("List:"):
            message =  message + " " + name 
            client.sendto(message.encode(),("localhost",9999))
        
        else:
            client.sendto(f"{name}: {message}".encode(), ("localhost",9999))
    except:
        sys.exit()
