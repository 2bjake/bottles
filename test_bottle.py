import bottle

position = (1,2)
width = 50
height = 100
percent_filled = 5

def make_default_bottle(fill=percent_filled):
    return bottle.Bottle(position, width, height, fill)

def test_ctor():
    b = bottle.Bottle(position, width, height, 0)
    assert b.position == position
    assert b.width == width
    assert b.height == height
    assert b.percent_filled == 0


    b2 = make_default_bottle()
    assert b2.position == position
    assert b2.width == width
    assert b2.height == height
    assert b2.percent_filled == percent_filled

def test_get_rect():
    b = make_default_bottle()
    rect = b.get_rect()
    assert rect == (position, (width, height))

def test_get_liquid_height():
    b = make_default_bottle()
    assert b.get_liquid_height() == (height * percent_filled / 100)
    assert b.liquid_height == (height * percent_filled / 100)
    assert b.liquid_height == b.get_liquid_height()

def adjust_liquid_helper(start, adjust, expect):
    b = make_default_bottle(start)
    b.adjust_liquid(adjust)
    assert b.liquid_height == expect

def test_adjust_liquid():
    adjust_liquid_helper(0, -5, 0)
    adjust_liquid_helper(0, 0, 0)
    adjust_liquid_helper(5, -5, 0)
    adjust_liquid_helper(5, -6, 0)

    adjust_liquid_helper(100, 1, 100)
    adjust_liquid_helper(100, 0, 100)
    adjust_liquid_helper(99, 1, 100)
    adjust_liquid_helper(99, 2, 100)