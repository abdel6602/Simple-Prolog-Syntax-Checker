
from scanner import *
from nltk.tree import *

def Parse():
    j = 0
    Children = []

    # Predicates Part
    Predicates_dict = Predicates(j)
    Children.append(Predicates_dict["node"])

    # Clause Part
    Clause_dict = Clause(Predicates_dict["index"])
    Children.append(Clause_dict["node"])

    # Goal Part
    Goal_dict = Goal(Clause_dict["index"])
    Children.append(Goal_dict["node"])

    if len(tokens) - 1 > Goal_dict["index"]:
        errors.append("Syntax Error: Extra Goal Statement(s)")

    Node = Tree('Program', Children)
    return Node


def Predicates(j):
    dict_output = dict()
    Children = []

    # predicates token
    predicates_dict = Match(TokenType.PREDICATE_KEYWORD, j)
    Children.append(predicates_dict["node"])

    # Pstatement Part
    Pstatement_dict = Pstatement(predicates_dict["index"])
    Children.append(Pstatement_dict["node"])

    dict_output["node"] = Tree("Predicates", Children)
    dict_output["index"] = Pstatement_dict["index"]
    return dict_output


def Clause(j):
    dict_output = dict()
    Children = []

    # clauses token
    clauses_dict = Match(TokenType.CLAUSES_KEYWORD, j)
    Children.append(clauses_dict["node"])

    # Cstatements Part
    Cstatements_dict = Cstatements(clauses_dict["index"])
    Children.append(Cstatements_dict["node"])

    dict_output["node"] = Tree("Clause", Children)
    dict_output["index"] = Cstatements_dict["index"]
    return dict_output


def Goal(j):
    dict_output = dict()
    Children = []

    # goal token
    goal_dict = Match(TokenType.GOAL_KEYWORD, j)
    Children.append(goal_dict["node"])

    # Fact Part
    Fact_dict = Fact(goal_dict["index"])
    Children.append(Fact_dict["node"])

    # dot token
    dot_dict = Match(TokenType.DOT_OP, Fact_dict["index"])
    Children.append(dot_dict["node"])

    dict_output["node"] = Tree("Goal", Children)
    dict_output["index"] = dot_dict["index"]
    return dict_output


def Pstatement(j):
    dict_output = dict()
    Children = []

    # Definition Part
    Definition_dict = Definition(j)
    Children.append(Definition_dict["node"])
    dict_output["index"] = Definition_dict["index"]

    condition = tokens[Definition_dict["index"]].token_type
    if condition == TokenType.IDENTIFIER:
        # Pstatement_ast Part   --> (recursion of Pstatement which is this function)
        Pstatement_dict = Pstatement(Definition_dict["index"])
        Children.append(Pstatement_dict["node"])
        dict_output["index"] = Pstatement_dict["index"]

    dict_output["node"] = Tree("Pstatement", Children)
    return dict_output


def Definition(j):
    dict_output = dict()
    Children = []

    # pred_name token
    predName_dict = Match(TokenType.IDENTIFIER, j)
    Children.append(predName_dict["node"])
    dict_output["index"] = predName_dict["index"]

    condition = tokens[predName_dict["index"]].lexeme
    if condition == '(':
        # Definition_ast Part
        Definition_ast_dict = Definition_ast(predName_dict["index"])
        Children.append(Definition_ast_dict["node"])
        dict_output["index"] = Definition_ast_dict["index"]

    dict_output["node"] = Tree("Definition", Children)
    return dict_output


def Definition_ast(j):
    dict_output = dict()
    Children = []

    # open-bracket token
    openBracket_dict = Match(TokenType.OPEN_BRACKET, j)
    Children.append(openBracket_dict["node"])

    # Parameters Part
    Parameters_dict = Parameters(openBracket_dict["index"])
    Children.append(Parameters_dict["node"])

    # close-bracket token
    closeBracket_dict = Match(TokenType.CLOSE_BRACKET, Parameters_dict["index"])
    Children.append(closeBracket_dict["node"])

    dict_output["node"] = Tree("Definition_ast", Children)
    dict_output["index"] = closeBracket_dict["index"]
    return dict_output


