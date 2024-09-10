"""
1. 读取文件内容
2. 预处理文本
3. 计算词频向量
4. 计算余弦相似度
5. 输出结果
"""
import sys
import re
import jieba


# 读取文件内容函数
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"文件{file_path}未找到，请检查文件路径是否正确。")
    except PermissionError:
        print(f"没有权限读取文件{file_path}，请检查该文件的权限设置。")
    except UnicodeError:
        print("文件编码错误，请尝试使用其他编码格式读取。")
    except IOError:
        print(f"文件{file_path}读取时发生I/O错误，请检查硬盘或文件系统")
    except Exception as e:
        print(f"读取文件{file_path}发生未知错误：{e}")
    return text


# 预处理文本函数
def preprocess(text):
    text = re.sub(r'[^\w\s]', '', text)  # 去除标点符号
    words = jieba.lcut(text, cut_all=False)  # 使用jieba分词，选择精确模式
    return words


def main():
    # 从命令行获取参数
    if len(sys.argv) != 4:
        print("用法: python cnki.py <原文文件路径> <抄袭版文件路径> <输出结果文件路径>")
        return

    original_file = sys.argv[1]
    plagiarized_file = sys.argv[2]
    output_file = sys.argv[3]

    # 读取文件内容
    original_text = read_file(original_file)
    plagiarized_text = read_file(plagiarized_file)
    output_text = read_file(output_file)

    # 预处理文本，使用jieba分词
    original_words = preprocess(original_text)
    plagiarized_words = preprocess(plagiarized_text)

    


if __name__ == "__main__":
    main()
