import socket
import sys
import os
import time
import threading
import pyDH
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Server(threading.Thread):
    def run(self):
        print("Hello")
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Server started successfully\n")
        hostname='localhost'
        # port=51412
        port = int(input("Enter port to listen on\n>>"))
        self.sock.bind((hostname,port))
        self.sock.listen(1)
        print("Listening on port %d\n" %port)        
        #time.sleep(2)    
        while 1:
            (clientname,address)=self.sock.accept()
            print("Connection from %s\n" % str(address))  

            server_dh = pyDH.DiffieHellman() 
            g = server_dh.g
            p = server_dh.p
            priv_key = server_dh.get_private_key()
            pub_key = server_dh.gen_public_key()
            
            print("Value of g: "+str(g))
            print("Value of p: "+str(p))
            print("Private variable (a): "+str(priv_key))
            print("Public key (g^a mod p): "+str(pub_key))

            clientname.send(bytes(str(pub_key),'utf-8'))
            client_pub_key = int(str(clientname.recv(4096),'utf-8'))
            print("Client public key: "+str(client_pub_key))
            shared_key = server_dh.gen_shared_key(client_pub_key)
            print("Shared key: "+shared_key)
            
            digest = hashes.Hash(hashes.SHA256())
            digest.update(bytes(shared_key,'utf-8'))
            data_key = digest.finalize()

            iv = os.urandom(16)
            self.cipher = Cipher(algorithms.AES(data_key), modes.CBC(iv))        
            print("IV: "+str(iv))
            clientname.send(iv)
            

            while 1:
                chunk=clientname.recv(4096)
                print(str(address)+' sent the following data: '+str(chunk))
                decryptor = self.cipher.decryptor()
                unpadder = padding.PKCS7(128).unpadder()
                decrypted_msg = decryptor.update(chunk) + decryptor.finalize()
                unpadded_msg = unpadder.update(decrypted_msg) + unpadder.finalize()
                msg = str(unpadded_msg,'utf-8')
                print('Decrypting...\n>>'+str(address)+':'+msg)
                if msg.lower() == 'exit':
                    break
                reply = input(">>")
                if reply != '':
                    encryptor = self.cipher.encryptor()
                    padder = padding.PKCS7(128).padder()
                    padded_msg = padder.update(bytes(reply,'utf-8')) + padder.finalize()
                    encrypted_msg = encryptor.update(padded_msg) + encryptor.finalize()
                    clientname.send(encrypted_msg)
            
            clientname.close()
            print("Closing client connection socket...")
        return 1

class Client(threading.Thread):    
    def connect(self,host,port):
        self.sock.connect((host,port))
    def client(self,host,port,msg):               
        sent=self.sock.send(msg)           
        print("Sent\n")
    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            host=input("Enter the hostname to connect to\n>>")            
            port=int(input("Enter the port to connect to\n>>"))
        except EOFError:
            print("Error")
            return 1
        
        print("Connecting\n")
        s=''
        self.connect(host,port)
        print("Connected\n")

        client_dh = pyDH.DiffieHellman()
        g = client_dh.g
        p = client_dh.p
        priv_key = client_dh.get_private_key()
        pub_key = client_dh.gen_public_key()

        print("Value of g: "+str(g))
        print("Value of p: "+str(p))
        print("Private variable (a): "+str(priv_key))
        print("Public key (g^a mod p): "+str(pub_key))

        self.sock.send(bytes(str(pub_key),'utf-8'))
        server_pub_key = int(str(self.sock.recv(4096),'utf-8'))
        print("Server public key: "+str(server_pub_key))
        shared_key = client_dh.gen_shared_key(server_pub_key)
        print("Shared key: "+shared_key)
        
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(shared_key,'utf-8'))
        data_key = digest.finalize()

        iv = self.sock.recv(4096)
        print("Received IV: "+str(iv))
        self.cipher = Cipher(algorithms.AES(data_key), modes.CBC(iv))

        while 1:            
            print("Waiting for message\n")
            msg=input('>>')
            if msg=='':
                continue

            print("Sending\n")
            # self.client(host,port,msg)
            encryptor = self.cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_msg = padder.update(bytes(msg,'utf-8')) + padder.finalize()
            encrypted_msg = encryptor.update(padded_msg) + encryptor.finalize()
            self.sock.send(encrypted_msg)

            if msg=='exit':
                break
            
            reply = self.sock.recv(4096)
            print(str((host,port))+' sent the following data: '+str(reply))
            decryptor = self.cipher.decryptor()
            unpadder = padding.PKCS7(128).unpadder()
            decrypted_msg = decryptor.update(reply) + decryptor.finalize()
            unpadded_msg = unpadder.update(decrypted_msg) + unpadder.finalize()
            print('Decrypting...\n>>'+str((host,port))+':'+str(unpadded_msg))
            
        
        self.sock.close()
        print("Closing client socket...")
        sys.exit()
        return 1

if __name__=='__main__':
    srv=Server()
    # srv.daemon=True
    print("Starting server")
    srv.start()
    time.sleep(3)
    op = input("Start client? (Y/N)\n>>").lower()
    if op == "y":
        print("Starting client")
        cli=Client()
        print("Started successfully")
        cli.start()
    