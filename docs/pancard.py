from docs.doc import Doc


class PanCard(Doc):
    def __init__(self, image):
        self.image = image
        super.__init__(self, "Pan Card")

    def store_info(self, PanNumber, Name, FathersName, DOB):
        self.pan_number = PanNumber
        self.name = Name
        self.fathers_name = FathersName
        self.dob = DOB
