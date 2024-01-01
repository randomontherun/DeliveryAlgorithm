class Truck:

    def __init__(self, name, packages, mileage, address, depart_time):
        self.name = name
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        return "%s, %s, %s, %s" % (self.packages, self.mileage, self.address, self.depart_time)