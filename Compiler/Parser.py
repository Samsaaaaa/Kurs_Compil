from helper.Tokens import *
from helper.TreeNodes import *

# Создается список сравнения, который содержит возможные операции сравнения:
comparison_operations = ['>','<','==','<=','>=','!=']

# Создается класс syntactical_analyzer. В его методе init инициализируется объект класса Parser аргументом tokens.
# В self.tokens добавляется токен Token("END",value="END"),
# так как этот токен необходим для правильной работы метода statements.
class syntactical_analyzer:
    def __init__(self,tokens):
        self.tokens = tokens
        self.tokens.push(Token("END",value="END"))
        self.dele = 0

        # функция проверки соответствия ожидаемого и фактического токена
    def readToken(self, expected, message):
        t = self.tokens.current()
        if(t.value != expected):
            raise Exception("{}  in line {}".format(message,t.line))
        self.tokens.next();


    # Метод factor получает токен tok, который является текущим токеном.
    # Если тип tok равен 'INT', то метод возвращает объект NumberNode с аргументом tok.
    # Если тип tok равен 'VAR', то метод возвращает объект IdentifierNode с аргументом tok.
    # Если значение tok равно '(', то метод вызывает метод expr и проверяет, что следующий токен равен ')'.
    # Если это не так, то метод выдает исключение. Если тип tok не равен 'INT',
    # а значение tok не равно 'VAR' или '(', то метод выдает исключение.
    def getToken(self):
        tok = self.tokens.current()
        if(tok.type in 'INT'):
            self.tokens.next();
            return NumberNode(tok)
        if(tok.type =="VAR"):
            self.tokens.next();
            return IdentifierNode(tok)
        elif(tok.value =='('):
            self.tokens.next()
            exp = self.expr()
            if(self.tokens.current().value==')'):
                self.tokens.next()
                return exp
            else:
                raise Exception('Syntax Error Expected ) in line {} '.format(self.tokens.current().line))
        else:
            raise Exception('Syntax Error : Expected Integer in line {} '.format(self.tokens.current().line))


    # Метод term вызывает метод factor и присваивает результат left.
    # Затем метод входит в цикл while, пока значение текущего токена равно '*' или '/'.
    # Внутри цикла метод присваивает операцию op_tok текущему токену, переходит к следующему токену,
    # вызывает метод factor и присваивает результат right.
    # Затем метод создает объект BinOpNode с аргументами left, op_tok и right, и присваивает его left.
    # После окончания цикла метод возвращает left.
    def term(self):
        left = self.getToken()

        while(self.tokens.current().value in '*/'):
            op_tok = self.tokens.current()
            self.tokens.next()
            right = self.getToken();
            left = BinOpNode(left,op_tok,right)

        return left

    # Метод expr вызывает метод term и присваивает результат left.
    # Затем метод входит в цикл while, пока значение текущего токена равно '+' или '-'.
    # Внутри цикла метод присваивает операцию op_tok текущему токену,
    # переходит к следующему токену, вызывает метод term и присваивает результат right.
    # Затем метод создает объект BinOpNode с аргументами left, op_tok и right, и присваивает его left.
    # После окончания цикла метод возвращает left.
    def expr(self):
        left = self.term()

        while(self.tokens.current().value in '+-'):
            op_tok = self.tokens.current()
            self.tokens.next()
            right = self.term();
            left = BinOpNode(left,op_tok,right)



        return left

    # Метод condition вызывает метод expr и присваивает результат left.
    # Затем метод присваивает переменной operation текущий токен.
    # Если значение operation не содержится в списке comparison_operations, то метод выдает исключение.
    # Затем метод переходит к следующему токену, вызывает метод expr и присваивает результат right.
    # Затем метод создает объект Condition с аргументами left, operation и right, и возвращает его.
    def condition(self):
        left = self.expr()
        operation = self.tokens.current()
        if(operation.value not in comparison_operations):
            raise Exception(f"un Expected {operation.value} in line {operation.line} Was Expecting comparison")
        self.tokens.next()
        right = self.expr()

        return Condition(left,operation,right)

    # определяет функцию, которая разбирает и возвращает объект IfStatement.
    # Она читает следующий токен, который должен быть открывающей скобкой, а затем разбирает условие,
    # используя функцию condition. Затем она читает закрывающую скобку,
    # открывающую фигурную скобку и операторы в теле блока if.
    # Если есть блок else, она читает следующий токен, который должен быть открывающей фигурной скобкой,
    # и затем считывает операторы в блоке else. Наконец, она возвращает объект IfStatement.
    def statementIf(self):
        else_body = None
        self.readToken('(', 'Expected ( in the beginnig of if condition ')

        condition = self.condition()

        self.readToken(')', 'Expected ) in the end of if condition ')

        self.readToken('{', 'Expected { in the beginnig of if body ')
        self.dele+=1

        body = self.statements();

        #self.read_token_pass('}','Missing } in the end of if body ')

        t = self.tokens.current()
        if(t.value == 'else'):
            self.tokens.next()

            self.readToken('{', 'Missing { in the beginnig of if body ')
            self.dele+=1

            else_body = self.statements();

            #self.read_token_pass('}','Missing } in the end of if body ')


        return IfStatement(condition,body,else_body)


    # определяет функцию, которая разбирает и возвращает объект Declaration.
    # Она считывает тип идентификатора, такой как "int" или "string", затем считывает список идентификаторов,
    # разделенных запятыми, и возвращает объект Declaration.
    def declarat(self):
        identifier_type = self.tokens.current()
        self.tokens.next()

        lis = [self.tokens.current()]
        self.tokens.next()
        while(self.tokens.current().value == ','):
            self.tokens.next()
            if(self.tokens.current().type!="VAR"):
                raise Exception(f"Syntax Error Expected Identifier in line {self.tokens.current().line}")
            lis.append(self.tokens.current())
            self.tokens.next()

        self.readToken(';', "Expected SemiColon  ");
        return Declaration(identifier_type,lis)


    # определяет функцию, которая разбирает и возвращает объект Assignment.
    # Она считывает идентификатор, затем знак равенства, затем разбирает выражение с помощью функции expr
    # и считывает точку с запятой. Она возвращает объект Assignment.
    def assignment(self):
        identifier = self.tokens.current()
        self.tokens.next()
        self.readToken('=', 'Missing = ')
        expression = self.expr()
        self.readToken(';', 'Missing ;')
        return Assignment(identifier,expression)

    # определяет функцию, которая разбирает и возвращает объект WhileStatement.
    # Она считывает следующий токен, который должен быть открывающей скобкой,
    # затем разбирает условие с помощью функции condition, затем считывает закрывающую скобку,
    # открывающую фигурную скобку и операторы в теле цикла while. Наконец, она возвращает объект WhileStatement.
    def statementWhile(self):

        self.readToken('(', 'Missing ( in the beginnig of if condition ')

        condition = self.condition()

        self.readToken(')', 'Missing ) in the end of if condition ')

        self.readToken('{', 'Missing { in the beginnig of if body ')
        self.dele+=1

        body = self.statements();

        return WhileStatement(condition,body)

    # определяет функцию, которая разбирает и возвращает объект PrintStatement.
    # Она считывает следующий токен, который должен быть открывающей скобкой, а затем либо считывает строку,
    # либо разбирает выражение в зависимости от параметра типа.
    # Затем она считывает закрывающую скобку и точку с запятой, и возвращает объект PrintStatement.
    def printing(self,type):
        self.tokens.next()
        self.readToken('(', 'Missing ( in the beginnig of printig ')

        if(type=='str'):
            cur_t = self.tokens.current()
            self.tokens.next()
            self.readToken(')', 'Missing ) in the end of printig ')
            self.readToken(';', 'Missing ; in the end of printig ')
            return PrintStatement('string',cur_t.value)
        else:
            exp = self.expr()
            self.readToken(')', 'Missing ) in the end of printig ')
            self.readToken(';', 'Missing ; in the end of printig ')
            return PrintStatement('int',exp)


    # определяет функцию, которая разбирает и возвращает объект Statement.
    # Она циклически проходит по токенам, считывая операторы и добавляя их в связанный список объектов Statement,
    # пока не достигнет токена END или }. Затем она возвращает связанный список объектов Statement.
    def statements(self):
        left = None;right = None
        t = self.tokens.current()

        while(t.value!='END' and t.value!='}'):
            if(t.type == 'IF'):
                self.tokens.next()
                right = self.statementIf()
            elif(t.type == 'WHILE'):
                self.tokens.next()
                right = self.statementWhile()
            elif(t.type in ('STRING','INT')):
                right = self.declarat();
            elif(t.type == 'PRINT'):
                right = self.printing('int');
            elif(t.type == 'PRINTS'):
                right = self.printing('str');
            elif(t.type == 'VAR'):
                right = self.assignment()
            else:
                raise Exception("Syntax Error in line {}".format(t.line))

            left = Statement(left, right)
            t = self.tokens.current()

        if(t.value=='END'):
            return left
        elif(t.value=='}'):
            if(self.dele>0):
                self.dele-=1;
                self.tokens.next()
                return left
            else:
                raise Exception("un Expected } at end of line {}".format(t.line))



    # определяет функцию, которая разбирает всю программу и возвращает корневой объект Statement.
    def getRoot(self):
        root = self.statements()
        if(self.tokens.current().type!="END"):
            raise Exception("Syntax Error")
        return root
