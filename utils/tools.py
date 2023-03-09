

class Tool(object):

    @staticmethod
    def str_to_list(line: str) -> list:

        lvl = 1
        i = 0
        length = len(line)

        # 获取级别
        while i < (length - 4):
            if line[i] == '\t':
                i += 1
                lvl += 1
            elif line[i:i + 4] == "    ":
                i += 4
                lvl += 1
            else:
                break

        # 处理字符串
        line = line.strip('\n \t')
        # 获取页码
        i = len(line) - 1
        while line[i] != ' ' and line[i] != '\t':
            i -= 1

        page = line[i + 1:].strip('\n \t')

        title = line[0:i].strip('\n \t')

        return [lvl, title, page]