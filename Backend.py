import os
import platform
from Objects import *
import re


# Main method
def Backend(files):
    # Make list of objects for program
    myAttributes = []
    myConstraints = []
    myPenalties = []
    myPossibilistics = []
    myQualitatives = []
    myFeasibleObjects = []
    myFeasibleObject = []

    # Parsing methods for files given
    parse_attributes_file(files[0], myAttributes)
    parse_constraints_file(files[1], myAttributes, myConstraints)
    parse_logic_file(files[2], myPenalties, myPossibilistics, myQualitatives, myAttributes)

    # Call Clasp and write to file
    os.system("clasp CNF.txt -n 0 > CLASPOutput.txt")


    # Storing feasible objects
    store_feasible_objects('CLASPOutput.txt', myFeasibleObjects, myAttributes)

    # Input for Penalty Logic with CLASP
    for index in range(len(myPenalties)):
        # Building and writing to input file for CLASP
        built_string = write_to_cnf_penalty_logic(myConstraints, myPenalties, index)
        add_beginning_of_clasp_penalty_statement(myAttributes, index, built_string)

        # Running CLASP
        os.system("clasp penalty_logic_input"
                  + str(index) + ".txt -n 0 > CLASP_Output_Penalty_Test" + str(index) + ".txt")

        # Storing results
        store_penalty_logic_results('CLASP_Output_Penalty_Test' + str(index) + '.txt', index, myPenalties)

    # Input for Possibilistic with CLASP
    for index in range(len(myPossibilistics)):
        # Building and writing to input file for CLASP
        built_string = write_to_cnf_possibilistic_logic(myConstraints, myPossibilistics, index)
        add_beginning_of_clasp_poss_statement(myAttributes, index, built_string)

        # Running CLASP
        os.system("clasp poss_logic_input" + str(index) + ".txt -n 0 > CLASP_Output_Poss_Test" + str(index)
                  + ".txt")

        # Storing results
        store_possibilistic_logic_results('CLASP_Output_Poss_Test' + str(index) + '.txt', myPossibilistics, index)

    # Cross-referencing feasible objects to apply penalty
    cross_reference_penalty(myFeasibleObjects, myPenalties)
    cross_reference_poss(myFeasibleObjects, myPossibilistics)
# ----------------------------------------------------------------------------------------------------------------------
# Writing to input files:
def write_to_cnf_hard_constraints(constraints):
    string_builder = ''
    for line in constraints:
        string_builder += line.output

    return string_builder

def add_beginning_of_clasp_constraints_statement(file_name, built_string, attributes):
    output_file = open(file_name, "w")
    test = built_string.split('\n')
    string_builder = ''

    clause_counter = 0
    for line in test:
        if line == '':
            clause_counter -= 1
        clause_counter += 1

    string_builder += "p cnf " + str(len(attributes)) + " " + str(clause_counter) + "\n" + built_string
    output_file.write(string_builder)
    output_file.close()

def write_to_cnf_penalty_logic(hard_constraints, penalty_logic, index):
    string_build = penalty_logic[index].input_as_num

    for line in hard_constraints:
        string_build += line.output

    return string_build

def add_beginning_of_clasp_penalty_statement(attributes, index, built_string):
    output_file = open('penalty_logic_input' + str(index) + '.txt', 'w')
    test = built_string.split('\n')

    clause_counter = 0
    for index in test:
        if index == '':
            clause_counter -= 1
        clause_counter += 1

    string_builder = built_string
    string_builder = 'p cnf ' + str(len(attributes)) + ' ' + str(clause_counter) + '\n' + string_builder
    output_file.write(string_builder)
    output_file.close()

def write_to_cnf_possibilistic_logic(hard_constraints, poss_logic, index):
    string_build = poss_logic[index].input_as_num

    for line in hard_constraints:
        string_build += line.output

    return string_build

def add_beginning_of_clasp_poss_statement(attributes, index, built_string):
    output_file = open('poss_logic_input' + str(index) + '.txt', 'w')
    test = built_string.split('\n')

    clause_counter = 0
    for index in test:
        if index == '':
            clause_counter -= 1
        clause_counter += 1

    string_builder = built_string
    string_builder = 'p cnf ' + str(len(attributes)) + ' ' + str(clause_counter) + '\n' + string_builder
    output_file.write(string_builder)
    output_file.close()


