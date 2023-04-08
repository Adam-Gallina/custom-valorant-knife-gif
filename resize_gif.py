from PIL import Image

# Based on https://stackoverflow.com/a/41827681

def resize_gif(path, new_size):
    im = Image.open(path)

    frames = []
    last_frame = im.convert('RGBA')
    for i in range(im.n_frames):
        #new_frame = Image.new('RGBA', im.size)

        im.seek(i)

        #new_frame.paste(im, (0, 0), im.convert('RGBA'))
        new_frame = im.convert('RGBA').resize(new_size)
        #new_frame.thumbnail(new_size, Image.LANCZOS)

        #print(im.size, new_frame.size, new_size)
        frames.append(new_frame)

    return frames
