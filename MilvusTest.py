# -*- coding: utf-8 -*-
from sentence_transformers import SentenceTransformer
import pymilvus
import numpy as np
import os


def main(): 
    # 连接Milvus数据库
    milvus_client = pymilvus.MilvusClient(uri='tcp://localhost:19530')
    collection_name = "test_1211"
    # 根据你选用的模型确定向量维度
    dim = 1024  

    # 检查集合是否存在，如果不存在则创建
    if collection_name not in milvus_client.list_collections():
        milvus_client.create_collection(
            collection_name=collection_name,
            dimension=dim
        )

    # 加载预训练的SentenceTransformer模型
    model_name = "BAAI/bge-large-zh-v1.5"  # 中文
    model = SentenceTransformer(model_name)

    # 读取txt文件并向量化
    file_path = "G:/Project/translationOpt/TestFile.txt"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            vectors = []  # 保持为普通列表
            for line in lines:
                line = line.strip()
                vec = model.encode(line)
                vectors.append({"vector": vec.tolist()})  # 将向量转换为字典格式

            # 将向量插入Milvus数据库
            insert_result = milvus_client.insert(
                collection_name=collection_name,
                data=vectors  # 直接传递列表，无需转换为ndarray
            )
            print("插入成功，插入的实体ID:", insert_result.primary_keys)
    else:
        print(f"文件 {file_path} 不存在，请检查文件路径是否正确。")
    
    query = "圣光之裔的成员目前应该都被集中关押在死寂囚牢，这是邪恶虚灵臭名昭著的牢笼，但我们并不清楚它具体在遗忘神域的什么地方。死寂囚牢信件显示，虚灵狱卒身上藏有囚牢路线图。从它们身上夺取囚牢路线图碎片，并将{0}片碎片拼合成完整的囚牢路线图。"
    query_vec = model.encode(query)
    search_param = {
        "nprobe": 16
    }
    search_result = milvus_client.search(
        collection_name=collection_name,
        query_records=[query_vec],
        top_k=5,
        params=search_param
    )
    print("检索结果：", search_result)
    
if __name__ == "__main__":
    # multiprocessing.freeze_support()
    main()