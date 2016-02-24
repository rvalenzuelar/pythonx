'''
Class for printing text in terminal with colors
Raul Valenzuela
raul.valenzuela@colorado.edu
'''


class ctext:

    def __init__(self, text):
        self.text = text
        self.preffix = '\033[1;{}m'
        self.suffix = '\033[1;m'

    def red(self):
        pre = self.preffix.format('31')
        return pre + self.text + self.suffix

    def green(self):
        pre = self.preffix.format('32')
        return pre + self.text + self.suffix

    def yellow(self):
        pre = self.preffix.format('33')
        return pre + self.text + self.suffix

    def redh(self):
        pre = self.preffix.format('41')
        return pre + self.text + self.suffix

    def greenh(self):
        pre = self.preffix.format('42')
        return pre + self.text + self.suffix

    def yellowh(self):
        pre = self.preffix.format('43')
        return pre + self.text + self.suffix
