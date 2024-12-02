from ui import UI
from in_out.stub_io import StubIO
from citation_repository import CitationRepository
from citation import Citation

class UiLibrary:
    def __init__(self):
        self._io = StubIO()
        self._citation_repository = CitationRepository("src/tests/tests.json")
        self._ui = UI(self._io, self._citation_repository)

    def input(self, value):
        self._io.add_input(value)

    def output_should_contain(self, value):
        outputs = self._io.outputs

        if not value in outputs:
            raise AssertionError(
                f"Output \"{value}\" is not in {str(outputs)}"
            )
    
    def output_should_contain_bib(self, id, author):
        self.output_should_contain(f"""@article{{{id},
    author = {{{author}}},
    title = {{title}},
    journal = {{journal}},
    year = {{1999}},
    volume = {{volume}},
    pages = {{1--100}}
}}""")

    def start_ui(self):
        self._ui.start()
