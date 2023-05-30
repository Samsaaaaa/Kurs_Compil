from helper.Tokens import *
from helper.TreeNodes import *
from helper.intermidatecodes import *

# count класс используется для генерации уникальных имен временных переменных путем
# добавления к символьному префиксу их номера (счетчика)
class count:
    def __init__(self,char):
        self.count = 1;
        self.char = char

    def increase(self):
        self.count+=1;

    def reset(self):
        self.count=1;

    def get(self):
        return f'{self.char}{self.count}';


# Класс intermediateCode принимает синтаксическое дерево в качестве входного параметра,
# инициализирует различные переменные, такие как счетчик временной переменной (t), счетчик меток (l)
# и счетчик строковых констант (s).
class intermediateCode:
    def __init__(self, tree_root):
        self.root = tree_root
        self.code = InterCodeArray()
        self.t = count('T')
        self.l = count('L')
        self.s = count('S')
        self.identifiers = {}
        self.constants = {}
        self.realizeStatement(tree_root)


    # Метод execute_exp генерирует код для арифметических выражений путем рекурсивной оценки левых
    # и правых подвыражений. Он генерирует инструкцию присваивания, которая присваивает результат
    # выражения новой временной переменной.
    def realizeExpression(self, root):
        if(isinstance(root,IdentifierNode) or isinstance(root,NumberNode)):
            return root.get_num()
        else:
            left = self.realizeExpression(root.left)
            op = root.op_tok.value
            right = self.realizeExpression(root.right)
            cur_t = self.t.get()
            self.identifiers[cur_t] = 'int'
            self.t.increase()
            self.code.append(AssignmentCode(cur_t,left,op,right))
            return cur_t;


    def realizeTasc(self, root):
        right = self.realizeExpression(root.expression)
        self.code.append(AssignmentCode(root.identifier.value,right))


    # Методы execute_if и execute_while генерируют код для конструкций if-else и циклов while соответственно.
    def realizeIf(self, root):
        self.realizeСomparison(root.if_condition);

        body = self.l.get();self.l.increase()
        end_if = self.l.get();self.l.increase()

        if(root.else_body):
            goto_else_end = self.l.get();self.l.increase()
            self.code.append(JumbCode(goto_else_end))
            self.code.append(LabelCode(body))
            self.realizeStatement(root.if_body)
            self.code.append(JumbCode(end_if))
            self.code.append(LabelCode(goto_else_end))
            self.realizeStatement(root.else_body)
            self.code.append(LabelCode(end_if))
        else:
            self.code.append(JumbCode(end_if))
            self.code.append(LabelCode(body))
            self.realizeStatement(root.if_body)
            self.code.append(LabelCode(end_if))

    def realizeWhile(self, root):
        start_loop = self.l.get();self.l.increase()
        self.code.append(LabelCode(start_loop))

        self.realizeСomparison(root.condition);
        body = self.l.get();self.l.increase()

        end_while = self.l.get();self.l.increase()

        self.code.append(JumbCode(end_while))
        self.code.append(LabelCode(body))
        self.realizeStatement(root.body)
        self.code.append(JumbCode(start_loop))
        self.code.append(LabelCode(end_while))

    # Метод execute_condition генерирует код для операций сравнения.
    def realizeСomparison(self, root):
        left = self.realizeExpression(root.left_expression)
        compare = root.comparison.value
        right = self.realizeExpression(root.right_expression)

        body = self.l.get()

        self.code.append(CompareCode(left,compare,right,body))

    # Метод execute_print генерирует код для инструкций вывода print. Если аргументом является строка,
    # он генерирует новую строковую константу и добавляет ее в список строковых констант.
    # Если аргументом является целочисленное выражение, он вычисляет выражение и генерирует инструкцию вывода
    # с результатом.
    def realizePrint(self, root):
        if(root.type=="string"):
            self.constants[self.s.get()] = root.value
            right = self.s.get()
            self.s.increase()
            self.code.append(PrintCode("string",right))
        elif(root.type=="int"):
            right = self.realizeExpression(root.value)
            self.code.append(PrintCode("int",right))

    # Метод execute_declaration генерирует код для объявления переменной.
    # Он добавляет каждый объявленный идентификатор в словарь идентификаторов вместе с его типом.
    def realizeVariableDeclaration(self, root):
        type = root.declaration_type
        for i in root.identifiers:
            self.identifiers[i.value]=type.value

    # Метод execute_statement выполняет соответствующий метод в зависимости от типа инструкции,
    # разобранной в синтаксическом дереве.
    def realizeStatement(self, root):
        if(root==None):
            return ;

        if(isinstance(root,Statement)):
            self.realizeStatement(root.left)
            self.realizeStatement(root.right)
        elif(isinstance(root,IfStatement)):
            self.realizeIf(root)
        elif(isinstance(root,WhileStatement)):
            self.realizeWhile(root)
        elif(isinstance(root,PrintStatement)):
            self.realizePrint(root)
        elif(isinstance(root,Declaration)):
            self.realizeVariableDeclaration(root)
        elif(isinstance(root,Assignment)):
            self.realizeTasc(root)


    # Метод get_code возвращает сгенерированный промежуточный код, а также словари типов
    # идентификаторов и строковых констант.
    def returnGeneratedCode(self):
        return self.code,self.identifiers,self.constants
