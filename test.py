import unittest
from colorer import colorer
# import colorer
import os, glob

class Test(unittest.TestCase):
    def test_load(self):
        p = './test_files/test_file'
        d = colorer.load_colorscheme(p)
        self.assertEqual({'colorscheme': os.path.abspath(p), 'key1': 'a', 'key2': 'b'}, d)
        self.assertIn('colorscheme', d)

    def test_replace(self):
        string = "hi {key1} {key2} {fakeeee}"
        new = colorer.replace_line(string,{'key1': 'a', 'key2': 'b'})
        self.assertEqual(new, "hi a b {fakeeee}")

    def test_write(self):
        self.test_load()
        colorer.write_to_files(colorer.load_colorscheme('./test_files/test_file'), './test_files/templates', './test_files/out', True)
        out = {}
        for p in glob.iglob('./test_files/out/*'):
            with open(p,'r') as file:
                out[os.path.basename(p)] = file.read()
        expect = {}
        for p in glob.iglob('./test_files/expect/*'):
            with open(p,'r') as file:
                expect[os.path.basename(p)] = file.read()
        self.assertEqual(out, expect)

if __name__ == '__main__':
    unittest.main()
