#MIT License
#
#Copyright (c) 2019 Matthijs Tadema
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


from . import block
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio','-a',action='store_true', default=False)
    parser.add_argument('--debug','-d',action='store_true', default=True)
    parser.add_argument('--test','-t',action='store_true', default=False)
    return parser.parse_args()

def add_tuples(tup_a, b):
    """
    Adds two tuples together, or adds a tuple to a list of tuples
    """
    if not isinstance(tup_a, tuple):
        raise TypeError("Input a has to be tuple")

    add = lambda i, j: tuple( m + n for m, n in zip(i, j) )

    if isinstance(b, tuple):
        return tuple(add(tup_a, b))
    elif isinstance(b, list):
        return list([
                add(tup_a, tup_b)
                for tup_b in b
                ])
    else:
        raise TypeError("input b has to be list or tup")

def switch_tuple(a):
    if isinstance(a, tuple):
        i, j = a
        out = (j, i)
    elif isinstance(a, list):
        out = [
                (j, i)
                for i, j in a
                ]
    else:
        raise TypeError
    return out

def invert_tuple(a):
    out = ''
    if isinstance(a, tuple):
        i, j = a
        out = (-i, -j)
    elif isinstance(a, list):
        out = [
                (-i, -j)
                for i, j in a
                ]
    else:
        raise TypeError
    return out
