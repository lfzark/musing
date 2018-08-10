### Musing -  A Music theme lib for human,  make  compose music easy for coders.
---

### 1. Installation

```bash
pip install musing
```

### 2. Usage

Simple Melody

```python
from musing import Musing
muse = Musing()
muse.add_notes(['C5','C5', 'G5', 'G5', 'A5', 'A5', 'G5','F5','F5','E5','E5','D5','D5','C5'])
muse.play()
```

With Rhythm

```python
from musing import MusingRhythm,Clip
r = '-- - - -- ..|-- - - -- -- -- ----'
mr = MusingRhythm(r,unit_time=3)
m = ['E5','E5','D5','E5','E5','E5','G5','E5','D5','E5']
Clip(mr,m).play()
```

Read & Play MIDI File

```python
from musing import Musing
muse = Musing()
notes = Musing.midi_to_note()
muse.add_notes(notes)
muse.play()
```

### 3. TODO

- O-matic
- cross-platform
- More easy for human being
- Some Chords & Progression

### 4. Use Helper

- 1 2 3 4 5 6 7
- C D E F G A B

#### 4.1 Midi Player

If you want to play the midi file, you should install a midi player first.

- Linux :
    - CentOS  
        -  `sudo rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro`
        -  `sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm`
        - ` yum install epel*  timidity++`

    - Debian/Ubuntu `apt install timidity++`