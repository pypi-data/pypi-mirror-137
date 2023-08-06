import argparse, pickle
from core.codebase.note import Note, retrieve_notes, write_notes

def start():
    parser = argparse.ArgumentParser(description='Easily keep track of your notes on your favorite terminal emulator!')
    subparsers = parser.add_subparsers(dest='subcommand')

    # parser for the new command
    newnote_parser = subparsers.add_parser('new', help='Create a new note.')
    newnote_parser.add_argument('-t', '--title', required=True)    
    newnote_parser.add_argument('-d', '--description')    
    newnote_parser.add_argument('-c', '--content', required=True)
    newnote_parser.add_argument('-f', '--file', required=True, help='File where notes will be stored.')  

    # parser for the list command
    listnote_parser = subparsers.add_parser('list', help='List all notes from a file.')  
    listnote_parser.add_argument('-f', '--file', required=True, help='File to list notes from.')  
    
    args = parser.parse_args()

    try:
        notes = retrieve_notes(args.file)  
    
    except AttributeError:
        print("Invalid usage. Type xnote -h for help.")
        
    if args.subcommand == 'new':
        note = Note(args.title, args.description, args.content)
        notes.append(note)

        write_notes(args.file, notes)

    elif args.subcommand == 'list':
        [print(x) for x in notes]        