import sys
import re
import jieba
from collections import Counter
import math
# from line_profiler import LineProfiler


# 读取文件函数
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"文件{file_path}未找到，请检查文件路径是否正确。")
        raise
    except PermissionError:
        print(f"没有权限读取文件{file_path}，请检查该文件的权限设置。")
        raise
    except UnicodeError:
        print("文件编码错误，请尝试使用其他编码格式读取。")
        raise
    except IOError:
        print(f"文件{file_path}读取时发生I/O错误，请检查硬盘或文件系统")
        raise
    except Exception as e:
        print(f"读取文件{file_path}发生未知错误：{e}")
        raise
    return text


# 预处理文本函数
def preprocess(text):
    # 初始化 jieba 分词器
    jieba.initialize()  # 提前加载词典，提高首次调用速度
    text_cleaned = re.sub(r'[^\w\s]|\s+', '', text)  # 去除标点符号、换行符和多余的空格
    words = jieba.lcut(text_cleaned, cut_all=False)  # 使用jieba分词，选择精确模式
    return words


# 计算余弦相似度函数
def cosine_similarity(text1, text2):
    # 统计词频
    c1 = Counter(text1)
    c2 = Counter(text2)

    words = set(c1.keys()).union(set(c2.keys()))  # 计算词汇的交集

    # 构造词频向量
    v1 = [c1.get(word, 0) for word in words]
    v2 = [c2.get(word, 0) for word in words]

    # 计算余弦相似度
    dot_product = sum(a * b for a, b in zip(v1, v2))  # 计算点积
    n1 = math.sqrt(sum(a * a for a in v1))  # 计算向量的模
    n2 = math.sqrt(sum(b * b for b in v2))

    if n1 == 0 or n2 == 0:
        return 0.00
    else:
        return dot_product / (n1 * n2)


def main():
    # 从命令行获取参数
    if len(sys.argv) != 4:
        print("用法: python main.py <原文文件路径> <抄袭版文件路径> <输出结果文件路径>")
        return

    original_file = sys.argv[1]
    plagiarized_file = sys.argv[2]
    output_file = sys.argv[3]

    # 读取文件内容
    original_text = read_file(original_file)
    plagiarized_text = read_file(plagiarized_file)

    # 预处理文本，使用jieba分词
    original_words = preprocess(original_text)
    plagiarized_words = preprocess(plagiarized_text)

    # 计算余弦相似度
    similarity = cosine_similarity(original_words, plagiarized_words)

    # 输出结果到答案文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"{similarity:.2f}")


if __name__ == "__main__":
    main()
    # 性能分析代码
    # lp = LineProfiler()
    # lp.add_function(main)
    # lp.add_function(read_file)
    # lp.add_function(preprocess)
    # lp.add_function(cosine_similarity)
    # test_func = lp(main)
    # test_func()
    # lp.print_stats()