def Parameters(j):
    dict_output = dict()
    Children = []
    condition = tokens[j].token_type

    # datatype token
    match condition:
        case TokenType.INTEGER_DATA_TYPE:
            datatype_dict = Match(TokenType.INTEGER_DATA_TYPE, j)
        case TokenType.REAL_DATA_TYPE:
            datatype_dict = Match(TokenType.REAL_DATA_TYPE, j)
        case TokenType.STRING_DATA_TYPE:
            datatype_dict = Match(TokenType.STRING_DATA_TYPE, j)
        case TokenType.CHAR_DATA_TYPE:
            datatype_dict = Match(TokenType.CHAR_DATA_TYPE, j)
        case _:
            datatype_dict = Match(TokenType.SYMBOL_DATA_TYPE, j)

    Children.append(datatype_dict["node"])
    dict_output["index"] = datatype_dict["index"]

    condition = tokens[datatype_dict["index"]].lexeme
    if condition == ',':
        # Parameters_ast Part
        Parameters_ast_dict = Parameters_ast(datatype_dict["index"])
        Children.append(Parameters_ast_dict["node"])
        dict_output["index"] = Parameters_ast_dict["index"]


    dict_output["node"] = Tree("Parameters", Children)
    return dict_output


def Parameters_ast(j):
    dict_output = dict()
    Children = []

    # comma token
    comma_dict = Match(TokenType.AND_OP, j)
    Children.append(comma_dict["node"])

    # Parameters Part
    Parameters_dict = Parameters(comma_dict["index"])
    Children.append(Parameters_dict["node"])

    dict_output["node"] = Tree("Parameters_ast", Children)
    dict_output["index"] = Parameters_dict["index"]
    return dict_output


def Cstatements(j):
    dict_output = dict()
    Children = []

    # Cstatement Part
    Cstatement_dict = Cstatement(j)
    Children.append(Cstatement_dict["node"])
    dict_output["index"] = Cstatement_dict["index"]

    condition = tokens[Cstatement_dict["index"]].token_type
    if condition == TokenType.IDENTIFIER:
        # Cstatements_ast Part  --> (recursion of Cstatements which is this function)
        Cstatements_dict = Cstatements(Cstatement_dict["index"])
        Children.append(Cstatements_dict["node"])
        dict_output["index"] = Cstatements_dict["index"]

    dict_output["node"] = Tree("Cstatements", Children)
    return dict_output


def Cstatement(j):
    dict_output = dict()
    Children = []
    condition = tokens[Fact(j)["index"]].lexeme

    if condition == ':-':
        # Rule Part
        Rule_dict = Rule(j)
        Children.append(Rule_dict["node"])

        # dot token
        dot_dict = Match(TokenType.DOT_OP, Rule_dict["index"])
        Children.append(dot_dict["node"])
        dict_output["index"] = dot_dict["index"]

    else:            # when condition == '.' or when it's error
        # Fact Part
        Fact_dict = Fact(j)
        Children.append(Fact_dict["node"])

        # dot token
        dot_dict = Match(TokenType.DOT_OP, Fact_dict["index"])
        Children.append(dot_dict["node"])
        dict_output["index"] = dot_dict["index"]

    dict_output["node"] = Tree("Cstatement", Children)
    return dict_output


def Fact(j):
    dict_output = dict()
    Children = []

    # pred_name token
    predName_dict = Match(TokenType.IDENTIFIER, j)
    Children.append(predName_dict["node"])
    dict_output["index"] = predName_dict["index"]

    condition = tokens[predName_dict["index"]].lexeme
    if condition == '(':
        # Fact_ast Part
        Fact_ast_dict = Fact_ast(predName_dict["index"])
        Children.append(Fact_ast_dict["node"])
        dict_output["index"] = Fact_ast_dict["index"]

    dict_output["node"] = Tree("Fact", Children)
    return dict_output


def Fact_ast(j):
    dict_output = dict()
    Children = []

    # open-bracket token
    openBracket_dict = Match(TokenType.OPEN_BRACKET, j)
    Children.append(openBracket_dict["node"])

    # Fparameters Part
    Fparameters_dict = Fparameters(openBracket_dict["index"])
    Children.append(Fparameters_dict["node"])

    # close-bracket token
    closeBracket_dict = Match(TokenType.CLOSE_BRACKET, Fparameters_dict["index"])
    Children.append(closeBracket_dict["node"])

    dict_output["node"] = Tree("Fact_ast", Children)
    dict_output["index"] = closeBracket_dict["index"]
    return dict_output


