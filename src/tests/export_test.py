import unittest
import sys, os
from src.in_out.stub_io import StubIO
from src.ui import UI
from src.citation_repository import CitationRepository
from src.citation import Citation

class TestExport(unittest.TestCase):
    def _create_citation(self, id, authors, title, journal, year, volume, pages, keywords):
        self.io.add_input("create")
        self.io.add_input(id)
        for author in authors:
            self.io.add_input(author)
        self.io.add_input("")
        self.io.add_input(title)
        self.io.add_input(journal)
        self.io.add_input(year)
        self.io.add_input(volume)
        self.io.add_input(pages)
        for key in keywords:
            self.io.add_input(key)
        self.io.add_input("")


    def setUp(self):
        self.test_file = "test_citations.json"
        self.export_file = "test_export.bib"
    
        self.io = StubIO()
        self.ui = UI(
            self.io,
            CitationRepository(self.test_file)
        )

        # Test citations
        self.test_citations = [
            Citation(
                "article",
                "ID1",
                {
                    "authors": ["Pekka Kirjoittaja", "Toimittaja, Tero"],
                    "title": "Otsikko",
                    "journal": "Lehti",
                    "year": 2000,
                    "volume": "2",
                    "pages": "2--300"
                },
                ["keyword1", "keyword2"],
            ),
            Citation(
                "article",
                "ID2",
                {
                    "authors": ["Janne Jannela", "Meikäläinen, Matti"],
                    "title": "Tämä ei ole otsikko",
                    "journal": "Vappulehti",
                    "year": 2001,
                    "volume": "5",
                    "pages": "3--400",
                },
                ["keyword2", "keyword3"]
            ),
            Citation(
                "article",
                "ID3",
                {
                    "authors": ["Kekkonen, Urho", "Räty, Seppo"],
                    "title": "Hiihtää hiihtää",
                    "journal": "Hesari",
                    "year": 1970,
                    "volume": "4",
                    "pages": "1--2",
                },
                ["keyword3", "keyword4"]
            )
        ]

        for citation in self.test_citations:
            self._create_citation(
                citation.key,
                citation.fields["authors"],
                citation.fields["title"],
                citation.fields["journal"],
                str(citation.fields["year"]),
                citation.fields["volume"],
                citation.fields["pages"],
                citation.keywords
            )

    def tearDown(self):
        for file in [self.export_file, self.test_file]:
            if os.path.exists(file):
                os.remove(file)
        return super().tearDown()

    def test_export_all(self):
        self.io.add_input("export")
        self.io.add_input("y")
        self.io.add_input(self.export_file)
        self.ui.start()
        with open(self.export_file) as file:
            data = file.read()
            for cit in self.test_citations:
                self.assertIn(str(cit), data)
    
    def test_export_keyword_matching_one_citation(self):
        self.io.add_input("export")
        self.io.add_input("n")
        self.io.add_input("keyword1")
        self.io.add_input("")
        self.io.add_input(self.export_file)
        self.ui.start()

        with open(self.export_file) as file:
            data = file.read()
            self.assertIn(str(self.test_citations[0]), data)
            self.assertNotIn(str(self.test_citations[1]), data)
            self.assertNotIn(str(self.test_citations[2]), data)
    
    def test_export_keyword_matching_two_citations(self):
        self.io.add_input("export")
        self.io.add_input("n")
        self.io.add_input("keyword2")
        self.io.add_input("")
        self.io.add_input(self.export_file)
        self.ui.start()

        with open(self.export_file) as file:
            data = file.read()
            self.assertIn(str(self.test_citations[0]), data)
            self.assertIn(str(self.test_citations[1]), data)
            self.assertNotIn(str(self.test_citations[2]), data)
