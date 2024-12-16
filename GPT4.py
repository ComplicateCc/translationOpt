def calculate_similarity(str1, str2):
    # 将字符串转换为集合，去除重复字符
    set1 = set(str1)
    set2 = set(str2)

    # 计算交集和并集
    intersection = set1.intersection(set2)
    union = set1.union(set2)

    # 计算相似度
    intersection_size = len(intersection)
    union_size = len(union)

    # 应用你提供的公式
    if intersection_size + 0.5 * (union_size - intersection_size) > 0:
        similarity = (intersection_size) / (intersection_size + 0.5 * (union_size - intersection_size)) * 100
    else:
        similarity = 100.0  # 如果整体为零，匹配度为100%

    return similarity

# 示例字符串
str1 = "噬魂邪使仍在守卫着维系暗魔裂隙能量的上古魔将，赶快与其他军团成员协力击败它！"
str2 = "焚炎兽仍在守卫着维系裂隙能量的上古魔将，赶快与其他军团成员协力击败它！"

s1 = "2268560002=我想要第1神火格位、追加等级为10级的救世神耀。"
s2 = "2268560003=我想要第2神火格位、追加等级为10级的救世神耀。"

# 计算匹配度
similarity_percentage = calculate_similarity(s1, s2)
print(f"匹配度: {similarity_percentage:.2f}%")