from lexer import Lexer
# from parser import build_tree

lexer = Lexer()
lexer.build()
lexer.main("code.txt")

# result = build_tree("code.txt")
# print(result)