def Rule(j):
    dict_output = dict()
    Children = []

    # Fact Part
    Fact_dict = Fact(j)
    Children.append(Fact_dict["node"])

    # rule-operator token
    assignment_dict = Match(TokenType.ASSIGNMENT_OP, Fact_dict["index"])
    Children.append(assignment_dict["node"])

    # Body Part
    Body_dict = Body(assignment_dict["index"])
    Children.append(Body_dict["node"])

    dict_output["node"] = Tree("Rule", Children)
    dict_output["index"] = Body_dict["index"]
    return dict_output


def Body(j):
    dict_output = dict()
    Children = []

    # Bstatement Part
    Bstatement_dict = Bstatement(j)
    Children.append(Bstatement_dict["node"])
    dict_output["index"] = Bstatement_dict["index"]

    condition = tokens[Bstatement_dict["index"]].lexeme
    if condition == ',' or condition == ';':
        # Body_ast Part
        Body_ast_dict = Body_ast(Bstatement_dict["index"])
        Children.append(Body_ast_dict["node"])
        dict_output["index"] = Body_ast_dict["index"]

    dict_output["node"] = Tree("Body", Children)
    return dict_output


def Bstatement(j):
    dict_output = dict()
    Children = []
    condition = tokens[j].token_type

    if condition == TokenType.IDENTIFIER:
        # Fact Part
        Fact_dict = Fact(j)
        Children.append(Fact_dict["node"])

        dict_output["index"] = Fact_dict["index"]

    elif condition == TokenType.VARIABLE or condition == TokenType.INTEGER_VALUE \
     or condition == TokenType.REAL_VALUE or condition == TokenType.STRING_VALUE \
     or condition == TokenType.IDENTIFIER:

        # Variable Part
        Variable_dict = Variable(j)
        Children.append(Variable_dict["node"])

        dict_output["index"] = Variable_dict["index"]

    elif condition == TokenType.WRITE_KEYWORD:
        # write token
        write_dict = Match(TokenType.WRITE_KEYWORD, j)
        Children.append(write_dict["node"])

        # open-bracket token
        openBracket_dict = Match(TokenType.OPEN_BRACKET, write_dict["index"])
        Children.append(openBracket_dict["node"])

        # String Part
        String_dict = String(openBracket_dict["index"])
        Children.append(String_dict["node"])

        # close-bracket token
        closeBracket_dict = Match(TokenType.CLOSE_BRACKET, String_dict["index"])
        Children.append(closeBracket_dict["node"])

        dict_output["index"] = closeBracket_dict["index"]

    else:
        # Input token
        match condition:
            case TokenType.READ_CHAR_KEYWORD:
                input_dict = Match(TokenType.READ_CHAR_KEYWORD, j)
            case TokenType.READ_INT_KEYWORD:
                input_dict = Match(TokenType.READ_INT_KEYWORD, j)
            case _:
                input_dict = Match(TokenType.READ_LN_KEYWORD, j)

        Children.append(input_dict["node"])

        # open-bracket token
        openBracket_dict = Match(TokenType.OPEN_BRACKET, input_dict["index"])
        Children.append(openBracket_dict["node"])

        # variable token
        variable_dict = Match(TokenType.VARIABLE, openBracket_dict["index"])
        Children.append(variable_dict["node"])

        # close-bracket token
        closeBracket_dict = Match(TokenType.CLOSE_BRACKET, variable_dict["index"])
        Children.append(closeBracket_dict["node"])

        dict_output["index"] = closeBracket_dict["index"]


    dict_output["node"] = Tree("Bstatement", Children)
    return dict_output


def Body_ast(j):
    dict_output = dict()
    Children = []
    condition = tokens[j].lexeme

    if condition == ',':
        # comma token
        comma_dict = Match(TokenType.AND_OP, j)
        Children.append(comma_dict["node"])

        # Body Part
        Body_dict = Body(comma_dict["index"])
        Children.append(Body_dict["node"])
        dict_output["index"] = Body_dict["index"]

    else:  # when condition == ';'
        # semicolon token
        semicolon_dict = Match(TokenType.OR_OP, j)
        Children.append(semicolon_dict["node"])

        # Body Part
        Body_dict = Body(semicolon_dict["index"])
        Children.append(Body_dict["node"])
        dict_output["index"] = Body_dict["index"]

    dict_output["node"] = Tree("Body_ast", Children)
    return dict_output


