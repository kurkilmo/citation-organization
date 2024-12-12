from src.citation import Citation

test_citations = [
            Citation(
                "article",
                "ID1",
                {
                    "author": ["Pekka Kirjoittaja", "Toimittaja, Tero"],
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
                    "author": ["Janne Jannela", "Meikäläinen, Matti"],
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
                    "author": ["Kekkonen, Urho", "Räty, Seppo"],
                    "title": "Hiihtää hiihtää",
                    "journal": "Hesari",
                    "year": 1970,
                    "volume": "4",
                    "pages": "1--2",
                },
                ["keyword3", "keyword4"]
            )
        ]

def create_article(io, id, authors, title, journal, year, volume, pages, keywords):
    io.add_input("create")
    io.add_input("article")
    io.add_input(id)
    for author in authors:
        io.add_input(author)
    io.add_input("")
    io.add_input(title)
    io.add_input(journal)
    io.add_input(year)
    io.add_input(volume)
    io.add_input(pages)
    for key in keywords:
        io.add_input(key)
    io.add_input("")

def create_inproceedings(io, id, authors, title, year, booktitle, keywords):
    io.add_input("create")
    io.add_input("inproceedings")
    io.add_input(id)
    for author in authors:
        io.add_input(author)
    io.add_input("")
    io.add_input(title)
    io.add_input(year)
    io.add_input(booktitle)
    for key in keywords:
        io.add_input(key)
    io.add_input("")

test_file = "test_citations.json"
export_file = "test_export.bib"
