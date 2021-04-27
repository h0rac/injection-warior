from injection_warrior import postman
from termcolor import colored
import sys

if len(sys.argv) < 4:
    print(colored("Usage ./postman.py -f 'collection.json' -n 'folder_name'", "red"))
    sys.exit(0)

parser = postman.Postman(collection_path=sys.argv[2], collection_name=sys.argv[4])
parser.parse_collection(parser.collection)