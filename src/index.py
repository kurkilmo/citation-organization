from ui import UI
from src.io.console_io import ConsoleIO
from citation_repository import CitationRepository

if __name__ == "__main__":
    interface = UI(ConsoleIO(), CitationRepository())
    interface.start()
