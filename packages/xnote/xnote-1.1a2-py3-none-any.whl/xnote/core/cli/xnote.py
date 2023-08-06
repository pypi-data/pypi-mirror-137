import argparse, pickle
from xnote.core.codebase.note import Note, retrieve_notes, write_notes, remove_note

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
    
    # parser for the remove command
    removenote_parser = subparsers.add_parser('remove', help='Removes a note from a list.')
    removenote_parser.add_argument('-i', '--id', required=True, help='Use the list command to retrieve the id.')
    removenote_parser.add_argument('-f', '--file', required=True, help='File to remove this note from.')

    args = parser.parse_args()

    try:
        notes = retrieve_notes(args.file)  
    
    except AttributeError:
        print("Invalid usage. Type xnote -h for help.")
        
    if args.subcommand == 'new':
        description = args.description if args.description else "No description."
        note = Note(args.title, description, args.content)
        notes.append(note)

        write_notes(args.file, notes)

    elif args.subcommand == 'list':
        [print(f'{x}\n') for x in notes]

        if len(notes) == 0: 
            print("Looks like this file is empty!")        

    elif args.subcommand == 'remove':
        remove_note(args.id, notes, args.file)