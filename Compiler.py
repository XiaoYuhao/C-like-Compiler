#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-

import ply.lex as lex
import ply.yacc as yacc
import copy
import tools
import math

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

literals = ['=','+','-','*','/','(',')',';','{','}','>','<',',']

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
    t.lexer.lineno+=len(t.value)    #修改行号

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
#创建符号表
symbol_table=dict()
#创建实参表
real_table=[]

class Symbol_type:
    def __init__(self,t,v):
        self.type=t
        self.value=v

#class Symbol_fun:
#    def __init__(self,t):
#        self.type="fun"
#        self.rtype=t
#        self.table=dict()

class Symbol_fun:
    def  __init__(self):
        self.type="fun"
        self.formal_table=dict()    #函数参数表
        self.temp_val=dict()        #临时变量表
        self.return_type=None       #函数返回值类型
        self.return_val=0           #函数返回值

    def clear(self):
        self.type="fun"
        self.formal_table.clear()
        self.temp_val.clear()
        self.return_type=None
        self.return_val=0


#当前函数作用域符号表
fun_table=Symbol_fun()

tools=tools.Tools()

def p_Program(p):
    'Progarm : DeclareStr'
    #print("Debug At Progarm...")

def p_DeclareStr(p):
    'DeclareStr : Declare TDeclare'
    print("Debug At DeclareStr...")

def p_Declare(p):
    '''Declare : INT ID DeclareFun
               | INT ID DeclareType
               | VOID ID DeclareFun '''
    #print("Debug At Declare...")
    #print(p[2])
    if p[3]=="DeclareFun":
        flag=symbol_table.get(p[2])
        if flag==None:
            symbol_table[p[2]]=copy.deepcopy(fun_table) #深拷贝
            fun_table.clear()   #清空表临时
        else:
            print("Error Row:'%d'  '%s' redefined..." %(p.lineno(3),p[2]))
        print("DeclareFun")
    elif p[3]=="DeclareType":
        flag=symbol_table.get(p[2])
        if flag==None:
            newnode=Symbol_type(p[1],0)
            symbol_table[p[2]]=newnode
        else:
            print("Error Row:%d  %s redefined..." %(p.lineno(3),p[2]))
        print("DeclareType")
 
def p_TDeclare(p):
    '''TDeclare : empty
                | Declare TDeclare '''

def p_DeclareType(p):
    "DeclareType : ';'"
    #print("Debug At DeclareType...")
    p[0]="DeclareType"

def p_DeclareFun(p):
    "DeclareFun : '(' FormalPara ')' Block"
    #print("Debug At DeclareFun...")
    p[0]="DeclareFun"

def p_FormalPara(p):
    '''FormalPara : ParaTable 
                  | VOID '''
    #print("Debug At FormalPara...")


def p_ParaTable(p):
    '''ParaTable : Parameter TParaTable '''
    print("Debug At ParaTable...")

def p_TParaTable(p):
    '''TParaTable : empty
                  | ',' Parameter TParaTable '''

def p_Parameter(p):
    'Parameter : INT ID'
    print("Debug At Parameter...")
    flag=fun_table.formal_table.get(p[2])
    if flag==None:
        fun_table.formal_table[p[2]]=['int',0]  #加入形式参数表，附初值为0
    else:
        print("Error Row:%d %s redefined ..." %(p.lineno(3),p[2]))

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
    flag=fun_table.formal_table.get(p[2])
    if flag==None:
        flag2=fun_table.temp_val.get(p[2])
        if flag2==None:
            fun_table.temp_val[p[2]]=['int',0]
        else:
            print("Error Row:%d  %s redefined ..." %(p.lineno(3),p[2]))
    else:
        print("Error Row:%d  %s redefined ..." %(p.lineno(3),p[2]))


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
    flag1=fun_table.temp_val.get(p[1])
    flag2=fun_table.formal_table.get(p[1])
    if flag1==None and flag2==None:
        print("Error Row:%d %s undefined ..." %(p.lineno(2),p[1]))
    else:
        address=tools.emit(':=',p[1],str(p[3][0]),'-')
        begin_address=address
        end_address=address+1
        p[0]=[begin_address,end_address]

