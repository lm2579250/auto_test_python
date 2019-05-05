import random

number = random.randint(0, 100)
guess = -1
answer = 'y'
count = 0

print("\n*****猜字谜游戏*****")

while int(guess) != number and answer == 'y':

    count += 1
    print("********************\n第", count, "次")
    guess = input("请输入你猜的数字（0-100）：\n")

    if guess.isdigit():
        guess = int(guess)
        if guess == number:
            print("恭喜，你猜对了！")
            answer = input("是否继续？(y/n)\n")
            if answer == 'y' or answer != 'n':
                number = random.randint(0,100)
                answer = 'y'
                count = 0
        elif guess < number:
            print("猜的数字小了...")
        elif guess > number:
            print("猜的数字大了...")
    elif guess == 'n':
        guess = -1
        answer = input("是否退出？(y/n)\n")
        if answer == 'y':
            answer = 'n'
        else:
            answer = 'y'
    else:
        print("请输入一个正整数！")
        guess = -1
else:
    print("再见！")