# Класс Token имеет три атрибута: type, value и line. Аргументы type и value не являются
# обязательными, аrgument line - это номер строки, в которой был найден токен.
class Token:
    def __init__(self,type,value=None,line=None):
        self.type=type
        self.value = value
        self.line=line

    # Метод str() возвращает строковое представление объекта в формате "тип : значение".
    def __str__(self):
        return "{} : {}".format(self.type,self.value)


# Класс TokenArray используется для хранения списка объектов Token.
class TokenArray:
    def __init__(self):
        self.lis = []
        self.cur_position=0
        self.cur_char = ""

    # Метод push() добавляет новый объект Token в список.
    def push(self,val):
        self.lis.append(val)

    # Метод next() позволяет перейти к следующему элементу списка.
    # Если текущий элемент является последним в списке, то метод ничего не делает.
    def next(self):
        if(self.cur_position+1 < len(self.lis)):
            self.cur_position+=1
        self.cur_char = self.lis[self.cur_position]

    # Метод current() возвращает текущий элемент списка.
    def current(self):
        return self.lis[self.cur_position]

    # Метод str() формирует строку, содержащую все объекты Token из списка.
    def __str__(self):
        j=""
        for i in self.lis:
            j+=str(i)+"\n"
        return j

    # Метод len() возвращает количество элементов списка.
    def __len__(self):
        return len(self.lis)
