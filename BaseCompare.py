def compare_and_replace(s1, s2, threshold=5):
    len_diff = abs(len(s1) - len(s2))
    if len_diff > threshold:
        return s1, s2
    # 记录不同部分的区间
    diff_ranges = []
    i = 0
    while i < min(len(s1), len(s2)):
        if s1[i]!= s2[i]:
            start = i
            while i < min(len(s1), len(s2)) and s1[i]!= s2[i]:
                i += 1
            end = i
            diff_ranges.append((start, end))
        else:
            i += 1
    if not diff_ranges:
        return s1
    new_s = s1
    placeholder_index = 0
    for start, end in reversed(diff_ranges):
        different_part = s1[start:end]
        placeholder = "{" + str(placeholder_index) + "}"
        new_s = new_s[:start] + placeholder + new_s[end:]
        placeholder_index += 1
    return new_s

# 示例用法
s1 = "2268560002=我想要第1神火格位、追加等级为10级的救世神耀。"
s2 = "2268560003=我想要第2神火格位、追加等级为10级的救世神耀。"
result = compare_and_replace(s1.split("=")[1], s2.split("=")[1])
print(result)