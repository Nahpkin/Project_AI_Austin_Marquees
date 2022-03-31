
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

# class Penalty_Object:
#     def __init__(self):
#         self.logic_statement = ''
#         self.feasible_object_as_num = ''
#         self.feasible_object = ''       # FixMe: Not sure if this is necessary
#         self.penalty = 0


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
        self.penalty_list = []
        self.pen2 = 0
        self.pen3 = 0
        self.pen_total = 0
        self.possib1 = 0
        self.possib2 = 0
        self.possib3 = 0
        self.possib_total = 0

class Qualitative:
    def __init__(self):
        self.num = 0
        self.input = ""
        self.output = ""

