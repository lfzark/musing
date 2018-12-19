from musing import MusingRhythm,Clip,Musing
r = '-- - - -- ..|-- - - -- -- --|- -'
mr = MusingRhythm(r,unit_time=3)
print (len(mr))
m = ['E5','E5','D5','E5','E5','E5','G5','E5','D5','E5','D5','D5']
#clip = Clip(mr,m)
clip = Clip()
clip.add_column_chords("C4M")
clip.last(0.2)
clip.add_arp("C4m",beat_time=2.0)
clip.last(1)
clip.add_column_chords("E4m")
clip.play()

# muse = Musing()
# muse.add_track(clip)
# muse.add_track(Clip(mr,['E5','E5','E5','E5','E5','E5','E5','E5','E5','E5'])+clip)
# muse.play()