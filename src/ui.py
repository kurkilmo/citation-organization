class UI:
    def __init__(self, io, citation_repository):
        self.citation_repository = citation_repository
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
        self.io.write("Adding new article")
        identifier = self.io.read("Give citation identifier: ")
        author = self.io.read("Give article author: ")
        title = self.io.read("Give article title: ")
        journal = self.io.read("Give article journal: ")
        while True:
            year = self.io.read("Give article year: ")
            if year == "": break
            try:
                year = int(year)
                break
            except ValueError:
                self.io.write("Invalid year")
        volume = self.io.read("Give journal volume: ")
        pages = self.io.read("Give pages of article: ")

        citation = [identifier, author, title, journal, year, volume, pages]
        self.io.write(citation)
        self.citation_repository.add_new(citation)

    def _print_all(self):
        citations = self.citation_repository.get_all()
        self.io.write("all printed")
