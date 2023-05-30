
# Класс NumberNode представляет узел, содержащий число.
# Он имеет одно поле tok, которое является токеном числа.
# Метод __str__ возвращает строковое представление узла.
# Метод get_num возвращает значение числа.
class NumberNode:
    def __init__(self,tok):
        self.tok = tok

    def __str__(self):
        return f'{self.tok}'

    def get_num(self):
        return self.tok.value

# Класс IdentifierNode представляет узел, содержащий идентификатор (имя переменной).
# Он имеет одно поле tok, которое является токеном идентификатора.
# Метод __str__ возвращает строковое представление узла.
# Метод get_num возвращает значение идентификатора.
class IdentifierNode:
    def __init__(self,tok):
        self.tok = tok

    def __str__(self):
        return f'{self.tok}'

    def get_num(self):
        return self.tok.value

# Класс BinOpNode представляет узел бинарной операции, например, сложение или умножение.
# Он имеет три поля: left (левый операнд), op_tok (токен операции) и right (правый операнд).
# Метод __str__ возвращает строковое представление узла.
class BinOpNode:
    def __init__(self,left,op_tok,right):
        self.left = left
        self.op_tok = op_tok
        self.right = right

    def __str__(self):
        return f'[{self.left} {self.op_tok} {self.right}]'


# Класс Statement представляет узел, содержащий оператор.
# Он имеет два поля: left (левый операнд) и right (правый операнд, необязательный).
# Метод __str__ возвращает строковое представление узла.
class Statement:
    def __init__(self,left,right=None):
        self.left = left
        self.right = right

    def __str__(self):
        return f'[{self.left} {self.right}]'


# Класс IfStatement представляет узел условного оператора if.
# Он имеет три поля: if_condition (условие), if_body (тело if-блока) и else_body (тело else-блока, необязательное).
# Метод __str__ возвращает строковое представление узла с условием и телами блоков.
class IfStatement:
    def __init__(self,if_condition,if_body,else_body=None):
        self.if_condition = if_condition
        self.if_body = if_body
        self.else_body = else_body

    def __str__(self):
        if(self.else_body):
            return f'[IF {self.if_condition} THEN {self.if_body} ELSE {self.else_body}]'
        return f'[IF {self.if_condition} THEN {self.if_body}]'


# Класс WhileStatement представляет узел цикла while.
# Он имеет два поля: condition (условие) и body (тело цикла).
# Метод __str__ возвращает строковое представление узла с условием и телом цикла.
class WhileStatement:
    def __init__(self,condition,body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return f'[WHILE {self.condition} THEN {self.body}]'


# Класс PrintStatement представляет узел оператора вывода на экран.
# Он имеет два поля: type (тип выводимого значения, например, строка или целое число) и value (значение для вывода).
# Метод __str__ возвращает строковое представление узла.
class PrintStatement: # string,stringVar,int
    def __init__(self,type,value):
        self.type=type
        self.value=value

    def __str__(self):
        return f'[print {self.value}]'



# Класс Condition представляет узел условия,
# используемого в операторах if и while.
# Он имеет три поля: left_expression (левое выражение),
# comparison (оператор сравнения) и right_expression (правое выражение).
# Метод `__
class Condition:
    def __init__(self,left_expression,comparision,right_expression):
        self.left_expression = left_expression
        self.comparison = comparision
        self.right_expression = right_expression

    def __str__(self):
        return f'[ {self.left_expression} {self.comparison} {self.right_expression} ]'


# Класс Assignment представляет оператор присваивания с идентификатором и выражением, которое будет присвоено.
# Метод __str__ форматирует строковое представление оператора присваивания с идентификатором и выражением.
class Assignment:
    def __init__(self,identifier,expression):
        self.identifier = identifier
        self.expression = expression

    def __str__(self):
        return f'[{self.identifier} EQUAL {self.expression}]';


# Класс StringAssignment представляет оператор присваивания строкового значения,
# аналогичный классу Assignment, но для строковых значений.
# Метод __str__ форматирует строковое представление оператора
# присваивания строкового значения с идентификатором и выражением.
class StringAssignment:
    def __init__(self,identifier,expression):
        self.identifier = identifier
        self.expression = expression

    def __str__(self):
        return f'[{self.identifier} EQUAL {self.expression}]';

# Класс Declaration представляет оператор объявления с типом объявления
# (например, "int" или "string") и списком идентификаторов, которые должны быть объявлены.
# Метод __str__ форматирует строковое представление оператора объявления с типом объявления
# и списком идентификаторов, разделенных запятой.
class Declaration:
    def __init__(self,declaration_type,identifiers):
        self.declaration_type = declaration_type
        self.identifiers = identifiers

    def __str__(self):
        return f'[{self.declaration_type}  ({",".join(map(str,self.identifiers))})]';

