def fun(a: list) -> tuple:
    """
    :return: 变量名，开始，结束，步长
    """
    s, t, step = 0, 0, 1
    if 'downTo' in a:  # for (i in 2 downTo -2 step 1)，i=2，1，0，-1，-2
        step = -1
        t = a[5]
        s = int(a[3])
    else:
        s, t = a[3].split('..')
        s = int(s)
    if t[-1] == ')':
        t = int(t[:-1])
    else:
        t = int(t)
    # t += step
    if 'step' in a:  # for (i in 0..5 step 2)，i=0，2，4
        step = step * int(a[-1][:-1])
    return a[1][1:], s, t, step


def my_length(s: int, t: int, d: int) -> int:
    return (t - s) // d+1


def my_add(s: int, t: int, d: int) -> int:
    n = my_length(s, t, d)
    return int(d / 2 * n ** 2 + (s - d / 2) * n)


input()
input()
s1 = input().split()
s2 = input().split()
s3 = input().split()
# s3 = input()
input()
input()
a1 = fun(s1)
a2 = fun(s2)
answer = 0

# raise Exception("\n%s\n\t%s\n\t\t%s\n" % (' '.join(s1), ' '.join(s2),s3))
# raise Exception(f"\nfor {a1[0]} in range({a1[1]},{a1[2]},{a1[3]}):\n\tfor {a2[0]} in range({a2[1]},{a2[2]},{a2[3]}):\n{s3}\n")
# # exec(f"for {a1[0]} in range({a1[1]},{a1[2]},{a1[3]}):\n\tfor {a2[0]} in range({a2[1]},{a2[2]},{a2[3]}):\n{s3}\n")
if a1[0] in s3:
    answer = my_add(a1[1], a1[2], a1[3]) * my_length(a2[1], a2[2], a2[3])
elif a2[0] in s3:
    # print(my_length(a1[1], a1[2], a1[3]))
    answer = my_add(a2[1], a2[2], a2[3])*my_length(a1[1], a1[2], a1[3])
# exec("for %s in range(%s,%s,%s):\n\tfor %s in range(%s,%s,%s):\n%s\n" % (
#     a1[0], a1[1], a1[2], a1[3], a2[0], a2[1], a2[2], a2[3], s3))
print(answer)
