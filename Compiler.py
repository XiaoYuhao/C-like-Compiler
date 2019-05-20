#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-

import ply.lex as lex
import ply.yacc as yacc
import copy
import tools
import math
import sys
import codecs

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


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type=reserved.get(t.value,'ID')   #先在保留字中寻找，不存在则为ID
    #t.value=(t.value,symbol_lookup(t.value))
    return t


def t_COMMENT2(t):
    r'/\*[\s\S]*\*/'

def t_COMMENT1(t):
    r'//.*'
    pass

def t_NUMBER(t):
    r'\d+'
    t.value=int(t.value)
    return t

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

#Argument Regs当前使用的个数
areg_count=0
#函数形式参数栈
para_stack=[]

fun_count=0
fun_name=[]

error_count=0

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
        self.max_argu=0             #子函数最大参数个数
        self.frame_size=0           #函数栈帧的大小
        self.frame_temp_sp=dict()   #临时变量在栈帧中的偏移量
        self.enter_address=0        #函数入口地址

    def clear(self):
        self.type="fun"
        self.formal_table.clear()
        self.temp_val.clear()
        self.return_type=None
        self.return_val=0
        self.max_argu=0
        self.frame_size=0
        self.frame_temp_sp=dict()
        self.enter_address=0

    def make_frame(self):
        temp_val_num=len(self.temp_val)
        if self.max_argu>=4:
            self.frame_size=(self.max_argu+temp_val_num+4)*4
        else:
            self.frame_size=(4+temp_val_num+4)*4

        start_sp=self.frame_size-12-temp_val_num*4

        for key in self.temp_val:
            self.frame_temp_sp[key]=start_sp
            start_sp+=4

        start_sp=self.frame_size
        for key in self.formal_table:
            self.frame_temp_sp[key]=start_sp
            start_sp+=4




#当前函数作用域符号表
fun_table=Symbol_fun()

tools=tools.Tools()

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
    #print(p[2])
    global fun_count
    global code_line
    if p[3]=="DeclareFun":
        flag=symbol_table.get(p[2])
        if flag==None:
            symbol_table[p[2]]=copy.deepcopy(fun_table) #深拷贝
            symbol_table[p[2]].make_frame()
            fun_table.clear()   #清空表临时
            fun_name.append(p[2])
            fun_count+=1
        else:
            print("Error at Row:%d  '%s' redefined" %(p.lineno(2),p[2]))
            show_error(p.lineno(2))
            error_count+=1
    elif p[3]=="DeclareType":
        flag=symbol_table.get(p[2])
        if flag==None:
            newnode=Symbol_type(p[1],0)
            symbol_table[p[2]]=newnode
        else:
            print("Error at Row:%d  '%s' redefined" %(p.lineno(2),p[2]))
            show_error(p.lineno(2))
            error_count+=1
 
def p_TDeclare(p):
    '''TDeclare : empty
                | Declare TDeclare '''

def p_DeclareType(p):
    "DeclareType : ';'"
    #print("Debug At DeclareType...")
    p[0]="DeclareType"

def p_DeclareType_error(p):
    "DeclareType : error"
    print("Error at Row:%d expect:';'" %p.lineno(1))
    show_error(p.lineno(1))

def p_DeclareFun(p):
    "DeclareFun : '(' FormalPara ')' Block"
    #print("Debug At DeclareFun...")
    p[0]="DeclareFun"

def p_DeclareFun_error(p):
    '''DeclareFun : error FormalPara ')' Block
                  | '(' FormalPara error Block '''
    #print("Debug At DeclareFun...")
    print("Error at Row:%d expect:'(' or ')' " %p.lineno(1))
    show_error(p.lineno(1))

def p_FormalPara(p):
    '''FormalPara : ParaTable 
                  | VOID '''
    #print("Debug At FormalPara...")
    global areg_count
    global fun_count
    tools.emit('enter',str(fun_count),'-','-')
    areg_count=0