def Fparameters(j):
    dict_output = dict()
    Children = []
    condition = tokens[j].token_type

    if condition == TokenType.VARIABLE:
        # variable token
        variable_dict = Match(TokenType.VARIABLE, j)
        Children.append(variable_dict["node"])
        dict_output["index"] = variable_dict["index"]

        condition = tokens[variable_dict["index"]].lexeme
        if condition == ',':
            # Fparameters_ast Part
            Fparameters_ast_dict = Fparameters_ast(variable_dict["index"])
            Children.append(Fparameters_ast_dict["node"])
            dict_output["index"] = Fparameters_ast_dict["index"]


    else:  # when condition == any value type or when it's error
        # value token
        match condition:
            case TokenType.INTEGER_VALUE:
                value_dict = Match(TokenType.INTEGER_VALUE, j)
            case TokenType.REAL_VALUE:
                value_dict = Match(TokenType.REAL_VALUE, j)
            case TokenType.STRING_VALUE:
                value_dict = Match(TokenType.STRING_VALUE, j)
            case _:
                value_dict = Match(TokenType.IDENTIFIER, j)

        Children.append(value_dict["node"])
        dict_output["index"] = value_dict["index"]

        condition = tokens[value_dict["index"]].lexeme
        if condition == ',':
            # Fparameters_ast Part
            Fparameters_ast_dict = Fparameters_ast(value_dict["index"])
            Children.append(Fparameters_ast_dict["node"])
            dict_output["index"] = Fparameters_ast_dict["index"]

    dict_output["node"] = Tree("Fparameters", Children)
    return dict_output


def Fparameters_ast(j):
    dict_output = dict()
    Children = []

    # comma token
    comma_dict = Match(TokenType.AND_OP, j)
    Children.append(comma_dict["node"])

    # Fparameters Part
    Fparameters_dict = Fparameters(comma_dict["index"])
    Children.append(Fparameters_dict["node"])

    dict_output["node"] = Tree("Fparameters_ast", Children)
    dict_output["index"] = Fparameters_dict["index"]
    return dict_output


def Variable(j):
    dict_output = dict()
    Children = []
    condition = tokens[j].token_type

    if condition == TokenType.VARIABLE:
        # variable token
        variable_dict = Match(TokenType.VARIABLE, j)
        Children.append(variable_dict["node"])
        dict_output["index"] = variable_dict["index"]

        condition = tokens[variable_dict["index"]].token_type

        if condition == TokenType.PLUS_OP or condition == TokenType.MINUS_OP or condition == TokenType.MULTIPLY_OP \
                or condition == TokenType.DIVIDE_OP or condition == TokenType.LESS_THAN_OP or condition == TokenType.LESS_THAN_EQUAL_OP \
                or condition == TokenType.GREATER_THAN_OP or condition == TokenType.GREATER_THAN_EQUAL_OP or condition == TokenType.ANGLED_BRACKETS_OP \
                or condition == TokenType.EQUAL_OP:

            # Variable_ast Part
            Variable_ast_dict = Variable_ast(variable_dict["index"])
            Children.append(Variable_ast_dict["node"])
            dict_output["index"] = Variable_ast_dict["index"]


    else:  # when condition == any value type or when it's error
        # value token
        match condition:
            case TokenType.INTEGER_VALUE:
                value_dict = Match(TokenType.INTEGER_VALUE, j)
            case TokenType.REAL_VALUE:
                value_dict = Match(TokenType.REAL_VALUE, j)
            case TokenType.STRING_VALUE:
                value_dict = Match(TokenType.STRING_VALUE, j)
            case _:
                value_dict = Match(TokenType.IDENTIFIER, j)

        Children.append(value_dict["node"])
        dict_output["index"] = value_dict["index"]

        condition = tokens[value_dict["index"]].token_type

        if condition == TokenType.PLUS_OP or condition == TokenType.MINUS_OP or condition == TokenType.MULTIPLY_OP \
         or condition == TokenType.DIVIDE_OP or condition == TokenType.LESS_THAN_OP or condition == TokenType.LESS_THAN_EQUAL_OP \
         or condition == TokenType.GREATER_THAN_OP or condition == TokenType.GREATER_THAN_EQUAL_OP or condition == TokenType.ANGLED_BRACKETS_OP \
         or condition == TokenType.EQUAL_OP:

            # Variable_ast Part
            Variable_ast_dict = Variable_ast(value_dict["index"])
            Children.append(Variable_ast_dict["node"])
            dict_output["index"] = Variable_ast_dict["index"]

    dict_output["node"] = Tree("Variable", Children)
    return dict_output


