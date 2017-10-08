# Python 2-to-3 compatibility code
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from PIL import Image
from wmark import watermark_photo

import unittest


class Tests(unittest.TestCase):

    def test_inputs(self):

        with self.assertRaises(TypeError):
            watermark_photo(0, 0)

    def test_watermarking(self):

        im = Image.open('testimg/test1.jpg')
        wm = Image.open('testimg/testwmark.png')

        im = watermark_photo(im, wm).convert('RGB')

        im.save('testimg/wmarked/test1_wmarked.jpg')

if __name__ == '__main__':
    unittest.main()
