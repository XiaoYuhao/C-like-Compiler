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

func:
addiu $sp $sp -40
sw $ra 36($sp)
sw $fp 32($sp)
move $fp $sp
sw $a0 40($fp)
sw $a1 44($fp)
li $t0 2
sw $t0 20($fp)
lw $t0 40($fp)
lw $t1 44($fp)
addu $t2 $t0 $t1
sw $t2 24($fp)
lw $t0 24($fp)
lw $t1 20($fp)
mul $t2 $t0 $t1
sw $t2 24($fp)
lw $v0 24($fp)
move $sp $fp
lw $fp 32($sp)
lw $ra 36($sp)
jr $ra
addiu $sp $sp 40
main:
addiu $sp $sp -44
sw $ra 40($sp)
sw $fp 36($sp)
move $fp $sp
li $t0 1
sw $t0 20($fp)
li $t0 2
sw $t0 24($fp)
lw $t0 20($fp)
lw $t1 24($fp)
addu $t2 $t0 $t1
sw $t2 28($fp)
Target2 :
lw $t0 20($fp)
li $t1 12
blt $t0 $t1 Target0
nop
j Target1
nop
Target0 :
lw $t0 20($fp)
li $t1 1
addu $t1 $t0 $t1
sw $t1 20($fp)
j Target2
nop
Target1 :
lw $t0 28($fp)
li $t1 10
blt $t0 $t1 Target3
nop
j Target4
nop
Target3 :
lw $t0 20($fp)
sw $t0 28($fp)
j Target5
nop
Target4 :
lw $t0 20($fp)
sw $t0 24($fp)
Target5 :
lw $a1 28($fp)
lw $a0 20($fp)
jal func
nop
sw $v0 24($fp)
lw $v0 24($fp)
move $sp $fp
lw $fp 36($sp)
lw $ra 40($sp)
jr $ra
addiu $sp $sp 44

real_end: