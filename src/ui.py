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
        export_all = False
        while True:
            cmd = self.io.read("Export all citations? [Y/n] > ").lower().strip()
            if cmd == 'y' or cmd == "":
                export_all = True
                break
            elif cmd == 'n': break
            else:
                print("Invalid option, specify 'y' or 'n' for yes/no or empty input for yes")

        keywords = []
        if not export_all:
            available_keywords = []
            for citation in self.citation_repository.get_all():
                available_keywords += citation.keywords
            self.io.write("Available keywords: " + ", ".join(set(available_keywords)))
            while True:
                keyword = self.io.read(
                    "Give keyword to include in export, empty input proceeds:\n> "
                ).strip()
                if not keyword: break
                if keyword not in available_keywords:
                    self.io.write("Unknown keyword")
                    continue
                keywords.append(keyword)

        working_path = os.getcwd()
        filename = self.io.read(
            f"""Give file path for export:
(relative to working path {working_path})
> """)
        succeed = self.citation_repository.export(filename, keywords)
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

    def _edit_citation(self, citation: Citation):
        self.io.write('\n in each attribute, enter new value or if you want to keep current value, keep empty')
        authors = []
        identifier = self.io.read("Give article identifier: ")
        while True:
            author = self.io.read("Give article author/authors\nformat: first name last name or last name, first name (Press Enter to continue): ")
            if author == "": break
            elif author.strip() == "":
                print("Error: Invalid input!")
                continue
  
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
        fields = citation.fields
        new_citation = Citation(
            "article",
            identifier or citation.key,
            {
                "authors" : authors or fields["authors"],
                "title" : title or fields["title"],
                "journal": journal or fields["journal"],
                "year": year or fields["year"],
                "volume": volume or fields["volume"],
                "pages": pages or fields["pages"],
            },
            keywords or citation.keywords
        )
        try:
            self.citation_repository.edit_citation(citation, new_citation)
            self.io.write('\nChanges saved')
        except Exception as e:
            self.io.write(e)
        
