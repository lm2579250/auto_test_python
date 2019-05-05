import os

DIR1 = r"E:\test\data\1"
DIR2 = r"E:\test\data\2"
# print(len([name for name in os.listdir(DIR1) if os.path.isfile(os.path.join(DIR1, name))]))

# file_array = []
file_list = os.listdir(DIR1)
for file_name in file_list:
    if os.path.splitext(file_name)[1] == ".js":
        # file_array.append(file_name)
        # print(len(file_array))
        # print(file_name)

        file_old = open(r"%s\%s" % (DIR1, file_name), "r", encoding="utf-8")
        file_new = open(r"%s\%s" % (DIR2, file_name), "w", encoding="utf-8")

        lines = file_old.readlines()
        # last_line = lines[-2]

        # print(len(lines))
        i = 0
        for line in lines:
            # print(line)
            if "export default class " in line:
                line = "export default {\n"
            if "static " in line:
                line = line.replace("static ", "")
            if "}" in line and i < len(lines)-1:
                line = line.replace("}", "},")
            file_new.write(line)
            i += 1

        file_old.close()
        file_new.close()
