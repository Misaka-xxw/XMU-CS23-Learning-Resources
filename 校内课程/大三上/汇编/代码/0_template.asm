;模板
datarea segment
datarea ends
prognam segment
            assume cs:prognam,ds:datarea,es:datarea
main proc far
    start:  
            push   ds
            sub    ax,ax
            push   ax
            mov    ax,datarea
            mov    ds,ax
            mov    es,ax
    ;...
            ret
main endp
prognam ends
    end start