import requests
import bibtexparser
from bibtexparser.bparser import BibTexParser
from citation import Citation

HEADER = {
    'Accept': 'application/x-bibtex'
}


def _doi_url(doi:str):
    return "https://doi.org/" + doi

def get_citation_from_doi(doi:str):
    response = requests.get(_doi_url(doi), headers=HEADER)

    if response.status_code != 200:
        return None
    
    parser = BibTexParser()
    entries, = bibtexparser.loads(response.text, parser).entries
    citation_type = entries.pop("ENTRYTYPE")
    key = entries.pop("ID")
    try:
        entries["author"] = entries["author"].split(" and ")
    except KeyError:
        pass

    citation = Citation(
        citation_type,
        key,
        entries
    )

    return citation
