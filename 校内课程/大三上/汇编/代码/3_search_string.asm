;p20
datarea segment
    keyword      db 20
    keyword_len  db ?
    keyword_str  db 20 dup(?)
    sentence     db 100
    sentence_len db ?
    sentence_str db 100 dup(?)
    cmd1         db 'Enter keyword:','$'
    cmd2         db 'Enter Sentence:','$'
    crlf_str     db 0dh,0ah,'$'
    no_match_str db 'No match.',0dh,0ah,'$'
    match_str    db 'Match at location:','$'
    match_str2   db ' H of the sentence.',0dh,0ah,'$'
datarea ends
prognam segment
main proc far
                   assume cs:prognam,ds:datarea,es:datarea
    start:         
                   push   ds
                   sub    ax,ax
                   push   ax
                   mov    ax,datarea
                   mov    ds,ax
                   mov    es,ax
                   mov    bx,0
                   lea    dx,cmd1
                   call   print_str
                   lea    dx,keyword
                   call   input_str
                   call   crlf
    input_sentence:
                   lea    dx,cmd2
                   call   print_str
                   lea    dx,sentence
                   call   input_str
                   call   crlf
                   mov    bx,0
                   cmp    sentence_str[bx],3
                   je     exit
                   call   compare
                   jmp    input_sentence
    exit:          
                   ret
main endp
input_str proc
                   mov    ah,0ah
                   int    21h
                   ret
input_str endp
print_str proc
                   mov    ah,09h
                   int    21h
                   ret
print_str endp
crlf proc
                   lea    dx,crlf_str
                   call   print_str
                   ret
crlf endp
compare proc
                   mov    cl,sentence_len
                   mov    dl,keyword_len
                   xor    ch,ch
                   xor    dh,dh
                   sub    cx,dx
                   inc    cx
                   lea    si,keyword_str
                   xor    bx,bx
    loop_cmp:      
                   push   cx
                   xor    ch,ch
                   mov    cl,keyword_len
                   lea    si,keyword_str
                   lea    di,sentence_str[bx]
                   cld
                   rep    cmpsb
                   pop    cx
                   je     match
                   inc    bx
                   loop   loop_cmp
    no_match:      
                   lea    dx,no_match_str
                   call   print_str
                   ret
    match:         
                   lea    dx,match_str
                   call   print_str
                   call   bin2hex
                   lea    dx,match_str2
                   call   print_str
                   ret
compare endp
bin2hex proc
                   inc    bx
                   xor    ch,ch
    rotate:        
                   mov    dx,bx
                   and    dx,0fh
                   add    dx,30h
                   cmp    dx,3ah
                   jl     not_letter
                   add    dx,07h
    not_letter:    
                   push   dx
                   inc    ch
                   mov    cl,4
                   shr    bx,cl
                   jnz    rotate
    printit:       
                   pop    dx
    ;    xor    dh,dh
                   mov    ah,2
                   int    21h
                   dec    ch
                   jnz    printit
                   ret
bin2hex endp
prognam ends
 end start