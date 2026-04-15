---
title: "NLTK 自然语言处理完全指南"
summary: "NLTK 自然语言处理完全指南 目录 1. NLTK 简介 2. 安装和配置 3. 基本功能 4. 高级功能 5. 实战案例 6. 常见问题 NLTK 简介 1.1 什么是 NLTK NLTK 代表自然语言工具包（Natural Language Toolkit）。它是一个用于处理人类语言数据的 Python 库，提供了许多工具和资源，"
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

# NLTK 自然语言处理完全指南

## 目录

- [1. NLTK 简介](#1-nltk-简介)
- [2. 安装和配置](#2-安装和配置)
- [3. 基本功能](#3-基本功能)
- [4. 高级功能](#4-高级功能)
- [5. 实战案例](#5-实战案例)
- [6. 常见问题](#6-常见问题)

## 1. NLTK 简介

### 1.1 什么是 NLTK

NLTK 代表自然语言工具包（Natural Language Toolkit）。它是一个用于处理人类语言数据的 Python 库，提供了许多工具和资源，用于在文本数据中进行自然语言处理（NLP）的任务。

NLTK 包括各种模块和类，用于标记化、词干提取、词性标注、分块、解析、语料库管理等。它还包含用于学习和教育目的的语言处理教材和语料库。由于其灵活性和丰富的功能，NLTK 在研究、教育和开发 NLP 应用程序方面都得到了广泛使用。

### 1.2 主要特点

- **丰富的语料库**：包含超过 50 个语料库和词汇资源
- **文本处理工具**：分词、词性标注、命名实体识别等
- **分类和聚类**：支持多种机器学习算法
- **语义推理**：支持语义分析和推理
- **易于学习**：提供详细的文档和教程
- **开源免费**：Apache 2.0 许可证

### 1.3 在什么情况下可以使用 NLTK

NLTK（Natural Language Toolkit）在许多自然语言处理（NLP）任务中都是有用的，包括但不限于以下情况：

1. **文本处理和标记化**：NLTK 提供了用于文本标记化和处理的工具，可以将文本拆分为单词、句子等。
2. **词干提取和词形还原**：对于文本处理，有时需要将单词还原为其基本形式。NLTK 包含用于词干提取和词形还原的模块。
3. **词性标注**：NLTK 允许你对文本中的单词进行词性标注，即确定单词是名词、动词、形容词等。
4. **句法分析**：NLTK 包括一些句法分析器，用于分析句子的结构，包括短语结构和依存关系分析。
5. **情感分析**：在情感分析任务中，NLTK 的工具可以用来确定文本中的情感极性，即文本表达的是正面、负面还是中性情感。
6. **语料库管理**：NLTK 提供了一些常用的语料库，用于训练和测试 NLP 模型。这些语料库可用于研究和开发 NLP 算法。
7. **机器学习和分类**：NLTK 与机器学习库（如 Scikit-Learn）结合使用，以构建文本分类器，用于将文本分为不同的类别。
8. **信息检索**：NLTK 可以用于构建文本搜索引擎或进行信息检索任务。

## 2. 安装和配置

### 2.1 安装 NLTK

```bash
# 使用 pip 安装
pip install nltk

# 或使用 conda 安装
conda install -c anaconda nltk

# 安装特定版本
pip install nltk==3.8.1

# 升级到最新版本
pip install --upgrade nltk
```

### 2.2 下载 NLTK 数据包

NLTK 需要下载额外的数据包才能使用完整功能。

```python
import nltk

# 方式一：交互式下载（推荐初学者）
nltk.download()

# 方式二：下载所有数据包（约 3.5GB）
nltk.download('all')

# 方式三：下载常用数据包
nltk.download('popular')

# 方式四：下载特定数据包
nltk.download('punkt')          # 分词器
nltk.download('averaged_perceptron_tagger')  # 词性标注器
nltk.download('maxent_ne_chunker')  # 命名实体识别
nltk.download('words')          # 英文词汇表
nltk.download('stopwords')      # 停用词
nltk.download('wordnet')        # WordNet 词汇数据库
nltk.download('vader_lexicon')  # 情感分析词典
nltk.download('brown')          # Brown 语料库
nltk.download('reuters')        # Reuters 语料库
```

### 2.3 验证安装

```python
import nltk

# 查看 NLTK 版本
print(nltk.__version__)

# 查看数据包路径
print(nltk.data.path)

# 测试基本功能
from nltk.tokenize import word_tokenize
text = "Hello, world! This is NLTK."
tokens = word_tokenize(text)
print(tokens)
# 输出: ['Hello', ',', 'world', '!', 'This', 'is', 'NLTK', '.']
```

### 2.4 配置数据包路径

```python
import nltk

# 添加自定义数据包路径
nltk.data.path.append('/custom/path/to/nltk_data')

# 查看当前路径
print(nltk.data.path)
```

## 3. 基本功能

### 3.1 文本标记化（Tokenization）

#### 句子分割

```python
from nltk.tokenize import sent_tokenize

text = "Hello world. This is NLTK. It's great for NLP!"
sentences = sent_tokenize(text)
print(sentences)
# 输出: ['Hello world.', 'This is NLTK.', "It's great for NLP!"]

# 中文句子分割（需要额外配置）
chinese_text = "你好世界。这是NLTK。它很适合NLP！"
chinese_sentences = sent_tokenize(chinese_text, language='chinese')
print(chinese_sentences)
```

#### 单词分割

```python
from nltk.tokenize import word_tokenize, wordpunct_tokenize

text = "Hello, world! This is NLTK."

# 标准分词
tokens = word_tokenize(text)
print(tokens)
# 输出: ['Hello', ',', 'world', '!', 'This', 'is', 'NLTK', '.']

# 按标点符号分词
tokens = wordpunct_tokenize(text)
print(tokens)
# 输出: ['Hello', ',', 'world', '!', 'This', 'is', 'NLTK', '.']
```

#### 正则表达式分词

```python
from nltk.tokenize import RegexpTokenizer

# 只保留字母和数字
tokenizer = RegexpTokenizer(r'\w+')
text = "Hello, world! This is NLTK 2024."
tokens = tokenizer.tokenize(text)
print(tokens)
# 输出: ['Hello', 'world', 'This', 'is', 'NLTK', '2024']
```

### 3.2 词干提取（Stemming）

词干提取是将单词还原为词根形式的过程。

```python
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer

# Porter Stemmer（最常用）
porter = PorterStemmer()
words = ["running", "runs", "ran", "runner", "easily", "fairly"]
stems = [porter.stem(word) for word in words]
print(stems)
# 输出: ['run', 'run', 'ran', 'runner', 'easili', 'fairli']

# Lancaster Stemmer（更激进）
lancaster = LancasterStemmer()
stems = [lancaster.stem(word) for word in words]
print(stems)
# 输出: ['run', 'run', 'ran', 'run', 'easy', 'fair']

# Snowball Stemmer（支持多语言）
snowball = SnowballStemmer('english')
stems = [snowball.stem(word) for word in words]
print(stems)
# 输出: ['run', 'run', 'ran', 'runner', 'easili', 'fair']
```

### 3.3 词形还原（Lemmatization）

词形还原比词干提取更准确，会考虑词性。

```python
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# 默认作为名词处理
print(lemmatizer.lemmatize("running"))  # running
print(lemmatizer.lemmatize("runs"))     # run

# 指定词性
print(lemmatizer.lemmatize("running", pos='v'))  # run
print(lemmatizer.lemmatize("better", pos='a'))   # good
print(lemmatizer.lemmatize("worst", pos='a'))    # bad

# 批量处理
words = ["running", "runs", "ran", "easily", "fairly"]
lemmas = [lemmatizer.lemmatize(word, pos='v') for word in words]
print(lemmas)
# 输出: ['run', 'run', 'run', 'easily', 'fairly']
```

### 3.4 停用词过滤

停用词是在文本处理中通常被过滤掉的常见词（如 "the", "is", "at" 等）。

```python
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# 获取英文停用词
stop_words = set(stopwords.words('english'))
print(f"停用词数量: {len(stop_words)}")
print(f"部分停用词: {list(stop_words)[:10]}")

# 过滤停用词
text = "This is a sample sentence showing off stop word filtration."
tokens = word_tokenize(text.lower())
filtered_tokens = [word for word in tokens if word not in stop_words]
print(f"原始: {tokens}")
print(f"过滤后: {filtered_tokens}")
# 输出: ['sample', 'sentence', 'showing', 'stop', 'word', 'filtration', '.']

# 其他语言的停用词
print(stopwords.fileids())  # 查看支持的语言
chinese_stop_words = set(stopwords.words('chinese'))
```

### 3.5 词性标注（POS Tagging）

词性标注是为每个单词标注其词性（名词、动词、形容词等）。

```python
from nltk import pos_tag
from nltk.tokenize import word_tokenize

text = "NLTK is a leading platform for building Python programs."
tokens = word_tokenize(text)
pos_tags = pos_tag(tokens)
print(pos_tags)
# 输出: [('NLTK', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('leading', 'VBG'), ...]

# 词性标签说明
# NN: 名词单数
# NNS: 名词复数
# NNP: 专有名词单数
# VB: 动词原形
# VBD: 动词过去式
# VBG: 动词现在分词
# VBN: 动词过去分词
# JJ: 形容词
# RB: 副词
# DT: 限定词
```

### 3.6 命名实体识别（NER）

命名实体识别用于识别文本中的人名、地名、组织名等。

```python
from nltk import ne_chunk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

text = "Apple Inc. is located in Cupertino, California. Tim Cook is the CEO."
tokens = word_tokenize(text)
pos_tags = pos_tag(tokens)
named_entities = ne_chunk(pos_tags)

print(named_entities)

# 提取命名实体
for chunk in named_entities:
    if hasattr(chunk, 'label'):
        print(f"{chunk.label()}: {' '.join(c[0] for c in chunk)}")
# 输出:
# ORGANIZATION: Apple Inc.
# GPE: Cupertino
# GPE: California
# PERSON: Tim Cook
```

### 3.7 频率分布

```python
from nltk import FreqDist
from nltk.tokenize import word_tokenize

text = "This is a sample text. This text is for testing. Testing is important."
tokens = word_tokenize(text.lower())

# 计算词频
freq_dist = FreqDist(tokens)

# 最常见的词
print(freq_dist.most_common(5))
# 输出: [('is', 3), ('.', 3), ('this', 2), ('text', 2), ('testing', 2)]

# 特定词的频率
print(freq_dist['is'])  # 3

# 绘制频率分布图
freq_dist.plot(10, cumulative=False)
```

## 4. 高级功能

### 4.1 情感分析

```python
from nltk.sentiment import SentimentIntensityAnalyzer

# 创建情感分析器
sia = SentimentIntensityAnalyzer()

# 分析情感
texts = [
    "I love this product! It's amazing!",
    "This is terrible. I hate it.",
    "It's okay, nothing special.",
    "Absolutely fantastic! Best purchase ever!"
]

for text in texts:
    scores = sia.polarity_scores(text)
    print(f"Text: {text}")
    print(f"Scores: {scores}")
    print(f"Sentiment: {'Positive' if scores['compound'] > 0.05 else 'Negative' if scores['compound']  {label}")

# 查看最有信息量的特征
classifier.show_most_informative_features(5)
```

### 4.3 N-gram 分析

```python
from nltk import ngrams
from nltk.tokenize import word_tokenize

text = "Natural language processing is fascinating"
tokens = word_tokenize(text)

# Bigrams (2-grams)
bigrams = list(ngrams(tokens, 2))
print("Bigrams:", bigrams)
# 输出: [('Natural', 'language'), ('language', 'processing'), ...]

# Trigrams (3-grams)
trigrams = list(ngrams(tokens, 3))
print("Trigrams:", trigrams)
# 输出: [('Natural', 'language', 'processing'), ...]

# 使用 FreqDist 统计 N-gram 频率
from nltk import FreqDist
bigram_freq = FreqDist(bigrams)
print(bigram_freq.most_common(5))
```

### 4.4 词汇相似度

```python
from nltk.corpus import wordnet

# 获取单词的同义词集
synsets = wordnet.synsets('dog')
print(f"'dog' 的同义词集: {synsets}")

# 获取定义
for syn in synsets[:3]:
    print(f"{syn.name()}: {syn.definition()}")
    print(f"例句: {syn.examples()}")

# 计算词汇相似度
word1 = wordnet.synset('dog.n.01')
word2 = wordnet.synset('cat.n.01')
word3 = wordnet.synset('car.n.01')

print(f"dog vs cat: {word1.path_similarity(word2)}")  # 0.2
print(f"dog vs car: {word1.path_similarity(word3)}")  # 0.07

# 获取上位词（更一般的概念）
print(f"dog 的上位词: {word1.hypernyms()}")

# 获取下位词（更具体的概念）
print(f"dog 的下位词: {word1.hyponyms()[:5]}")
```

### 4.5 句法分析

```python
from nltk import CFG
from nltk.parse import ChartParser

# 定义上下文无关文法
grammar = CFG.fromstring("""
    S -> NP VP
    NP -> Det N | Det N PP
    VP -> V NP | V NP PP
    PP -> P NP
    Det -> 'the' | 'a'
    N -> 'dog' | 'cat' | 'park'
    V -> 'chased' | 'sat'
    P -> 'in' | 'on'
""")

# 创建解析器
parser = ChartParser(grammar)

# 解析句子
sentence = "the dog chased a cat in the park".split()
for tree in parser.parse(sentence):
    print(tree)
    tree.draw()  # 绘制句法树
```

### 4.6 文本相似度

```python
from nltk.metrics import edit_distance
from nltk.tokenize import word_tokenize

# 编辑距离（Levenshtein 距离）
word1 = "kitten"
word2 = "sitting"
distance = edit_distance(word1, word2)
print(f"编辑距离: {distance}")  # 3

# 余弦相似度
from nltk import FreqDist
from math import sqrt

def cosine_similarity(text1, text2):
    # 分词
    tokens1 = word_tokenize(text1.lower())
    tokens2 = word_tokenize(text2.lower())
    
    # 计算词频
    freq1 = FreqDist(tokens1)
    freq2 = FreqDist(tokens2)
    
    # 获取所有词汇
    all_words = set(freq1.keys()) | set(freq2.keys())
    
    # 计算向量
    vec1 = [freq1[word] for word in all_words]
    vec2 = [freq2[word] for word in all_words]
    
    # 计算余弦相似度
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sqrt(sum(a * a for a in vec1))
    magnitude2 = sqrt(sum(b * b for b in vec2))
    
    return dot_product / (magnitude1 * magnitude2)

text1 = "I love natural language processing"
text2 = "I enjoy NLP and machine learning"
similarity = cosine_similarity(text1, text2)
print(f"余弦相似度: {similarity:.4f}")
```

## 5. 实战案例

### 5.1 文本清洗和预处理

```python
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

def preprocess_text(text):
    """完整的文本预处理流程"""
    # 1. 转小写
    text = text.lower()
    
    # 2. 分词
    tokens = word_tokenize(text)
    
    # 3. 去除标点符号
    tokens = [word for word in tokens if word not in string.punctuation]
    
    # 4. 去除停用词
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # 5. 词形还原
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # 6. 去除数字
    tokens = [word for word in tokens if not word.isdigit()]
    
    # 7. 去除短词（长度 = 3]
    
    return tokens

# 测试
text = "This is a sample text! It contains 123 numbers and punctuation..."
cleaned = preprocess_text(text)
print(f"原始: {text}")
print(f"清洗后: {cleaned}")
# 输出: ['sample', 'text', 'contains', 'number', 'punctuation']
```

### 5.2 关键词提取

```python
from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

def extract_keywords(text, top_n=10):
    """提取文本中的关键词"""
    # 预处理
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # 计算词频
    freq_dist = FreqDist(tokens)
    
    # 返回最常见的词
    return freq_dist.most_common(top_n)

# 测试
text = """
Natural language processing (NLP) is a subfield of linguistics, computer science, 
and artificial intelligence concerned with the interactions between computers and 
human language, in particular how to program computers to process and analyze 
large amounts of natural language data.
"""

keywords = extract_keywords(text, top_n=5)
print("关键词:")
for word, freq in keywords:
    print(f"  {word}: {freq}")
```

### 5.3 文本摘要

```python
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
import string

def summarize_text(text, num_sentences=3):
    """生成文本摘要"""
    # 分句
    sentences = sent_tokenize(text)
    
    # 分词并计算词频
    words = word_tokenize(text.lower())
    words = [word for word in words if word not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    freq_dist = FreqDist(words)
    
    # 计算句子得分
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in freq_dist:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = freq_dist[word]
                else:
                    sentence_scores[sentence] += freq_dist[word]
    
    # 选择得分最高的句子
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    
    # 按原文顺序排列
    summary = [s for s in sentences if s in summary_sentences]
    
    return ' '.join(summary)

# 测试
text = """
Artificial intelligence (AI) is intelligence demonstrated by machines, 
in contrast to the natural intelligence displayed by humans and animals. 
Leading AI textbooks define the field as the study of "intelligent agents": 
any device that perceives its environment and takes actions that maximize 
its chance of successfully achieving its goals. Colloquially, the term 
"artificial intelligence" is often used to describe machines that mimic 
"cognitive" functions that humans associate with the human mind, such as 
"learning" and "problem solving".
"""

summary = summarize_text(text, num_sentences=2)
print("摘要:")
print(summary)
```

### 5.4 垃圾邮件分类器

```python
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def extract_features(text):
    """提取邮件特征"""
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    return {word: True for word in words}

# 训练数据
train_data = [
    ("Win a free iPhone now!", "spam"),
    ("Congratulations! You've won $1000", "spam"),
    ("Click here for amazing deals", "spam"),
    ("Meeting scheduled for tomorrow at 3pm", "ham"),
    ("Can you review this document?", "ham"),
    ("Lunch plans for today?", "ham"),
    ("Get rich quick! Limited time offer!", "spam"),
    ("Project deadline reminder", "ham")
]

# 训练分类器
train_set = [(extract_features(text), label) for text, label in train_data]
classifier = NaiveBayesClassifier.train(train_set)

# 测试
test_emails = [
    "Free money! Click now!",
    "Meeting notes from yesterday",
    "You've won a prize!"
]

print("邮件分类结果:")
for email in test_emails:
    features = extract_features(email)
    label = classifier.classify(features)
    print(f"  {email[:30]}... -> {label}")

# 显示最有信息量的特征
print("\n最有信息量的特征:")
classifier.show_most_informative_features(5)
```

### 5.5 聊天机器人

```python
from nltk.chat.util import Chat, reflections

# 定义对话模式
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, how can I help you today?",]
    ],
    [
        r"hi|hello|hey",
        ["Hello!", "Hi there!", "Hey! How can I help you?"]
    ],
    [
        r"what is your name?",
        ["I am a chatbot created with NLTK.", "You can call me NLTK Bot."]
    ],
    [
        r"how are you?",
        ["I'm doing well, thank you!", "I'm great! How about you?"]
    ],
    [
        r"(.*) (weather|temperature) (.*)",
        ["I'm sorry, I don't have access to weather information.",]
    ],
    [
        r"quit",
        ["Goodbye! Have a great day!", "Bye! Come back soon!"]
    ],
    [
        r"(.*)",
        ["I'm not sure I understand. Can you rephrase that?",
         "Interesting. Tell me more.",
         "I see. What else would you like to know?"]
    ]
]

# 创建聊天机器人
chatbot = Chat(pairs, reflections)

# 开始对话
print("Chatbot: Hi! I'm a simple chatbot. Type 'quit' to exit.")
chatbot.converse()
```

## 6. 常见问题

### 6.1 下载数据包失败

**问题**：执行 `nltk.download()` 时连接超时或失败。

**解决方案**：

```python
# 方法1：手动指定下载路径
import nltk
nltk.download('punkt', download_dir='/custom/path')

# 方法2：使用代理
import nltk
nltk.set_proxy('http://proxy.example.com:8080')
nltk.download('punkt')

# 方法3：手动下载并解压到 nltk_data 目录
# 下载地址: https://github.com/nltk/nltk_data
# 解压到: ~/nltk_data/ (Linux/Mac) 或 C:\nltk_data\ (Windows)
```

### 6.2 中文处理

**问题**：NLTK 对中文支持不够好。

**解决方案**：

```python
# 使用 jieba 进行中文分词
import jieba

text = "自然语言处理是人工智能的重要分支"
words = jieba.cut(text)
print(list(words))
# 输出: ['自然语言', '处理', '是', '人工智能', '的', '重要', '分支']

# 结合 NLTK 进行后续处理
from nltk import FreqDist
freq_dist = FreqDist(words)
print(freq_dist.most_common(5))
```

### 6.3 性能优化

**问题**：处理大量文本时速度慢。

**解决方案**：

```python
# 1. 使用生成器而不是列表
def process_large_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            tokens = word_tokenize(line)
            yield tokens

# 2. 使用多进程
from multiprocessing import Pool
from nltk.tokenize import word_tokenize

def tokenize_text(text):
    return word_tokenize(text)

texts = ["text1", "text2", "text3", ...]
with Pool(4) as pool:
    results = pool.map(tokenize_text, texts)

# 3. 缓存结果
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_tokenize(text):
    return word_tokenize(text)
```

### 6.4 内存不足

**问题**：处理大型语料库时内存不足。

**解决方案**：

```python
# 1. 分批处理
def process_in_batches(texts, batch_size=1000):
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        # 处理批次
        yield process_batch(batch)

# 2. 使用 NLTK 的 LazyCorpusLoader
from nltk.corpus import brown
# brown 语料库是延迟加载的，不会一次性加载到内存

# 3. 使用生成器
def read_large_corpus(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()
```

### 6.5 词性标注不准确

**问题**：默认的词性标注器准确率不够。

**解决方案**：

```python
# 使用更准确的标注器（需要训练）
from nltk.tag import PerceptronTagger
from nltk.corpus import brown

# 训练自定义标注器
train_sents = brown.tagged_sents(categories='news')[:10000]
tagger = PerceptronTagger(load=False)
tagger.train(train_sents)

# 使用自定义标注器
text = "This is a test sentence"
tokens = word_tokenize(text)
tags = tagger.tag(tokens)
print(tags)
```

## 参考资源

- [NLTK 官方网站](https://www.nltk.org/)
- [NLTK 官方文档](https://www.nltk.org/api/nltk.html)
- [NLTK Book](https://www.nltk.org/book/)
- [NLTK GitHub](https://github.com/nltk/nltk)
- [NLTK 数据包下载](https://github.com/nltk/nltk_data)

## 推荐学习路径

1. **入门阶段**
   - 学习基本的文本处理（分词、词干提取、词形还原）
   - 掌握停用词过滤和词频统计
   - 练习简单的文本清洗

2. **进阶阶段**
   - 学习词性标注和命名实体识别
   - 掌握情感分析和文本分类
   - 了解 N-gram 和词汇相似度

3. **高级阶段**
   - 学习句法分析和语义分析
   - 构建完整的 NLP 应用（聊天机器人、文本摘要等）
   - 结合机器学习库（如 Scikit-Learn）进行深度学习

4. **实战项目**
   - 垃圾邮件分类器
   - 情感分析系统
   - 文本摘要生成器
   - 问答系统
   - 聊天机器人
