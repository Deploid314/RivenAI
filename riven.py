class Riven:

    def __init__(self, weapon, stats, price):
        self.weapon = weapon
        self.calculated_stats = [0,0,0,0]
        for i in range(4):
            self.calculated_stats[i] = (float(stats[i])*9)/(float(stats[8])+1)
        self.stats = stats
        del self.stats[8]
        self.price = price