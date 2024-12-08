import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from citation import Citation
from citation_repository import CitationRepository

class TestCitation(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_citations.json"
        self.citation_repository = CitationRepository(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_new(self):
        test_fields = {"authors": ["Markola, Marko", "Kerkko Möttönen"], "title": "Tutkiminen", "journal": "tutkimuslehti", "year": 2000, "volume": "", "pages": ""}
        citation = Citation("article", "ID1", test_fields, ["Marko", "tutkimus", "viite"])
        self.citation_repository.add_new(citation)
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 1)
        self.assertEqual(citations[0].key, "ID1")
        self.assertEqual(citations[0].fields["authors"][0], "Markola, Marko")
        self.assertEqual(citations[0].fields["title"], "Tutkiminen")
        self.assertEqual(citations[0].fields["pages"], "")
        self.citation_repository.add_new(citation)
        self.assertEqual(len(citations), 2)
        
    def test_remove_one(self):
        test_fields = {"authors": ["Markola, Marko", "Kerkko Möttönen"], "title": "Tutkiminen", "journal": "tutkimuslehti", "year": 2000, "volume": "", "pages": ""}
        citation = Citation("article", "ID1", test_fields, ["Marko", "tutkimus", "viite"])
        self.citation_repository.add_new(citation)
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 1)
        self.citation_repository.remove_one(citation)
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 0)
    
    def test_delete_all(self):
        test_fields = {"authors": ["Markola, Marko", "Kerkko Möttönen"], "title": "Tutkiminen", "journal": "tutkimuslehti", "year": 2000, "volume": "", "pages": ""}
        citation = Citation("article", "ID1", test_fields, ["Marko", "tutkimus", "viite"])
        citation2 = Citation("article", "ID2", test_fields, ["Toinen", "tutkimus", "kokeilu"])
        self.citation_repository.add_new(citation)
        self.citation_repository.add_new(citation2)
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 2)
        self.citation_repository.delete_all()
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 0)
