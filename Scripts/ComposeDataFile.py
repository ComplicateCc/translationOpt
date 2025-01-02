# -*- coding: utf-8 -*-


import json

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

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CleanStrData):
            return {
                'clean_str_data': obj.clean_str_data,
                'guids': list(obj.guids)
            }
        if isinstance(obj, TranslationTemplateData):
            return {
                'template': obj.template,
                'clean_str_datas': [self.default(data) for data in obj.clean_str_datas],
                'placeholders': list(obj.placeholders)
            }
        return json.JSONEncoder.default(self, obj)

# decode json
def decode_json(data):
    if 'clean_str_data' in data:
        return CleanStrData(data['clean_str_data'], set(data['guids']))
    if 'template' in data:
        return TranslationTemplateData(data['template'], [decode_json(data) for data in data['clean_str_datas']], set(data['placeholders']))

json_path = r'G:\Project\TranslationOptimization\Files\TranslationTemplateData.json'

# 解析 json_path下的json文件 解析成TranslationTemplateData对象
def parse_json():
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f, object_hook=decode_json)
    # 打印解析结果
    print(data)
    return data

