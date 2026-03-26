from PIL import Image

def make_white_transparent(image_path, output_path):
    img = Image.open(image_path)
    img = img.convert("RGBA")
    datas = img.getdata()
    
    newData = []
    # If pixel is close to white, make it transparent
    for item in datas:
        # Check if the pixel is white or very close to white (allow slight anti-aliasing tolerance, e.g. >240)
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            newData.append((255, 255, 255, 0)) # Fully transparent
        else:
            newData.append(item)
            
    img.putdata(newData)
    
    # Also crop the transparent space to make it tight
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    img.save(output_path, "PNG")

make_white_transparent(
    r"g:\YT_VIDEO\LeafyPop_D\LeafyPop\leafypop_project\store\static\store\images\companyname_D.png",
    r"g:\YT_VIDEO\LeafyPop_D\LeafyPop\leafypop_project\store\static\store\images\companyname_transparent.png"
)
print("Made transparent!")
