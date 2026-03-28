from PIL import Image, ImageChops

def trim(im):
    # Get top-left pixel color as background color
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

im = Image.open(r"g:\YT_VIDEO\LeafyPop_D\LeafyPop\leafypop_project\store\static\store\images\companyname_D.png")
# Convert to RGBA if possible to ensure clean crop, but ImageChops works best on RGB
if im.mode == 'RGBA':
    # create white background to replace alpha
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[3]) # 3 is the alpha channel
    im = bg

im_cropped = trim(im)
im_cropped.save(r"g:\YT_VIDEO\LeafyPop_D\LeafyPop\leafypop_project\store\static\store\images\companyname_cropped.png")
print("Cropped successfully!")
