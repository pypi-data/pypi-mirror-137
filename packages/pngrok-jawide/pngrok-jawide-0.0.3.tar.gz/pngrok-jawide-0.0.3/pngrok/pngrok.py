import socket
import threading
import traceback
import logging

def sum_bytes_16(data):
    return sum([int.from_bytes(d, "big") for d in [data[i*2:(i+1)*2] for i in range(len(data))]])

def checksum(data):
    s = sum_bytes_16(data)
    s = (s & 0xffff) + (s >> 16)
    s += (s >> 16)
    return (~s & 0xffff)

class PngrokMessage:
    message_type = bytes(6)
    checksum = bytes(2)
    option_size = bytes(4)
    data_size = bytes(4)
    option = bytes()
    data = bytes()
    def __init__(self, option:bytes=bytes(), data:bytes=bytes()):
        self.message_type = b"pngrok"
        self.option_size = len(option).to_bytes(4, "big")
        self.data_size = len(data).to_bytes(4, "big")
        self.option = option
        self.data = data
    def from_bytes(self, bs:bytes):
        if len(bs) < 16 or checksum(bs) != 0x0000 or bs[:6] != self.message_type:
            return False
        self.checksum = bs[6:8]
        self.option_size = bs[8:12]
        self.data_size = bs[12:16]
        option_size = int.from_bytes(self.option_size, "big")
        data_size = int.from_bytes(self.data_size, "big")
        self.option = bs[16:16+option_size]
        self.data = bs[16+option_size:16+option_size+data_size]
        return True
    def to_bytes(self) -> bytes:
        self.checksum = checksum(self.message_type+self.option_size+self.data_size+self.option+self.data).to_bytes(2, "big")
        return self.message_type+self.checksum+self.option_size+self.data_size+self.option+self.data
    def __str__(self) -> str:
        self.to_bytes()
        def format_attr(ss):
            return "".join([f"{s:>12s} = {getattr(self, s)}\n" for s in ss])
        return format_attr(["message_type","checksum","option_size","data_size","option","data"])


class AliceListener(threading.Thread):
    def __init__(self, alice_listen_addr: tuple, client_listen_addr: tuple, buffer_size=2048):
        super().__init__()
        self.alice_listen_addr = alice_listen_addr
        self.client_listen_addr = client_listen_addr
        self.buffer_size = buffer_size

    def run(self) -> None:
        def get_alice_socket():
            alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            alice_socket.bind(self.alice_listen_addr)
            alice_socket.listen(5)
            return alice_socket

        def get_client_socket():
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.bind(self.client_listen_addr)
            client_socket.listen(5)
            return client_socket

        alice_socket = get_alice_socket()
        logging.log(logging.INFO, "Listen alice connection")
        while True:
            # Waitting alice connection
            try:
                alice_conn, alice_addr = alice_socket.accept()
            except Exception as e:
                logging.log(logging.DEBUG, traceback.format_exc())
                exit(0)
            logging.log(logging.INFO, f"Alice {alice_addr} connected")

            # Get client socket
            try:
                client_socket = get_client_socket()
            except OSError as e:
                if e.errno == 10048:
                    logging.log(logging.DEBUG, e)
                    pass
                elif e.errno == 98:
                    logging.log(logging.DEBUG, e)
                    pass
                else:
                    logging.log(logging.DEBUG, traceback.format_exc())
                    exit(0)
            except Exception as e:
                logging.log(logging.DEBUG, traceback.format_exc())
                exit(0)

            # Listen client connection
            logging.log(logging.INFO, "Listen client connection")
            try:
                client_conn, client_addr = client_socket.accept()
            except Exception as e:
                logging.log(logging.DEBUG, traceback.format_exc())
                exit(0)
            logging.log(logging.INFO, f"Client {alice_addr} connected")

            flag_continue = False
            while True:
                # Receive alice data
                try:
                    data = alice_conn.recv(self.buffer_size)
                except socket.timeout as e:
                    logging.log(logging.DEBUG, "alice timeout: "+traceback.format_exc())
                    flag_continue = True
                    break
                except Exception as e:
                    logging.log(logging.DEBUG, traceback.format_exc())
                    exit(0)
                logging.log(logging.INFO, f"Receive alice data {len(data)}")

                if not data:
                    logging.log(logging.DEBUG, "Receive empty data from alice")
                    break
                
                # Send client data
                try:
                    client_conn.send(data)
                except OSError as e:
                    if e.errno == 10054:
                        logging.log(logging.INFO, "Client close connection")
                        flag_continue = True
                        break
                    else:
                        logging.log(logging.DEBUG, traceback.format_exc())
                        exit(0)
                except Exception as e:
                    logging.log(logging.DEBUG, traceback.format_exc())
                    exit(0)
                logging.log(logging.INFO, f"Send client data {len(data)}")

                if len(data) < self.buffer_size:
                    logging.log(logging.DEBUG, "Receive data size less than last data size")
                    break
            if flag_continue:
                continue

            flag_continue = False
            while True:
                # Receive client data
                try:
                    data = client_conn.recv(self.buffer_size)
                except socket.timeout as e:
                    logging.log(logging.DEBUG, "client timeout: "+traceback.format_exc())
                    flag_continue = True
                    break
                except OSError as e:
                    if e.errno == 10054:
                        logging.log(logging.DEBUG, "Client close connection")
                        flag_continue = True
                        break
                    else:
                        logging.log(logging.DEBUG, traceback.format_exc())
                        exit(0)
                except Exception as e:
                    logging.log(logging.DEBUG, traceback.format_exc())
                    exit(0)
                logging.log(logging.INFO, f"Receive client data {len(data)}")

                if not data:
                    logging.log(logging.DEBUG, "Receive empty data from alice")
                    break

                # Send alice data
                try:
                    alice_conn.send(data)
                except Exception as e:
                    logging.log(logging.DEBUG, traceback.format_exc())
                    exit(0)
                logging.log(logging.INFO, f"Send alice data {len(data)}")

                if len(data) < self.buffer_size:
                    logging.log(logging.DEBUG, "Receive data size less than last data size")
                    break
            if flag_continue:
                continue

            client_conn.shutdown(0)
            logging.log(logging.INFO, "Close client connection")

