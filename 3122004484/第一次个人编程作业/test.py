import unittest
from unittest.mock import patch
# 从main.py中导入要测试的函数
from main import read_file, preprocess, cosine_similarity, main


class TestMain(unittest.TestCase):

    # 测试读取文件函数
    def test_read_file(self):
        # 模拟文件内容
        file_path = 'test_file.txt'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("测试读取文件函数")

        # 测试文件存在的情况
        result = read_file(file_path)
        self.assertEqual(result, "测试读取文件函数")

        # 测试文件不存在情况
        with self.assertRaises(FileNotFoundError):
            read_file('non_existent_file.txt')

        # 模拟权限错误
        with patch("builtins.open", side_effect=PermissionError):
            with self.assertRaises(PermissionError):
                read_file('permission_error.txt')

        # 模拟文件编码错误
        with patch("builtins.open", side_effect=UnicodeError):
            with self.assertRaises(UnicodeError):
                read_file('encoding_error.txt')

        # 模拟 I/O 错误
        with patch("builtins.open", side_effect=IOError("I/O 错误")):
            with self.assertRaises(IOError):
                read_file('io_error.txt')

        # 测试未知错误
        with patch("builtins.open", side_effect=Exception("未知错误")):
            with self.assertRaises(Exception):
                read_file('unknown_error.txt')

    # 测试预处理文本函数
    def test_preprocess(self):
        text = "测试一下！\n这个，函数。"
        expected_result = ['测试', '一下', '这个', '函数']
        result = preprocess(text)
        print(result)
        self.assertEqual(result, expected_result)

    # 测试计算余弦相似度函数
    def test_cosine_similarity(self):
        # 测试部分相同的文本
        text1 = ['测试', '函数', '运行']
        text2 = ['测试', '函数', '成功']
        expected_similarity = 0.6667
        result = cosine_similarity(text1, text2)
        self.assertAlmostEqual(result, expected_similarity, places=4)

        # 测试完全不同的文本
        text3 = ['不同', '内容']
        expected_similarity = 0.0
        result = cosine_similarity(text1, text3)
        self.assertAlmostEqual(result, expected_similarity)

        # 测试完全相同的文本
        text4 = text1
        expected_similarity = 1.0
        result = cosine_similarity(text1, text4)
        self.assertAlmostEqual(result, expected_similarity)


if __name__ == '__main__':
    unittest.main()