def p_ParaTable(p):
    '''ParaTable : Parameter TParaTable '''
    #print("Debug At ParaTable...")

def p_TParaTable(p):
    '''TParaTable : empty
                  | ',' Parameter TParaTable '''

def p_Parameter(p):
    'Parameter : INT ID'
    global areg_count
    flag=fun_table.formal_table.get(p[2])
    if flag==None:
        fun_table.formal_table[p[2]]=['int',0]  #加入形式参数表，附初值为0
        #tools.emit(':=',str(p[2]),'a'+str(areg_count),'-')
        areg_count+=1
    else:
        print("Error Row:%d %s redefined ..." %(p.lineno(3),p[2]))
        show_error(p.lineno(3))

def p_Parameter_error(p):
    'Parameter : error ID'
    print("Error at Row:%d illegal types:%s " %(p.lineno(2),p[1]))
    show_error(p.lineno(2))

def p_Block(p):
    "Block : '{' LangStr TLangStr '}'"
    #print("Debug At Block...")

def p_Block_error1(p):
    '''Block : error LangStr TLangStr '}' '''
    print("Error at Row:%d expect:'{' " %p.lineno(1))
    show_error(p.lineno(1))

def p_Block_error2(p):
    '''Block : '{' LangStr TLangStr error '''
    print("Error at Row:%d expect:'}' " %p.lineno(5))
    show_error(p.lineno(5))

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
    'InterVarDeclare : INT ID'                      #语法规则
    global error_count
    flag=fun_table.formal_table.get(p[2])           #在函数形式参数表中查找是否有同名变量
    if flag==None:
        flag2=fun_table.temp_val.get(p[2])          #在函数临时变量表中查找是否有同名变量
        if flag2==None:
            fun_table.temp_val[p[2]]=['int',0]      #加入函数临时变量表并赋初值为0
        else:
            print("Error at Row:%d  '%s' redefined " %(p.lineno(2),p[2]))   #打印出错信息
            show_error(p.lineno(2))
            error_count+=1
            
    else:
        print("Error at Row:%d  '%s' redefined " %(p.lineno(2),p[2]))       #打印出错信息
        show_error(p.lineno(2))
        error_count+=1
        

def p_InterVarDeclare_error(p):
    'InterVarDeclare : error ID'
    print("Error at Row:%d illegal types:%s " %(p.lineno(2),p[1]))
    show_error(p.lineno(2))

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
    flag3=fun_table.temp_val.get(p[3][0])
    flag4=fun_table.formal_table.get(p[3][0])
    if flag1==None and flag2==None:
        print("Error Row:%d %s undefined ..." %(p.lineno(2),p[1]))
    elif flag3!=None or flag4!=None:
        tn=tools.newTemp()
        begin_address=tools.emit(':=',str(p[3][0]),'-',tn)
        address=tools.emit(':=',tn,'-',p[1])
        end_address=address+1
        p[0]=[begin_address,end_address]
    else:
        address=tools.emit(':=',str(p[3][0]),'-',p[1])
        begin_address=address
        end_address=address+1
        p[0]=[begin_address,end_address]

def p_AssignSentence_error(p):
    "AssignSentence : ID '=' Expression error "
    print("Error at Row:%d expect: ';' " %p.lineno(1))
    show_error(p.lineno(1))

def p_ReturnSentence(p):
    '''ReturnSentence : RETURN ';'
                      | RETURN Expression ';' '''
    #print("Debug At ReturnSentence...")
    if len(p)==3:
        fun_table.return_val=None
        fun_table.return_type='void'
        tools.emit('ret','-','-','-')
    else:
        fun_table.return_type='int'   #函数返回值类型
        fun_table.return_val=p[2]    #函数返回值
        tools.emit(':=',str(p[2][0]),'-','_v0')
        tools.emit('ret','-','-','-')

def p_ReturnSentence_error(p):
    '''ReturnSentence : RETURN error
                      | RETURN Expression error '''
    print("Error at Row:%d expect: ';' " %p.lineno(1))
    show_error(p.lineno(1))

