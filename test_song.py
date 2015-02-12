import music

def test_ctor():
    s = music.Song()
    assert len(s.notes) > 0
    assert s.note_index == 0

    s2 = music.Song(['D4'])
    assert len(s2.notes) == 1
    assert s2.note_index == 0
