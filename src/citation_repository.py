from citation import Citation


class CitationRepository:
    def __init__(self):
        self._citations = []

    def add_new(self, citation):
        citations = self.get_all()
        citations.append(citation)
        self._citations = citations

    def get_all(self):
        return self._citations