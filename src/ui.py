from citation import Citation
from doi_service import get_citation_from_doi
import signal, sys, os
import re

class UI:
    def __init__(self, io, citation_repository):
        self.citation_repository = citation_repository
        self.io = io
        self.commands = {
            "help": (self._help, "Print this help message"),
            "create": (self._create, "Create new publication citation"),
            "doi": (self._doi, "Import citation from DOI (Digital Object Identifier)"),
            "print": (self._print_all, "Print all citations"),
            "export": (self._export, "Export citations in bibtex format"),
            "select": (self._select, "Select an existing citation to interact with"),
        }

    def _quit(self, signal = None, frame = None):
        self.io.write("\nGoodbye!")
        sys.exit(0)

    def start(self):
        signal.signal(signal.SIGINT, self._quit)
        self.io.write("Welcome!\nType \"help\" for help.")
        self.io.write("Type \"create\" to create a new publication citation")
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

    def _add_keywords(self, citation: Citation):
        keywords = []
        self.io.write("Add keywords: ")
        while True:
            keyword = self.io.read("Keyword: ")
            if not keyword:
                break
            keywords.append(keyword)
        citation.keywords += keywords
    
    def _create(self):
        while True:
            citation_type = self.io.read("Which type of publication would you like to create?\n(article or inproceedings, empty to cancel): ")
            if not citation_type:
                self.io.write("Cancelled creating citation\n")
                return
            if citation_type == "article" or citation_type == "inproceedings":
                break
            self.io.write("Unfortunately that type is not supported\n")
        if citation_type == "article":
            self.io.write("Adding new article")
        if citation_type == "inproceedings":
            self.io.write("Adding new inproceedings")
        identifier = self.io.read("Give citation identifier: ")
        authors = []
        while True:
            author = self.io.read("Give publication author/authors\nformat: Firstname Lastname or Lastname, Firstname (Press Enter to continue): ")
            if not author or author.strip()=="":
                if not authors:
                    print("Invalid input: No authors!")
                    continue
                break   
            authors.append(author)
        title = self.io.read("Give publication title: ")
        if citation_type == "article":
            journal = self.io.read("Give article journal: ")
            while True:
                year = self.io.read("Give publication year: ")
                if year == "": break
                try:
                    year = int(year)
                    break
                except ValueError:
                    self.io.write("Invalid year")
            volume = self.io.read("Give journal volume: ")
            pages = self.io.read("Give pages of article: ")
            fields = {
                "author": authors,
                "title": title,
                "journal": journal,
                "year": year,
                "volume": volume,
                "pages": pages
            }
        if citation_type == "inproceedings":
            while True:
                year = self.io.read("Give publication year: ")
                if year == "": break
                try:
                    year = int(year)
                    break
                except ValueError:
                    self.io.write("Invalid year")
            booktitle = self.io.read("Give inproceedings booktitle: ")
            fields = {
                "author": authors,
                "title": title,
                "year": year,
                "booktitle": booktitle
            }
        new_citation = Citation(
            citation_type,
            identifier,
            fields
        )
        self._add_keywords(new_citation)
        self.citation_repository.add_new(new_citation)

        self.io.write(f"Publication {identifier} added.")

    def _doi(self):
        doi = ""
        regex = r"10(.\d{4,})+\/\d+(.\d+)*" # Matches any valid DOI
        while True:
            self.io.write("Give DOI string or an URL containing a DOI string.")
            doi = self.io.read("DOI: ")
            match = re.search(regex, doi)
            if not match:
                self.io.write("Invalid DOI")
                continue
            doi = match.group()
            break
        citation = get_citation_from_doi(doi)
        if not citation:
            self.io.write("An error occurred when requesting content")
            return
        
        self.io.write(f"Citation {citation.key} imported succesfully.")
        
        self._add_keywords(citation)

        self.citation_repository.add_new(citation)

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
            keys = self.io.read("Enter a keyword/keywords, empty to cancel \nYou can inspect existing keywords by printing all citations\n: ")
            if keys == "":
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
                    action = self.io.read("\nWould you like to:\nedit\nremove\nselected citation? (empty will cancel selection): ")
                    if action == 'remove':
                        try:
                            self.citation_repository.remove_one(matching[choice])
                            self.io.write('\nCitation removed successfully')
                            break
                        except Exception:
                            self.io.write('Removing citation failed')
                    if action == 'edit':
                        try:
                            self._edit_citation(matching[choice])
                            break
                        except Exception as e:
                            self.io.write(e)
                            self.io.write('\nEdition did not succeed, might be limited')
                    if not action:
                        self.io.write('\nexited')
                        break
                    self.io.write('\nSorry, that option isn\'t available')
            else:
                self.io.write('\nNo citations match given keywords')

    def _edit_citation(self, citation: Citation):
        self.io.write('\nIn each attribute, enter new value or if you want to keep current value, keep empty')
        authors = []
        fields = citation.fields
        identifier = self.io.read(f"\nCurrent id is {citation.key}\nGive new identifier: ")
        self.io.write(f"\nCurrent author/s: {', '.join(fields['author'])}")
        while True:
            author = self.io.read("Give new author/authors\nformat: Firstname Lastname or Lastname, Firstname (Press Enter to continue)\nAuthor: ")
            if author == "": break
            elif author.strip() == "":
                print("Error: Invalid input!")
                continue
  
            authors.append(author)


        new_fields = citation.fields.copy()
        new_fields["author"] = authors or citation.fields["author"]
        
        for key in citation.fields.keys():
            if key in ["author", "doi", "url"]: continue
            self.io.write(f"Current {key}: {citation.fields[key]}")
            new_value = ""
            if key == "year":
                while True:
                    year = self.io.read("Give new year: ")
                    if year == "": break
                    try:
                        new_value = int(year)
                        break
                    except ValueError:
                        self.io.write("Invalid year")
            else:
                new_value = self.io.read(f"Give new {key}: ")
            if new_value:
                new_fields[key] = new_value

        keywords = []
        self.io.write(f"\nCurrent keywords: {citation.keywords}")
        self.io.write("Add keywords: ")
        while True:
            keyword = self.io.read("Keyword: ")
            if not keyword:
                break
            keywords.append(keyword)
        

        new_citation = Citation(
            citation.citation_type,
            identifier or citation.key,
            new_fields,
            keywords or citation.keywords
        )
        try:
            self.citation_repository.edit_citation(citation, new_citation)
            self.io.write('\nChanges saved')
        except Exception as e:
            self.io.write(e)
        
