#!/usr/bin/env python

# Python 2-to-3 compatibility code
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import glob
import argparse as ap
from PIL import Image
from wmark import watermark_photo


def wmark_all(path_photos, path_wmark, save_path, wmark_prefix='wmarked_',
              **params):
    """Run through all files in path_photos and apply path_wmark on them.
    Pass params to the watermarking function."""

    wmark = Image.open(path_wmark)

    for f in glob.glob(path_photos):
        try:
            photo = Image.open(f)
        except IOError:
            print('Warning: skipping invalid image {0}'.format(f))

        fname = os.path.split(f)[1]
        wmphoto = watermark_photo(photo, wmark, **params)
        wmphoto = wmphoto.convert('RGB')
        wmphoto.save(os.path.join(save_path, wmark_prefix + fname))


if __name__ == '__main__':

    wmark_all('testimg/test*.jpg', 'testimg/testwmark.png', '')
