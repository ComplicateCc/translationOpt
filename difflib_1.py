from difflib import SequenceMatcher

def get_different_with_placeholder(str1, str2):
    s = SequenceMatcher(None, str1, str2)
    parts = []
    last_j = 0
    holder_index = 0
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            parts.append(str2[j1:j2])
        else:
            placeholder = "{" + str(holder_index) + "}"
            holder_index += 1
            parts.append(placeholder)
    return "".join(parts)

str1 = "噬魂邪使仍在守卫着维系暗魔裂隙能量的上古魔将，赶快与其他军团成员协力击败它！"
str2 = "焚炎兽仍在守卫着维系裂隙能量的上古魔将，赶快与其他军团成员协力击败它！"

s1 = "2268560003=我想要第1神火格位、追加等级为10级的救世神耀。"
s2 = "2268560003=我想要第2神火格位、追加等级为10级的救世神耀。"

result = get_different_with_placeholder(str1, str2)
print(result)