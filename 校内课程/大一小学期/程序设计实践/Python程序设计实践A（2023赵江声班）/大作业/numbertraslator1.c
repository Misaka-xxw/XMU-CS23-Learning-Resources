//���룺Character encoding��GB2312�����ܻ�����
//LCD�Զ����ַ�����
#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <time.h>
#include <windows.h>
#define w 16//width������������ֵ�ı仭����С�����Ե����ػ���
#define h 16//height
#define  white    0
#define  black    1
#define  white_c  2//white_current
#define  black_c  3//black_current
void newpicture();
void show();
void UpdateInput();
void result();
void gotoxy(int x, int y);
void HideCursor() ;
void noHideCursor();

int x0,y0;
int n[h][w];
int isOver=1;
char name[100];
int main() {
start:
    newpicture();
    while(isOver) {
        UpdateInput();
        show();
        Sleep(100);
    }
    noHideCursor();
    printf("���س�����");
    gets(name);
    printf("�����Ǵ��룬��1���¿�ʼ�����������˳���\n");
    result();
    while(1) {
        if (kbhit()) {
            if (GetKeyState('1')<0){
			}
            else return 0;
        }
    }
}
void newpicture() {
    int x,y;
    isOver=1;
    for(y=0; y<h; y++) {
        for(x=0; x<w; x++) {
            n[y][x]=white;
        }
    }
    x0=0;
    y0=0;
    n[y0][x0]=white_c;
}
void show() {
    int x,y;
    HideCursor();   //���ع��
    gotoxy(1, 1);    //�ص���ꡢˢ�»���
    for(y=0; y<h; y++) {
        for(x=0; x<w; x++) {
            if(n[y][x]==white)  printf("��");
            else if(n[y][x]==black) printf("��");
            else if(n[y][x]==white_c)  printf("��");
            else if(n[y][x]==black_c) printf("��");
        }
        printf("\n");
    }
    printf("�������꣺(%d,%d)\n",x0+1,y0+1);
    printf("�÷�����wsad���ƻ����ƶ���\n��m��������n�����\n���ո�����LCD�Զ����ַ�����\n");
}
void UpdateInput() {
    char key_up=GetKeyState('W'),
         key_down=GetKeyState('S'),
         key_left=GetKeyState('A'),
         key_right=GetKeyState('D'),
         key_draw=GetKeyState('M'),
         key_clear=GetKeyState('N'),
         key_space=GetKeyState(32);
    if (kbhit()) {
        if (key_up < 0) {
            if(y0>0) {
                n[y0][x0]-=2;
                n[--y0][x0]+=2;
            }
        }
        if (key_down < 0) {
            if(y0<h-1) {
                n[y0][x0]-=2;
                n[++y0][x0]+=2;
            }
        }
        if (key_left < 0) {
            if(x0>0) {
                n[y0][x0]-=2;
                n[y0][--x0]+=2;
            }
        }
        if (key_right < 0) {
            if(x0<w-1) {
                n[y0][x0]-=2;
                n[y0][++x0]+=2;
            }
        }
        if (key_draw < 0) {
            if(n[y0][x0]==white_c) n[y0][x0]+=1;
            //n[y0][x0]=5-n[y0][x0];
        }
        if (key_clear < 0) {
            if(n[y0][x0]==black_c) n[y0][x0]-=1;
            //n[y0][x0]=5-n[y0][x0];
        }
        if (key_space < 0) {
            isOver=0;
        }
    }
}
void result() {
    int x,y;
    for(y=0; y<h; y++) {
        printf("(");
        for(x=0; x<w; x++) {
            printf("%d",n[y][x]%2);
        }
        if(y<h-1) {
            printf(",");
        }
        printf("\n");
    }
    printf("};\n");
}
void gotoxy(int x, int y) { //�ص����,�ο�csdn
    COORD pos;
    pos.X = x - 1;
    pos.Y = y - 1;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), pos);
}
void HideCursor() { //���ع�꺯��,�ο�csdn
    CONSOLE_CURSOR_INFO cursor;
    cursor.bVisible = FALSE;
    cursor.dwSize = sizeof(cursor);
    HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleCursorInfo(handle, &cursor);
}
void noHideCursor() { //��ô�Ͱ�FALSE�ĳ�TRUE! 
    CONSOLE_CURSOR_INFO cursor;
    cursor.bVisible = TRUE;
    cursor.dwSize = sizeof(cursor);
    HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleCursorInfo(handle, &cursor);
}
