# Класс AssignmentCode представляет операцию присваивания.
# Аргументы конструктора - переменная var, значение left, оператор op (не обязательный) и
# значение right (также не обязательный).
class AssignmentCode:
    def __init__(self,var,left,op=None,right=None):
        self.var = var
        self.left = left
        self.op = op
        self.right = right

    # Метод str() формирует строковое представление объекта в соответствии с правилами языка программирования.
    def __str__(self):
        if(self.op==None):
            return f'{self.var} = {self.left}'
        return f'{self.var} = {self.left}{self.op}{self.right}'

# Класс ChangeCode представляет операцию изменения значения переменной.
# Аргументы конструктора - переменная var, оператор op и новое значение right.
# Метод str() также формирует строковое представление объекта.
class ChangeCode:
    def __init__(self,var,op,right):
        self.var = var
        self.op = op
        self.right = right

    def __str__(self):
        return f'{self.var} {self.op}= {self.right}'

# Класс JumbCode представляет переход к метке. Аргумент конструктора - дистанция до метки.
# Метод str() формирует строку, содержащую операцию перехода.
class JumbCode:
    def __init__(self,dist):
        self.dist = dist

    def __str__(self):
        return f"GOTO({self.dist})"

# Класс LabelCode представляет метку. Аргумент конструктора - имя метки.
# Метод str() формирует строку, содержащую имя метки.
class LabelCode:
    def __init__(self,label):
        self.label = label

    def __str__(self):
        return f'{self.label} : '

# Класс DeclareCode представляет операцию объявления переменной.
# Аргументы конструктора - имя переменной name и количество байт bytes.
# Метод str() формирует строку, содержащую операцию объявления переменной.
class DeclareCode:
    def __init__(self,name,bytes):
        self.name=name
        self.bytes = bytes

    def __str__(self):
        return f'Declare {self.name} {self.bytes} bytes'

# Класс CompareCode представляет операцию сравнения двух значений.
# Аргументы конструктора - левый операнд left, операция operation (например, "<", ">=", "!="),
# правый операнд right и дистанция до метки jump. Метод str() формирует строку, содержащую операцию сравнения.
class CompareCode:
    def __init__(self,left,operation,right,jump):
        self.left = left
        self.operation = operation
        self.right = right
        self.jump = jump

    def __str__(self):
        return f"if {self.left}{self.operation}{self.right} GOTO({self.jump})"

# Класс PrintCode представляет операцию вывода значения на экран.
# Аргументы конструктора - тип значения type (например, int, float, string) и значение value.
# Метод str() формирует строку, содержащую операцию вывода.
class PrintCode:
    def __init__(self,type,value):
        self.type=type
        self.value=value

    def __str__(self):
        return f'print_{self.type} {self.value}'

# Класс InterCodeArray используется для хранения последовательности объектов, представляющих промежуточный код.
# Метод append() добавляет новый объект в список, метод push() не реализован.
# Метод print_extra() выводит на экран все объекты списка.
# Метод combine_next() объединяет текущий объект с следующим объектом списка, если он существует,
# и возвращает результат объединения в виде строки.
class InterCodeArray:
    def __init__(self):
        self.code=[]

    def append(self,n):
        self.code.append(n)

    def push(self):
        pass

    def print_extra(self):
        for i in self.code:
            print(i)

    def combine_next(self,i):
        if(i+1<len(self.code)):
            s = self.code.pop(i+1)
            self.code[i].str_rep += s.str_rep
            self.code[i].type = s.type
