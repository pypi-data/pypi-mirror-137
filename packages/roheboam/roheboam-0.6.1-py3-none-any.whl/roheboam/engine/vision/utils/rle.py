import numpy as np


# ref.: https://www.kaggle.com/stainsby/fast-tested-rle
def rle_encode(mask):
    pixels = mask.T.flatten()
    # We need to allow for cases where there is a '1' at either end of the sequence.
    # We do this by padding with a zero at each end when needed.
    use_padding = False
    if pixels[0] or pixels[-1]:
        use_padding = True
        pixel_padded = np.zeros([len(pixels) + 2], dtype=pixels.dtype)
        pixel_padded[1:-1] = pixels
        pixels = pixel_padded
    rle = np.where(pixels[1:] != pixels[:-1])[0] + 2
    if use_padding:
        rle = rle - 1
    rle[1::2] = rle[1::2] - rle[:-1:2]
    return " ".join(map(str, rle.tolist()))


# This is copied from https://www.kaggle.com/paulorzp/run-length-encode-and-decode.
def rle_decode(rle_str, mask_shape, mask_dtype=np.uint8):
    s = rle_str.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths
    mask = np.zeros(np.prod(mask_shape), dtype=mask_dtype)
    for lo, hi in zip(starts, ends):
        mask[lo:hi] = 1
    return mask.reshape(mask_shape[::-1]).T


lookup = {"rle_encode": rle_encode, "rle_decode": rle_decode}
"""
Test

img = np.array([[0,0,0,1,0],
                [0,0,1,1,0],
                [1,0,0,0,1],
                [1,1,0,0,1]])

rle = rle_encode(img)

decode_img = rle_decode(rle, shape=img.shape)

assert img == decode_img

"""
