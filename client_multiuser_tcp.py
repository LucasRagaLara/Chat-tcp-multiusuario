import socket
import threading
#Envia los mensajes al servidor.
def enviar_mensaje(sock_client):
    while True:
        try:
            mensaje = input("\n")
            sock_client.sendall(mensaje.encode())
        except Exception as e:
            print("Error de conexión con el servidor al enviar:", e)
            break
#Recibe y procesa los mensajes del servidor.
def recibir_mensaje(sock_client):
    while True:
        try:
            datos_servidor = sock_client.recv(1024).decode('utf-8')
            if not datos_servidor:
                print("El servidor se ha desconectado.")
                break
            print(datos_servidor)
        except Exception as e:
            print("Error de conexión con el servidor al recibir:", e)
            break
PORT = 65444
HOST = 'localhost'
#Creamos el socket
sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_client.connect((HOST, PORT))
print("Conectado.")

#Creamos un hilo para enviar y otro para recibir.
hilo_cliente_recv = threading.Thread(target=recibir_mensaje, args=((sock_client,)))
hilo_cliente = threading.Thread(target=enviar_mensaje, args=((sock_client, )))
hilo_cliente_recv.start()
hilo_cliente.start()