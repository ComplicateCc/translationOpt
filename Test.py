# -*- coding: utf-8 -*-
import os
from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer
import numpy as np

def main():
    client = MilvusClient(uri='tcp://localhost:19530')
    collection_name = "test_1211_01"

    # 读取txt文件并向量化
    file_path = "G:/Project/translationOpt/TestFile.txt"
    
    docs = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                docs.append(line)
                print(line)
    else:
        print(f"文件 {file_path} 不存在，请检查文件路径是否正确。")

    # 加载预训练的 SentenceTransformer 模型
    model_name = "BAAI/bge-large-zh-v1.5"  # 中文模型
    model = SentenceTransformer(model_name)

    # vectors = [[ np.random.uniform(-1, 1) for _ in range(384) ] for _ in range(len(docs)) ]
    vectors = [model.encode(doc) for doc in docs]
    
    data = [ {"id": i, "vector": vectors[i], "text": docs[i], "subject": "history"} for i in range(len(vectors)) ]
    res = client.insert(
        collection_name="demo_collection",
        data=data
    )
    
    # 查询的句子
    query = "圣光之裔的成员目前应该都被集中关押在死寂囚牢，这是邪恶虚灵臭名昭著的牢笼，但我们并不清楚它具体在遗忘神域的什么地方。死寂囚牢信件显示，虚灵狱卒身上藏有囚牢路线图。从它们身上夺取囚牢路线图碎片，并将{0}片碎片拼合成完整的囚牢路线图。"
    query_vec = model.encode(query).tolist()  # 转换为列表
    # search_param = {
    #     "nprobe": 16
    # }
    search_result = pymilvus.Collection(collection_name).search(
        data=[query_vec],
        anns_field="vector_field",
        # param=search_param,
        limit=5
    )
    print("检索结果：", search_result)

    # # This will exclude any text in "history" subject despite close to the query vector.
    # res = client.search(
    #     collection_name="demo_collection",
    #     data=[vectors[0]],
    #     filter="subject == 'history'",
    #     limit=2,
    #     output_fields=["text", "subject"],
    # )
    # print(res)

    # # a query that retrieves all entities matching filter expressions.
    # res = client.query(
    #     collection_name="demo_collection",
    #     filter="subject == 'history'",
    #     output_fields=["text", "subject"],
    # )
    # print(res)

    # # delete
    # res = client.delete(
    #     collection_name="demo_collection",
    #     filter="subject == 'history'",
    # )
    # print(res)
    
if __name__ == "__main__":
    # main()
    str = """\n【Ⅹ阶橙品】\n【功能说明】\n·镶嵌装备\n·融合更高阶宝石\n·每件装备仅可镶嵌$$$份该宝石。\n\n【圣装传奇】\n 我通常不会用“信赖感”去形容珠宝，但这颗金黄色的家伙相当值得信赖。\n\n    ——宝石评鉴册
匠造·人物魔防"""
    print(str.replace("\n", ""))