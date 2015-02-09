class Bottle:
    """Bottle which can be filled with liquid """
    def __init__(self, height, width, percent_filled=0):
        self.height = height
        self.width = width
        self.percent_filled = percent_filled

    def liquid_height(self):
        return self.height * self.percent_filled / 100

    #TODO: concurrency issues
    def adjust_liquid(self, fill_adjust):
        new_fill_percent = self.percent_filled + fill_adjust
        if  new_fill_percent > 100:
            new_fill_percent = 100
        elif new_fill_percent < 0:
            new_fill_percent = 0;

        self.percent_filled = new_fill_percent
