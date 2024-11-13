;p17 rank
datarea segment
    grade   dw 88,75,95,63,98,78,87,73,90,60
    rank    dw 10 dup(?)
datarea ends
;*********************************************
;ax存储外循环的成绩
;cx存储内循环的次数
;dx存储排名
;si存储外循环的指针
;di存储内循环的指针
prognam segment
main proc far
             assume cs:prognam, ds:datarea,es:datarea
    start:   
             push   ds
             sub    ax,ax
             push   ax

             mov    ax,datarea
             mov    ds,ax
             mov    es,ax
    ;模板
             mov    di,10                                ;目的变址寄存器放进循环次数10
             mov    bx,0                                 ;基址寄存器放上0
    loops:   
             mov    ax,grade[bx]                         ;第bx名学生的成绩
             mov    dx,0                                 ;名次
             mov    cx,10                                ;内循环10次
             lea    si,grade                             ;加载成绩到源变址寄存器
    next:    
             cmp    ax,[si]                              ;比较已存的成绩和源变址寄存器中的成绩
             jg     no_count                             ;大于的话跳转no_count，即排名不往后推一名
             inc    dx                                   ;dx++
    no_count:
             add    si,2                                 ;源变址寄存器+=2，即跳转到下一位进行比较
             loop   next                                 ;cx不为0时，继续小循环比较
             mov    rank[bx],dx                          ;和最后一个同学比完，成绩里记录dx排名
             add    bx,2                                 ;后一位同学进行操作
             dec    di                                   ;di--
             jne    loops                                ;ZF不为0，继续跳转；否则开始输出
    ;以十进制形式输出
             mov    cx,10
             lea    si,rank
             mov    bl,10
    ;ret
             
             
    twototen:
             mov    ax,[si]                              ;放要输出的成绩
             div    bl                                   ;除以10，除数和余数分别存在ah和al
             add    al,30h
             add    ah,30h
             mov    dx,ax
             mov    ah,02h
             int    21h
             mov    dl,dh
             int    21h
             mov    dl,20h
             int    21h
             add    si,2
             loop   twototen
             mov    dl,0dh
             int    21h
             mov    dl,0ah
             int    21h
             ret
    
             
main endp
prognam ends
    end start



