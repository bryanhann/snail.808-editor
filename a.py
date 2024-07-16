import sys
from util import getch, clear

DEBUG=True
acc=[]

def fixch(ch):
    if ch=='\r':
        return '\n'
    else:
        return ch

def string4buffer(buffer):
    return ''.join(buffer)

def show_buffer(buffer):
    clear()
    sys.stdout.write(string4buffer(buffer))
    sys.stdout.flush()

def edit(initial=''):
    buffer = [ch for ch in initial]
    while True:
        show_buffer(buffer)
        buffer.append(fixch(getch()))
        if buffer[-1:] == ['-']:
            return acc[:-1]
        elif buffer[-1:] in ['\x7f']:
            acc=acc[:-2]
        print(acc)


acc=myread('some\ntext')
print( 777, acc )
