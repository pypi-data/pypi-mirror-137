from contextlib import contextmanager
from typing import Generator


@contextmanager
def inner(want_int):
    if want_int:
        yield 1
    else:
        yield "mystring"


@contextmanager
def outer() -> Generator[str, None, None]:
    with inner(False) as myinner:
        myinner: str
        try:
            myinner: str
            yield myinner
        except:
            pass


with outer() as myouter:
    myouter.capitalize()