def p_ReturnSentence(p):
    '''ReturnSentence : RETURN ';'
                      | RETURN Expression ';' '''
    #print("Debug At ReturnSentence...")
    if len(p)==3:
        fun_table.return_val=None
        fun_table.return_type='void'
    else:
        fun_table.return_type='int'   #函数返回值类型
        fun_table.return_val=p[2]    #函数返回值

def p_WhileSentence(p):
    "WhileSentence : WHILE  M '(' Expression ')' M Block"
    #print("Debug At WhileSentence...")
    print(p[4])
    true_list=p[4][0]
    false_list=p[4][1]
    again_address=p[2]
    true_address=p[6]

    tools.emit('j','-','-',str(again_address))

    false_address=tools.nextquad()
    tools.backpatch(true_list,true_address)
    tools.backpatch(false_list,false_address)

    begin_address=p[2]
    end_address=false_address
    p[0]=[begin_address,end_address]


def p_M(p):
    "M : empty"
    p[0]=tools.nextquad()

def p_S(p):
    "S : empty"


def p_IfSentence(p):
    "IfSentence : IF '(' Expression ')' M Block N M ElseSentence"
    #print("Debug At IfSentence...")
    true_list=p[3][0]
    false_list=p[3][1]
    true_address=p[5]
    false_address=p[8]

    end_list=p[7]

    tools.backpatch(true_list,true_address)
    tools.backpatch(false_list,false_address)

    end_address=tools.nextquad()
    tools.backpatch(end_list,end_address)



def p_N(p):
    "N : empty"
    address=tools.emit('j','-','-',str(0)) 
    p[0]=address



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
    #if len(p)==4:
    #    print(p[2])
    if len(p)==2:
        p[0]=[p[1],0]
        print(p[0])
    elif p[2]=='<':
        if type(p[1]) is str or type(p[3]) is str:
            true_address=tools.emit('j<',str(p[1]),str(p[3]),'0')
            false_address=tools.emit('j','-','-','0')
            p[0]=[true_address,false_address]
            print("???")
            print(p[0])
        else:
            if p[1]<p[3]:
                p[0]=[1,1]
            else:
                p[0]=[0,0]
    elif p[2]=='<=':
        if type(p[1]) is str or type(p[3]) is str:
            true_address=tools.emit('j<=',str(p[1]),str(p[3]),'0')
            false_address=tools.emit('j','-','-','0')
            p[0]=[true_address,false_address]
            print("<=")
            print(p[0])
        else:
            if p[1]<=p[3]:
                p[0]=[1,1]
            else:
                p[0]=[0,0]
    elif p[2]=='>':
        if type(p[1]) is str or type(p[3]) is str:
            print(p[3])
            true_address=tools.emit('j>',str(p[1]),str(p[3]),'0')
            false_address=tools.emit('j','-','-','0')
            p[0]=[true_address,false_address]
        else:
            if p[1]>p[3]:
                p[0]=[1,1]
            else:
                p[0]=[0,0]    
    elif p[2]=='>=':
        if type(p[1]) is str or type(p[3]) is str:
            true_address=tools.emit('j>=',str(p[1]),str(p[3]),'0')
            false_address=tools.emit('j','-','-','0')
            p[0]=[true_address,false_address]
        else:
            if p[1]>=p[3]:
                p[0]=[1,1]
            else:
                p[0]=[0,0]  
    elif p[2]=='==':
        if type(p[1]) is str or type(p[3]) is str:
            true_address=tools.emit('j==',str(p[1]),str(p[3]),'0')
            false_address=tools.emit('j','-','-','0')
            p[0]=[true_address,false_address]
        else:
            if p[1]==p[3]:
                p[0]=[1,1]
            else:
                p[0]=[0,0] 
    elif p[2]=='!=':
        if type(p[1]) is str or type(p[3]) is str:
            true_address=tools.emit('j!=',str(p[1]),str(p[3]),'0')
            false_address=tools.emit('j','-','-','0')
            p[0]=[true_address,false_address]
        else:
            if p[1]!=p[3]:
                p[0]=[1,1]
            else:
                p[0]=[0,0]  