# ----------------------------------------------------------------------------------------------------------------------
# Parsing files from user:
# Parses the Attributes file from Words to Binary Logic (Stored in list of Attribute objects)
def parse_attributes_file(file_name, attributes):
    # Open file pointer to read lines
    input_file = open(file_name, "r")
    Lines = input_file.readlines()

    # Start parsing Attribute File
    i = 0
    for line in Lines:
        # Initialize new Attribute object and add to list
        attributes.append(Attribute())
        # Use regex to parse lines into variables and assign to attribute object
        tokens = re.split(r"[:,\s\n]+", line)
        attributes[i].name = tokens[0]
        attributes[i].op1 = tokens[1]
        attributes[i].op2 = tokens[2]
        attributes[i].numop1 = i + 1
        attributes[i].numop2 = -i - 1

        # Iterate variable
        i += 1

    # Close input file stream
    input_file.close()
    return attributes
    # Parses the Hard Constraints file from Words to Binary Logic(Stored in list of Constraint objects)


def parse_constraints_file(file_name, attributes, constraints):
    # Open file pointer to read lines
    input_file = open(file_name, "r")
    Lines = input_file.readlines()

    # Start parsing the file
    # Add "p cnf" header to CNF output
    constraints.append(Constraint())
    # constraints[0].output = "p cnf " + str(len(attributes)) + " " + str(len(Lines)) + "\n"
    # Body of CNF file
    i = 0
    for line in Lines:
        # Initialize new constraint Object
        constraints.append(Constraint())

        # Split line into tokens
        constraints[i].input = line
        tokens = re.split(r"[\n\s]", line)

        # Parse tokens using attribute object (Compatible with any type of file)
        j = 0
        while j < len(tokens):
            if tokens[j] == "NOT":
                k = 0
                while (tokens[j + 1] != attributes[k].op1) & (tokens[j + 1] != attributes[k].op2):
                    k += 1
                if tokens[j + 1] == attributes[k].op1:
                    constraints[i].output += " " + str(attributes[k].numop2)
                if tokens[j + 1] == attributes[k].op2:
                    constraints[i].output += " " + str(attributes[k].numop1)
                j += 2
                continue
            # Case: OR condition
            elif tokens[j] == "OR":
                # Iterative variable
                j += 1
                continue
            # Case: for EOL and random empty blo
            elif tokens[j] == '':
                break
            else:
                k = 0
                while ((tokens[j] != attributes[k].op1) & (tokens[j] != attributes[k].op2)):
                    # Iterative variable
                    k += 1
                if tokens[j] == attributes[k].op1:
                    constraints[i].output += " " + str(attributes[k].numop1)
                if tokens[j] == attributes[k].op2:
                    constraints[i].output += " " + str(attributes[k].numop2)
            # Iterative variable
            j += 1
        # Add a new line to output
        constraints[i].output += " 0\n"

        i += 1

    # Print out constraints output
    built_string = write_to_cnf_hard_constraints(constraints)
    add_beginning_of_clasp_constraints_statement("CNF.txt", built_string, attributes)

    # Close file stream
    input_file.close()
    return constraints

# Parses Logic file to save into Object lists
def parse_logic_file(file_name, penalties, possibilistics, qualitatives, attributes):
    # Open and read file lines
    input_file = open(file_name, "r")
    Lines = input_file.readlines()

    # Create str to hold Logic inputs
    pen_input = []
    possib_input = []
    qual_input = []

    # Split up File into respective Logic inputs
    # Penalty
    i = 0
    while (Lines[i] != "\n"):
        pen_input.append(Lines[i].split("\n"))
        i += 1
    i += 2
    # Possibilistic
    while (Lines[i] != "\n"):
        possib_input.append(Lines[i].split("\n"))
        i += 1
    # Qualitative Form
    i += 2
    while i < len(Lines):
        qual_input.append(Lines[i].split("\n"))
        i += 1

    # Call parse functions to store Logics in respective Objects
    Logics = []
    Logics.append(parse_penalty_logic(pen_input, penalties, attributes))
    Logics.append(parse_possibilistic_logic(possib_input, possibilistics, attributes))
    Logics.append(parse_qualitative_logic(qual_input, qualitatives, attributes))

    # Return List of all 3 logics in Object List format
    return Logics

