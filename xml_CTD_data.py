#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    BioC(XML)格式ConNLL格式
    从 .XML 原始document文件中解析获取训练数据和标签文件

    1、通过offset，将句子中所有的实体用一对标签 <B^>entity<^I> 进行标记
       注意：offset 是在二进制编码下索引的，要对句子进行编码 s=s.encode(‘utf-8’)
    2、对于嵌套实体（offset 相同），仅保留其中长度较长的实体
    3、对句子中的标点符号  !\”#$%‘()*+,-./:;<=>?@[\\]_`{|}~ 进行切分；^ 保留用于实体标签！！
    4、利用GENIA tagger工具对标记过的语料进行分词和词性标注
    5、根据预处理语料的标记 <B^><^I> 获取BIO标签
'''
from xml.dom.minidom import parse
import re
import codecs
import os
from tqdm import tqdm

# def entityReplace(splited_sen, splited_tagged, i, item, sen_length):
#     '''
#     将句子中的实体用<></>标签包裹
#     '''
#     # 1、先处理嵌套实体的问题
#     if B_tag in splited_sen[i] and I_tag in splited_sen[i]:
#         k1 = splited_sen[i].index(B_tag)+4
#         k2 = splited_sen[i].index(I_tag)
#         splited_sen[i] = splited_sen[i][:k1] + item + splited_sen[i][k2:]
#     elif B_tag in splited_sen[i]:
#         k1 = splited_sen[i].index(B_tag)+4
#         splited_sen[i] = splited_sen[i][:k1] + item
#     elif I_tag in splited_sen[i]:
#         k2 = splited_sen[i].index(I_tag)
#         splited_sen[i] = item + splited_sen[i][k2:]
#     else:
#         splited_sen[i] = item
#     # 2、对于嵌入在单词内部的实体，包裹标签后 需要重新调整句子的长度
#     gap = i+1
#     diff = len(splited_tagged) - sen_length    # 标记后的句子与原始句子的长度差
#     while diff:
#         splited_sen.insert(gap, splited_tagged[gap])
#         diff-=1
#         gap+=1


def readXML(files, BioC_PATH):

    for file in files:  #遍历文件夹
        if not os.path.isdir(file):  #判断是否是文件夹，不是文件夹才打开
            f = BioC_PATH + "/" + file
            DOMTree = parse(f) # 使用minidom解析器打开 XML 文档
            collection = DOMTree.documentElement  # 得到了根元素

            # 在集合中获取所有 document
            documents = collection.getElementsByTagName("Row")

            for document in documents:
                doc_id = document.getElementsByTagName("DiseaseID")[0].childNodes[0].data
                if document.getElementsByTagName("Synonyms"):
                    passages = document.getElementsByTagName("Synonyms")[0].childNodes[0].data

                line = doc_id +'\t' +passages

                with codecs.open('train.txt', 'a', encoding='utf-8') as f:
                    f.write(line)
                    f.write('\n')

    text = []

    with codecs.open('train.txt', 'r', encoding='utf-8') as data:
        for line in data:
            t = line.replace('|', '\t')
            text.append(t)

    with codecs.open('train_clean.txt', 'w', encoding='utf-8') as f:
        for b in text:
            f.write(b)

if __name__ == '__main__':

    B_tag = ['B‐^', 'B‐^^']   # '‐' != '-'
    I_tag = ['^‐I', '^^‐I']

    train_path = r'data'
    BioC_PATH = r'../pp'
    files = os.listdir(BioC_PATH)  # 得到文件夹下的所有文件名称
    files.sort()
    
    # Read the original corpus
    readXML(files, BioC_PATH)
