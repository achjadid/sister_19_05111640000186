import shlex
import os


class GreetServer(object):
    def __init__(self):
        pass
		
    def command_success(self):
        return "command success"

    def bye(self) -> str:
        return "exit success"
		
    def commands(self) -> str:
        return "1. list: list -a / -all\n" \
               "2. create: create filename1 filename2 filename3\n" \
               "3. read: 'read filename'\n" \
               "4. delete: delete filename1 filename2 filename3\n" \
               "5. update: update --append / -a, -overwrite / -o\n" \
               "6. exit: exit"

    def delete_file(self, path, name) -> str:
        result = self.command_success()
        try:
            os.remove(os.path.join(path, name))
        except Exception as e:
            return str(e)
        return result

    def _process_file(self, path, name, operation, *args, **kwargs) -> str:
        result = self.command_success()
        try:
            f = open(os.path.join(path, name), operation)
            if operation == "r":
                result = f.read()
            elif operation == "a+":
                f.write(kwargs.get('content', None))
            f.close()

        except Exception as e:
            return str(e)
        return result

    def _root_folder_exists(self, root):
        if not os.path.exists(root):
            os.makedirs(root)

    def _get_storage_path(self) -> str:
        root = os.path.dirname(os.path.abspath(__file__)) + "/storage"
        self._root_folder_exists(root)
        return root

    def get_list(self, req) -> str:
        args = req.split()
        dirs = os.listdir(self._get_storage_path())
        result = ""
        if len(args) == 1:
            for dir in dirs:
                result = result + "{}   ".format(dir)
        elif len(args) == 2 and args[1] in ["-a", "-all"]:
            result = result + "."
            for dir in dirs:
                result = result + "\n{}".format(dir)
        else:
            result = "command not found"
        return result

    def create(self, req) -> str:
        args = shlex.split(req)
        dirs = self._get_storage_path()
        result = ""
        if len(args) > 1:
            for file_name in args[1:]:
                result = self._process_file(dirs, file_name, "w+")
                if result != self.command_success():
                    return result
        else:
            result = "command not found"
        return result

    def delete(self, req) -> str:
        args = shlex.split(req)
        dirs = self._get_storage_path()
        result = ""
        if len(args) > 1:
            for file_name in args[1:]:
                result = self.delete_file(dirs, file_name)
                if result != self.command_success():
                    return result
        else:
            result = "command not found"
        return result

    def read(self, req) -> str:
        args = shlex.split(req)
        dirs = self._get_storage_path()
        result = ""
        if len(args) > 1:
            result = self._process_file(dirs, args[1], "r")
        else:
            result = "command not found"
        return result

    def update(self, req):
        args = shlex.split(req)
        dirs = self._get_storage_path()
        result = ""
        if len(args) == 4:
            if args[1] in ["-append", "-a"]:
                result = self._process_file(dirs, args[2], "a+", content=args[3])
            elif args[1] in ["-overwrite", "-o"]:
                result = self._process_file(dirs, args[2], "w")
                result = self._process_file(dirs, args[2], "a+", content=args[3])
            else:
                result = "command not found"
        else:
            result = "command not found"
        return result