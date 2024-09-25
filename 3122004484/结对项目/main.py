import argparse
import random
from fractions import Fraction
import re
from typing import Union


# 解析命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description="自动生成小学四则运算题目的命令行程序") # 为程序生成的帮助信息添加描述
    parser.add_argument("-n", type=int, help="生成题目的数量") # 添加必须的整型参数-n
    parser.add_argument("-r", type=int, help="数值范围（自然数、真分数和真分数分母的范围）") # 添加必须的整型参数-r
    parser.add_argument("-e", type=str, help="题目文件路径") # 添加参数-e
    parser.add_argument("-a", type=str, help="答案文件路径") # 添加参数-a
    args = parser.parse_args()

    # 判断是否输入参数-r
    if args.n and not args.r:
        print("请输入数值范围！")

    # 验证参数合理性
    if args.n and args.n < 0:
        print("题目数量必须为正数！")
        exit(1)
    if args.r and args.r < 0:
        print("数值范围必须为正数！")
        exit(1)
    return args


# 随机生成自然数或真分数
def generate_number(max_range):
    # 随机生成自然数或分数
    if random.choice([True, False]):
        # 生成自然数
        return random.randint(1, max_range - 1)
    else:
        # 生成分数
        numerator = random.randint(1, max_range - 1)
        denominator = random.randint(1, max_range - 1)
        return Fraction(numerator, denominator)


# 生成四则运算表达式
def generate_expression(max_range):
    operators = ['+', '-', '*', '/'] # 定义可选运算符

    # 定义布尔标志用于判断左右括号是否生成
    left_flag = False
    right_flag = False

    expression = str(generate_number(max_range)) # 随机生成第一个数

    # 随机生成左括号
    if random.choice([True, False]):
        expression = "(" + expression
        left_flag = True

    # 随机循环1~3次，生成剩余的运算符和数字
    for _ in range(random.randint(1, 3)):
        op = random.choice(operators)
        num = generate_number(max_range)

        # 如果没有左括号，则再随机生成左括号
        if not left_flag and random.choice([True, False]):
            expression += f" {op} ({num}"
            left_flag = True
        # 如果有左括号没有右括号，则生成右括号
        elif left_flag and not right_flag:
            expression += f" {op} {num})"
            right_flag = left_flag = False
        else:
            expression += f" {op} {num}"

    # 如果最后有左括号没右括号，则生成右括号
    if left_flag and not right_flag:
        expression = expression + ")"

    # 去除无意义的括号
    if expression[0] == '(' and expression[-1] == ')':# 去除整个式子给括号括起来的情况
        expression = expression.replace('(', '').replace(')', '')
    expression = re.sub(r'\((\d+|\d+/\d+)\)', r'\1', expression) # 去除单个数字给括号括起来的情况
    return expression


# 格式化分数
def format_fraction(fraction: Union[Fraction, re.Match]):
    if isinstance(fraction, re.Match):
        fraction = Fraction(fraction.group(0))
    if fraction.denominator == 1:
        return str(fraction.numerator)  # 如果分母为1，则返回整数
    elif fraction.numerator > fraction.denominator:
        whole_number = fraction.numerator // fraction.denominator
        remainder = fraction.numerator % fraction.denominator
        return f"{whole_number}'{remainder}/{fraction.denominator}"  # 返回带整数部分的真分数
    else:
        return f"{fraction.numerator}/{fraction.denominator}"  # 返回真分数


# 生成题目文件和答案文件
def generate_exercises(n, r):
    exercises = []
    answers = []

    while n > 0:
        expression = generate_expression(r)
        try:
            answer = eval(expression)  # 计算表达式答案
        except ZeroDivisionError:
            continue
        if answer < 0:
            continue
        fraction_answer = Fraction(answer).limit_denominator() # 将答案转化为分数并限制分母，避免失真
        format_answer = format_fraction(fraction_answer)

        if format_answer not in answers:  # 避免重复题目
            exercises.append(expression)
            answers.append(format_answer)
            n = n - 1

    # 将题目和答案写入文件
    with open("Exercises.txt", "w", encoding='utf-8') as f_ex, open("Answers.txt", "w", encoding='utf-8') as f_ans:
        for idx, ex in enumerate(exercises, 1):
            ex = re.sub(r'\d+/\d+', format_fraction, ex) # 将表达式中的分数格式化
            ex = ex.replace('*', '×').replace(' / ', ' ÷ ') # 将 * 替换为 ×，/ 替换为 ÷
            f_ex.write(f"{idx}. {ex} = \n")
            f_ans.write(f"{idx}. {answers[idx - 1]}\n")



# 判卷功能
def grade_exercises(exercise_file, answer_file):
    with open(exercise_file, "r") as f_ex, open(answer_file, "r") as f_ans:
        exercises = f_ex.readlines()
        answers = f_ans.readlines()

    correct = []
    wrong = []

    for idx, (ex, ans) in enumerate(zip(exercises, answers), 1):
        # 使用 enumerate 和 zip 同时遍历 exercises 和 answers，idx 从 1 开始
        ex_ans = re.search(r'=(.*)', ex).group(1).strip() # 提取用户答案
        ans_ans = re.search(r'\d+\.(.*)', ans).group(1).strip()  # 提取正确答案

        if ex_ans == ans_ans:
            correct.append(idx)
        else:
            wrong.append(idx)

    # 输出成绩
    with open("Grade.txt", "w") as f_grade:
        f_grade.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        f_grade.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")


# 主程序
def main():
    args = parse_args()

    if args.n and args.r:
        generate_exercises(args.n, args.r)
    if args.e and args.a:
        grade_exercises(args.e, args.a)


if __name__ == "__main__":
    main()
