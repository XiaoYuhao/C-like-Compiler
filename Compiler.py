#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-

#--------------------------------------------------
#calclex.py
#
#tokenizer for a simple expression evaluator for
#numbers and +,-,=,/
#--------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc

reserved={
    'int' : 'INT',
    'void' : 'VOID',
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'return' : 'RETURN'
}

tokens=[
    'NUMBER',
    'ID',
    'EQUAL',
    'GREATER',
    'LESS',
    'UNEQUAL'
]+list(reserved.values())

literals = ['=','+','-','*','/','(',')',';','{','}','>','<']

t_EQUAL = r'=='
t_GREATER= r'>='
t_LESS  = r'<='
t_UNEQUAL=r'!='


def t_NUMBER(t):
    r'\d+'
    t.value=int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type=reserved.get(t.value,'ID')   #先在保留字中寻找，不存在则为ID
    #t.value=(t.value,symbol_lookup(t.value))
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno+=len(t.value)

t_ignore=' \t'

def t_error(t):
    print ("Illegal character '%s'" %t.value[0])
    t.lexer.skip(1)


#
precedence=(
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS'),
    )

ids = { }

def p_Program(p):
    'Progarm : DeclareStr'
    #print("Debug At Progarm...")

def p_DeclareStr(p):
    'DeclareStr : Declare TDeclare'
    #print("Debug At DeclareStr...")

def p_Declare(p):
    '''Declare : INT ID DeclareFun
               | INT ID DeclareType
               | VOID ID DeclareFun '''
    #print("Debug At Declare...")

def p_TDeclare(p):
    '''TDeclare : empty
                | Declare TDeclare '''

def p_DeclareType(p):
    "DeclareType : ';'"
    #print("Debug At DeclareType...")

def p_DeclareFun(p):
    "DeclareFun : '(' FormalPara ')' Block"
    #print("Debug At DeclareFun...")

def p_FormalPara(p):
    '''FormalPara : ParaTable 
                  | VOID '''
    #print("Debug At FormalPara...")

def p_ParaTable(p):
    '''ParaTable : Parameter
                 | ',' ParaTable   '''
    #print("Debug At ParaTable...")

def p_Parameter(p):
    'Parameter : INT ID'
    #print("Debug At Parameter...")

def p_Block(p):
    "Block : '{' LangStr TLangStr '}'"
    #print("Debug At Block...")

def p_TLangStr(p):
    '''TLangStr : empty 
                | LangStr TLangStr'''
    #print("Debug At TLangStr...")

def p_LangStr(p):
    '''LangStr : InterDeclare 
               | InterStr'''
    #print("Debug At LangStr...")

def p_InterDeclare(p):
    '''InterDeclare : InterVarDeclare ';' '''
    #print("Debug At InterDeclare...")



def p_InterVarDeclare(p):
    'InterVarDeclare : INT ID'
    #print("Debug At InterVarDeclare...")

def p_InterStr(p):
    '''InterStr : Sentence '''
    #print("Debug At InterStr...")

def p_Sentence(p):
    '''Sentence : IfSentence 
                | WhileSentence 
                | ReturnSentence
                | AssignSentence '''
    #print("Debug At Sentence...")

def p_AssignSentence(p):
    "AssignSentence : ID '=' Expression ';' "
    #print("Debug At AssignSentence...")

def p_ReturnSentence(p):
    '''ReturnSentence : RETURN ';'
                      | RETURN Expression ';' '''
    #print("Debug At ReturnSentence...")

def p_WhileSentence(p):
    "WhileSentence : WHILE '(' Expression ')' Block"
    #print("Debug At WhileSentence...")

def p_IfSentence(p):
    "IfSentence : IF '(' Expression ')' Block ElseSentence"
    #print("Debug At IfSentence...")

def p_ElseSentence(p):
    '''ElseSentence : empty
                    | ELSE Block'''
    #print("Debug At ElseSentence...")

def p_Expression(p):
    '''Expression : AddExpression 
                  | AddExpression '<' AddExpression
                  | AddExpression LESS AddExpression
                  | AddExpression '>' AddExpression
                  | AddExpression GREATER AddExpression
                  | AddExpression EQUAL AddExpression
                  | AddExpression UNEQUAL AddExpression
                  '''
    #print("Debug At Expression...")

def p_Expression_uminus(p):
    "Expression : '-' Expression %prec UMINUS"
    p[0]=-p[2]
    #print("Debug At Expression_uminus...")

def p_AddExpression(p):
    '''AddExpression : Term
                     | Term '+' Term
                     | Term '-' Term '''
    #print("Debug At AddExpression...")

def p_Term(p):
    '''Term : Factor
            | Factor '*' Factor
            | Factor '/' Factor '''

def p_Factor(p):
    '''Factor : NUMBER
              | '(' Expression ')' 
              | ID FTYPE '''
    #print("Debug At Factor...")

def p_FTYPE(p):
    '''FTYPE : Call
             | empty '''
    #print("Debug At FTYPE...")

def p_Call(p):
    "Call : '(' RealPara ')'"
    #print("Debug At Call...")

def p_RealPara(p):
    '''RealPara : RealParaTable
                | empty '''
    #print("Debug At RealPara...")

def p_RealParaTable(p):
    '''RealParaTable : Expression
                     | ',' RealParaTable '''
    #print("Debug At RealParaTable...")

def p_empty(p):
    'empty : '
    #print("Debug At empty...")
    pass

def p_error(p):
    if p:
        print("Syntax error at '%s'" %p.value)
    else:
        print("Syntax error at EOF")

#build the lexer
lexer=lex.lex()

#build the parser
yacc.yacc()


#Test it out
data='''
int d;
void function(void){
    int a;
    int b;
    int c;
    a=10;
    b=20;
    c=a+b;
    if(c>=0){
        c=10;
    }
    else{
        c=55;
    }
    while(c<0){
        c=a+b;
    }
    return ;
}
int func(void){
    int a;
    int e;
    e=a+1;
    if(e<0){
        e=e+1;
    }
    else{
        e=e*3;
    }
    while(e<=2){
        e=e/2;
    }
    return e;
}
'''

lexer.input(data)

while True:
    tok=lexer.token()
    if not tok :
        break
    print (tok)

yacc.parse(data)
#while True:
#   try:
#       s=input('calc > ')
#   except EOFError:
#       break
#   if not s:
#       continue
#   print(s)
#   yacc.parse(s)
