
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
        self.penalty = 0
        self.tolerance = 0

class Penalty:
    def __init__(self):
        self.num = 0
        self.pen = 0
        self.input_as_words = ""
        self.input_as_num = ""
        self.output_as_words = ''
        self.output_as_num = []


class Possibilistic:
    def __init__(self):
        self.num = 0
        self.tol = 0
        self.input_as_words = ''
        self.input_as_num = ''
        self.output_as_words = ''
        self.output_as_num = []

class Possibilistic_Object:
    def __init__(self):
        self.feasible_object_as_num = ''
        self.feasible_object = ''

class Feasible:
    def __init__(self):
        self.name = ""
        self.name_as_num = ''
        self.penalty_list = None
        self.pen_total = 0
        self.poss_list = None
        self.tolerance = 1
        self.penalty_exemp = ''
        self.poss_exemp = ''

class Qualitative:
    def __init__(self):
        self.num = 0
        self.input = ""
        self.output = ""