# Parses penalty logic into Object Penalty format
def parse_penalty_logic(pen_input, penalties, attributes):
    i = 1
    penalties.append(Penalty())
    while i < len(pen_input):
        # Add new Penalty object to list
        penalties.append(Penalty())

        # Split line into tokens
        penalties[i].input_as_words = pen_input[i]
        tokens = re.split(r'[,]+', pen_input[i][0])
        penalties[i].pen = tokens[1]
        tokens = tokens[0].split(" ")

        j = 0
        while j < len(tokens):
            # Case: NOT condition
            if tokens[j] == "NOT":
                k = 0
                while (tokens[j + 1] != attributes[k].op1) & (tokens[j + 1] != attributes[k].op2):
                    k += 1
                if tokens[j + 1] == attributes[k].op1:
                    penalties[i].input_as_num += str(attributes[k].numop2) + " "
                if tokens[j + 1] == attributes[k].op2:
                    penalties[i].input_as_num += str(attributes[k].numop1) + " "
                j += 2
                continue
            # Case: OR condition
            elif tokens[j] == "OR":
                # Iterative variable
                j += 1
                continue
            # Case: for EOL and random empty block
            elif tokens[j] == '':
                break
                # Case: AND condition
            elif tokens[j] == "AND":
                penalties[i].input_as_num += "0\n"
                j += 1
                continue
            else:
                k = 0
                while (tokens[j] != attributes[k].op1) & (tokens[j] != attributes[k].op2):
                    # Iterative variable
                    k += 1
                if tokens[j] == attributes[k].op1:
                    penalties[i].input_as_num += str(attributes[k].numop1) + " "
                if tokens[j] == attributes[k].op2:
                    penalties[i].input_as_num += str(attributes[k].numop2) + " "
            # Iterative variable
            j += 1
        penalties[i].input_as_num += '0\n'
        i += 1
    penalties.remove(penalties[0])
    return penalties


def parse_possibilistic_logic(possib_input, possibilistics, attributes):
    i = 1
    possibilistics.append(Possibilistic())
    while i < len(possib_input):
        # Add new Penalty object to list
        possibilistics.append(Possibilistic())

        # Split line into tokens
        possibilistics[i].input_as_words = possib_input[i]
        tokens = re.split(r'[,]+', possib_input[i][0])
        possibilistics[i].tol = tokens[1]
        tokens = tokens[0].split(" ")

        j = 0
        while j < len(tokens):
            # Case: NOT condition
            if tokens[j] == "NOT":
                k = 0
                while (tokens[j + 1] != attributes[k].op1) & (tokens[j + 1] != attributes[k].op2):
                    k += 1
                if tokens[j + 1] == attributes[k].op1:
                    possibilistics[i].input_as_num += str(attributes[k].numop2) + " "
                if tokens[j + 1] == attributes[k].op2:
                    possibilistics[i].input_as_num += str(attributes[k].numop1) + " "
                j += 2
                continue
            # Case: OR condition
            elif tokens[j] == "OR":
                # Iterative variable
                j += 1
                continue
            # Case: for EOL and random empty block
            elif tokens[j] == '':
                break
                # Case: AND condition
            elif tokens[j] == "AND":
                possibilistics[i].input_as_num += "0\n"
                j += 1
                continue
            else:
                k = 0
                while (tokens[j] != attributes[k].op1) & (tokens[j] != attributes[k].op2):
                    # Iterative variable
                    k += 1
                if tokens[j] == attributes[k].op1:
                    possibilistics[i].input_as_num += str(attributes[k].numop1) + " "
                if tokens[j] == attributes[k].op2:
                    possibilistics[i].input_as_num += str(attributes[k].numop2) + " "
            # Iterative variable
            j += 1
        possibilistics[i].input_as_num += '0\n'
        i += 1
    possibilistics.remove(possibilistics[0])
    return possibilistics


