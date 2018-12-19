from musing import MusingRhythm,Clip,Musing
r = '-- - - -- ..|-- - - -- -- --|- -'
mr = MusingRhythm(r,unit_time=4)
print (len(mr))
m = ['E5','E5','D5','E5','E5','E5','G5','E5','D5','E5']
clip = Clip(mr,m)
clip.play()
muse = Musing()
muse.add_track(clip)
muse.add_track(Clip(mr,['E5','E5','E5','E5','E5','E5','E5','E5','E5','E5'])+clip)
muse.play()