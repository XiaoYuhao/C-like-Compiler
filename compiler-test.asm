lui $sp 0x8000
addiu $sp $sp 0x0000
move $fp $sp
start:
lui $ra 0x0040
addiu $ra $ra 0x001c
j main
nop
end:
j real_end
nop

main:
addiu $sp $sp -44
sw $ra 40($sp)
sw $fp 36($sp)
move $fp $sp
li $t0 0
sw $t0 20($fp)
li $t0 0
sw $t0 24($fp)
li $t0 0
sw $t0 28($fp)
Target2 :
lw $t0 20($fp)
li $t1 100
blt $t0 $t1 Target0
nop
j Target5
nop
Target0 :
lw $t0 20($fp)
li $t1 1
addu $t1 $t0 $t1
sw $t1 20($fp)
j Target2
nop
Target5 :
lw $t0 24($fp)
lw $t1 20($fp)
blt $t0 $t1 Target3
nop
j Target4
nop
Target3 :
lw $t0 24($fp)
li $t1 1
addu $t1 $t0 $t1
sw $t1 24($fp)
j Target5
nop
Target4 :
lw $t0 24($fp)
li $t1 2
div $t1 $t0 $t1
sw $t1 28($fp)
lw $t0 20($fp)
lw $t1 28($fp)
bgt $t0 $t1 Target6
nop
j Target8
nop
Target6 :
lw $t0 28($fp)
sw $t0 20($fp)
j Target8
nop
Target8 :
lw $v0 28($fp)
move $sp $fp
lw $fp 36($sp)
lw $ra 40($sp)
jr $ra
addiu $sp $sp 44

real_end: