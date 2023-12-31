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
        self.time_delivered = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (
        self.ID, self.address, self.city, self.state, self.zip_code, self.deadline, self.weight, self.status)

    def update_status(self, convert_timedelta):
        if self.delivery_time < convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time > convert_timedelta:
            self.status = "En route"
        else:
            self.status = "At Hub"