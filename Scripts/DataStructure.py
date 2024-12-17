# -*- coding: utf-8 -*-
# origin_string_data 初始数据 用于索引
# guid 唯一标识符
# clean_string_data 清洗后的数据 删除富文本格式和换行符等符号
# placeholder 占位符
# source_file 来源文件名称

class DataStructure:
    def __init__(self, origin_string_data, guid, clean_string_data, placeholder, source_file = None):
        self.origin_string_data = origin_string_data
        self.guid = guid
        self.clean_string_data = clean_string_data
        self.placeholder = set(placeholder)
        self.source_file = source_file

    def __repr__(self):
        return f"DataStructure(origin_string_data={self.origin_string_data}, guid={self.guid}, clean_string_data={self.clean_string_data}, placeholder={self.placeholder}, source_file={self.source_file})"