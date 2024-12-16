# -*- coding: utf-8 -*-
import time
from openai import OpenAI
from TranslationOptimization_Prompt import prompt

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # required but ignored
)

instructions = """
"""

test_content = """
听起来挺有意思的。
听起来很有意思。


听说你有事想要寻求帮助？（酒馆委托）
听说你需要帮助？（酒馆委托）


军团名称已存在，创建失败。
角色名称已存在，创建失败。


抱歉此物品已达兑换上限，请明日再尝试兑换吧。
抱歉此物品已达兑换上限，请下一周再尝试兑换吧。
抱歉此物品已达兑换上限，请下个月再尝试兑换吧。


{0}{1}点新魔石，是否选择兑换？
{0}{1}枚恒晶石，是否选择兑换？


你获得了{0}点新魔石！
恭喜你获得{0}点魔石！


道具存在
道具不存在


【{0}】对你释放了神速，你的移动速度增加了50％，持续5秒。
你对【{0}】释放了神速，你和他的移动速度增加了50％，持续5秒。


很抱歉，当前你与大法师崔尔登不在同一区域，还请返回雷鸣大陆后重试。
很抱歉，当前你与时空裂隙不在同一区域，还请返回雷鸣大陆后重试。
很抱歉，当前你与爱德·科洛诺斯不在同一区域，还请返回雷鸣大陆后重试。
很抱歉，当前你与三尾白狐不在同一区域，还请返回雷鸣大陆后重试。
很抱歉，当前你与王者风云榜不在同一区域，还请返回雷鸣大陆后重试。
很抱歉，当前你与妙梦仙灵不在同一区域，还请返回雷鸣大陆后重试。


正在前往黑袍大法师崔尔登所在的位置……
你正前往黑袍大法师崔尔登的所在处……
正在前往大法师崔尔登所在的位置……
你正在前往黑袍大法师崔尔登的所在地……


只有等级达到130级，神等级达到90级且属性评分达到{0}的勇士才能进行挑战。你当前实力不足，无法参与该挑战。
只有等级达到110级，神等级达到70级且属性评分达到{0}的勇士才能进行挑战。你当前实力不足，无法参与该挑战。
只有等级达到120级，神等级达到50级且属性评分达到{0}的勇士才能进行挑战。你当前实力不足，无法参与该挑战。
"""

test_result = """
模板：{0}已存在，创建失败。
军团名称已存在，创建失败。
角色名称已存在，创建失败。

模板：抱歉此物品已达兑换上限，请{0}再尝试兑换吧。
抱歉此物品已达兑换上限，请明日再尝试兑换吧。
抱歉此物品已达兑换上限，请下一周再尝试兑换吧。
抱歉此物品已达兑换上限，请下个月再尝试兑换吧。

模板：当前你与{0}不在同一区域，还请返回雷鸣大陆后重试。
很抱歉，当前你与大法师崔尔登不在同一区域，还请返回雷鸣大陆后重试。
很抱歉，当前你与时空裂隙不在同一区域，还请返回雷鸣大陆后重试。
很抱歉，当前你与爱德·科洛诺斯不在同一区域，还请返回雷鸣大陆后重试。
很抱歉，当前你与三尾白狐不在同一区域，还请返回雷鸣大陆后重试。
很抱歉，当前你与王者风云榜不在同一区域，还请返回雷鸣大陆后重试。
很抱歉，当前你与妙梦仙灵不在同一区域，还请返回雷鸣大陆后重试。

模板：只有等级达到{0}级，神等级达到{1}级且属性评分达到{2}的勇士才能进行挑战。你当前实力不足，无法参与该挑战。
只有等级达到130级，神等级达到90级且属性评分达到{0}的勇士才能进行挑战。你当前实力不足，无法参与该挑战。
只有等级达到110级，神等级达到70级且属性评分达到{0}的勇士才能进行挑战。你当前实力不足，无法参与该挑战。
只有等级达到120级，神等级达到50级且属性评分达到{0}的勇士才能进行挑战。你当前实力不足，无法参与该挑战。
"""

