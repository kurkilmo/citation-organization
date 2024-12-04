from citation import Citation
import signal, sys, os

class UI:
    def __init__(self, io, citation_repository):
        self.citation_repository = citation_repository
        self.io = io
        self.commands = {
            "help": (self._help, "Print this help message"),
            "create": (self._create, "Create new article citation"),
            "print": (self._print_all, "Print all citations"),
            "export": (self._export, "Export citations in bibtex format")
        }

    def handle_SIGINT(self, signal, frame):
        self.io.write("\nGoodbye!")
        sys.exit(0)

    def start(self):
        signal.signal(signal.SIGINT, self.handle_SIGINT)
        self.io.write("Welcome!\nType \"help\" for help.")
        self.io.write("Type \"create\" to create a new article citation")
        while True:
            command = self.io.read("> ")
            if not command: break
            try:
                cmd = self.commands[command][0]
                cmd()
            except KeyError:
                self.io.write("Unknown command")

    def _help(self):
        self.io.write("Available commands:\n")
        for key in self.commands:
            self.io.write(f"{key}: {self.commands[key][1]}")
    
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
        keywords = []
        self.io.write("Add keywords: ")
        while True:
            keyword = self.io.read("Keyword: ")
            if not keyword:
                break
            keywords.append(keyword)

        self.citation_repository.add_new(
            Citation(
                "article",
                identifier,
                {
                    "author": author,
                    "title": title,
                    "journal": journal,
                    "year": year,
                    "volume": volume,
                    "pages": pages
                },
                keywords
            )
        )

        self.io.write(f"Article {identifier} added.")

    def _print_all(self):
        citations = self.citation_repository.get_all()
        for citation in citations:
            self.io.write('\n' + str(citation))
    
    def _export(self):
        working_path = os.getcwd()
        filename = self.io.read(
            f"""Give file path for export:
(relative to working path {working_path})
> """)
        succeed = self.citation_repository.export_all(filename)
        if succeed:
            self.io.write(f"Successfully wrote to {filename}")
        else:
            self.io.write("Error while writing")
