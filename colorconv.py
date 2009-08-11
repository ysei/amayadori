
# -*- coding: utf-8 -*-

import png
import imglib
import ppmlib

#file = open("00.png", "rb")
file = open("200908111530-00.png", "rb")
bin  = file.read()
png  = png.Png8bitPalette.load(bin)
width  = png.bitmap.width
height = png.bitmap.height

bitmap = imglib.RgbBitmap(width, height)
for y in range(height):
  for x in range(width):
    rgb = png.get_color((x, y))
    bitmap.set_pixel(x, y, rgb)

ctable = {
  (255,   0,   0): (255,   0,   0), # 80mm/h �ȏ�
  (255,   0, 255): (255,   0, 255), # 50-80mm/h
  (255, 153,   0): (255, 153,   0), # 30-50mm/h
  (255, 255,   0): (255, 255,   0), # 20-30mm/h
  (  0, 255,   0): (  0, 255,   0), # 10-20mm/h
  (  0,   0, 255): (  0,   0, 255), #  5-10mm/h
  ( 51, 102, 255): ( 51, 102, 255), #  1- 5mm/h
  (153, 204, 255): (153, 204, 255), #  0- 1mm/h

  ( 96,  57,  19): ( 96,  57,  19), # �ϑ��_
  (230, 230, 230): (255, 255, 255), # �s���{�����E
  (255, 255, 255): (255, 255, 255), # �C�݋��E
  (102, 102, 102): (102, 102, 102), # �C�݋��E/�O���b�h

  (116, 123, 114): (116, 123, 114), # �C�݋��E
  (160, 160, 160): (160, 160, 160), # �C�݋��E

  (184, 184, 228): (184, 184, 228), # �C
  (193, 193, 193): (193, 193, 193), # �C

  (117, 141, 201): (117, 141, 201), # ��
  (134, 164, 205): (134, 164, 205), # ��
  (136, 166, 207): (136, 166, 207), # ��
  (141, 172, 210): (141, 172, 210), # ��
  (143, 173, 210): (143, 173, 210), # ��
  (144, 173, 211): (144, 173, 211), # ��
  (145, 176, 210): (145, 176, 210), # ��
  (184, 184, 228): (184, 184, 228), # ��

  ( 92, 115, 159): ( 92, 115, 159), # �΋��E
  ( 94, 117, 158): ( 94, 117, 158), # �΋��E
  (102, 125, 145): (102, 125, 145), # �΋��E
  (112, 138, 162): (112, 138, 162), # �΋��E
  (114, 141, 159): (114, 141, 159), # �΋��E
  (114, 142, 169): (141, 142, 169), # �΋��E
  (115, 141, 183): (115, 141, 183), # �΋��E
  (118, 146, 175): (118, 146, 175), # �΋��E
  (126, 156, 187): (126, 156, 187), # �΋��E
  (128, 158, 192): (128, 158, 192), # �΋��E
  (142, 173, 180): (142, 173, 180), # �΋��E
  (151, 181, 180): (151, 181, 180), # �΋��E

  (125, 158, 142): (125, 158, 142), # �΋��E
  (137, 170, 168): (137, 170, 168), # �΋��E

  (109, 141,  94): (109, 141,  94), # ��n
  (117, 150, 102): (117, 150, 102), # ��n
  (118, 152, 102): (118, 152, 102), # ��n
  (118, 153, 102): (118, 153, 102), # ��n
  (120, 149, 132): (120, 149, 132), # ��n
  (122, 157, 107): (122, 157, 107), # ��n
  (125, 161, 108): (125, 161, 108), # ��n
  (125, 161, 109): (125, 161, 109), # ��n
  (127, 163, 111): (127, 163, 111), # ��n
  (128, 163, 111): (128, 163, 111), # ��n
  (129, 158, 146): (129, 158, 146), # ��n
  (129, 165, 112): (129, 165, 112), # ��n
  (130, 165, 113): (130, 165, 113), # ��n
  (132, 163, 155): (132, 163, 155), # ��n
  (132, 167, 115): (132, 167, 115), # ��n
  (132, 168, 115): (132, 168, 115), # ��n
  (133, 168, 116): (133, 168, 116), # ��n
  (134, 169, 117): (134, 169, 117), # ��n
  (135, 170, 118): (135, 170, 118), # ��n
  (136, 168, 155): (136, 168, 155), # ��n
  (136, 171, 120): (136, 171, 120), # ��n
  (137, 169, 158): (137, 169, 158), # ��n
  (138, 172, 121): (138, 172, 121), # ��n
  (139, 173, 122): (139, 173, 122), # ��n
  (140, 174, 125): (140, 174, 125), # ��n
  (140, 175, 124): (140, 175, 124), # ��n
  (141, 174, 126): (141, 174, 126), # ��n
  (142, 175, 127): (142, 175, 127), # ��n
  (143, 176, 128): (143, 176, 128), # ��n
  (144, 172, 137): (144, 172, 137), # ��n
  (144, 176, 128): (144, 176, 128), # ��n
  (146, 174, 143): (146, 174, 143), # ��n
  (146, 178, 131): (146, 178, 131), # ��n
  (147, 178, 131): (147, 178, 131), # ��n
  (148, 178, 156): (148, 178, 156), # ��n
  (151, 181, 136): (151, 181, 136), # ��n
  (151, 182, 136): (151, 182, 136), # ��n
  (156, 185, 142): (156, 185, 142), # ��n
  (157, 186, 143): (157, 186, 143), # ��n
  (158, 185, 189): (158, 185, 189), # ��n
  (159, 187, 145): (159, 187, 145), # ��n
  (161, 189, 147): (161, 189, 147), # ��n
  (161, 189, 148): (161, 189, 148), # ��n
  (163, 191, 151): (163, 191, 151), # ��n
  (164, 191, 151): (164, 191, 151), # ��n
}

missing = {}

for y in range(bitmap.height):
  for x in range(bitmap.width):
    rgb1 = bitmap.get_pixel(x, y)
    rgb2 = ctable.get(rgb1, (255, 128, 255))
    if ctable.get(rgb1) == None:
      missing[rgb1] = missing.get(rgb1, 0) + 1

    bitmap.set_pixel(x, y, rgb2)

outfile = open("tmp.ppm", "wb")
ppm = ppmlib.PpmWriter(bitmap)
ppm.write(outfile)
outfile.close()

def cmp(a, b):
  argb, ac = a
  brgb, bc = b
  return ac - bc
missing = missing.items()
missing.sort(cmp)
for (rgb, count) in missing:
  r, g, b = rgb
  #if g > r and g > b:
  if b > r and b > g:
    print (rgb, count)
