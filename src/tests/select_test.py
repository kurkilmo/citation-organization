import unittest
import os
from src.in_out.stub_io import StubIO
from src.ui import UI
from src.citation_repository import CitationRepository
from . import *

class TestSelect(unittest.TestCase):
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

    def test_can_delete_citation(self):
        self.io.add_input("select")
        self.io.add_input("keyword1")
        self.io.add_input("remove")
        self.io.add_input("exit")
        self.ui.start()

        self.io.add_input("print")
        self.ui.start()

        found = False
        for output in self.io.outputs:
            if str(test_citations[0]) in output:
                found = True
        self.assertTrue(found)
        