def p_Expression_uminus(p):
    "Expression : '-' Expression %prec UMINUS"
    p[0]=-p[2]
    #print("Debug At Expression_uminus...")

def p_AddExpression(p):
    '''AddExpression : Term
                     | Term '+' Term
                     | Term '-' Term '''
    #print("Debug At AddExpression...")
    if len(p)==2:
        p[0]=p[1]
    elif p[2]=='+':
        if type(p[1]) is str or type(p[3]) is str:
            p[0]=tools.newTemp()
            #s=p[0]+str(p[1])+'+'+str(p[3])
            tools.emit(p[0],str(p[1]),'+',str(p[3]))
        else:
            p[0]=p[1]+p[3]
    elif p[2]=='-':
        if type(p[1]) is str or type(p[3]) is str:
            p[0]=tools.newTemp()
            #s=p[0]+str(p[1])+'-'+str(p[3])
            tools.emit(p[0],str(p[1]),'-',str(p[3]))
        else:
            p[0]=p[1]-p[3]

def p_Term(p):
    '''Term : Factor
            | Factor '*' Factor
            | Factor '/' Factor '''
    if len(p)==2:
        p[0]=p[1]
    elif p[2]=='*':
        if type(p[1]) is str or type(p[3]) is str:
            p[0]=tools.newTemp()
            #s=p[0]+str(p[1])+'*'+str(p[3])
            tools.emit(p[0],str(p[1]),'*',str(p[3]))
        else:
            p[0]=p[1]*p[3]
    elif p[2]=='/':
        if type(p[1]) is str or type(p[3]) is str:
            p[0]=tools.newTemp()
            #s=p[0]+str(p[1])+'/'+str(p[3])
            tools.emit(p[0],str(p[1]),'/',str(p[3]))
        else:
            p[0]=int(p[1]/p[3])



def p_Factor(p):
    '''Factor : NUMBER
              | '(' Expression ')' 
              | ID FTYPE '''
    #print("Debug At Factor...")
    if len(p)==2:
        p[0]=p[1]
    elif len(p)==4:
        p[0]=p[2][0]
    elif len(p)==3:
        if p[2]==0:
            p[0]=p[1]
            print(p[0])
        else:
            i=0
            for key in symbol_table[p[1]].formal_table:
                symbol_table[p[1]].formal_table[key][1]=real_table[i]
                i+=1

def p_FTYPE(p):
    '''FTYPE : Call
             | empty '''
    #print("Debug At FTYPE...")
    if p[1]==1:
        p[0]=1
    else:
        p[0]=0

def p_Call(p):
    "Call : '(' RealPara ')'"
    #print("Debug At Call...")
    p[0]=1

def p_RealPara(p):
    '''RealPara : RealParaTable
                | empty '''
    #print("Debug At RealPara...")

def p_RealParaTable(p):
    '''RealParaTable : Para TRealParaTable'''
    #print("Debug At RealParaTable...")

def p_TRealParaTable(p):
    '''TRealParaTable : ',' Para TRealParaTable
                      | empty '''

def p_Para(p):
    'Para : Expression '
    p[0]=tools.newTemp()
    tools.emit(':=',p[0],str(p[1][0]),'-')
    real_table.append(p[0])


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
int func(int f , int g){
    int a;
    int e;
    a=10;
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
int program(int a,int b,int c){
    int i;
    int j;
    i=0;
    if(a>(b+c)){
        a=a+(b*c+1);
    }
    else{
        j=a;
    }
    while(i<=100){
        i=j*2;
    }
    i=func(j,2);
    return i;
}
'''

#lexer.input(data)

#while True:
#    tok=lexer.token()
#    if not tok :
#       break
#    print (tok)

yacc.parse(data)


#print(symbol_table['function'].formal_table)
#print(symbol_table['function'].temp_val)
print(symbol_table['func'].formal_table)
print(symbol_table['func'].temp_val)

tools.show_me_code()

#while True:
#   try:
#       s=input('calc > ')
#   except EOFError:
#       break
#   if not s:
#       continue
#   print(s)
#   yacc.parse(s)
