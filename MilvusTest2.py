# -*- coding: utf-8 -*-
import multiprocessing
from sentence_transformers import SentenceTransformer
import pymilvus
import numpy as np
import os
# from EmbeddingModel import emb_text
from tqdm import tqdm
import chardet

# # 加载预训练的 SentenceTransformer 模型，只初始化一次
# model_name = "BAAI/bge-large-zh-v1.5"
# model = SentenceTransformer(model_name)

# def emb_text(text):
#     return model.encode(text)

def main():
    
    # 加载预训练的 SentenceTransformer 模型，只初始化一次
    model_name = "BAAI/bge-large-zh-v1.5"
    model = SentenceTransformer(model_name)
    multiprocessing.freeze_support()
    
    test_embedding = model.encode("This is a test")
    embedding_dim = len(test_embedding)
    
    print(embedding_dim)
    print(test_embedding[:10])

    # 连接Milvus数据库
    milvus_client = pymilvus.MilvusClient(uri='tcp://localhost:19530')
    collection_name = "milvus_test_01"
    # 根据你选用的模型确定向量维度
    dim = embedding_dim
    
    # 检查集合是否存在，如果不存在则创建
    if collection_name not in milvus_client.list_collections():
        milvus_client.create_collection(
            collection_name=collection_name,
            dimension=dim
        )
        
    data = []
    
    #读取本地文档TestFile.txt  设置text_lines
    file_path = "G:/Project/translationOpt/TestFile.txt"
    
    # 检测文件编码
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    print(encoding)
    
    # 然后按照检测出的编码读取文件
    with open(file_path, "r", encoding=encoding) as file:
        text_lines = file.readlines()
    
    for i, line in enumerate(tqdm(text_lines, desc="Creating embeddings")):
        data.append({"id": i, "vector": model.encode(line), "text": line})
    
    milvus_client.insert(collection_name=collection_name, data=data)


if __name__ == "__main__":
    main()