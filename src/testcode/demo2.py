
from PIL import Image

file_path = "/Users/apple/autoTest/workspace/pytest/pics/test-2018-01-11_10-09-28.png"

#
# lena = Image.open(file_path)
# lena_L =lena.convert("L")
# lena_L_rgb =lena_L.convert("RGB")
#
# print(lena.getpixel((0,0)) )
# print(lena.size)
im = Image.open(file_path)

rgb_im = im.convert('RGB')

width = im.size[0]
height = im.size[1]

# 输出图片的像素值

t= rgb_im.getpixel((176/1080 * width, 1592/1920 * height))

print(t)

t2= rgb_im.getpixel((134, 1592))
print(t2)

print((t==t2))