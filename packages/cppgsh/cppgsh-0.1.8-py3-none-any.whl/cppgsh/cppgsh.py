#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cppgsh.py | MIT License | https://github.com/kirin123kirin/cppgsh/raw/main/LICENSE
"""
Generate C++ Single Header File from C/C++ sources and headers file.

MIT License

"""

__all__ = ["GenSingleHeader"]

PGNAME = "cppgsh"
ENCODING = "utf-8"
LINESEP = "\n"
EXCLUDES = ['test', 'tests', 'test*/**', 'tool', 'tool/**', '.*', 'bak', 'old', 'org']

from email.policy import default
import os
import sys
import re
from glob import glob
from fnmatch import fnmatch
from os.path import basename
from collections import defaultdict, Counter
from io import StringIO
from itertools import chain

from pathlib import Path
from quom.tokenizer import (tokenize, PreprocessorToken, PreprocessorDefineToken, PreprocessorIfNotDefinedToken, PreprocessorIncludeToken,
                            PreprocessorUnknownIncludeToken, PreprocessorEndIfToken, WhitespaceToken, CommentToken, RemainingToken)

class GenSingleHeader(object):
    # mcrwords = set(["if", "ifndef", "ifdef", "else", "elif", "define", "include", "pragma", "endif"])
    # ifwords = set(["if", "ifndef", "ifdef"])

    # re_preproc = re.compile(f"^\s*#\s*({"|".join(macrowords)})\s+.*$").match
    # is_whitespace = re.compile("^\s*$").match

    # def preproc(x, default=""):
    # 	if x in mcrwords:
    # 		return x
    # 	r = re_preproc(x)
    # 	if r:
    # 		return r.group(1)
    # 	return default

    # is_ifndef = lambda x: preproc(x) == "ifndef"
    # is_if = lambda x: preproc(x) in ifwords
    # is_define = lambda x: preproc(x) == "define"
    # is_include = lambda x: preproc(x) == "include"
    # is_endif = lambda x: preproc(x) == "endif"
    # is_macro = lambda x: preproc(x) in macrowords
    # is_sp_comment = lambda x: is_whitespace(x)

    re_externC = re.compile(
        r'(?:^extern\s+"C"\s+|(?:/\*.+\*/|//[^\r\n]*)?\s*#ifdef __cplusplus\s+(extern\s+"C"\s+\{|\})[^\r\n]*\s*#endif\s*(?:/\*.+\*/|//[^\r\n]+)?)')

    def __init__(self, include_directories, source_directories=None, exclude_patterns=EXCLUDES,
                 include_guard=None, license_files=[], del_extern_C=False,
                 encoding=ENCODING, linesep=LINESEP, quiet=False):

        self.include_directories = include_directories
        self.source_directories = source_directories
        self.exclude_patterns = exclude_patterns
        self.include_guard = include_guard.replace('.', '_').upper() if include_guard else None
        self.del_extern_C = del_extern_C
        self.encoding = encoding

        self.license_files = license_files
        self.linesep = linesep
        self.quiet = quiet

        self._data = None
        self.target_src = ('.c', '.cpp', '.cxx', '.cc', '.c++', '.cp', '.C')
        self.target_header = ('.h', 'hpp', 'hxx', 'hh')

        self._global_headers = None
        self._private_headers = None
        self._sources = None
        self.result = StringIO()
        self.signature = f"{self.linesep}// delete by {basename(sys.argv[0])} :"

    @property
    def data(self):
        if self._data is None:
            self._data = {}
            extensions = set(self.target_src + self.target_header)
            done = set()

            for x in self.include_directories + self.source_directories:
                for p in map(Path, glob(str(x.joinpath('**')), recursive=True)):
                    if p.is_dir() or p.resolve() in done or p.suffix.lower() not in extensions:
                        continue
                    if next((True for pat in self.exclude_patterns if fnmatch(p, pat)), False):
                        continue
                    data = p.read_text(self.encoding)
                    if self.del_extern_C:
                        ret = self.re_externC.search(data)
                        if ret:
                            matchtxt = ret.group(0)
                            if "#" in matchtxt:
                                matchtxt = matchtxt.replace(self.linesep, f"{self.linesep}// {self.signature}: ")
                            else:
                                matchtxt = f"/* {self.signature} {matchtxt} */"
                            data = self.re_externC.sub(matchtxt, data)
                    self._data[p.name] = tokenize(data)
                    done.add(p.resolve())
                    if not self.quiet:
                        print("   loading... ", p)

        return self._data

    def index_include_guard(self, name):
        tokens = self.data[name]
        for i, token in enumerate(tokens):
            if isinstance(token, PreprocessorIfNotDefinedToken) and isinstance(tokens[i + 1], PreprocessorDefineToken):
                return i
        return -2

    def index_include_last(self, name):
        tokens = self.data[name]
        for i in range(len(tokens) - 1, 0, -1):
            if isinstance(tokens[i], (PreprocessorIncludeToken, PreprocessorUnknownIncludeToken)):
                for j in range(i + 1, len(tokens)):
                    if isinstance(tokens[j], PreprocessorEndIfToken):
                        return j
                return i
        return -1

    def delete_lines(self, name, deletelineslist):
        # deletelineslist.reverse()
        # for d in deletelineslist:
        #     del self.data[name][d]
        for d in deletelineslist:
            commentout = self.signature + self.data[name][d].raw
            self.data[name][d] = tokenize(commentout)[1]

    def is_if(self, tokens):
        for t in tokens:
            if isinstance(t, PreprocessorToken) and t.preprocessor_instruction[-1].raw in ["if", "ifndef", "ifdef"]:
                return True
        return False

    @property
    def global_headers(self):
        if self._global_headers is None:

            past = set()
            self._global_headers = []

            for name in [*self.private_headers, *(self.data.keys() - set(self.private_headers))]:

                dellist = []
                prep = []
                start = self.index_include_guard(name) + 2
                end = self.index_include_last(name) + 1

                tokens = self.data[name]

                opened = 0
                inced = 0

                for i, t in enumerate(tokens[start:end], start):
                    if isinstance(t, PreprocessorToken):
                        tag = t.preprocessor_instruction[-1].raw
                        if tag == "pragma":
                            continue
                        if tag in ["if", "ifndef", "ifdef", "define"]:
                            prep.append(i)
                            opened += (tag != "define")
                            continue

                        if tag == "include":
                            path = str(t.path)
                            if path in past and self.is_if(tokens[p] for p in prep) is False:
                                dellist.append(i)
                                continue
                            past.add(path)
                            inced += 1
                            prep.append(i)

                        if tag == "endif":
                            opened -= 0

                        if inced > 0 and opened == 0:
                            for p in prep:
                                tk = self.data[name][p]
                                self._global_headers.append(tk.raw)
                                dellist.append(p)
                            prep = []
                            inced = 0

                    elif isinstance(t, (WhitespaceToken, CommentToken)):
                        prep.append(i)

                if inced > 0 and opened == 0:
                    for p in prep:
                        tk = self.data[name][p]
                        self._global_headers.append(tk.raw)
                        dellist.append(p)

                self.delete_lines(name, dellist)

        return self._global_headers

    @property
    def private_headers(self):
        if self._private_headers is None:
            parent_score = 2
            child_score = 1
            atomic_score = 3
            interest = 0.05
            disporder = defaultdict(int)
            defs = defaultdict(list)
            tree = defaultdict(list)

            def getarg(token):
                for i in range(1, token.preprocessor_arguments_idx - 1):
                    t = token.preprocessor_arguments[i]
                    if isinstance(t, RemainingToken):
                        return t.raw
                return None

            for name, token in self.data.items():
                dellist = []
                total = len(token)
                for i, t in enumerate(token):
                    if isinstance(t, PreprocessorIncludeToken):
                        path = basename(str(t.path))
                        if '"' in t.raw and path in self.data:
                            dellist.append(i)
                            rate = int(100 * (total - i) / total)
                            disporder[path] += parent_score * rate
                            disporder[name] += child_score * rate
                            tree[path].append(name)
                    elif isinstance(t, PreprocessorDefineToken):
                        defs[getarg(t)].append(name)

                self.delete_lines(name, dellist)

            for name, token in self.data.items():
                for t in token:
                    if isinstance(t, RemainingToken) and t.raw in defs:
                        for x in defs[t.raw]:
                            disporder[x] += atomic_score

            for name, token in self.data.items():
                for par in tree.get(name, []):
                    disporder[name] += int(disporder[par] * interest)
            headers_only = (d for d in disporder if any(map(d.endswith, self.target_header)))
            self._private_headers = sorted(headers_only, key=lambda k: disporder[k], reverse=True)

        return self._private_headers

    @property
    def sources(self):
        if self._sources is None:
            self._sources = [x for x in self.data if any(map(x.endswith, self.target_src))]
        return self._sources

    @property
    def page_break(self):
        self.result.write(self.linesep * 2)

    @property
    def eof(self):
        self.result.write(self.linesep)

    def begin_of(self, filename):
        self.page_break
        self.result.write(f"/* {{{{{{ start of {filename} */")
        self.page_break

    def end_of(self, filename):
        self.page_break
        self.result.write(f"/* }}}}}} end of {filename} */")
        self.page_break

    def write_license(self):
        if self.license_files:
            dat = None
            for i, ls in enumerate(self.license_files):
                if os.path.exists(ls) and os.path.isfile(ls):
                    if i == 0:
                        self.result.write(f"/* ***{self.linesep}")
                    dat = Path(ls).read_text()
                    self.result.write(dat)
                    self.page_break
            if dat:
                self.result.write("*** */")
                self.page_break
        else:
            def get_license(ld):
                ls = next(chain(ld.glob("LICEN[CS]E*"), ld.glob("COPYING*"), ld.glob("COPYRIGHT")), None)
                if ls:
                    self.result.write(f"/* ***{self.linesep}")
                    self.result.write(Path(ls).read_text())
                    self.result.write("*** */")
                    self.page_break
                return ls

            datadir = self.include_directories + self.source_directories
            datadir = set((d for d in datadir if str(d) != "."))
            for i in range(5):
                for ld in datadir:
                    if get_license(ld):
                        return
                datadir = set(d.parent for d in datadir)
            get_license(Path("."))

    def write_headline(self):
        if self.include_guard:
            self.result.write(f"#ifndef {self.include_guard}{self.linesep}")
            self.result.write(f"#define {self.include_guard}")

        self.page_break
        self.result.writelines(self.global_headers)

    def write_headers(self):
        for header in self.private_headers:
            self.begin_of(header)
            for token in self.data[header]:
                self.result.write(token.raw)
            self.end_of(header)

    def write_sources(self):
        self.page_break
        for source in self.sources:
            self.begin_of(source)
            for token in self.data[source]:
                self.result.write(token.raw)
            self.end_of(source)

    def write_footer(self):
        if self.include_guard:
            self.result.write(f"#endif /* {self.include_guard} */")
        self.eof

    def make(self):
        if not self.quiet:
            print("make license")
        self.write_license()
        if not self.quiet:
            print("make headline")
        self.write_headline()
        if not self.quiet:
            print("make headers")
        self.write_headers()
        if not self.quiet:
            print("make sources")
        self.write_sources()
        if not self.quiet:
            print("make fotter")
        self.write_footer()
        if not self.quiet:
            print("make redefine check & repair")
        self.redefine_repair()
        return self.result.getvalue()

