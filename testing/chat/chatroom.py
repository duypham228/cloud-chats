


class Chatroom:
    def __init__(self, flightNum):
        self.flightNum = flightNum
        self.guests = []

    def flight(self):
        return self.flightNum

    def guestNum(self):
        return len(self.guests)
    
    def guestList(self):
        return self.guests

    def addGuest(self, guest):
        self.guests += [guest]


class Guest:
    def __init__(self, name, flightNum = ""):
        self.name = name
        
    








