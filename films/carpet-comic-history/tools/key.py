"""Extract and despill the eight generated puppet components."""
from pathlib import Path
from PIL import Image
import numpy as np
p=Path(__file__).resolve().parents[1]/'assets'
im=Image.open(p/'puppets.png').convert('RGB')
for row in range(2):
 for col,part in enumerate(('head','arm','torso','legs')):
  a=np.asarray(im.crop((im.width*col//4,im.height*row//2,im.width*(col+1)//4,im.height*(row+1)//2))).astype(float)
  m=np.maximum(a[:,:,0],a[:,:,2]);d=a[:,:,1]-m
  alpha=np.clip((73-d)/53,0,1)
  a[:,:,1]-=np.maximum(d-8,0)*np.clip((d-8)/35,0,1)
  rgba=Image.fromarray(np.dstack((a,255*alpha)).clip(0,255).astype('uint8'))
  rgba.crop(rgba.getbbox()).save(p/f'{row}-{part}.png')
