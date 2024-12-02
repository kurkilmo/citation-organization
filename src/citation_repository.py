from citation import Citation
import json
import io


class CitationRepository:
    def __init__(self, file_path="src/citations.json"):
        self._file_path = file_path
        self._citations = self._load_from_file()

    def _load_from_file(self):
        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Citation(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_to_file(self):
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(
                [citation.__dict__ for citation in self._citations], file, ensure_ascii=False, indent=4
            )

    def add_new(self, citation):
        self._citations.append(citation)
        self._save_to_file()

    def get_all(self):
        return self._citations
    
    def delete_all(self):
        self._citations = []
        self._save_to_file()