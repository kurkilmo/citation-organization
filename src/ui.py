from console_io import ConsoleIO

class UI:
    def __init__(self, io):
        self.io = io

    def start(self):
        while True:
            command = self.io.read("> ")
            match command:
                case "create":
                    self._create()
                case "print":
                    self._print_all()
                case "":
                    break
    
    def _create(self):
        self.io.write("created")

    def _print_all(self):
        self.io.write("all printed")