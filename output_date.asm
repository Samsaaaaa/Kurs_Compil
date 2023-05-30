section .bss
	digitSpace resb 100
	digitSpacePos resb 8

	Va resb 8
	Vb resb 8
	Vc resb 8
	Vd resb 8
	T1 resb 8
	T2 resb 8
	T3 resb 8
section .data
	text db "start",10

	S1 db "Первый исход:",10,0
	S2 db "Второй исход:",10,0
section .text
	global _start

_start:

	mov rax,580
	mov [Va],rax
	mov rax,192
	mov [Vb],rax
	mov rax,19657
	mov [Vc],rax
	mov rax,[Va]
	mov rbx,[Vb]
	cmp rax,rbx
	jge L1
	jmp L3
	L1 : 
	mov rax,[Va]
	mov rbx,[Vc]
	mul rbx
	mov [T1],rax
	add rax,10
	mov [T2],rax
	mov rax,[T2]
	mov [Vd],rax
	mov rax,S1
	call _print_string
mov rax,[Vd]
	call _print_num
	jmp L2
	L3 : 
	mov rax,[Va]
	mov rbx,[Vb]
	mul rbx
	mov [T3],rax
	mov rax,[T3]
	mov [Vc],rax
	mov rax,S2
	call _print_string
mov rax,[Vc]
	call _print_num
	L2 : 

	mov rax, 60
	mov rdi, 0
	syscall



_print_num:
    mov rcx, digitSpace
    mov rbx, 10
    mov [rcx], rbx
    inc rcx
    mov [digitSpacePos], rcx

_printRAXLoop:
    mov rdx, 0
    mov rbx, 10
    div rbx
    push rax
    add rdx, 48

    mov rcx, [digitSpacePos]
    mov [rcx], dl
    inc rcx
    mov [digitSpacePos], rcx

    pop rax
    cmp rax, 0
    jne _printRAXLoop

_printRAXLoop2:
    mov rcx, [digitSpacePos]

    mov rax, 1
    mov rdi, 1
    mov rsi, rcx
    mov rdx, 1
    syscall

    mov rcx, [digitSpacePos]
    dec rcx
    mov [digitSpacePos], rcx

    cmp rcx, digitSpace
    jge _printRAXLoop2

    ret


_print_string:
    push rax
    mov rbx, 0

_printLoop:
    inc rax
    inc rbx
    mov cl, [rax]
    cmp cl, 0
    jne _printLoop

    mov rax, 1
    mov rdi, 1
    pop rsi
    mov rdx, rbx
    syscall

    ret

        
