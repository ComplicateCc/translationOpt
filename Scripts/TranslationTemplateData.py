# -*- coding: utf-8 -*-
# 用于存放翻译模板的数据结构
# template 翻译模板内容
# clean_str_datas 清洗后的字符串数据的集合
#     每个集合元素
#     clean_str_data 清洗后的字符串数据
#     guids 对应的唯一标识组
#     tag 占位方法标签
# placeholders 占位符集合
#     每个集合元素
#     placeholder 占位符
#     guids 对应的唯一标识组

#初始化数据
class TranslationTemplateData:
    def __init__(self, template, clean_str_datas, placeholders, need_check = False):
        self.template = template
        self.clean_str_datas = clean_str_datas
        self.placeholders = placeholders
        self.need_check = need_check

    def __repr__(self):
        return f"TranslationTemplateData(template={self.template}, clean_str_datas={self.clean_str_datas}, placeholders={self.placeholders}, need_check={self.need_check})"
    
class CleanStrData:
    def __init__(self, clean_str_data, guids):
        self.clean_str_data = clean_str_data
        self.guids = guids

    def __repr__(self):
        return f"CleanStrData(clean_str_data={self.clean_str_data}, guids={self.guids})"