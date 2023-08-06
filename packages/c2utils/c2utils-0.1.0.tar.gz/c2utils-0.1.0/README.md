# C2 Toolkit

总结了一些可能会在项目中用到的工具（方法）

## 安装

```bash
pip install --upgrade c2utils
```

## 基本使用

### 1. 公共方法

```python
from c2utils.utils import common

print(common.is_chinese_string('科创信息'))
print(common.is_number_in_string('科创信息666'))
print(common.clear_all_spaces('科 创  信   息'))
```

* `calculate_execution_time`: 计算程序执行时间装饰器
* `is_chinese`: 判断一个字符是否是汉字
* `is_chinese_string`: 判断输入文本是否全为汉字
* `is_digit`: 判断输入对象是否是数字
* `is_number_in_string`: 判断文本中是否含有数字
* `extract_numbers`: 提取文本中的数字
* `clear_all_spaces`: 去除文本中的所有空格
* `clear_all_punctuation`: 去除文本中的标点符号
* `is_alphabet`: 判断一个字符是否是英文字母
* `is_alphabet_string`: 判断输入文本是否全是英文
* `randomly_generate_string`: 随机生成n位字符串
* `extract_text_through_re`: 通过正则表达式抽取文本
* `ReadConfig`: 读取配置文件类

### 2. 文本处理

```python
from c2utils.utils import text_processing

print(text_processing.simple2tradition('科创'))
print(text_processing.tradition2simple('科創'))
print(text_processing.get_homophones_by_char('科'))
print(text_processing.get_homophones_by_pinyin('ke1'))
print(text_processing.pinyin_split('hunankechuangxinxijishugufenyouxiangongsi'))
```

* `simple2tradition`: 将简体转换成繁体
* `tradition2simple`: 将繁体转换成简体
* `get_homophones_by_char`: 根据汉字取同音字
* `get_homophones_by_pinyin`: 根据拼音取同音字
* `chinese2pinyin`: 中文文本转拼音
* `pinyin_split`: 拼音分割
* `text_split`: 文本分割（分句）

### 3. 分词

```python
from c2utils.utils.text_segmentation import Segment, load_user_dictionary

segment = Segment('baidu_stopwords.txt')  # 默认使用百度停用词
load_user_dictionary('user_dict.txt')  # 加载用户词典
print(segment.cut('湖南科创信息技术股份有限公司'))
print(segment.pseg_cut('湖南科创信息技术股份有限公司'))
print(segment.cut_for_search('湖南科创信息技术股份有限公司'))
```

* `segment.cut`: jieba分词
* `segment.pseg_cut`: 词性标注
* `segment.cut_for_search`: 搜索引擎模式
* `segment.extract_keywords_through_tfidf`: 关键词抽取（TF-IDF）
* `segment.extract_keywords_through_text_rank`: 关键词抽取（TextRank）

### 4. 时间处理

```python
from c2utils.utils import time_processing

print(time_processing.get_current_time())
print(time_processing.get_current_date())
```

* `date2timestamp_s`: 日期时间转换成秒级时间戳
* `date2timestamp`: 日期时间转换成毫秒级时间戳
* `timestamp2date`: 时间戳转换为指定格式的日期
* `get_current_time`: 获取当前日期时间
* `get_current_date`: 获取当前日期
* `get_yesterday_date`: 获取昨天日期
* `get_current_timestamp_s`: 获取当前日期时间对应的时间戳（秒级）
* `get_current_timestamp_ms`: 获取当前日期时间对应的时间戳（毫秒级）

### 5. 文件处理

```python
from c2utils.utils.file_processing import FileProcessing

file_processing = FileProcessing('file.txt')
print(file_processing.get_file_size())
print(file_processing.get_file_dir())
print(file_processing.get_file_data_len())
for line in file_processing.read_file_by_line():
    print(line)
```

* `file_processing.read_all_data`: 一次读取整个文件
* `file_processing.read_file_by_line`: 按行读取，去掉行尾换行符
* `file_processing.write_file_all`: 写入数据到文件
* `file_processing.check_file_exist`: 检查文件是否存在
* `file_processing.get_file_data_len`: 获取文件总行数
* `file_processing.get_file_dir`: 获取文件所在目录
* `file_processing.get_file_size`: 获取文件大小
* `check_file_contents`: 比较两个文件内容是否一致
* `print_file_directory_tree`: 打印文件目录树
* `unzip_file`: zip文件解压
* `save_pickle`: 保存成pickle文件
* `load_pickle`: 读取pickle文件
* `save_json`: 保存成json文件
* `load_json`: 加载json文件

### 6. 科学计算

```python
from c2utils.utils import calculation

```

## TODO

* `科学计算模块`
* `预处理模块`
