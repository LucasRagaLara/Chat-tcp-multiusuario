import socket
import threading

#Declaro puerto y host
PORT = 65444
HOST = 'localhost'

#Función para manejar los clientes
def recibir_cliente(conn):
    try:
        conn.sendall("Introduce tu nombre de usuario:".encode())
        nombre_user = conn.recv(1024).decode()
        if not nombre_user:
            conn.sendall("El nombre de usuario no puede estar vacío. Por favor, elige otro.".encode())
        if nombre_user in clientes:
            conn.sendall("El nombre ya está en uso. Por favor elige otro.".encode())
        else:
            #Si el cliente no está, lo agrego e igualo su nombre a su conexión para luego verificar al enviar mensajes.
            clientes[nombre_user] = conn
            conn.sendall("Sé bienvenido.".encode())
            while True:
                try:
                    datos = conn.recv(1024).decode()
                    if not datos:
                        break  
                    mensaje = "{}: {}".format(nombre_user, datos)
                    enviar_cliente(mensaje, conn)
                except Exception as e:
                    print(e)
                    break
            #Elimino del diccionario al cliente que se ha desconectado
    except Exception as e:
        print("Error en función recibir_cliente", e)
    finally:
        conn.close()
#Función para enviar los mensajes al resto de clientes
def enviar_cliente(mensaje, conn):
    try:
        #Si el cliente está en la lista, le envio los mensajes a todos menos a él. 
        for cliente in clientes.values():
            if cliente!=conn:
                cliente.sendall((mensaje.encode()))
    except Exception as e:
        print("Error en función enviar_cliente", e)

clientes = {}
#abro el socket y creo el servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    print("Servidor conectado.")
    while True:
        conn, addr = sock.accept()
        print("cliente {} conectado".format(conn))
        #Agrego el cliente conectado a la lista de clientes
        print("Esperando peticiones...")
        #Genero un hilo para cada cliente
        thread_cliente = threading.Thread(target=recibir_cliente, args=(conn,))
        #Lo ejecuto.
        thread_cliente.start()  