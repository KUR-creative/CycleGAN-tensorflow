import pathlib

import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2
import funcy as F
 
import fp
import file_utils as fu

b,g,r,a = 255,255,255,0
fontpath = "fonts/reko.ttf"
#fontpath = "fonts/gulim.ttf"
font = ImageFont.truetype(fontpath, 28) # <- size

'''
# jap: 169 chars
n_list = fp.go(
    F.lconcat(range(0x3041, 0x309f+1),  # Hiragana
              range(0x30a0, 0x30ff+1)), # Katakana
              #range(0xff00, 0xffef+1), # Full-width roman characters and half-width katakana
    fp.lremove(
        {0x3094, 0x3095, 0x3096, 0x3097, 0x3098, 0x3099, 0x309a,
         0x309b, 0x309c, 0x309d, 0x309e, 0x309f, 0x30a0, 0x30f7,
         0x30f8, 0x30f9, 0x30fa, 0x30fb, 0x30fc, 0x30fd, 0x30fe, 0x30ff}))
    #fp.lmap(chr))
    
'''
# kor: 966 chars
n_list = fp.go(
    fu.read_text("./freq_kor_words.txt"),
    F.distinct,
    fp.remove({"\n", " "}),
    fp.lmap(ord))
    
print(len(n_list))
print(n_list)
#exit()
    
#for n in n_list[:10]:
for n in n_list:
    img_pil = Image.fromarray( np.zeros((32,32,3),np.uint8) )
    draw = ImageDraw.Draw(img_pil)
    draw.text((3, 1),  chr(n), font=font, fill=(b,g,r,a))
    cv2.imshow("res", np.array(img_pil))
    ans = cv2.waitKey()
    if ans != 102:
        print(chr(n), '| num =', n) 
        
        
cv2.destroyAllWindows()
