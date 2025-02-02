import threading

import server

web = server.Server()

@web.get("/hello")
def hello():
    return "{\"message\":\"Hello, World!\"}"

@web.get("/about")
def about():
    return "{\"message\":\"This is a simple Python web server\"}"

@web.get("/")
def web_page():
  try:
    with open("index.html", "r") as f:
      return f.read()
  except OSError:
    return "404 Not Found"

def main():
  pass

if __name__ == '__main__':
  web.async_start_server()
  main()
  threading.Event().wait()
