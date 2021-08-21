#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 数据持久化  方法名前缀 insert update select delete

# pymysql 用来做数据库操作的

import pymysql


def select_users(uname: str) -> dict:
    r"""
    """
    # 打开数据库连接
    db = pymysql.connect(host="101.34.48.210", user="root",
                         password="Wangweijie123", database="wwj")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    # SQL 插入语句
    sql = """SELECT * FROM `user`"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        data = cursor.fetchall()
        # 把查询的数据填充到person对象是否可以(要循环这个游标进行数据的填充)
        # 可以将查询的数据填充(组合)到自定义的模型中
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()
    return data
