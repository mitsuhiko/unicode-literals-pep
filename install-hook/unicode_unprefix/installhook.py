from distutils.command.build_py import build_py
from . import tokenize


def strip_unicode_from_iterable(iterable):
    for token in iterable:
        if token[0] == tokenize.STRING:
            yield tokenize.TokenInfo(tokenize.STRING, token[1].lstrip('uU'),
                                     *token[2:])
        else:
            yield token


class build_py_strip_unicode(build_py):

    def run(self):
        self.updated_files = []

        if self.py_modules:
            self.build_modules()

        if self.py_modules:
            self.build_modules()
        if self.packages:
            self.build_packages()
            self.build_package_data()

        for filename in self.updated_files:
            self.strip_unicode_in_file(filename)

        self.byte_compile(self.get_outputs(include_bytecode=0))

    def strip_unicode_in_file(self, filename):
        with open(filename, 'rb') as f:
            tokens = tokenize.tokenize(f.readline)
            tokens = list(strip_unicode_from_iterable(tokens))
        with open(filename, 'wb') as f:
            f.write(tokenize.untokenize(tokens))

    def build_module(self, module, module_file, package):
        res = build_py.build_module(self, module, module_file, package)
        if res[1]:
            # file was copied
            self.updated_files.append(res[0])
        return res
