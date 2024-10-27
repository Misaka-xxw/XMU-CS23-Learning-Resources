prompt='输入一个数字，我将告诉你，它是奇数，还是偶数'
prompt+='\n输入“结束游戏”，将退出程序：'
exit='结束游戏'
content=""
while content!=exit:
    content=input(prompt)
    if content.isdigit():
        number=int (content)
        if(number%2==0):
            print('该数是偶数')
        else:
            print('该数是奇数')
    elif content!=exit:
        print('输入的必须是数字')