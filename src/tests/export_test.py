import unittest
import os
from src.in_out.stub_io import StubIO
from src.ui import UI
from src.citation_repository import CitationRepository
from . import *

class TestExport(unittest.TestCase):
    def setUp(self):
    
        self.io = StubIO()
        self.ui = UI(
            self.io,
            CitationRepository(test_file)
        )

        for citation in test_citations:
            create_article(
                self.io,
                citation.key,
                citation.fields["author"],
                citation.fields["title"],
                citation.fields["journal"],
                str(citation.fields["year"]),
                citation.fields["volume"],
                citation.fields["pages"],
                citation.keywords
            )

    def tearDown(self):
        for file in [export_file, test_file]:
            if os.path.exists(file):
                os.remove(file)
        return super().tearDown()

    def test_export_all(self):
        self.io.add_input("export")
        self.io.add_input("y")
        self.io.add_input(export_file)
        self.ui.start()
        with open(export_file) as file:
            data = file.read()
            for cit in test_citations:
                self.assertIn(str(cit), data)
    
    def test_export_keyword_matching_one_citation(self):
        self.io.add_input("export")
        self.io.add_input("n")
        self.io.add_input("keyword1")
        self.io.add_input("")
        self.io.add_input(export_file)
        self.ui.start()

        with open(export_file) as file:
            data = file.read()
            self.assertIn(str(test_citations[0]), data)
            self.assertNotIn(str(test_citations[1]), data)
            self.assertNotIn(str(test_citations[2]), data)
    
    def test_export_keyword_matching_two_citations(self):
        self.io.add_input("export")
        self.io.add_input("n")
        self.io.add_input("keyword2")
        self.io.add_input("")
        self.io.add_input(export_file)
        self.ui.start()

        with open(export_file) as file:
            data = file.read()
            self.assertIn(str(test_citations[0]), data)
            self.assertIn(str(test_citations[1]), data)
            self.assertNotIn(str(test_citations[2]), data)
