import os
from pathlib import Path

import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2
import funcy as F
 
import fp
import file_utils as fu

    
def ucode2img(hwc, init_xy, font, bgra, ucode):
    img_pil = Image.fromarray( np.zeros(hwc, np.uint8) )
    draw = ImageDraw.Draw(img_pil)
    draw.text(init_xy, chr(ucode), font=font, fill=bgra)
    return np.array(img_pil)

def char_imgs(font, ucode_list, hwc=(32,32,3), init_xy=(3,1)):
    #return fp.lmap(
    return fp.tmap(
        lambda ucode: ucode2img(
            hwc, init_xy, font, (255,255,255,0), ucode),
        ucode_list)

     #dst_path os.makedirs(dst_path)

def main():
    gulim_font = ImageFont.truetype("fonts/gulim.ttf", 28)
    reko_font = ImageFont.truetype("fonts/reko.ttf", 28)
    
    # jap: 169 chars
    jap_ucodes = fp.go(
        F.lconcat(range(0x3041, 0x309f+1),  # Hiragana
                  range(0x30a0, 0x30ff+1)), # Katakana
                 #range(0xff00, 0xffef+1), # Full-width roman characters and half-width katakana
        fp.lremove(
            {0x3094, 0x3095, 0x3096, 0x3097, 0x3098, 0x3099,
             0x309a, 0x309b, 0x309c, 0x309d, 0x309e, 0x309f,
             0x30a0, 0x30f7, 0x30f8, 0x30f9, 0x30fa, 0x30fb,
             0x30fc, 0x30fd, 0x30fe, 0x30ff}))
    # kor: 966 chars
    kor_ucodes = fp.go(
        fu.read_text("./freq_kor_words.txt"),
        F.distinct, fp.remove({"\n", " "}), fp.tmap(ord))

    # Create imgs
    jap_gulim_imgs = char_imgs(gulim_font, jap_ucodes)
    jap_reko_imgs  = char_imgs( reko_font, jap_ucodes)
    kor_gulim_imgs = char_imgs(gulim_font, kor_ucodes)
    kor_reko_imgs  = char_imgs( reko_font, kor_ucodes)

    # Create dirs
    os.makedirs("datasets/jk_all/testA", exist_ok=True)
    os.makedirs("datasets/jk_all/testB", exist_ok=True)
    os.makedirs("datasets/jk_all/trainA", exist_ok=True)
    os.makedirs("datasets/jk_all/trainB", exist_ok=True)
    
    os.makedirs("datasets/jk_no_kg/testA", exist_ok=True)
    os.makedirs("datasets/jk_no_kg/testB", exist_ok=True)
    os.makedirs("datasets/jk_no_kg/trainA", exist_ok=True)
    os.makedirs("datasets/jk_no_kg/trainB", exist_ok=True)
    
    os.makedirs("datasets/jk_no_kr/testA", exist_ok=True)
    os.makedirs("datasets/jk_no_kr/testB", exist_ok=True)
    os.makedirs("datasets/jk_no_kr/trainA", exist_ok=True)
    os.makedirs("datasets/jk_no_kr/trainB", exist_ok=True)

    @F.autocurry
    def dst_path(base, split, type, ucode, ext=".png"):
        return str(Path(base, split, type + str(ucode) + ext))
    # Save imgs
    jk_all   = dst_path("datasets/jk_all")
    jk_no_kg = dst_path("datasets/jk_no_kg") # no kor gulim
    jk_no_kr = dst_path("datasets/jk_no_kr") # no kor reko

    path_ucodes_imgs_tups = (
        (jk_all("testA","g"), jap_ucodes, jap_gulim_imgs ),
        (jk_all("testA","g"), kor_ucodes, kor_gulim_imgs ),
        (jk_all("testB","r"), jap_ucodes, jap_reko_imgs  ),
        (jk_all("testB","r"), kor_ucodes, kor_reko_imgs  ),
        (jk_all("trainA","g"), jap_ucodes, jap_gulim_imgs),
        (jk_all("trainA","g"), kor_ucodes, kor_gulim_imgs),
        (jk_all("trainB","r"), jap_ucodes, jap_reko_imgs ),
        (jk_all("trainB","r"), kor_ucodes, kor_reko_imgs ),
        
        (jk_no_kg("testA","g"), jap_ucodes, jap_gulim_imgs ),
        #(jk_no_kg("testA","g"), kor_ucodes, kor_gulim_imgs ),
        (jk_no_kg("testB","r"), jap_ucodes, jap_reko_imgs  ),
        (jk_no_kg("testB","r"), kor_ucodes, kor_reko_imgs  ),
        (jk_no_kg("trainA","g"), jap_ucodes, jap_gulim_imgs),
        #(jk_no_kg("trainA","g"), kor_ucodes, kor_gulim_imgs),
        (jk_no_kg("trainB","r"), jap_ucodes, jap_reko_imgs ),
        (jk_no_kg("trainB","r"), kor_ucodes, kor_reko_imgs ),
        
        (jk_no_kr("testA","g"), jap_ucodes, jap_gulim_imgs ),
        (jk_no_kr("testA","g"), kor_ucodes, kor_gulim_imgs ),
        (jk_no_kr("testB","r"), jap_ucodes, jap_reko_imgs  ),
        #(jk_no_kr("testB","r"), kor_ucodes, kor_reko_imgs  ),
        (jk_no_kr("trainA","g"), jap_ucodes, jap_gulim_imgs),
        (jk_no_kr("trainA","g"), kor_ucodes, kor_gulim_imgs),
        (jk_no_kr("trainB","r"), jap_ucodes, jap_reko_imgs ),
        #(jk_no_kr("trainB","r"), kor_ucodes, kor_reko_imgs ),
    )
    
                             
    for path, ucodes, imgs in path_ucodes_imgs_tups:
        for ucode, img in zip(ucodes, imgs):
            cv2.imwrite(path(ucode), img)
        

    
if __name__ == '__main__':
    main()
    #cv2.destroyAllWindows()
