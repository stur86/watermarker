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
    failed = {}

    for f in path_photos:
        try:
            photo = Image.open(f)
        except IOError:
            print('Warning: skipping invalid image {0}'.format(f))
            continue

        fname = os.path.split(f)[1]
        try:
            wmphoto = watermark_photo(photo, wmark, **params)
        except Exception as e:
            failed[f] = str(e)
            continue

        wmphoto = wmphoto.convert('RGB')
        wmphoto.save(os.path.join(save_path, wmark_prefix + fname))

    return failed


if __name__ == '__main__':

    parser = ap.ArgumentParser(prog='WATERMARKER',
                               description='''A command line tool to apply '''
                               '''a watermark to one or '''
                               '''multiple photos at once''')
    parser.add_argument('photos', type=str, nargs='+',
                        help='Photos to process')
    parser.add_argument('watermark', type=str,
                        help='Watermark to add')
    parser.add_argument('-trect', type=float, nargs=4,
                        default=[0.1, 0.1, 0.9, 0.9],
                        help='Target rectangle')
    parser.add_argument('-method', type=str, choices=['ADAPT',
                                                      'RESIZE_PHOTO',
                                                      'RESIZE_WMARK'],
                        default='ADAPT',
                        help='Method used to fit watermark to photo. ADAPT'
                        ' will shrink whichever one is needed, whereas '
                        'RESIZE_PHOTO will always resize the photo (shrink or'
                        ' enlarge) and RESIZE_WMARK will do the same with the'
                        ' watermark')
    args = parser.parse_args()

    # Map arguments to parameters
    params = {}
    params['targ_rect'] = args.trect
    params['fill_method'] = {
        'ADAPT': 0,
        'RESIZE_PHOTO': 1,
        'RESIZE_WMARK': 2
    }[args.method]

    failed = wmark_all(args.photos, args.watermark, '', **params)

    if len(failed) > 0:
        print('The following photos failed:')
        for f, err in failed.iteritems():
            print('{0}:\t{1}'.format(f, err))
