from Compiler.Lexer import lexical_analyzer
from Compiler.Parser import syntactical_analyzer
from Compiler.Intermediate_code import intermediateCode
from Compiler.Optimizer import optimizer
from Compiler.gen_code import generatedCode

"""
o = nasm -f elf64 output.asm
man ld
ld -m elf_x86_64 -s -o output output.o
./output
"""
counter = 0


while True:
    counter += 1
    f = open("input_date.txt", 'r')
    a = f.read()

    try:
        arr = lexical_analyzer(a).returnTokensArray();
        print('TOKENS:')
        print('T,L\n')
        print(arr)

        tree = syntactical_analyzer(arr).getRoot();
        print("-" * 50)
        print('AST:\n')
        print(tree)
        print("-" * 50)


        code, identifiers, constants = intermediateCode(tree).returnGeneratedCode();


        code, identifiers, constants, tempmap = optimizer(code, identifiers, constants).genCode();
        print("-" * 50)
        print('Code Optimization:\n')
        print(identifiers)
        print(constants)
        code.print_extra()
        print("-"*50)

        print("-"*50)
        print(f"[{counter}] : ", end="\n\n")
        generatedCode(code, identifiers, constants, tempmap)
        print("-"*50)

    except Exception as e:
        print(e)

    f.close()
    input()
