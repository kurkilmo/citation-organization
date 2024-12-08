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
            "export": (self._export, "Export citations in bibtex format"),
            "select": (self._select, "Select an existing citation to interact with")
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
        authors = []
        while True:
            author = self.io.read("Give article author/authors\nformat: first name last name or last name, first name (Press Enter to continue): ")
            if(author.strip()==""):
                print("Error: Invalid input!")
            if not author:
                if not authors:
                    print("Invalid input: No authors!")
                    continue
                break   
            authors.append(author)
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
                    "authors": authors,
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

    def _select(self):
        citations = self.citation_repository.get_all()
        if not citations:
            self.io.write('\nThere are no citations yet')
            return
        while True:
            matching = []
            keys = self.io.read("Enter a keyword/keywords (type exit to exit): ")
            if keys == 'exit':
                break
            i = 0
            for citation in citations:
                if keys in citation.keywords:
                    self.io.write(f'\n numero {str(i)}:\n {str(citation)}')
                    matching.append(citation)
                    i+=1
            
            if len(matching) > 0:
                choice = 0
                if len(matching) > 1:
                    while True:
                        which = self.io.read("Which one to interact with? (type number): ")
                        try:
                            if int(which) < len(matching):
                                choice = int(which)
                                break
                            else:
                                self.io.write("Give one of the displayed numbers\n")
                        except ValueError:
                            self.io.write("Please enter a number\n")
                while True:
                    action = self.io.read("Would you like to:\nedit\nremove\nselected citation? (empty will cancel selection): ")
                    if action == 'remove':
                        try:
                            self.citation_repository.remove_one(matching[choice])
                            self.io.write('\nCitation removed successfully')
                            break
                        except Exception:
                            self.io.write('ei onnistunu tämä näi nyt')
                    if action == 'edit':
                        try:
                            self._edit_citation(matching[choice])
                            break
                        except Exception:
                            self.io.write('\nEdition did not succeed, might be limited')
                    if not action:
                        self.io.write('\nexited')
                        break
                    self.io.write('\nSorry, that option isn\'t available')
            else:
                self.io.write('\nNo citations match given keywords')

    def _edit_citation(self, citation):
        self.io.write('\n in each attribute, enter new value or if you want to keep current value, keep empty')
        authors = []
        while True:
            author = self.io.read("Give article author/authors\nformat: first name last name or last name, first name (Press Enter to continue): ")
            if(author.strip()==""):
                print("Error: Invalid input!")
            if not author:
                if not authors:
                    print("Invalid input: No authors!")
                    continue
                break   
            authors.append(author)
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
        newFields = {
                        "authors": authors,
                        "title": title,
                        "journal": journal,
                        "year": year,
                        "volume": volume,
                        "pages": pages,
                        "keywords": keywords
                    }
        try:
            self.citation_repository.edit_citation(citation, newFields)
            self.io.write('\nChanges saved')
        except Exception as e:
            self.io.write(e)
        