def p_WhileSentence(p):
    "WhileSentence : WHILE  M '(' Expression ')' M Block"

    true_list=p[4][0]                           #获取true回填链表
    false_list=p[4][1]                          #获取false回填链表
    again_address=p[2]                          #获取循环地址
    true_address=p[6]                           #获取true跳转地址

    tools.emit('j','-','-',str(again_address))  #生成中间代码

    false_address=tools.nextquad()              #获取false跳转地址
    tools.backpatch(true_list,true_address)     #回填true链表
    tools.backpatch(false_list,false_address)   #回填false链表

    begin_address=p[2]                          #while语句块起始地址
    end_address=false_address                   #while语句块结束地址
    p[0]=[begin_address,end_address]            #将语句块始末地址向上传递


def p_M(p):
    "M : empty"
    p[0]=tools.nextquad()

#def p_S(p):
#    "S : empty"


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
    elif p[2]=='<':
        if type(p[1]) is str or type(p[3]) is str:
            true_address=tools.emit('j<',str(p[1]),str(p[3]),'0')
            false_address=tools.emit('j','-','-','0')
            p[0]=[true_address,false_address]
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
        else:
            if p[1]<=p[3]:
                p[0]=[1,1]
            else:
                p[0]=[0,0]
    elif p[2]=='>':
        if type(p[1]) is str or type(p[3]) is str:
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

def p_Expression_error(p):
    '''Expression : error '<' AddExpression
                  | AddExpression '<' error
                  | error LESS AddExpression
                  | AddExpression LESS error
                  | error '>' AddExpression
                  | AddExpression '>' error
                  | error GREATER AddExpression
                  | AddExpression GREATER error
                  | error EQUAL AddExpression
                  | AddExpression EQUAL error
                  | error UNEQUAL AddExpression
                  | AddExpression UNEQUAL error
                  '''
    print("Error at Row:%d illegal expressions on the %s side" %(p.lineno(3),p[2]))
    show_error(p.lineno(3))

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
            tools.emit('+',str(p[1]),str(p[3]),p[0])
        else:
            p[0]=p[1]+p[3]
    elif p[2]=='-':
        if type(p[1]) is str or type(p[3]) is str:
            p[0]=tools.newTemp()
            #s=p[0]+str(p[1])+'-'+str(p[3])
            tools.emit('-',str(p[1]),str(p[3]),p[0])
        else:
            p[0]=p[1]-p[3]

#def p_AddExpression_error(p):
#    '''AddExpression : error '+' Term
#                     | Term '+' error
#                     | error '-' Term
#                     | Term '-' error '''
#    print("Error at Row:%d illegal operands on the %s side" %(p.lineno(3),p[2]))

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
            tools.emit('*',str(p[1]),str(p[3]),p[0])
        else:
            p[0]=p[1]*p[3]
    elif p[2]=='/':
        if type(p[1]) is str or type(p[3]) is str:
            p[0]=tools.newTemp()
            #s=p[0]+str(p[1])+'/'+str(p[3])
            tools.emit('/',str(p[1]),str(p[3]),p[0])
        else:
            p[0]=int(p[1]/p[3])

def p_Term_error(p):
    '''Term : error '*' Factor
            | Factor '*' error
            | error '/' Factor 
            | Factor '/' error '''
    print("Error at Row:%d illegal operands on the %s side" %(p.lineno(3),p[2]))
    show_error(p.lineno(3))



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
        else:
            para_num=len(symbol_table[str(p[1])].formal_table)
            if fun_table.max_argu<para_num:
                fun_table.max_argu=para_num
            for i in range(para_num):
                global para_stack
                para=para_stack.pop()
                tools.emit(':=',para,'-','_a'+str(para_num-i-1))

            tools.emit('call',str(p[1]),'-','-')
            p[0]='_v0'

