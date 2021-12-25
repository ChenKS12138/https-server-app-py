# from infra.https import HttpsServer
# import socket
# import io


# srv = HttpsServer()


# srv.bind_addr = ("0.0.0.0", 3000)
# srv.cert = "./script/server.cert.pem"
# srv.key = "./script/server.private.pem"


# def on_request(conn: socket.socket):
#     conn.send("hello".encode())

#     conn.close()


# srv.launch(on_request)


# while True:
#     pass

from infra.http.message import Response

# headers = map()
# headers["Content-Type"] = "text/plain"

# r = Response(headers=headers, code=200, body=bytes())
# print(r)
print(bytes())
