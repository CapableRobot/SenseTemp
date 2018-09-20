# import socket
# addr = socket.getaddrinfo('0.0.0.0', 8000)[0][-1]

# s = socket.socket()
# s.bind(addr)
# s.listen(1)

# while True:
#     cl, addr = s.accept()
#     print('client connected from', addr)
#     cl_file = cl.makefile('rwb', 0)


#     while True:
#         line = cl_file.readline()
#         print('  :', line)
#         if not line or line == b'\r\n':
#             break

#     lines = ["["]
#     lines.append("  {'id':0, 'temp':%.2f}" % sensor.temperature)
#     lines.append("]")

#     cl.send('\n'.join(lines))
#     cl.close()