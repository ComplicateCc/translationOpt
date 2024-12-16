# -*- coding: utf-8 -*-
import multiprocessing
from sentence_transformers import SentenceTransformer
import pymilvus
import numpy as np
import os
# from EmbeddingModel import emb_text
from tqdm import tqdm
import chardet

# # ����Ԥѵ���� SentenceTransformer ģ�ͣ�ֻ��ʼ��һ��
# model_name = "BAAI/bge-large-zh-v1.5"
# model = SentenceTransformer(model_name)

# def emb_text(text):
#     return model.encode(text)

def main():
    
    # ����Ԥѵ���� SentenceTransformer ģ�ͣ�ֻ��ʼ��һ��
    model_name = "BAAI/bge-large-zh-v1.5"
    model = SentenceTransformer(model_name)
    multiprocessing.freeze_support()
    
    test_embedding = model.encode("This is a test")
    embedding_dim = len(test_embedding)
    
    print(embedding_dim)
    print(test_embedding[:10])

    # ����Milvus���ݿ�
    milvus_client = pymilvus.MilvusClient(uri='tcp://localhost:19530')
    collection_name = "milvus_test_01"
    # ������ѡ�õ�ģ��ȷ������ά��
    dim = embedding_dim
    
    # ��鼯���Ƿ���ڣ�����������򴴽�
    if collection_name not in milvus_client.list_collections():
        milvus_client.create_collection(
            collection_name=collection_name,
            dimension=dim
        )
        
    data = []
    
    #��ȡ�����ĵ�TestFile.txt  ����text_lines
    file_path = "G:/Project/translationOpt/TestFile.txt"
    
    # ����ļ�����
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    print(encoding)
    
    # Ȼ���ռ����ı����ȡ�ļ�
    with open(file_path, "r", encoding=encoding) as file:
        text_lines = file.readlines()
    
    for i, line in enumerate(tqdm(text_lines, desc="Creating embeddings")):
        data.append({"id": i, "vector": model.encode(line), "text": line})
    
    milvus_client.insert(collection_name=collection_name, data=data)


if __name__ == "__main__":
    main()