from citation import Citation
from citation_repository import CitationRepository

class CitationLibrary:
    def __init__(self):
        self.repo = CitationRepository("src/tests/tests.json")

    def add_new_citation(self, author, title):
        """Add New Citation"""
        citation = Citation("article", "key", {"author": author, "title": title})
        self.repo.add_new(citation)

    def get_all_citations(self):
        """Get All Citations"""
        return [f"{c.fields["author"]}: {c.fields["title"]}" for c in self.repo.get_all()]
    
    def empty_file(self):
        """create empty json file"""
        self.repo.delete_all()
    