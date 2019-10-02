import socket
import sys
import threading


max_conn = 5
buffer_size = 8192


def start():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 8001))
    s.listen(1)
    print('\n[*] Initiliazing Sockets ... Done')
    print('\n[*] Socket Binding Successfully')
    print(f'\n[*] Server Started Successfully ')
    print('\n[*] ')
  except Exception:
    print(' Unable to Initialize Socket')
    sys.exit(2)

  while 1:
    try:
      conn, addr = s.accept()
      data = conn.recv(buffer_size)
      threading.Thread(None, conn_string, (conn, data, addr))
    except KeyboardInterrupt:
      s.close()
      print('Shutting down ***')
      sys.exit(1)


def conn_string(conn, data, addr):
  try:
    first_line = data.split('\n')[0]
    url = first_line.split(' ')[1]

    http_pos = url.find('://')
    if http_pos == -1:
      temp = url
    else:
      temp = url[(http_pos+3):]

    port_pos = temp.find(':')
    webserver_pos = temp.find('/')
    if webserver_pos == -1:
      webserver_pos = len(temp)

    webserver = ''
    port = -1
    if port == -1 or webserver_pos < port_pos:
      port = 80
      webserver = temp[:webserver_pos]
    else:
      port = int((temp[(port_pos + 1):])[:webserver_pos-port_pos - 1])
      webserver = temp[:port_pos]
  except Exception as e:
    print(f'error {e}')


def proxy_server(webserver, port, conn, data, addr):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(data)
    while 1:
      reply = s.recv(buffer_size)

      if len(reply) > 0:
        conn.send(reply)
        dar = float(len(reply))
        dar = float(dar/1024)
        dar = "%.3s" % (str(dar))
        dar = "%s KB" % (dar)
        print(f"request done {str(addr[0])} => {str(dar)} <=")
      else:
        break
    s.close()
    conn.close()
  except socket.error:
    s.close()
    conn.close()
    sys.exit(1)


start()