def Variable_ast(j):
    dict_output = dict()
    Children = []

    # OP Part
    OP_dict = OP(j)
    Children.append(OP_dict["node"])

    # Variable Part
    Variable_dict = Variable(OP_dict["index"])
    Children.append(Variable_dict["node"])

    dict_output["node"] = Tree("Variable_ast", Children)
    dict_output["index"] = Variable_dict["index"]
    return dict_output


def String(j):
    dict_output = dict()
    Children = []
    condition = tokens[j].token_type

    if condition == TokenType.VARIABLE:
        # variable token
        variable_dict = Match(TokenType.VARIABLE, j)
        Children.append(variable_dict["node"])
        dict_output["index"] = variable_dict["index"]

        condition = tokens[variable_dict["index"]].lexeme
        if condition == ',':
            # String_ast Part
            String_ast_dict = String_ast(variable_dict["index"])
            Children.append(String_ast_dict["node"])
            dict_output["index"] = String_ast_dict["index"]


    else:  # when condition == any value type or when it's error
        # string-value token
        value_dict = Match(TokenType.STRING_VALUE, j)
        Children.append(value_dict["node"])
        dict_output["index"] = value_dict["index"]

        condition = tokens[value_dict["index"]].lexeme
        if condition == ',':
            # String_ast Part
            String_ast_dict = String_ast(value_dict["index"])
            Children.append(String_ast_dict["node"])
            dict_output["index"] = String_ast_dict["index"]

    dict_output["node"] = Tree("String", Children)
    return dict_output


def String_ast(j):
    dict_output = dict()
    Children = []

    # comma token
    comma_dict = Match(TokenType.AND_OP, j)
    Children.append(comma_dict["node"])

    # String Part
    String_dict = String(comma_dict["index"])
    Children.append(String_dict["node"])

    dict_output["node"] = Tree("String_ast", Children)
    dict_output["index"] = String_dict["index"]
    return dict_output


def OP(j):
    dict_output = dict()
    Children = []
    condition = tokens[j].token_type

    # operator token
    match condition:
        case TokenType.PLUS_OP:
            op_dict = Match(TokenType.PLUS_OP, j)
        case TokenType.MINUS_OP:
            op_dict = Match(TokenType.MINUS_OP, j)
        case TokenType.MULTIPLY_OP:
            op_dict = Match(TokenType.MULTIPLY_OP, j)
        case TokenType.DIVIDE_OP:
            op_dict = Match(TokenType.DIVIDE_OP, j)
        case TokenType.LESS_THAN_OP:
            op_dict = Match(TokenType.LESS_THAN_OP, j)
        case TokenType.LESS_THAN_EQUAL_OP:
            op_dict = Match(TokenType.LESS_THAN_EQUAL_OP, j)
        case TokenType.GREATER_THAN_OP:
            op_dict = Match(TokenType.GREATER_THAN_OP, j)
        case TokenType.GREATER_THAN_EQUAL_OP:
            op_dict = Match(TokenType.GREATER_THAN_EQUAL_OP, j)
        case TokenType.ANGLED_BRACKETS_OP:
            op_dict = Match(TokenType.ANGLED_BRACKETS_OP, j)
        case _:
            op_dict = Match(TokenType.EQUAL_OP, j)

    Children.append(op_dict["node"])

    dict_output["node"] = Tree("OP", Children)
    dict_output["index"] = op_dict["index"]
    return dict_output


def Match(a, j):
    output = dict()
    if (j < len(tokens)):
        Temp = tokens[j].to_dict()
        if (Temp['token_type'] == a):
            j += 1
            output["node"] = [Temp['Lexeme']]
            output["index"] = j
            return output
        else:
            output["node"] = ["error"]
            output["index"] = j + 1
            errors.append("Syntax error : Encountered token is " + Temp['Lexeme'] + " but Expected token is of type " + f"{a}")
            return output
    else:
        output["node"] = ["error"]
        output["index"] = j + 1
        errors.append("Syntax error : Missing Token here")
        return output


