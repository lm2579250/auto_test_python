import os, re

pro_dir = os.path.split(os.path.realpath(__file__))[0]
result_path = os.path.join(pro_dir, "result")

print(pro_dir)
print(result_path)
s1 = "d:/Project/a/b/c/d/file.py"
s2 = r"d:\project\a\b\c\d\file.py"
print(os.getcwd())
print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.abspath("/"))

for i in [os.getcwd(), s1, s2]:
    abs_path = os.path.abspath(i).split(os.sep)
    print(os.path.abspath(abs_path[0] + os.sep + abs_path[1]))

# 测试
paths = ['d:\\Project\\', 'home/Python/Project/', 'c:/balabala/Python/Project/']
for path in paths:
    pj_dir = re.match('.*Project', path)
    print(pj_dir.group())

# 在子文件下就应该这样用
# print(re.match('(.*\{sep}Project)\{sep}'.format(sep=os.sep), __file__).group(1))