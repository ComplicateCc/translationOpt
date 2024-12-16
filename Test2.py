from difflib import SequenceMatcher

str1 = "噬魂邪使仍在守卫着维系暗魔裂隙能量的上古魔将，赶快与其他军团成员协力击败它！"
str2 = "焚炎兽仍在守卫着维系裂隙能量的上古魔将，赶快与其他军团成员协力击败它！"

# 创建SequenceMatcher对象
matcher = SequenceMatcher(None, str1, str2)

# 获取相似度比例
similarity_ratio = matcher.ratio()
print("相似度比例:", similarity_ratio)

# 获取匹配块信息
matching_blocks = matcher.get_matching_blocks()
print("匹配块信息:")
for block in matching_blocks:
    print(f"在str1中的起始索引: {block.a}，在str2中的起始索引: {block.b}，匹配块长度: {block.size}")
    
    
matcher = SequenceMatcher(None, str1, str2)
similarity_ratio = matcher.ratio()
print(similarity_ratio)