class ClientConnecter(threading.Thread):
    def __init__(self, server_connect_addr: socket.socket, bob_connect_addr: socket.socket, buffer_size=2048):
        super().__init__()
        self.server_connect_addr = server_connect_addr
        self.bob_connect_addr = bob_connect_addr
        self.buffer_size = buffer_size

    def run(self) -> None:
        def get_server_socket():
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return server_socket

        def get_bob_socket():
            bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return bob_socket

        while True:
            server_socket = get_server_socket()

            # Connect server
            try:
                server_socket.connect(self.server_connect_addr)
            except ConnectionRefusedError as e:
                logging.log(logging.DEBUG, e)
                continue
            except TimeoutError as e:
                logging.log(logging.DEBUG, e)
                continue
            except OSError as e:
                if e.errno == 10056:
                    pass
                elif e.errno == 10061:
                    logging.log(logging.INFO, "Connect server is refused")
                    server_socket.close()
                    continue
                else:
                    logging.log(logging.DEBUG, traceback.format_exc())
                    exit(0)
            except Exception as e:
                logging.log(logging.DEBUG, traceback.format_exc())
                exit(0)
            logging.log(logging.INFO, "Connect server success")

            # Connect bob socket
            while True:
                bob_socket = get_bob_socket()
                try:
                    bob_socket.connect(self.bob_connect_addr)
                except OSError as e:
                    if e.errno == 10056:
                        pass
                    elif e.errno == 10061:
                        logging.log(logging.INFO, "Connect bob is refused")
                        bob_socket.close()
                        continue
                    else:
                        logging.log(logging.DEBUG, traceback.format_exc())
                        exit(0)
                except Exception as e:
                    logging.log(logging.DEBUG, traceback.format_exc())
                    exit(0)
                break

            flag_continue = False
            last_data_size = 0
            while True:
                # Receive server data
                try:
                    data = server_socket.recv(self.buffer_size)
                except socket.timeout as e:
                    logging.log(logging.INFO, "Receive server timeout")
                    flag_continue = True
                    break
                except ConnectionResetError as e:
                    logging.log(logging.INFO, "Server reset connection")
                    flag_continue = True
                    break
                except Exception as e:
                    logging.log(logging.DEBUG, traceback.format_exc())
                    exit(0)
                logging.log(logging.INFO, f"Receive server data {len(data)}")

                if not data:
                    break

                # Send data to bob
                try:
                    bob_socket.send(data)
                except Exception as e:
                    logging.log(logging.DEBUG, traceback.format_exc())
                    exit(0)
                logging.log(logging.INFO, f"Send bob data {len(data)}")

                if len(data) < last_data_size:
                    break
                if last_data_size == 0 and len(data) < self.buffer_size:
                    break
                last_data_size = len(data)
            if flag_continue:
                continue

            flag_continue = False
            last_data_size = 0
            while True:
                # Receive data from bob
                try:
                    data = bob_socket.recv(self.buffer_size)
                except socket.timeout as e:
                    logging.log(logging.INFO, "Receive bob timeout")
                    flag_continue = True
                    break
                except Exception as e:
                    logging.log(logging.DEBUG, traceback.format_exc())
                    exit(0)
                logging.log(logging.INFO, f"Receive bob data {len(data)}")

                if not data:
                    break

                # Send data to server
                try:
                    server_socket.send(data)
                except Exception as e:
                    logging.log(logging.DEBUG, traceback.format_exc())
                    exit(0)
                logging.log(logging.INFO, f"Send server data {len(data)}")

                if len(data) < last_data_size:
                    break
                if last_data_size == 0 and len(data) < self.buffer_size:
                    break
                last_data_size = len(data)
            if flag_continue:
                continue

            # Close socket
            server_socket.shutdown(0)
            logging.log(logging.INFO, "Close server connection")
            bob_socket.shutdown(0)
            logging.log(logging.INFO, "Close bob connection")