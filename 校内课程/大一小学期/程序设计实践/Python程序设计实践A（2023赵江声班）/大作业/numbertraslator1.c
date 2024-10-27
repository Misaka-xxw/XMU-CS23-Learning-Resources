//编码：Character encoding：GB2312。可能会乱码
//LCD自定义字符生成
#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <time.h>
#include <windows.h>
#define w 16//width，改这两个数值改变画布大小，可以当像素画玩
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
    printf("按回车继续");
    gets(name);
    printf("以下是代码，按1重新开始，按其它键退出。\n");
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
    HideCursor();   //隐藏光标
    gotoxy(1, 1);    //回调光标、刷新画面
    for(y=0; y<h; y++) {
        for(x=0; x<w; x++) {
            if(n[y][x]==white)  printf("□");
            else if(n[y][x]==black) printf("■");
            else if(n[y][x]==white_c)  printf("◇");
            else if(n[y][x]==black_c) printf("◆");
        }
        printf("\n");
    }
    printf("画笔坐标：(%d,%d)\n",x0+1,y0+1);
    printf("用法：按wsad控制画笔移动，\n按m画画，按n清除，\n按空格生成LCD自定义字符代码\n");
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
void gotoxy(int x, int y) { //回调光标,参考csdn
    COORD pos;
    pos.X = x - 1;
    pos.Y = y - 1;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), pos);
}
void HideCursor() { //隐藏光标函数,参考csdn
    CONSOLE_CURSOR_INFO cursor;
    cursor.bVisible = FALSE;
    cursor.dwSize = sizeof(cursor);
    HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleCursorInfo(handle, &cursor);
}
void noHideCursor() { //那么就把FALSE改成TRUE! 
    CONSOLE_CURSOR_INFO cursor;
    cursor.bVisible = TRUE;
    cursor.dwSize = sizeof(cursor);
    HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleCursorInfo(handle, &cursor);
}