def p_Factor_error(p):
    '''Factor : error Expression ')'
              | '(' Expression error '''
    print("Error at Row:%d expect : '(' or ')' " %p.lineno(2))       
    show_error(p.lineno(2))


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
    #global areg_count
    #fun_table.max_argu=areg_count
    #areg_count=0

def p_Call_error(p):
    '''Call : '(' RealPara error
            | error RealPara ')' '''
    print("Error at Row:%d expect : '(' or ')' " %p.lineno(2))
    show_error(p.lineno(2))

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

def p_TRealParaTable_error(p):
    '''TRealParaTable : error Para TRealParaTable'''
    print("Error at Row:%d expect: ','" %p.lineno(2))
    show_error(p.lineno(2))
 

def p_Para(p):
    'Para : Expression '
    #p[0]=tools.newTemp()
    #global areg_count
    #tools.emit(':=',str(p[1][0]),'-','_a'+str(areg_count))
    #areg_count+=1
    global para_stack
    para_stack.append(str(p[1][0]))
    #real_table.append(p[0])


def p_empty(p):
    'empty : '
    #print("Debug At empty...")
    pass

def p_error(p):
    global error_count
    error_count+=1
    #print("Syntax error at Row:%d : %s" %(p.lineno,p.value))
    if p==None:
        #print("Syntax error at Row:%d : %s" %(p.lineno,p.value))
        #exit(p.lineno)
        #p[0]=p.value
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
    j=i;
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
    return i+j;
}
'''

test_data='''
int func(int e,int f){
    int a;
    int b;
    a=0;
    b=1;
    if(a<10){
        a=b+1;
        b=b+1;
    }
    b=e+f;
    a=a+b;
    return a;
}
int main(void){
    int a;
    int b;
    b=10;
    a=0;
    while(a<b){
        a=a+1;
    }
    b=func(a,5);
    return b;
}
'''

test_data2='''
int main(void){
    int a;
    int b;
    int c;
    a=0;
    b=0;
    c=0;
    while(a<100){
        a=a+1;
    }
    while(b<a){
        b=b+1;
    }
    c=b/2
    if(a>c){
        a=c;
    }
    return c;
}
'''

#lexer.input(data)

#while True:
#    tok=lexer.token()
#    if not tok :
#       break
#    print (tok)

#yacc.parse(test_data2)


#print(symbol_table['function'].formal_table)
#print(symbol_table['function'].temp_val)
#print(symbol_table['main'].formal_table)
#print(symbol_table['main'].temp_val)
#print(symbol_table['main'].max_argu)
#symbol_table['main'].make_frame()
#print(symbol_table['main'].frame_temp_sp)
#symbol_table['func'].make_frame()
#print(symbol_table['func'].frame_temp_sp)
#tools.show_me_code()
#tools.code_block()
#print(fun_count)
#print(fun_name)

#tools.make_code(symbol_table,fun_name)

#while True:
#   try:
#       s=input('calc > ')
#   except EOFError:
#       break
#   if not s:
#       continue
#   print(s)
#   yacc.parse(s)
def show_error(current):
    global code_line
    print((" %d         " %(current-1))+code_line[current-2])
    print((" %d       >>" %(current))+code_line[current-1])
    print((" %d         " %(current+1))+code_line[current])
    print("--------------------------------------------------")

if __name__ == '__main__':
    in_file=sys.argv[1]
    words_list=in_file.strip().split('.')
    out_asm_file=words_list[0]+'.asm'
    out_mid_file=words_list[0]+'.mid'
    fin=open(in_file,'r',)

    code_data=fin.read()
    code_line=code_data.split('\n')
    #print(code_line)
    #print("--------------------------------------------------")
    yacc.parse(code_data)
    if error_count>0:
        #print("--------------------------------------------------")
        print("Error :%d" %error_count)
    else:
        #print("Error :%d" %error_count)
        #print("--------------------------------------------------")
        tools.open_file(out_asm_file,out_mid_file)
        tools.code_block()
        tools.make_code(symbol_table,fun_name)

