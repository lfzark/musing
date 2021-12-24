from musing import MusingRhythm,Clip
r = '.. - -|--- -|- - - -|-- - -|-- - -|- - - -|-'
mr = MusingRhythm(r,unit_time=1.8)
m = ['G5','B5',\
'C6','E6' , \
'F6','G6','B6','C7',
'G6','B6','C7',\
'F6','E6','F6', \
'D6','C6','B5','D6',\
'C6']
# 3

# for i in range(1,7):
#     Clip(mr,m,offset=i).play()
# c = Clip(mr,m,offset=3)
c = Clip(mr,m)
c.init_last_time(start = 0.9)
c.add_column_chords("G5M",beat_time=3)
c.play()
