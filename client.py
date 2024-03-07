import socket
import threading
import random
import sys
import ssl

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.bind(("192.168.126.48" , random.randint(8000,9000)))

ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_verify_locations("server.crt")

global name
name = input("Nickname :")
def extract_after_sended_file(input_string):
    # Find the index of "sended->FILE:"
    start_index = input_string.find("sended->FILE:")
    if start_index != -1:
        # Extract whatever comes after "sended->FILE:"
        extracted_text = input_string[start_index + len("sended->FILE:"):]
        return extracted_text.strip()
    else:
        return None
def process_file_name(file_name):
    # Check if the string contains "FILE:"
    if "FILE:" in file_name:
        # Extract the filename after "FILE:"
        _, file_name = file_name.split("FILE:")
        # Split the filename and extension
        file_name, extension = os.path.splitext(file_name)
        # Add "(1)" before the extension
        file_name = f"{file_name}(1){extension}"
        return file_name
    else:        return None

def receive():
    global cond
    while cond:
        try:
            message, _ = client.recvfrom(1024)
            sys.stdout.write('\r')
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
                    
                    print(message.decode())

    
            else:
                print(message.decode())
        except:
            pass


cond = True
t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode() , ("192.168.126.142",9999))

while True:
    try:
        message=input()
        output_f=""
        if message == "Exit":
            client.sendto(f"exit:{name}".encode(),("192.168.126.142",9999))
            cond = False
            client.close()
            sys.exit()
        elif message[0:5] == "Kick:":
            message = message + " " + name
            client.sendto(message.encode(),("192.168.126.142", 9999))
        elif message.startswith("Direct:"):
            message = message + " " + name 
            client.sendto(message.encode(),("192.168.126.142",9999))
        elif message.startswith("Leave:"):
            message = message + " " + name 
            client.sendto(message.encode(),("192.168.126.142",9999))
        elif message.startswith("List:"):
            message =  message + " " + name 
            client.sendto(message.encode(),("192.168.126.142",9999))
        
        else:
            client.sendto(f"{name}: {message}".encode(), ("192.168.126.142",9999))
    except:
        sys.exit()


