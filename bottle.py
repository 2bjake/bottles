class Bottle:
    """Bottle which can be filled with liquid """
    def __init__(self, width, height, percent_filled=0, liquid_color=(0, 0, 255)):
        self.width = width
        self.height = height
        self.percent_filled = percent_filled
        self.liquid_color = liquid_color

    def get_liquid_height(self):
        return self.height * self.percent_filled / 100

    liquid_height = property(get_liquid_height)

    #TODO: concurrency issues
    #TODO: adjusting the percentage is a hack. Ideally liquid is added/removed by volume.
    # the percentage filled after a certain amount of liquid is added/removed
    # should depend on the volume of the bottle
    def adjust_liquid(self, fill_adjust):
        new_fill_percent = self.percent_filled + fill_adjust
        if  new_fill_percent > 100:
            new_fill_percent = 100
        elif new_fill_percent < 0:
            new_fill_percent = 0;

        self.percent_filled = new_fill_percent