def parse_qualitative_logic(qual_input, qualitatives, attributes):
    i = 1
    qualitatives.append(Qualitative())
    while i < len(qual_input):
        # Add new Penalty object to list
        qualitatives.append(Qualitative())

        # Split line into tokens
        qualitatives[i].input = qual_input[i][0]
        tokens = qual_input[i][0].split(" ")
        i += 1
    qualitatives.remove(qualitatives[0])
    return qualitatives
    # ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Stores feasible objects given by CLASP in Object Feasible Format
def store_feasible_objects(file_name, feasible_objects, attributes):
    clasp_output = open(file_name, 'r')

    # Converting words to numbers for CLASP later on
    index = 0
    for line in clasp_output.readlines():
        if line[0] == 'v':
            feasible_objects.append(Feasible())
            line = line.split('v ')
            line.remove(line[0])
            line = line[0].split(' 0\n')
            feasible_objects[index].name_as_num = line[0]
            index += 1

    # Converting numbers back to words for output
    for object in feasible_objects:
        # Splitting numbers by spaces
        individual_feasibleobject_list = object.name_as_num.split(' ')
        attribute_index = 0
        object.name += '<'
        for number in individual_feasibleobject_list:
            number = int(number)
            if number == attributes[attribute_index].numop1:
                object.name += attributes[attribute_index].op1 + ' '
            elif number == attributes[attribute_index].numop2:
                object.name += attributes[attribute_index].op2 + ' '
            attribute_index += 1
        object.name += '>'

# Stores objects from output with penalty logic
def store_penalty_logic_results(file_name, index, penalty_list):
    clasp_output = open(file_name, 'r')

    for line in clasp_output.readlines():
        if line[0] == 'v':
            line = line.split('v ')
            line.remove(line[0])
            line = line[0].split(' 0\n')
            penalty_list[index].output_as_num.append(line[0])
        if line[0] == 's' and line[2] == 'U':
            penalty_list[index].output_as_num.append('')

# Store objects from output with possibilistic logic
def store_possibilistic_logic_results(file_name, poss_list, index):
    clasp_output = open(file_name, 'r')

    for line in clasp_output.readlines():
        if line[0] == 'v':
            line = line.split('v ')
            line.remove(line[0])
            line = line[0].split(' 0\n')
            poss_list[index].output_as_num.append(line[0])

# ----------------------------------------------------------------------------------------------------------------------

# Cross-Referencing Feasible Objects and Objects from CLASP To Apply Penalty
def cross_reference_penalty(feasible_objects_list, penalty_list):
    for outer_index in range(len(feasible_objects_list)):
        feasible_objects_list[outer_index].penalty_list = [0] * len(penalty_list)
        for middle_index in range(len(penalty_list)):
            for inner_index in range(len(penalty_list[middle_index].output_as_num)):
                if (feasible_objects_list[outer_index].name_as_num ==
                        penalty_list[middle_index].output_as_num[inner_index]):
                    feasible_objects_list[outer_index].penalty_list[middle_index] = 0
                    break
                feasible_objects_list[outer_index].penalty_list[middle_index] = int(penalty_list[middle_index].pen)

    for feasible_object in feasible_objects_list:
        for penalty in feasible_object.penalty_list:
            feasible_object.pen_total += penalty

# Cross-Reference Feasible Objects and Objects from CLASP to Apply Tolerance
def cross_reference_poss(feasible_objects_list, poss_list):
    for outer_index in range(len(feasible_objects_list)):
        feasible_objects_list[outer_index].poss_list = [1] * len(poss_list)
        for middle_index in range(len(poss_list)):
            for inner_index in range(len(poss_list[middle_index].output_as_num)):
                if feasible_objects_list[outer_index].name_as_num == poss_list[middle_index].output_as_num[inner_index]:
                    feasible_objects_list[outer_index].poss_list[middle_index] = 1
                    break
                feasible_objects_list[outer_index].poss_list[middle_index] = 1 - float(poss_list[middle_index].tol)

    for feasible_object in feasible_objects_list:
        for tolerance in feasible_object.poss_list:
            if tolerance < feasible_object.tolerance:
                feasible_object.tolerance = tolerance
