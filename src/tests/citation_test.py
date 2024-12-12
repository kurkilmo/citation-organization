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


    def test_empty_citation(self):
        citation1 = Citation("inproceedings", "idid")
        self.citation_repository.add_new(citation1)
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 1)

        self.assertEqual(citations[0].key, "idid")
        self.assertEqual(citations[0].fields, {})
        self.assertEqual(citations[0].keywords, [])


    def test_duplicate_keys(self):
        citation1 = Citation("inproceedings", "idid")
        citation2 = Citation("article", "idid")

        self.citation_repository.add_new(citation1)
        self.citation_repository.add_new(citation2)

        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 2)

        self.assertEqual(citations[0].key, "idid")
        self.assertEqual(citations[1].key, "idid")


    def test_remove_nonexistent_citation(self):
        citation = Citation("article", "id1", {})
        with self.assertRaises(Exception):
            self.citation_repository.remove_one(citation)


    def test_add_new(self):
        article_test_fields = {"author": ["Markola, Marko", "Kerkko Möttönen"], "title": "Tutkiminen", "journal": "tutkimuslehti", "year": 2000, "volume": "", "pages": ""}
        inproceedings_test_fields = {"author": ["Marko Markola", "Kerkko Möttönen"], "title": "Tutkiminen", "year": 2000, "booktitle": "kirjatitteli" }
        article = Citation("article", "ID1", article_test_fields, ["artikkeli", "Marko", "tutkimus", "viite"])
        inproceedings = Citation("inproceedings", "ID2", inproceedings_test_fields, ["inproceedingi", "Marko", "tutkimus", "viite"])
        self.citation_repository.add_new(article)
        citations = self.citation_repository.get_all()

        self.assertEqual(len(citations), 1)
        self.assertEqual(citations[0].key, "ID1")
        self.assertEqual(citations[0].fields["author"][0], "Markola, Marko")
        self.assertEqual(citations[0].fields["author"][1], "Kerkko Möttönen")
        self.assertEqual(citations[0].fields["title"], "Tutkiminen")
        self.assertEqual(citations[0].fields["pages"], "")

        self.citation_repository.add_new(inproceedings)
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 2)

        self.assertEqual(citations[1].citation_type, "inproceedings")
        self.assertEqual(citations[1].key, "ID2")
        self.assertEqual(citations[1].fields["author"][0], "Marko Markola")
        self.assertEqual(citations[1].fields["title"], "Tutkiminen")
        self.assertEqual(citations[1].fields["year"], 2000)
        self.assertEqual(citations[1].fields["booktitle"], "kirjatitteli")
        
        self.citation_repository.add_new(article)
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 3)


    def test_update_citation_field(self):
        fields = {"author": ["Markku Matinen"], "title": "Markun artikkeli", "year": 2021}
        citation = Citation("article", "ID3", fields)
        self.citation_repository.add_new(citation)

        updated_fields = {"author": ["Markku matinen"], "title": "Markun päivitettyu", "year": 2021}
        updated_citation = Citation("article", "ID3", updated_fields)
        self.citation_repository.remove_one(citation)
        self.citation_repository.add_new(updated_citation)

        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 1)
        self.assertEqual(citations[0].fields["title"], "Markun päivitettyu")
        self.assertEqual(citations[0].fields["author"][0], "Markku matinen")


    def test_remove_one(self):
        article_test_fields = {"author": ["Markola, Marko", "Kerkko Möttönen"], "title": "Tutkiminen", "journal": "tutkimuslehti", "year": 2000, "volume": "", "pages": ""}
        inproceedings_test_fields = {"author": ["Marko Markola", "Kerkko Möttönen"], "title": "Tutkiminen", "year": 2000, "booktitle": "kirjatitteli" }
        article = Citation("article", "ID1", article_test_fields, ["artikkeli", "Marko", "tutkimus", "viite"])
        inproceedings = Citation("inproceedings", "ID2", inproceedings_test_fields, ["inproceedingi", "Marko", "tutkimus", "viite"])
        
        self.citation_repository.add_new(article)
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 1)

        self.citation_repository.add_new(inproceedings)
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 2)

        self.citation_repository.remove_one(inproceedings)
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 1)

        self.citation_repository.remove_one(article)
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 0)
    

    def test_delete_all(self):
        article_test_fields = {"author": ["Markola, Marko", "Kerkko Möttönen"], "title": "Tutkiminen", "journal": "tutkimuslehti", "year": 2000, "volume": "", "pages": ""}
        inproceedings_test_fields = {"author": ["Marko Markola", "Kerkko Möttönen"], "title": "Tutkiminen", "year": 2000, "booktitle": "kirjatitteli" }
        article = Citation("article", "ID1", article_test_fields, ["artikkeli", "Marko", "tutkimus", "viite"])
        inproceedings = Citation("inproceedings", "ID2", inproceedings_test_fields, ["inproceedingi", "Marko", "tutkimus", "viite"])
        citation = Citation("article", "ID1", article_test_fields, ["toinen", "Marko ja Kerkko", "tutkimus2", "viite"])
        
        self.citation_repository.add_new(article)
        self.citation_repository.add_new(citation)
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 2)

        self.citation_repository.delete_all()
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 0)

        self.citation_repository.add_new(inproceedings)
        self.citation_repository.add_new(inproceedings)
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 2)

        self.citation_repository.delete_all()
        citations = self.citation_repository.get_all()
        self.assertEqual(len(citations), 0)
