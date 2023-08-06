import threading
import logging
import select
import socket
import json
import hmac
import binascii
import os
from commons.metaclasses import ServerVerifier
from commons.descryptors import Port
from commons.commons import *
from commons.utils import send_message, get_message


logger = logging.getLogger('server')


class MessageProcessor(threading.Thread):

    """
    The main class of the server.
    Accepts connections, dictionary packets from clients,
    processes incoming messages.
    Works as a separate thread.
    The constructor accepts positional arguments:
    the values of the ip address and port on which it will be launched,
    and the database object.
    """

    port = Port()

    def __init__(self, listen_address, listen_port, database):

        self.addr = listen_address
        self.port = listen_port
        self.database = database

        self.sock = None

        self.clients = []

        self.listen_sockets = None
        self.error_sockets = None

        self.running = True

        # Dict includes items -  name client: socket
        self.names = dict()

        super().__init__()

    def run(self):

        """
        A method that implements the main flow cycle.
        Overloaded method of the parent Thread class
        """

        self.init_socket()

        # main cycle
        while self.running:
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                logger.info(f"Connection established with PC {client_address}")
                client.settimeout(5)
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            try:
                if self.clients:
                    recv_data_lst, self.listen_sockets, self.error_sockets = select.select(
                        self.clients, self.clients, [], 0)
            except OSError as err:
                logger.error(f"Error working with sockets: {err.errno}")

            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_message(get_message(client_with_message), client_with_message)
                    except (OSError, json.JSONDecodeError, TypeError) as err:
                        logger.debug(f"Getting data from client exception.", exc_info=err)
                        self.remove_client(client_with_message)

    def init_socket(self):

        """A method of creating and configuring a server socket."""

        logger.info(f"Start server without parameters: {self.addr}, {self.port}")

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        self.sock = transport
        self.sock.listen(MAX_CONNECTIONS)

    def process_message(self, message):

        """The method of sending messages to the client.
        Enables user verification in the list of connected users.
        If it is not there, then the user deletion function is called.
        """

        if message[DESTINATION] in self.names and self.names[message[DESTINATION]] in self.listen_sockets:
            try:
                send_message(self.names[message[DESTINATION]], message)
                logger.info(
                    f"Send message to user {message[DESTINATION]} from user {message[SENDER]}.")
            except OSError:
                self.remove_client(message[DESTINATION])
        elif message[DESTINATION] in self.names and self.names[message[DESTINATION]] not in self.listen_sockets:
            logger.error(f"Communication with the client {message[DESTINATION]} was lost."
                         f"The connection is closed, delivery is not possible.")
            self.remove_client(self.names[message[DESTINATION]])
        else:
            logger.error(
                f'User {message[DESTINATION]} not registered on the server, sending the message is not possible.')

    def process_client_message(self, message, client):

        """A method that implements the processing of a message from a client."""

        logger.debug(f"Processing client message : {message}")
        # presence
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            self.autorize_user(message, client)
        # message
        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message and self.names[message[SENDER]] == client:
            if message[DESTINATION] in self.names:
                self.database.process_message(
                    message[SENDER], message[DESTINATION])
                self.process_message(message)
                try:
                    send_message(client, RESPONSE_200)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Пользователь не зарегистрирован на сервере.'
                try:
                    send_message(client, response)
                except OSError:
                    pass
            return
        # Quit
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            self.remove_client(client)
        # Get contacts
        elif ACTION in message and message[ACTION] == GET_CONTACTS and USER in message and \
                self.names[message[USER]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = self.database.get_contacts(message[USER])
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)
        # add contact
        elif ACTION in message and message[ACTION] == ADD_CONTACT and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.add_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)
        # delete contact
        elif ACTION in message and message[ACTION] == REMOVE_CONTACT and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.remove_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)
        # get known users
        elif ACTION in message and message[ACTION] == USERS_REQUEST and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0]
                                   for user in self.database.users_list()]
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)
        # get pub key
        elif ACTION in message and message[ACTION] == PUBLIC_KEY_REQUEST and ACCOUNT_NAME in message:
            response = RESPONSE_511
            response[DATA] = self.database.get_pubkey(message[ACCOUNT_NAME])
            if response[DATA]:
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Нет публичного ключа для данного пользователя'
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен.'
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

    def remove_client(self, client):
        """
        The handler method of the client
        which the connection was interrupted.
        Removes the client from the list of connected users
        and from the server database.
        """

        logger.info(f"Client {client.getpeername()} disconnected from the server.")
        for name in self.names:
            if self.names[name] == client:
                self.database.user_logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()

    def autorize_user(self, message, sock):

        """
        A method that implements user authorization.
        Users must first be registered on the server.
        Therefore, if the user is not in the database,
        400 response is returned.
        """

        logger.debug(f'Start auth process for {message[USER]}')
        if message[USER][ACCOUNT_NAME] in self.names.keys():
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            try:
                logger.debug(f'Username busy, sending {response}')
                send_message(sock, response)
            except OSError:
                logger.debug('OS Error')
                pass
            self.clients.remove(sock)
            sock.close()
        elif not self.database.check_user(message[USER][ACCOUNT_NAME]):
            # a block triggered in the case of an unknown user
            response = RESPONSE_400
            response[ERROR] = 'Пользователь не зарегистрирован.'
            try:
                logger.debug(f'Unknown username, sending {response}')
                send_message(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        else:
            logger.debug('Correct username, starting passwd check.')
            message_auth = RESPONSE_511
            random_str = binascii.hexlify(os.urandom(64))
            message_auth[DATA] = random_str.decode('ascii')
            hash = hmac.new(self.database.get_hash(message[USER][ACCOUNT_NAME]), random_str, 'MD5')
            digest = hash.digest()
            logger.debug(f'Auth message = {message_auth}')
            try:
                send_message(sock, message_auth)
                ans = get_message(sock)
            except OSError as err:
                logger.debug('Error in auth, data:', exc_info=err)
                sock.close()
                return
            client_digest = binascii.a2b_base64(ans[DATA])
            if RESPONSE in ans and ans[RESPONSE] == 511 and hmac.compare_digest(
                    digest, client_digest):
                self.names[message[USER][ACCOUNT_NAME]] = sock
                client_ip, client_port = sock.getpeername()
                try:
                    send_message(sock, RESPONSE_200)
                except OSError:
                    self.remove_client(message[USER][ACCOUNT_NAME])
                self.database.user_login(
                    message[USER][ACCOUNT_NAME],
                    client_ip,
                    client_port,
                    message[USER][PUBLIC_KEY])
            else:
                response = RESPONSE_400
                response[ERROR] = 'Неверный пароль.'
                try:
                    send_message(sock, response)
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    def service_update_lists(self):

        """
        A method that implements sending a message to clients
        about updating the list of registered users.
        Response (205).
        """

        for client in self.names:
            try:
                send_message(self.names[client], RESPONSE_205)
            except OSError:
                self.remove_client(self.names[client])