target_content = """
你身上携带的魔石数量不足，无法换购新手超值换购礼，请携带足够的魔石之后再试！
你身上携带的魔石数量不足，无法换购尊享特权，请携带足够的魔石之后再试！
你身上携带的魔石数量不足，无法换购{0}[赠]，请携带足够的魔石之后再试！

未满足条件，不可领取
未满足条件，不可换购

了解女神经验特权详情。
了解神火经验特权详情。
了解双倍经验特权详情。

勇士，你尚未解锁女神系统，无法领取这份成长特权，请先解锁女神系统后再来吧！
勇士，你尚未解锁女神系统，无法换购这份尊享特权，请先解锁女神系统后再来吧！

新手之希翼礼盒提供的女神经验成长特权，每人每天只能领取一次，你今天已经成功领取过了。
新手之希翼礼盒提供的神火经验成长特权，每人每天只能领取一次，你今天已经成功领取过了。
新手之希翼礼盒提供的双倍经验成长特权，每人每天只能领取一次，你今天已经成功领取过了。
新手之希翼礼盒提供的双倍经验尊享特权，每人每天只能换购一次，你今天已经成功换购过了。
新手之希翼礼盒提供的神之祝福成长特权，每人每天只能领取一次，你今天已经成功领取过了。
新手之希翼礼盒提供的传送大师成长特权，每人每天只能领取一次，你今天已经成功领取过了。
新手之希翼礼盒提供的时尚达人成长特权，每人每天只能领取一次，你今天已经成功领取过了。
新手之希翼礼盒提供的幻兽养成成长特权，每人每天只能领取一次，你今天已经成功领取过了。

新手之希翼礼盒提供的女神经验尊享特权，每人仅限换购10次。当前你已换购过10次该特权了，无法再次换购。
新手之希翼礼盒提供的神火经验尊享特权，每人仅限换购10次。当前你已换购过10次该特权了，无法再次换购。

勇士，你尚未飞升成神，无法领取这份成长特权，请先飞升成神后再来吧！
勇士，你尚未飞升成神，无法换购这份尊享特权，请先飞升成神后再来吧！

你从新手之希翼礼盒中获得了1小时双倍经验状态，好好利用吧！
你从新手之希翼礼盒中获得了1小时神之祝福，好好利用吧！

新手之希翼礼盒提供的神之祝福尊享特权，每人仅限换购一次。当前你已换购过了，无法再次换购。
新手之希翼礼盒提供的时尚达人尊享特权，每人仅限换购一次。当前你已换购过了，无法再次换购。
新手之希翼礼盒提供的珍稀跟宠尊享特权，每人仅限换购一次。当前你已换购过了，无法再次换购。
"""

target_content2 = """
当前家族报名人数未满足匹配要求。
当前家族人数未满足玩法要求。

前往击败第一只小Boss
前往击败第二只小Boss
前往击败第三只小Boss
前往击败第四只小Boss

你的物品背包没有足够的空间了，暂时无法获得你的酬劳——1个原初神火箱。请尽快整理出1格的空间后再重新尝试。
你的物品背包没有足够的空间了，暂时无法获得你的酬劳——20个精纯神火碎焰【赠】。请尽快整理出1格的空间后再重新尝试。

恭喜！你获得了1个原初神火箱。
恭喜！你获得了1个烈焰神火箱。
恭喜！你获得了1个遗忘神火箱。

我已经击败了18只虚灵了！
我已经击败了12只虚灵了！

你已成功击败{0}/30只虚灵守卫。
你已成功击败{0}/30只虚灵战士。

入混沌废墟，请你现在就去用诡光宝石开启混沌核心的大门吧！请一定要小心行事，毕竟放
为了尽快进入混沌废墟，请你现在就去用诡光宝石开启混沌核心的大门吧！请一定要

上古的神力似乎还残留在混沌之门上，穿过这道门，后面就是混乱的混沌废墟——混沌核心正是被封印在那里。
古的神力似乎还残留在混沌之门上，穿过这道门，后面就是混乱的混沌废墟——混沌核心正是被封印在那里。

我这就试试合成虚灵水晶。
我明白了，我这就试试合成虚灵水晶。

在与虚灵使徒的战斗中，你已经成功除去了{0}只虚灵使徒！
在与虚灵爪牙的战斗中，你已经成功除去了{0}只虚灵爪牙！

不存在1000079状态
存在1000079状态

{0}对你说：{1}
{0}说：{1}
{0}：{1}

冥魂妖王已被击败！同时，寒冰阵枢的封印之门已经开启，赶快前去击败寒冰妖王吧！
寒冰妖王已被击败！同时，邪焰阵枢的封印之门已经开启，赶快前去击败邪焰妖王吧！
邪焰妖王已被击败！同时，岩魔阵枢的封印之门已经开启，赶快前去击败岩魔妖王吧！
岩魔妖王已被击败！同时，毒影阵枢的封印之门已经开启，赶快前去击败毒影妖王吧！
"""

# 开始计时
start_time = time.time()

#创建对话 打印返回结果
chat_completion = client.chat.completions.create(
    messages=[
        {
            'role': 'user',
            'content': prompt + target_content,
        }
    ],
    model='qwen2.5:7b',
    temperature=0.1  # 设置 temperature 参数，值越低输出越稳定
)

# 结束计时
end_time = time.time()
elapsed_time = end_time - start_time

print(chat_completion.choices[0].message.content)
print(f"请求耗时: {elapsed_time:.2f} 秒")