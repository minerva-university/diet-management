import platform

port = 5000
system = platform.system()
if 'Linux' in system:
    host = '172.17.0.1'
else:
    host = 'host.docker.internal'
