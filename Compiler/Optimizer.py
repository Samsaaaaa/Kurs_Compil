from helper.Tokens import *
from helper.TreeNodes import *
from helper.intermidatecodes import *

# eval_op принимает два операнда и оператор, и выполняет соответствующую операцию с использованием оператора.
# Возвращает результат.
def operator(left, op, right):
    if(op=='+'):
        return left+right
    elif(op=='*'):
        return left*right
    elif(op=='-'):
        return left-right
    elif(op=='/'):
        if(right==0):
            raise Exception("Error Division By Zero");
        return left//right

# eval_comparison принимает два операнда и оператор сравнения, и выполняет соответствующее сравнение.
# Возвращает булево значение (True или False).
def comparison(left, op, right):
    if(op=='>'):
        return left>right
    elif(op=='=='):
        return left==right
    elif(op=='<'):
        return left<right
    elif(op=='>='):
        return left>=right
    elif(op=='<='):
        return left<=right
    elif(op=='!='):
        return left!=right

# isint проверяет, является ли переданный аргумент целым числом.
# Если аргумент можно успешно преобразовать в целое число, функция возвращает 1, иначе - 0.
def integer(s):
    try:
        int(s)
        return 1
    except Exception as e:
        return 0

# Класс optimization принимает три входных параметра: промежуточный код программы,
# словарь идентификаторов и список строковых констант.
# Конструктор класса сохраняет входные данные в соответствующие поля и инициализирует переменные
# для хранения выходных данных и временного отображения (tempmap).
class optimizer:
    def __init__(self,input_code,input_identifiers,input_constants):
        self.input_code = input_code
        self.input_identifiers = input_identifiers
        self.input_constants = input_constants
        self.output_code = self.input_code
        self.output_identifiers = self.input_identifiers
        self.output_constants = self.input_constants
        self.tempmap={}
        self.optimizer();

    # Метод remove_temp проходит по каждой инструкции присваивания в промежуточном коде и заменяет временные
    # переменные на значения, которые они представляют, если возможно.
    # Затем он удаляет объявления переменных-временных из списка идентификаторов.
    # Если правая и левая части равны целочисленным значениям, метод вычисляет результат операции
    # и сохраняет его во временное отображение.
    def replaceVariables(self, codearray):
        temparray = InterCodeArray()
        for code in codearray.code:
            if(isinstance(code,AssignmentCode)):
                left = self.tempmap.get(code.left,code.left)
                right = self.tempmap.get(code.right,code.right)
                if(integer(left) and integer(right)):
                    self.tempmap[code.var] = operator(int(left), code.op, int(right))
                    del self.output_identifiers[code.var];
                else:
                    code.left = self.tempmap.get(code.left,code.left)
                    code.right = self.tempmap.get(code.right,code.right)
                    temparray.append(code)
            else:
                temparray.append(code)


        return temparray

    # Метод loading_once оптимизирует код, выполняя загрузку переменной только один раз, если это возможно.
    # Если инструкция присваивания использует переменную, которая уже была загружена ранее, метод заменяет
    # правую часть на имя переменной, которое было загружено в последний раз.
    def variableLoading(self, codearray):
        temparray = InterCodeArray()
        last_loaded = ""
        for code in codearray.code:
            if(isinstance(code,AssignmentCode)):
                left = code.left
                right = code.right
                if(code.op!=None and left==last_loaded):
                    c = ChangeCode(code.var,code.op,right)
                    temparray.append(c)
                elif(code.op!=None and (right==last_loaded and code.op in '*+')):
                    c = ChangeCode(code.var,code.op,left)
                    temparray.append(c)
                else:
                    temparray.append(code)

                last_loaded = code.var
            else:
                temparray.append(code)
                last_loaded=""


        return temparray

    # Метод end_comparisions удаляет из кода блоки, которые никогда не будут выполнены из-за условий сравнения.
    # Если левая и правая части равны целочисленным значениям, метод выполняет сравнение и затем определяет блок,
    # который нужно удалить.
    def removeBlocks(self, codearray):
        temparray = InterCodeArray()
        remove_until = ""
        for index,code in enumerate(codearray.code):
            if(remove_until!=""):
                if(isinstance(code,LabelCode) and code.label == remove_until):
                    remove_until = ""
                continue

            if(isinstance(code,CompareCode)):
                left = code.left
                right = code.right
                if(integer(left) and integer(right)):
                    x = comparison(int(left), code.operation, int(right))
                    if(x):
                        remove_until = code.jump
                    else:
                        remove_until = codearray.code[index+1].dist
                else:
                    temparray.append(code)
            else:
                temparray.append(code)
        return temparray

    # Метод optimize вызывает каждый из описанных выше методов для оптимизации промежуточного кода.
    def optimizer(self):
        self.output_code = self.replaceVariables(self.input_code)
        self.output_code = self.variableLoading(self.output_code)
        self.output_code = self.removeBlocks(self.output_code)

    # Метод get_code возвращает оптимизированный промежуточный код, список
    # идентификаторов и строковых констант, а также временное отображение значений.
    def genCode(self):
        return self.output_code,self.output_identifiers,self.output_constants,self.tempmap
