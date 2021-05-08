# -*- coding: utf-8 -*-


"""
采用前向、后向最大匹配算法，基于已经搜集词典进行命名实体标注；
"""


# 设置最大匹配长度，一般是实体最大长度
MAX_LEN = 4
MY_DIC = {"PER": ["张三", "王小明"], "ORG": ["中国移动"]}


# 前向匹配
def forward(text):
    ner_label = []
    len_text = len(text)
    while len_text > 0:
        cur_len = min(len_text, MAX_LEN)
        cur_text = text[:cur_len]
        # 标记是否找到匹配向
        flag = False
        while cur_len > 0:
            # 检查当前长度是否找到
            for label, words in MY_DIC.items():
                if cur_text in words:
                    flag = True
                    ner_label.append("B-{}".format(label))
                    for i in range(cur_len-1):
                        ner_label.append("I-{}".format(label))
                    break
            # 没有找到，缩短长度
            if not flag:
                cur_text = cur_text[:-1]
                cur_len -= 1
            # 已经找到，退出
            if flag:
                text = text[cur_len:]
                len_text = len(text)
                break
        # 如果退出都没有找到，标记“O”，继续向前一步
        if not flag:
            ner_label.append("O")
            text = text[1:]
            len_text = len(text)
    return ner_label


# 后向匹配
def backward(text):
    ner_label = []
    len_text = len(text)
    while len_text > 0:
        cur_len = min(len_text, MAX_LEN)
        cur_text = text[-cur_len:]
        # 标记是否找到匹配向
        flag = False
        while cur_len > 0:
            # 检查当前长度是否找到
            for label, words in MY_DIC.items():
                tmp = []
                if cur_text in words:
                    flag = True
                    tmp.append("B-{}".format(label))
                    for i in range(cur_len - 1):
                        tmp.append("I-{}".format(label))
                    ner_label.extend(tmp[::-1])
                    break
            # 没有找到，缩短长度
            if not flag:
                cur_text = cur_text[1:]
                cur_len -= 1

            # 已经找到，退出
            if flag:
                text = text[:-cur_len]
                len_text = len(text)
                break

        # 如果退出都没有找到，标记“O”，继续向前一步
        if not flag:
            ner_label.append("O")
            text = text[:-1]
            len_text = len(text)

    return ner_label[::-1]


if __name__ == "__main__":
    text = "张三在中国移动工作。"
    res_f = forward(text)
    for t, r in zip(text, res_f):
        print(t, "=>", r)

    print("\n*********\n")

    res_b = backward(text)
    for t, r in zip(text, res_b):
        print(t, "=>", r)