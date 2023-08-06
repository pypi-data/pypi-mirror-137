# -*- coding: UTF-8 -*-
from c2utils.utils import common, time_processing, text_processing
from c2utils.utils.file_processing import FileProcessing
from c2utils.utils.text_processing import text_split
from c2utils.utils.text_segmentation import Segment, load_user_dictionary

print("\033[31m --- 公共方法 ---\033[0m")
print(common.is_chinese_string('科创信息'))
print(common.is_zhs('科创信息'))
print(common.is_number_in_string('科创信息666'))
print(common.extract_numbers('666科创666信息666'))
print(common.clear_all_spaces('a a  a   a    a     a      a       a        a         a          a'))
print(common.clear_all_punctuation(r"""HHHa，b。c、d；e’f【g】h-i=j·k《l》m？n：o“p|q{r}s—t—u+v~w！x@y#z￥A%B…C…D&E*F（G）H,I
.J/K;L'M'N[O]P\Q<R>S?T:U"V"W{X}Y|Z`HHH"""))
print(common.randomly_generate_string(6))

print("\033[31m --- 文本处理 ---\033[0m")
print(text_processing.simple2tradition('科创'))
print(text_processing.tradition2simple('科創'))
print(text_processing.get_homophones_by_char('科'))
print(text_processing.get_homophones_by_pinyin('ke1'))
print(text_processing.pinyin_split('hunankechuangxinxijishugufenyouxiangongsi'))

print("\033[31m --- 分词 ---\033[0m")
segment = Segment()
load_user_dictionary()
print(segment.cut('湖南科创信息技术股份有限公司'))
print(segment.pseg_cut('湖南科创信息技术股份有限公司'))
print(segment.cut_for_search('湖南科创信息技术股份有限公司'))

print("\033[31m --- 时间处理 ---\033[0m")
print(time_processing.get_current_time())
print(time_processing.get_current_date())
print(time_processing.get_yesterday_date())

print("\033[31m --- 文件处理 ---\033[0m")
file_processing = FileProcessing('test_file.txt')
print(file_processing.get_file_size())
print(file_processing.get_file_dir())
print(file_processing.get_file_data_len())
for i in file_processing.read_file_by_line():
    print(text_split(i))
# unzip_file('stopwords-master.zip', 'test_dir')

print("\033[31m --- 科学计算 ---\033[0m")
