import Pyro4
import sys

namainstance = sys.argv[1] or "fileserver"

def get_fileserver_object():
    uri = "PYRONAME:{}@localhost:7777" . format(namainstance)
    fserver = Pyro4.Proxy(uri)
    fserver.pyro_connect()
    return fserver

if __name__ == '__main__':

    f = get_fileserver_object()
    print("Command list: list, create 'FILENAME', read 'FILENAME', delete 'FILENAME', update 'FILENAME' ")
    while True:
        str = input("> ").split()
        if str[0] == "list":
            print(f.list())
        elif str[0] == "create":
            print(f.create(str[1]))
        elif str[0] == "read":
            print(f.read(str[1]))
        elif str[0] == "delete":
            print(f.delete(str[1]))
        elif str[0] == "update":
            print(f.update(str[1], str[2]))
        elif (str[0] == 'exit'):
            exit()
        else:
            print("Please check your input")