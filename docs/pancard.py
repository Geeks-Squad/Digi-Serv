class PanCard():
    def __init__(self, image):
        self.image = image

    def store_info(self, PanNumber, Name, FathersName, DOB):
        self.pan_number = PanNumber
        self.name = Name
        self.fathers_name = FathersName
        self.dob = DOB
