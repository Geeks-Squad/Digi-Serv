from doc import Doc


class DrivingLicense(Doc):
    def __init__(self, image):
        self.image = image
        super(DrivingLicense, self).__init__("Driving License")

    def store_info(self, DOI, DLNumber, Name, Relation, DOB):
        self.doi = DOI
        self.DLNumber = DLNumber
        self.name = Name
        self.relation = Relation
        self.dob = DOB
