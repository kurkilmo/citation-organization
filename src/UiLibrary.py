from ui import UI
from in_out.stub_io import StubIO
from citation_repository import CitationRepository
import os

class UiLibrary:
    def __init__(self):
        self._io = StubIO()
        self._citation_repository = CitationRepository("src/tests/tests.json")
        self._ui = UI(self._io, self._citation_repository)

    def input(self, value):
        self._io.add_input(value)

    def output_should_contain(self, value):
        outputs = self._io.outputs
        contains = False
        for output in outputs:
            if value in output:
                contains = True
        if not contains:
            raise AssertionError(
                f"Output \"{value}\" is not in {str(outputs)}"
            )
    
    def output_should_contain_bib(self, id, author):
        self.output_should_contain('\n' + self._format_bib(id, [author]))
        
    def _format_bib(self, id, authors):
        return f"""@article{{{id},
    authors = {{{" and ".join(authors)}}},
    title = {{title}},
    journal = {{journal}},
    year = {{1999}},
    volume = {{volume}},
    pages = {{1--100}}
}}% Keywords: keyword1, keyword2"""
    
    def file_should_containt(self, filename, id, author):
        with open(filename, "r") as file:
            text = file.read()
            if not self._format_bib(id, [author]) in text:
                raise AssertionError(
                    f"Citation {id}, {author} is not in {filename}"
                )
    
    def delete_file(self, filename):
        os.remove(filename)

    def start_ui(self):
        self._ui.start()
