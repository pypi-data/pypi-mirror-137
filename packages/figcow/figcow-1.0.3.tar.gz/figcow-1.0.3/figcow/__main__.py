from . import cow
from sys import argv, stdin
def main(): print(cow(stdin.read() if len(argv) == 1 else " ".join(argv[1:])))
if __name__ == "__main__": main()