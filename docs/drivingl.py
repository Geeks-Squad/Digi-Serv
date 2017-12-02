
class DrivingLicense():
    def __init__(self, image):
        self.image = image

    def store_info(self, DOI, DLNumber, Name, Relation, DOB):
        self.doi = DOI
        self.DLNumber = DLNumber
        self.name = Name
        self.relation = Relation
        self.dob = DOB
