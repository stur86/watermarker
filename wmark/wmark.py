# Python 2-to-3 compatibility code
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from PIL import Image


def watermark_photo(photo, wmark, targ_rect=(0.1, 0.1, 0.9, 0.9),
                    fill_method=0, rescaling=Image.BICUBIC):
    """
    Apply a watermark to a photo

    Args:
    |   photo (PIL.Image.Image): the photo to watermark
    |   wmark (PIL.Image.Image): the watermark image
    |   targ_rect ([float]*4): the rectangle (in fractional coordinates) over
    |                          which to apply the watermark
    |   fill_method (int): the method with which to fill the target rectangle:
    |                      0 (default) - always resize the one that is too big 
    |                      1 - resize photo to fit watermark
    |                      2 - resize watermark to fit photo
    |   rescaling (PIL resize method): method with which to resize the image.
    |                                  Default is BICUBIC

    Returns:
    |   photo_wmarked (PIL.Image.Image): the watermarked photo

    """

    # Both have to be PIL Images

    if (not isinstance(photo, Image.Image) or
            not isinstance(wmark, Image.Image)):
        raise TypeError('Photos passed are not PIL images')

    # Sizes?
    sp = photo.size
    sw = wmark.size

    # Target rectangle?
    tr = [int(sp[i % 2]*t) for i, t in enumerate(targ_rect)]
    tr_size = [tr[2]-tr[0], tr[3]-tr[1]]

    ratio = [(sw[i]/t) for i, t in enumerate(tr_size)]
    scaling = max(ratio)

    # Resize photo and watermark as needed
    if fill_method == 0:

        if (scaling > 1):
            wmark = wmark.resize([int(s/scaling) for s in sw], rescaling)
            sw = wmark.size
        else:
            photo = photo.resize([int(s*scaling) for s in sp], rescaling)
            sp = photo.size

    elif fill_method == 1:
        photo = photo.resize([int(s*scaling) for s in sp], rescaling)
        sp = photo.size
    elif fill_method == 2:
        wmark = wmark.resize([int(s/scaling) for s in sw], rescaling)
        sw = wmark.size

    # Add alpha channel if not present
    photo = photo.convert('RGBA')
    # Now apply watermark
    photo.alpha_composite(wmark, dest=(int(targ_rect[0]*sp[0]),
                                       int(targ_rect[1]*sp[1])))

    return photo
