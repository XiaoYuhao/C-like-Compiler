
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "left+-left*/rightUMINUSELSE EQUAL GREATER ID IF INT LESS NUMBER RETURN UNEQUAL VOID WHILEProgarm : DeclareStrDeclareStr : Declare TDeclareDeclare : INT ID DeclareFun\n               | INT ID DeclareType\n               | VOID ID DeclareFun TDeclare : empty\n                | Declare TDeclare DeclareType : ';'DeclareFun : '(' FormalPara ')' BlockFormalPara : ParaTable \n                  | VOID ParaTable : Parameter\n                 | ',' ParaTable   Parameter : INT IDBlock : '{' LangStr TLangStr '}'TLangStr : empty \n                | LangStr TLangStrLangStr : InterDeclare \n               | InterStrInterDeclare : InterVarDeclare ';' InterVarDeclare : INT IDInterStr : Sentence Sentence : IfSentence \n                | WhileSentence \n                | ReturnSentence\n                | AssignSentence AssignSentence : ID '=' Expression ';' ReturnSentence : RETURN ';'\n                      | RETURN Expression ';' WhileSentence : WHILE '(' Expression ')' BlockIfSentence : IF '(' Expression ')' Block ElseSentenceElseSentence : empty\n                    | ELSE BlockExpression : AddExpression \n                  | AddExpression '<' AddExpression\n                  | AddExpression LESS AddExpression\n                  | AddExpression '>' AddExpression\n                  | AddExpression GREATER AddExpression\n                  | AddExpression EQUAL AddExpression\n                  | AddExpression UNEQUAL AddExpression\n                  Expression : '-' Expression %prec UMINUSAddExpression : Term\n                     | Term '+' Term\n                     | Term '-' Term Term : Factor\n            | Factor '*' Factor\n            | Factor '/' Factor Factor : NUMBER\n              | '(' Expression ')' \n              | ID FTYPE FTYPE : Call\n             | empty Call : '(' RealPara ')'RealPara : RealParaTable\n                | empty RealParaTable : Expression\n                     | ',' RealParaTable empty : "
    
