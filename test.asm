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

program:
addiu $sp $sp -40
sw $ra 36($sp)
sw $fp 32($sp)
move $fp $sp
sw $a0 40($fp)
sw $a1 44($fp)
sw $a2 48($fp)
li $t0 0
sw $t0 20($fp)
lw $t0 44($fp)
lw $t1 48($fp)
addu $t2 $t0 $t1
lw $t0 40($fp)
bgt $t0 $t2 Target0
nop
j Target1
nop
Target0 :
lw $t0 44($fp)
lw $t1 48($fp)
mul $t2 $t0 $t1
li $t0 1
addu $t0 $t2 $t0
lw $t1 40($fp)
addu $t2 $t1 $t0
sw $t2 24($fp)
j Target5
nop
Target1 :
lw $t0 40($fp)
sw $t0 24($fp)
Target5 :
lw $t0 20($fp)
li $t1 100
ble $t0 $t1 Target3
nop
j Target4
nop
Target3 :
lw $t0 24($fp)
li $t1 2
mul $t1 $t0 $t1
sw $t1 20($fp)
j Target5
nop
Target4 :
lw $v0 20($fp)
move $sp $fp
lw $fp 32($sp)
lw $ra 36($sp)
jr $ra
addiu $sp $sp 40
demo:
addiu $sp $sp -32
sw $ra 28($sp)
sw $fp 24($sp)
move $fp $sp
sw $a0 32($fp)
lw $t0 32($fp)
li $t1 2
addu $t1 $t0 $t1
sw $t1 32($fp)
lw $t0 32($fp)
li $t1 2
mul $t1 $t0 $t1
move $v0 $t1 
move $sp $fp
lw $fp 24($sp)
lw $ra 28($sp)
jr $ra
addiu $sp $sp 32
main:
addiu $sp $sp -44
sw $ra 40($sp)
sw $fp 36($sp)
move $fp $sp
li $t0 3
sw $t0 20($fp)
li $t0 4
sw $t0 24($fp)
li $t0 2
sw $t0 28($fp)
lw $a0 20($fp)
lw $a1 24($fp)
lw $a2 28($fp)
jal demo
nop
move $t0 v0
jal program
nop
sw $v0 20($fp)
move $sp $fp
lw $fp 36($sp)
lw $ra 40($sp)
jr $ra
addiu $sp $sp 44

real_end: