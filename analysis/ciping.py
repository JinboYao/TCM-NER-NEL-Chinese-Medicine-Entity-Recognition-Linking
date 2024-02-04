import pkuseg
from collections import Counter
import pprint

media_con = []
with open ( "medical.txt") as f:
    media_con= f.read ()
seg = pkuseg.pkuseg(model_name= ' medicine ' )
meida_text = seg.cut(media_con)
media_stop = []
with open ( "stop.txt ", encoding="utf-8" ) as f :
    media_stop = f.read ()
n_text = []
for p in meida_text:
    if p not in media_stop:
        n_text.append(p)
conter = Counter(n_text)
pprint.pprint(conter.most_common (9))