_lr_action_items = {'INT':([0,3,6,12,13,14,15,16,21,26,27,28,29,30,32,35,36,37,38,42,45,50,60,64,81,100,101,104,105,107,],[4,4,4,-3,-4,22,-8,-5,22,-9,33,33,-18,-19,-22,-23,-24,-25,-26,33,-20,-28,-15,-29,-27,-58,-30,-31,-32,-33,]),'VOID':([0,3,6,12,13,14,15,16,26,60,],[5,5,5,-3,-4,19,-8,-5,-9,-15,]),'$end':([1,2,3,6,7,8,11,12,13,15,16,26,60,],[0,-1,-58,-58,-2,-6,-7,-3,-4,-8,-5,-9,-15,]),'ID':([4,5,22,27,28,29,30,32,33,35,36,37,38,41,42,45,47,48,49,50,53,57,60,64,65,66,67,68,69,70,72,73,74,75,80,81,99,100,101,104,105,107,],[9,10,25,34,34,-18,-19,-22,46,-23,-24,-25,-26,58,34,-20,58,58,58,-28,58,58,-15,-29,58,58,58,58,58,58,58,58,58,58,58,-27,58,-58,-30,-31,-32,-33,]),'(':([9,10,39,40,41,47,48,49,53,57,58,65,66,67,68,69,70,72,73,74,75,80,99,],[14,14,48,49,57,57,57,57,57,57,80,57,57,57,57,57,57,57,57,57,57,57,57,]),';':([9,31,41,46,51,52,54,55,56,58,61,71,77,78,79,84,85,86,87,88,89,90,91,92,93,94,102,],[15,45,50,-21,64,-34,-42,-45,-48,-58,81,-41,-50,-51,-52,-35,-36,-37,-38,-39,-40,-43,-44,-46,-47,-49,-53,]),',':([14,21,80,99,],[21,21,99,99,]),')':([17,18,19,20,24,25,52,54,55,56,58,62,63,71,76,77,78,79,80,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,102,103,],[23,-10,-11,-12,-13,-14,-34,-42,-45,-48,-58,82,83,-41,94,-50,-51,-52,-58,-35,-36,-37,-38,-39,-40,-43,-44,-46,-47,-49,102,-54,-55,-56,-53,-57,]),'{':([23,82,83,106,],[27,27,27,27,]),'IF':([27,28,29,30,32,35,36,37,38,42,45,50,60,64,81,100,101,104,105,107,],[39,39,-18,-19,-22,-23,-24,-25,-26,39,-20,-28,-15,-29,-27,-58,-30,-31,-32,-33,]),'WHILE':([27,28,29,30,32,35,36,37,38,42,45,50,60,64,81,100,101,104,105,107,],[40,40,-18,-19,-22,-23,-24,-25,-26,40,-20,-28,-15,-29,-27,-58,-30,-31,-32,-33,]),'RETURN':([27,28,29,30,32,35,36,37,38,42,45,50,60,64,81,100,101,104,105,107,],[41,41,-18,-19,-22,-23,-24,-25,-26,41,-20,-28,-15,-29,-27,-58,-30,-31,-32,-33,]),'}':([28,29,30,32,35,36,37,38,42,43,44,45,50,59,60,64,81,100,101,104,105,107,],[-58,-18,-19,-22,-23,-24,-25,-26,-58,60,-16,-20,-28,-17,-15,-29,-27,-58,-30,-31,-32,-33,]),'=':([34,],[47,]),'-':([41,47,48,49,53,54,55,56,57,58,77,78,79,80,92,93,94,99,102,],[53,53,53,53,53,73,-45,-48,53,-58,-50,-51,-52,53,-46,-47,-49,53,-53,]),'NUMBER':([41,47,48,49,53,57,65,66,67,68,69,70,72,73,74,75,80,99,],[56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,]),'<':([52,54,55,56,58,77,78,79,90,91,92,93,94,102,],[65,-42,-45,-48,-58,-50,-51,-52,-43,-44,-46,-47,-49,-53,]),'LESS':([52,54,55,56,58,77,78,79,90,91,92,93,94,102,],[66,-42,-45,-48,-58,-50,-51,-52,-43,-44,-46,-47,-49,-53,]),'>':([52,54,55,56,58,77,78,79,90,91,92,93,94,102,],[67,-42,-45,-48,-58,-50,-51,-52,-43,-44,-46,-47,-49,-53,]),'GREATER':([52,54,55,56,58,77,78,79,90,91,92,93,94,102,],[68,-42,-45,-48,-58,-50,-51,-52,-43,-44,-46,-47,-49,-53,]),'EQUAL':([52,54,55,56,58,77,78,79,90,91,92,93,94,102,],[69,-42,-45,-48,-58,-50,-51,-52,-43,-44,-46,-47,-49,-53,]),'UNEQUAL':([52,54,55,56,58,77,78,79,90,91,92,93,94,102,],[70,-42,-45,-48,-58,-50,-51,-52,-43,-44,-46,-47,-49,-53,]),'+':([54,55,56,58,77,78,79,92,93,94,102,],[72,-45,-48,-58,-50,-51,-52,-46,-47,-49,-53,]),'*':([55,56,58,77,78,79,94,102,],[74,-48,-58,-50,-51,-52,-49,-53,]),'/':([55,56,58,77,78,79,94,102,],[75,-48,-58,-50,-51,-52,-49,-53,]),'ELSE':([60,100,],[-15,106,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'Progarm':([0,],[1,]),'DeclareStr':([0,],[2,]),'Declare':([0,3,6,],[3,6,6,]),'TDeclare':([3,6,],[7,11,]),'empty':([3,6,28,42,58,80,100,],[8,8,44,44,79,97,105,]),'DeclareFun':([9,10,],[12,16,]),'DeclareType':([9,],[13,]),'FormalPara':([14,],[17,]),'ParaTable':([14,21,],[18,24,]),'Parameter':([14,21,],[20,20,]),'Block':([23,82,83,106,],[26,100,101,107,]),'LangStr':([27,28,42,],[28,42,42,]),'InterDeclare':([27,28,42,],[29,29,29,]),'InterStr':([27,28,42,],[30,30,30,]),'InterVarDeclare':([27,28,42,],[31,31,31,]),'Sentence':([27,28,42,],[32,32,32,]),'IfSentence':([27,28,42,],[35,35,35,]),'WhileSentence':([27,28,42,],[36,36,36,]),'ReturnSentence':([27,28,42,],[37,37,37,]),'AssignSentence':([27,28,42,],[38,38,38,]),'TLangStr':([28,42,],[43,59,]),'Expression':([41,47,48,49,53,57,80,99,],[51,61,62,63,71,76,98,98,]),'AddExpression':([41,47,48,49,53,57,65,66,67,68,69,70,80,99,],[52,52,52,52,52,52,84,85,86,87,88,89,52,52,]),'Term':([41,47,48,49,53,57,65,66,67,68,69,70,72,73,80,99,],[54,54,54,54,54,54,54,54,54,54,54,54,90,91,54,54,]),'Factor':([41,47,48,49,53,57,65,66,67,68,69,70,72,73,74,75,80,99,],[55,55,55,55,55,55,55,55,55,55,55,55,55,55,92,93,55,55,]),'FTYPE':([58,],[77,]),'Call':([58,],[78,]),'RealPara':([80,],[95,]),'RealParaTable':([80,99,],[96,103,]),'ElseSentence':([100,],[104,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> Progarm","S'",1,None,None,None),
  ('Progarm -> DeclareStr','Progarm',1,'p_Program','Compiler.py',75),
  ('DeclareStr -> Declare TDeclare','DeclareStr',2,'p_DeclareStr','Compiler.py',79),
  ('Declare -> INT ID DeclareFun','Declare',3,'p_Declare','Compiler.py',83),
  ('Declare -> INT ID DeclareType','Declare',3,'p_Declare','Compiler.py',84),
  ('Declare -> VOID ID DeclareFun','Declare',3,'p_Declare','Compiler.py',85),
  ('TDeclare -> empty','TDeclare',1,'p_TDeclare','Compiler.py',89),
  ('TDeclare -> Declare TDeclare','TDeclare',2,'p_TDeclare','Compiler.py',90),
  ('DeclareType -> ;','DeclareType',1,'p_DeclareType','Compiler.py',93),
  ('DeclareFun -> ( FormalPara ) Block','DeclareFun',4,'p_DeclareFun','Compiler.py',97),
  ('FormalPara -> ParaTable','FormalPara',1,'p_FormalPara','Compiler.py',101),
  ('FormalPara -> VOID','FormalPara',1,'p_FormalPara','Compiler.py',102),
  ('ParaTable -> Parameter','ParaTable',1,'p_ParaTable','Compiler.py',106),
  ('ParaTable -> , ParaTable','ParaTable',2,'p_ParaTable','Compiler.py',107),
  ('Parameter -> INT ID','Parameter',2,'p_Parameter','Compiler.py',111),
  ('Block -> { LangStr TLangStr }','Block',4,'p_Block','Compiler.py',115),
  ('TLangStr -> empty','TLangStr',1,'p_TLangStr','Compiler.py',119),
  ('TLangStr -> LangStr TLangStr','TLangStr',2,'p_TLangStr','Compiler.py',120),
  ('LangStr -> InterDeclare','LangStr',1,'p_LangStr','Compiler.py',124),
  ('LangStr -> InterStr','LangStr',1,'p_LangStr','Compiler.py',125),
  ('InterDeclare -> InterVarDeclare ;','InterDeclare',2,'p_InterDeclare','Compiler.py',129),
  ('InterVarDeclare -> INT ID','InterVarDeclare',2,'p_InterVarDeclare','Compiler.py',135),
  ('InterStr -> Sentence','InterStr',1,'p_InterStr','Compiler.py',139),
  ('Sentence -> IfSentence','Sentence',1,'p_Sentence','Compiler.py',143),
  ('Sentence -> WhileSentence','Sentence',1,'p_Sentence','Compiler.py',144),
  ('Sentence -> ReturnSentence','Sentence',1,'p_Sentence','Compiler.py',145),
  ('Sentence -> AssignSentence','Sentence',1,'p_Sentence','Compiler.py',146),
  ('AssignSentence -> ID = Expression ;','AssignSentence',4,'p_AssignSentence','Compiler.py',150),
  ('ReturnSentence -> RETURN ;','ReturnSentence',2,'p_ReturnSentence','Compiler.py',154),
  ('ReturnSentence -> RETURN Expression ;','ReturnSentence',3,'p_ReturnSentence','Compiler.py',155),
  ('WhileSentence -> WHILE ( Expression ) Block','WhileSentence',5,'p_WhileSentence','Compiler.py',159),
  ('IfSentence -> IF ( Expression ) Block ElseSentence','IfSentence',6,'p_IfSentence','Compiler.py',163),
  ('ElseSentence -> empty','ElseSentence',1,'p_ElseSentence','Compiler.py',167),
  ('ElseSentence -> ELSE Block','ElseSentence',2,'p_ElseSentence','Compiler.py',168),
  ('Expression -> AddExpression','Expression',1,'p_Expression','Compiler.py',172),
  ('Expression -> AddExpression < AddExpression','Expression',3,'p_Expression','Compiler.py',173),
  ('Expression -> AddExpression LESS AddExpression','Expression',3,'p_Expression','Compiler.py',174),
  ('Expression -> AddExpression > AddExpression','Expression',3,'p_Expression','Compiler.py',175),
  ('Expression -> AddExpression GREATER AddExpression','Expression',3,'p_Expression','Compiler.py',176),
  ('Expression -> AddExpression EQUAL AddExpression','Expression',3,'p_Expression','Compiler.py',177),
  ('Expression -> AddExpression UNEQUAL AddExpression','Expression',3,'p_Expression','Compiler.py',178),
  ('Expression -> - Expression','Expression',2,'p_Expression_uminus','Compiler.py',183),
  ('AddExpression -> Term','AddExpression',1,'p_AddExpression','Compiler.py',188),
  ('AddExpression -> Term + Term','AddExpression',3,'p_AddExpression','Compiler.py',189),
  ('AddExpression -> Term - Term','AddExpression',3,'p_AddExpression','Compiler.py',190),
  ('Term -> Factor','Term',1,'p_Term','Compiler.py',194),
  ('Term -> Factor * Factor','Term',3,'p_Term','Compiler.py',195),
  ('Term -> Factor / Factor','Term',3,'p_Term','Compiler.py',196),
  ('Factor -> NUMBER','Factor',1,'p_Factor','Compiler.py',199),
  ('Factor -> ( Expression )','Factor',3,'p_Factor','Compiler.py',200),
  ('Factor -> ID FTYPE','Factor',2,'p_Factor','Compiler.py',201),
  ('FTYPE -> Call','FTYPE',1,'p_FTYPE','Compiler.py',205),
  ('FTYPE -> empty','FTYPE',1,'p_FTYPE','Compiler.py',206),
  ('Call -> ( RealPara )','Call',3,'p_Call','Compiler.py',210),
  ('RealPara -> RealParaTable','RealPara',1,'p_RealPara','Compiler.py',214),
  ('RealPara -> empty','RealPara',1,'p_RealPara','Compiler.py',215),
  ('RealParaTable -> Expression','RealParaTable',1,'p_RealParaTable','Compiler.py',219),
  ('RealParaTable -> , RealParaTable','RealParaTable',2,'p_RealParaTable','Compiler.py',220),
  ('empty -> <empty>','empty',0,'p_empty','Compiler.py',224),
]
