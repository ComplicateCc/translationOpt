import fuzzywuzzy
from fuzzywuzzy import fuzz

str1 = "噬魂邪使仍在守卫着维系暗魔裂隙能量的上古魔将，赶快与其他军团成员协力击败它！"
str2 = "焚炎兽仍在守卫着维系裂隙能量的上古魔将，赶快与其他军团成员协力击败它！"

s1 = "2268560002=我想要第1神火格位、追加等级为10级的救世神耀。"
s2 = "2268560003=我想要第2神火格位、追加等级为10级的救世神耀。"

print(fuzz.ratio(s1,s2))