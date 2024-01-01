class Package:

    def __init__(self, ID, address, city, state, zip_code, deadline, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.depart_time = None
        self.time_delivered = None
        self.on_truck = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (
        self.address, self.deadline, self.city, self.zip_code, self.weight + ' kilos', self.status)

    def status_at_time(self, time_lookup):
        if self.time_delivered <= time_lookup:
            self.status = "Delivered at " + str(self.time_delivered)
        elif self.depart_time < time_lookup:
            self.status = "En route on " + str(self.on_truck)
        else:
            self.status = "At Hub"