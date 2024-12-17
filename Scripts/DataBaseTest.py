# -*- coding: utf-8 -*-
# 暂时用普通数据库替代

import sqlite3
import os
import DataStructure as ds
import uuid

def create_connection(db_file):
    """创建一个数据库连接到SQLite数据库"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """创建一个表"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def create_project(conn, project):
    """创建一个新的项目"""
    sql = ''' INSERT INTO projects(name, description)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

#按照DataStructure的格式插入数据
def create_data_structure(conn, data_structure):
    sql = ''' INSERT INTO data_structures(origin_string_data, guid, clean_string_data, placeholder, source_file)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data_structure)
    conn.commit()
    return cur.lastrowid
