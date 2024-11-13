;实验指导书p67
datarea segment
    cmd_input_name      db 'Input name:',0dh,0ah,'$'
    cmd_input_tel       db 'Input a telephone number:',0dh,0ah,'$'
    cmd_query_input_tel db 'Continue to input telephone number?(Y/N)',0dh,0ah,'$'
    cmd_query_find_tel  db 'Continue to find telephone number?(Y/N)',0dh,0ah,'$'
    found_string        db 'Find it:',0dh,0ah,'$'
    not_find_string     db 'Not find!',0dh,0ah,'$'
    clrf                db 0dh,0ah,'$'                                               ;回车
    tel_head            db 'names',15 dup(' '),'tels',0dh,0ah,'$'
    teltab              db 50 dup('$',27 dup(' '),0dh,0ah),'$'                       ;50个人，每个人8个字符的电话号码
    total               db 0
    ;输入区
    buffer_max          db 30
    buffer_len          db ?
    buffer_str          db 30 dup(' '),'$'
datarea ends

prognam segment
main proc far
                     assume cs:prognam,ds:datarea,es:datarea
    start:           
    ;模板
                     push   ds
                     sub    ax,ax
                     push   ax
                     mov    ax,datarea
                     mov    ds,ax
                     mov    es,ax

    inputs:          
                     call   next_row
    ;输入姓名
                     lea    dx,cmd_input_name
                     call   print_str
                     call   input_name
                     call   next_row
    ;输入电话号码
                     lea    dx,cmd_input_tel
                     call   print_str
                     call   input_tel
                     call   next_row
                     call   sort
                     call   output_teltab
                     call   next_row
    ;是否继续输入新信息
                     lea    dx,cmd_query_input_tel
                     call   print_str
                     mov    ah,1
                     int    21h
                     cmp    al,'Y'
                     je     inputs
                     cmp    al,'y'
                     je     inputs
    ;开始寻找电话号码
                     lea    di,teltab                           ;重新遍历电话表
                     call   next_row
    loop1:           
                     lea    dx,cmd_query_find_tel               ;是否继续查询？
                     call   print_str
                     mov    ah,1
                     int    21h
                     cmp    al,'Y'
                     je     find
                     cmp    al,'y'
                     je     find
                     jmp    exit
    ;查找
    find:            
                     call   next_row
                     call   input_name                          ;输入名字
                     call   clear_buffer
                     call   next_row
                     call   name_search                         ;根据名字查找
                     jmp    loop1                               ;循环
    exit:            
                     ret
main endp

    ; 输出字符串的子程序，要把字符串放在dx里
print_str proc
                     mov    ah,09h
                     int    21h
                     ret
print_str endp
    ;输出换行符
next_row proc
                     lea    dx,clrf
                     call   print_str
                     ret
next_row endp
    ;输入一个字符串
input_str proc
                     lea    dx,buffer_max                       ;cin>>buffer_str
                     mov    ah, 0ah
                     int    21h
                     ret
input_str endp
    ;输入名字
input_name proc
                     call   input_str
                     xor    ch,ch
                     mov    cl,buffer_len
                     call   where_name_start
                     mov    bx,offset buffer_str
    input_name_loop: 
                     mov    al,[bx]
                     mov    teltab[si],al
                     inc    bx
                     inc    si
                     loop   input_name_loop
                     ret
input_name endp
input_tel proc
                     call   input_str
                     xor    ch,ch
                     mov    cl,buffer_len
                     call   where_name_start
                     mov    ax,si
                     add    ax,20
                     mov    si,ax
                     mov    bx,offset buffer_str
    input_tel_loop:  
                     mov    al,[bx]
                     mov    teltab[si],al
                     inc    bx
                     inc    si
                     loop   input_tel_loop
    input_tel_end:   
                     mov    al,total
                     inc    al
                     mov    total,al
                     ret
input_tel endp
output_teltab proc
                     lea    dx,tel_head
                     call   print_str
                     lea    dx,teltab
                     call   print_str
                     ret
output_teltab endp
    ;al里放入索引，返回teltab的偏移量到ax里
where_name_index proc
                     xor    ah,ah
                     mov    bl,30
                     mul    bl
                     ret
where_name_index endp
    ;si和ax里存teltab目前的偏移量
where_name_start proc
                     mov    al,total
                     mov    si,0
                     call   where_name_index
                     mov    si,ax
                     ret
where_name_start endp
    ;查找电话号码并输出
name_search proc
                     xor    ch,ch
                     mov    cl,total
                     mov    si,0

    loop_search:     
                     push   cx
                     push   si
    
                     mov    cx,20                               ;  mov    cl,buffer_len
                     lea    di,buffer_str
                     lea    si,[teltab + si]
                     cld
                     rep    cmpsb
                     pop    si
                     pop    cx
                     je     found_name
                     add    si,30
                     loop   loop_search

    not_find:        
                     lea    dx,not_find_string
                     call   print_str
                     ret

    found_name:      
                     lea    dx,found_string
                     call   print_str
                     lea    dx,tel_head
                     call   print_str
                     mov    cx,30
                     mov    ah,2
    output_char:     
                     mov    dl,[teltab+si]
                     int    21h
                     inc    si
                     loop   output_char
                     ret
name_search endp
    ;buffer_str后面的都填写空格
clear_buffer proc
                     xor    ah,ah
                     mov    al,buffer_len
                     mov    cx, 20
                     sub    cx,ax
                     mov    bx, offset buffer_str + 19
                     mov    al, ' '
    clear_loop:      
                     mov    [bx], al
                     dec    bx
                     loop   clear_loop
                     ret
clear_buffer endp

    ;按名字排序。for(int i=0;i<n-1;i++)//n-1次;for(int j=i+1;j<n;j++)//n-i-1次，cx=n-i
    ;si存外循环偏移量，di存内循环偏移量
sort proc
                     xor    ch,ch
                     mov    cl,total
                     dec    cx
                     cmp    cx,0
                     je     loop1_end
                     mov    si,0
    loop_sort1:      
                     push   cx                                  ;loop1 cx
                     mov    di,si
    loop_sort2:      
                     add    di,30
                     push   cx
                     push   si
                     push   di
                     mov    cx,20
                     lea    si,[teltab+si]
                     lea    di,[teltab+di]
                     cld
                     rep    cmpsb
                     pop    di
                     pop    si
                     jle    sort_continue
                     call   swap_tel
    sort_continue:   
                     pop    cx
                     loop   loop_sort2
    loop2_end:       
                     pop    cx                                  ;loop1 cx
                     add    si,30
                     loop   loop_sort1
    loop1_end:       
                     ret
                     
sort endp
swap_tel proc
                     push   cx
                     push   si
                     push   di
                     mov    cx,28
    swap_loop:       
                     mov    al,[teltab+si]
                     mov    bl,[teltab+di]
                     mov    [teltab+si],bl
                     mov    [teltab+di],al
                     inc    si
                     inc    di
                     loop   swap_loop
                     pop    di
                     pop    si
                     pop    cx
                     ret
swap_tel endp
prognam ends
    end start