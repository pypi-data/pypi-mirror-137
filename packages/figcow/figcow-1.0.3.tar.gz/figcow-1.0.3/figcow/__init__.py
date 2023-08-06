from .process import process
def cow(message: str, wrapping = 100) -> str:
    lines, length = process(message, wrapping)
    return f" {'_' * (length + 1)}\n/ {lines[0].ljust(length)}\\\n" + "".join([f"| {line.ljust(length)}|\n" for line in lines[1: -1]]) + f"\\ {lines[-1].ljust(length)}/\n" + " {} \n     \\   ^__^\n      \\  (oo)\\_______\n         (__)\\       )\\/\\\n            ||----w |\n            ||     ||".format('\u203e' * (length + 1))
