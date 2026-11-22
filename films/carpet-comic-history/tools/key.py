"""Extract and despill the eight generated puppet components."""
from pathlib import Path
from PIL import Image
import numpy as np
p=Path(__file__).resolve().parents[1]/'assets'
def extract(sheet, rows):
    im = Image.open(p/sheet).convert('RGB')
    columns = len(rows[0])
    for row, names in enumerate(rows):
        for col, name in enumerate(names):
            if name is None:
                continue
            bounds = (im.width*col//columns, im.height*row//len(rows),
                      im.width*(col+1)//columns, im.height*(row+1)//len(rows))
            a = np.asarray(im.crop(bounds)).astype(float)
            d = a[:,:,1] - np.maximum(a[:,:,0], a[:,:,2])
            alpha = np.clip((73-d)/53,0,1)
            a[:,:,1] -= np.maximum(d-8,0)*np.clip((d-8)/35,0,1)
            rgba = Image.fromarray(np.dstack((a,255*alpha)).clip(0,255).astype('uint8'))
            rgba.crop(rgba.getbbox()).save(p/f'{name}.png')

extract('puppets.png', [[f'{i}-{part}' for part in ('head','arm','torso','legs')]
                       for i in range(2)])
extract('actions-v2.png', [['weaver-question','weaver-smile','rug-cut'],
                           ['merchant-shock','merchant-doubt','wool']])
extract('actions-v3.png', [['weaver-focus','weaver-delight','merchant-sheepish','merchant-thinking'],
                           ['pattern-chart','weaving-shuttle','beater-comb',None]])
extract('actions-v4.png', [['trade-ledger','travel-parcel']])
