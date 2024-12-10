from citation import Citation
import json
import io


class CitationRepository:
    def __init__(self, file_path="citations.json"):
        self._file_path = file_path
        self._citations = self._load_from_file()

    def _load_from_file(self):
        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Citation(item['citation_type'], item['key'], item['fields'], item.get('keywords', [])) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_to_file(self):
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(
                [vars(citation) for citation in self._citations], file, ensure_ascii=False, indent=4
            )

    def add_new(self, citation):
        self._citations.append(citation)
        self._save_to_file()

    def remove_one(self, citation):
        index = self._citations.index(citation)
        self._citations.pop(index)
        self._save_to_file()

    def edit_citation(self, citation, fields):
        #print(fields['authors'])
        print(citation.fields['authors'])
        if not fields['authors']:
            fields['authors'] = citation.fields['authors']
        self._save_to_file()


    def get_all(self):
        return self._citations
    
    def delete_all(self):
        self._citations = []
        self._save_to_file()
    
    def export(self, filename, keywords):
        '''Exports citations in bibtex format.
Returns True if succesful.'''
        try:
            with open(filename, "w") as file:
                for citation in self._citations:
                    include = len(
                        set(keywords).intersection(set(citation.keywords))
                    ) > 0 or not keywords

                    if include:
                        file.writelines(str(citation)+'\n\n')
                return True
        except:
            return False
    