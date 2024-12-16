# -*- coding: utf-8 -*-
from sentence_transformers import SentenceTransformer

model_name = "BAAI/bge-large-zh-v1.5"
model = SentenceTransformer(model_name)

def emb_text(text):
    return model.encode(text)