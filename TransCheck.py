
from PIL import Image



def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False


print(has_transparency(Image.open(r"I:\Scripts\Test\iw9_models\head_sp_hero_ghost_shadowbase_lod\_images\usmc_headset\ximage_69eda2f98ad2e571.tiff")))