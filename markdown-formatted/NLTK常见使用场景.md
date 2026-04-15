---
title: "分词"
summary: "文本标记化 **nltk.tokenize.word_tokenize(text)**: 将文本分割为单词。 **nltk.tokenize.sent_tokenize(text)**: 将文本分割为句子。 **词性标注** **nltk.pos_tag(words)**: 对给定的单词列表进行词性标注，返回每个单词的词性标签。"
board: "tech"
category: "编程语言-Python"
tags:
  - "NLTK"
  - "Python"
  - "NLP"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

## 文本标记化
+ **nltk.tokenize.word_tokenize(text)**: 将文本分割为单词。
+ **nltk.tokenize.sent_tokenize(text)**: 将文本分割为句子。

```python
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('punkt')  # 下载分词所需的数据

text = "NLTK is a powerful library for natural language processing. It's used in various applications."

# 分词
words = word_tokenize(text)
print("Tokenized Words:", words)

# 句子分割
sentences = sent_tokenize(text)
print("Tokenized Sentences:", sentences)

```


## **词性标注**
+ **nltk.pos_tag(words)**: 对给定的单词列表进行词性标注，返回每个单词的词性标签。

```python
from nltk import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('averaged_perceptron_tagger')  # 下载词性标注所需的数据

text = "NLTK is a powerful library for natural language processing."

# 分词
words = word_tokenize(text)

# 词性标注
pos_tags = pos_tag(words)
print("POS Tags:", pos_tags)

```


## **情感分析**
+ **nltk.sentiment.SentimentIntensityAnalyzer()**: 创建情感分析器的实例。
+ **sia.polarity_scores(text)**: 对文本进行情感分析，返回一个包含情感得分的字典，包括正面、负面和中性情感的分数。

```python
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')  # 下载情感分析所需的数据

text = "NLTK is a fantastic library for NLP. I love using it!"

# 创建情感分析器
sia = SentimentIntensityAnalyzer()

# 获取情感分数
sentiment_scores = sia.polarity_scores(text)

# 输出情感分数
print("Sentiment Scores:", sentiment_scores)

```
