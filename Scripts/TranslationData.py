# -*- coding: utf-8 -*-
# 用于存放翻译数据的数据结构
# string_data 初始数据 用于索引
# translation_data 翻译后数据

class TranslationData:
    def __init__(self, string_data, translation_data):
        self.string_data = string_data
        self.translation_data = translation_data

    def __repr__(self):
        return f"TranslationData(string_data={self.string_data}, translation_data={self.translation_data})"