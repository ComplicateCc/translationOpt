# -*- coding: utf-8 -*-
import multiprocessing
import time
import pymilvus
from sentence_transformers import SentenceTransformer
import json

import json
import multiprocessing
from sentence_transformers import SentenceTransformer
import pymilvus


def main():
    # 开始计时
    start_time = time.time()
    
    # 加载预训练的 SentenceTransformer 模型，只初始化一次
    model_name = "BAAI/bge-large-zh-v1.5"
    model = SentenceTransformer(model_name)
    multiprocessing.freeze_support()
    
    # 结束计时
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"加载预训练的 SentenceTransformer 模型耗时: {elapsed_time:.4f} 秒")
    

    # 开始计时
    start_time = time.time()

    # 连接Milvus数据库
    milvus_client = pymilvus.MilvusClient(uri='tcp://localhost:19530')
    collection_name = "milvus_test_01"
    # 根据你选用的模型确定向量维度
    dim = 1024
    
    # 结束计时
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"连接Milvus数据库耗时: {elapsed_time:.4f} 秒")


    # 开始计时
    start_time = time.time()
    
    query = "圣光之裔的成员目前应该都被集中关押在死寂囚牢，这是邪恶虚灵臭名昭著的牢笼，你要寻找到有用的线索。"

    search_res = milvus_client.search(
        collection_name=collection_name,
        data=[model.encode(query)],  # Use the `emb_text` function to convert the question to an embedding vector
        limit=10,  # 修改为5，返回最接近的5条结果
        # # search_params={"metric_type": "IP", "params": {}},  # Inner product distance
        output_fields=["text"],  # Return the text field
    )
    
    # 结束计时
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"查询据库耗时: {elapsed_time:.4f} 秒")

    retrieved_lines_with_distances = [
        (res["entity"]["text"], res["distance"]) for res in search_res[0]
    ]
    print(json.dumps(retrieved_lines_with_distances, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()