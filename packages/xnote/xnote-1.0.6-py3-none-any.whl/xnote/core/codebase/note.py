import random, string
import pickle

class Note:
    title: str
    description: str
    content: str
    id: str


    def __init__(self, title, description, content):
        self.title = title
        self.description = description
        self.content = content
        self.id = ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(24)])


    def __str__(self):
        return f'[{self.title}, {self.description}, {self.content}, {self.id}]'


def retrieve_notes(path: str) -> []:
    """Retrieves a list of notes from the desired file."""
    notes = []

    try:
        with open(path, 'rb') as f:
            # If the file isn't empty.
            if f.readlines():
                f.seek(0)
                notes = pickle.load(f)
                
    
    except FileNotFoundError: # Creates the file if it doesn't exist.
        open(path, 'x')

    return notes


def write_notes(path: str, notes: []):
    """Writes all notes to the desired file."""
    with open(path, 'wb') as f:
        pickle.dump(obj=notes, file=f)