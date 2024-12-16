# pip install sentence-transformers
# -*- coding: utf-8 -*-
import numpy as np
import multiprocessing

from sentence_transformers import SentenceTransformer
from numpy import dot
from numpy.linalg import norm


def cos_sim(a, b):
    """余弦距离 -- 越大越相似"""
    return dot(a, b) / (norm(a) * norm(b))


def l2(a, b):
    """欧氏距离 -- 越小越相似"""
    x = np.asarray(a) - np.asarray(b)
    return norm(x)


def main():
    # model_name = "BAAI/bge-large-zh-v1.5"  # 中文
    # model_name = 'moka-ai/m3e-base'  # 中英双语，但效果一般
    # model_name = 'BAAI/bge-m3' # 多语言，但效果一般
    model_name = "BAAI/bge-large-zh-v1.5"  # 中文
    model = SentenceTransformer(model_name)


    query = "凝聚全身的斗气，对敌人发动致命的八连斩，每击造成$$$%魔法伤害，并有[@$$$+$$$@]%几率触发处决宣判，对敌人造成额外$$$%魔法伤害。"
    # query = "global conflicts"

    documents = [
    "凝聚全身的斗气，对敌人发动致命的八连斩，每击造成$$$%物理伤害，并有[@$$$+$$$@]%几率触发处决宣判，对敌人造成额外$$$%物理伤害。",
    "凝聚全身的斗气，对敌人发动致命的八连斩，每击造成$$$%物理伤害，并有$$$%几率触发处决宣判，对敌人造成额外$$$%物理伤害。",
    "凝聚全身的斗气，对敌人发动致命的八连斩，每击造成$$$%物理伤害，并有[@$$$+$$$@]%几率触发处决宣判，对敌人造成额外$$$%物理伤害。触发处决宣判时必然暴击。\n[/$$$X$$$ff$$$]（已领悟神性天赋·无双）",
    "凝聚全身的斗气，对敌人发动致命的八连斩，每击造成$$$%物理伤害，并有$$$%几率触发处决宣判，对敌人造成额外$$$%物理伤害。触发处决宣判时必然暴击。\n[/$$$X$$$ff$$$]（已领悟神性天赋·无双）",
    ]

    query_vec = model.encode(query)
    print("query_vec的维度：", query_vec.shape)

    doc_vecs = [model.encode(doc) for doc in documents]

    print("Cosine distance:")  # 越大越相似
    # print(cos_sim(query_vec, query_vec))
    for vec in doc_vecs:
        print(cos_sim(query_vec, vec))


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