def main():
    import argparse

    parser = argparse.ArgumentParser(prog=PGNAME, description='Single header generator for C++ libraries.')
    parser.add_argument('output_path', metavar='output', type=Path,
                        help='Output file path of the generated single header file.')
    parser.add_argument('--include_guard', '-g', metavar='format', type=str, default=None,
                        help='Regex format of the include guard. Default: %(default)s')
    parser.add_argument('--include_directory', '-I', type=Path, action='append', default=[],
                        help='Add include directories for header files.')
    parser.add_argument('--source_directory', '-S', type=Path, action='append', default=[Path('.')],
                        help='Set the source directories for source files. '
                             'Use ./ or .\\ in front of a path to mark as relative to the header file.')
    parser.add_argument('--exclude_patterns', '-E', type=str, action='append', default=EXCLUDES,
                        help='Set the source directories for source files. '
                             'Use ./ or .\\ in front of a path to mark as relative to the header file.')
    parser.add_argument('--license_files', '-L', type=Path, action='append', default=[],
                        help='Set headline writing License text file path')
    parser.add_argument('--del_extern_C', action='store_false', help='delete define "extern \"C\""')
    parser.add_argument('--linesep', '-l', type=lambda x: x.encode().decode("unicode_escape"), default=LINESEP,
                        help='line separator of output file.')
    parser.add_argument('--encoding', '-e', type=str, default=ENCODING,
                        help='The encoding used to read and write all files.')
    parser.add_argument('--quiet', '-q', action='store_true', help='no print progress info')

    args = parser.parse_args(sys.argv[1:])

    with args.output_path.open('w+', encoding=args.encoding) as file:
        ish = GenSingleHeader(args.include_directory, args.source_directory, args.exclude_patterns,
                              args.include_guard, args.license_files, args.del_extern_C,
                              args.encoding, args.linesep, args.quiet)
        file.write(ish.make())

    if not args.quiet:
        print("\nDone.")


if __name__ == '__main__':
    main()
