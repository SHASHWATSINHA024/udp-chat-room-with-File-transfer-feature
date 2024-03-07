import socket 
import threading
import queue
from functools import *
import ssl
import re 
import os 
import time
def delete_until_file(text):
    file_index = text.find("FILE:")
    if file_index != -1:
        return text[file_index + len("FILE:"):]
    else:
        return text
def contains_file_word(sentence):
    pattern = 'FILE:'
    if re.search(pattern, sentence):
        return True
    else:
        return False


messages = queue.Queue()
clients = []
client_2 = {}

# server = dtls.DTLSSocket(dtls.SocketType.DGRAM)
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(("localhost",9999))

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")


def receive():  
    while True:
        try:    
            message, addr = server.recvfrom(1024)
            messages.put((message,addr))
        except:
                pass

global cond
cond = True

def broadcast():
    while True:
        while not messages.empty():
            message,addr = messages.get()
            if message.decode().startswith("SIGNUP_TAG"):
                name = message.decode()[message.decode().index(":") + 1 : ]

                if addr not in clients and name not in client_2:

                    print(addr)
                    clients.append(addr)
                    name = message.decode()[message.decode().index(":") + 1 : ]
                    client_2.update({name:addr})
                    greeting(addr)
                    print(message.decode())
                    cond = True
                else:
                    name = message.decode()[message.decode().index(":") + 1 : ]
                    server.sendto(f"Taken: {name} has already been taken".encode(),addr)
                    cond = False
            elif message.decode().startswith("List:"):
                str1 = reduce(lambda x,y: x + " " + y, client_2)
                str1 = "List:" + str1
                server.sendto(str1.encode(),addr)
                cond = False
            elif message.decode().startswith("exit"):
                name = message.decode()[message.decode().index(":")+1:]
                clients.remove(addr)
                del client_2[name]
                cond = True
            elif contains_file_word(message.decode()):
                print("file__sending")
                file_name = delete_until_file(message.decode()).strip()
                # file_name="audio.mp3"

                file_path = os.path.join(r"C:\Users\LEN0VO\Documents\client", file_name)
                g=file_name
                g1="sended->FILE:"+g
                bytes_data = bytes(g1, 'utf-8')
                server.sendto(bytes_data, addr)

                with open(file_path, "rb") as file:
                 while True:
                    data = file.read(1024)
                    if data:
                        print("-")
                        server.sendto(data, addr)
                        time.sleep(0.02)
                    else:
                        print("*")
                        server.sendto(b"qend",addr)
                        break
                cond=True


            else:
                print(message.decode())
                cond = True
            if cond:
                for client in clients:
                    try:
                        if client == addr:
                            continue
                        elif message.decode().startswith("SIGNUP_TAG") and addr in clients:
                            name = message.decode()[message.decode().index(":")+1:]
                            
                            server.sendto(f"{name} joined!".encode(),client)
                        elif message.decode().startswith("exit"):
                            name = message.decode()[message.decode().index(":")+1:]
                            server.sendto(f"{name} has left the Chatroom!".encode(),client)
                        elif message.decode().startswith("Kick"):
                            l1 = message.decode().split()
                            if l1[1] not in client_2:
                                server.sendto(f"No_exist: {l1[1]} not in the chatroom".encode(),addr)
                                print(f"{l1[1]} not in the chatroom")
                                break
                            if client == client_2[l1[1]]:
                                server.sendto(f"Kicked: {l1[-1]} has kicked you.".encode(),client)
                                clients.remove(client_2[l1[1]]) 
                                del client_2[l1[1]]
                            else:
                                server.sendto(f"{l1[-1]} has kicked {l1[1]}".encode(),client)
                        elif message.decode().startswith("Direct:"):
                            names = message.decode()[message.decode().find("(") + 1 : message.decode().find(")")]
                            name = message.decode()[message.decode().rfind(" ") + 1 : ]
                            names = names.split(",")
                            names = list(map(str.strip,names))
                            names = list(filter(lambda x: len(x) != 0 ,names))
                            names = list(map(lambda x: client_2[x],names))
                            if client in names:
                                mes = "(DM) " + name + ": " + message.decode()[message.decode().find(")") + 2: message.decode().rfind(" ")]
                                server.sendto(mes.encode(),client)
                        elif message.decode().startswith("Leave:"):
                            names = message.decode()[message.decode().find("(") + 1 : message.decode().find(")")]
                            name = message.decode()[message.decode().rfind(" ") + 1 : ]
                            names = names.split(",")
                            names = list(map(str.strip,names))
                            names = list(filter(lambda x: len(x) != 0 ,names))
                            names = list(map(lambda x: client_2[x],names))
                            if client not in names:
                                mes = "(DM) " + name + ": " + message.decode()[message.decode().find(")") + 2: message.decode().rfind(" ")]
                                server.sendto(mes.encode(),client)
                        else:
                            server.sendto(message,client)
                    except Exception as e:
                        print(e)
                        pass
            cond = True


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()

def greeting(addr):
    mes = """Welcome to the Chatroom
    Instructions:-
    1.Please be friendly to everyone in the chatroom.
    2.To exit just type "Exit" <Enter>.
    3.To make use of the features. Make sure to suffix the keyword with ":".
        For Ex:-
        i)"List:" -> for listing the clients available in the chatroom.
        ii)"Direct: (<client_names>,) <message>" -> To send direct messages.
        iii)"Leave: (<client_names>,) <messages>" -> To leave the clients and send others the message. 
        iv)"Kick: <client_name>" -> To kick the given client name.\n
        """
    server.sendto(mes.encode(),addr)
