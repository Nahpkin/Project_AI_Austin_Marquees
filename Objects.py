
class Attribute:
    def __init__(self):
        self.name = ""
        self.numop1 = 0
        self.op1 = ""
        self.op2 = ""
        self.numop2 = -self.numop1


def print_attributes(attributes):
    # Print for testing Attribute reading
    for attribute in attributes:
        print("Attribute name: " + attribute.name)
        print("Option 1: " + attribute.op1 + ", " + str(attribute.numop1))
        print("Option 2: " + attribute.op2 + ", " + str(attribute.numop2) + "\n")

class Constraint:
    def __init__(self):
        self.num = 0
        self.input = ""
        self.output = ""

class Penalty:
    def __init__(self):
        self.num = 0
        self.pen = 0
        self.input = ""
        self.output = ""
