import socket
from functools import wraps
import _thread

class Server:
  HOST = "127.0.0.1"  # Localhost
  PORT = 8085  # Port to listen on

  def __init__(self, host=HOST, port=PORT):
    self.__routes = {}
    self.__host = host
    self.__port = port

  def async_start_server(self):
    _thread.start_new_thread(self.start_server, ())

  def get(self, path):
      """Decorator to register a function for a specific GET path."""
      def decorator(func):
          @wraps(func)
          def wrapper():
              return func()
          self.__routes[path] = wrapper
          return wrapper
      return decorator



  def __handle_request(self, request):
      """Parses the request and returns the appropriate response."""
      lines = request.split("\r\n")
      if not lines or len(lines[0].split()) < 2:
          return "HTTP/1.1 400 Bad Request\nContent-Type: text/html\n\n<h1>400 Bad Request</h1>"

      method, path = lines[0].split()[:2]

      if method != "GET":
          return "HTTP/1.1 405 Method Not Allowed\nContent-Type: text/html\n\n<h1>405 Method Not Allowed</h1>"

      # Check if the path exists in routes
      if path in self.__routes:
          response_body = self.__routes[path]()
          return f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n{response_body}"
      else:
          return "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n<h1>404 Not Found</h1>"

  def start_server(self):
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((self.__host, self.__port))
    server_socket.listen(5)  # Listen for incoming connections

    print(f"Server running on {self.__host}:{self.__port}...")

    while True:
      client_socket, addr = server_socket.accept()  # Accept a connection
      print(f"Connected by {addr}")

      request = client_socket.recv(1024).decode()  # Receive request
      print(f"Request:\n{request}")

      client_socket.sendall(self.__handle_request(request).encode())  # Send response

      client_socket.close()  # Close connection
