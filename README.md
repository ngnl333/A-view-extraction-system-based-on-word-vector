## Automatically extract the views of people in news articles

这个项目的目标是：



这个项目的具体实现过程是：

用户输入一个新闻网址。例如:https://www.bbc.co.uk/news/uk-england-london-49307088

然后程序会自动读取这个网址里面的内容。

然后程序遍历新闻里面所有的句子。

先把文章分为不同的块。

每一个块中的句向量的值都小于一定的值。这说明这个块中的所有句子都是相关的。

然后遍历这些块。寻找哪些块里面有表示说的同义词。

然后把这些带有说的同义词的块提取出来。变成一个列表。

然后使用工具对这些块进行分析。

分析出是哪个人或者哪个组织发表的言论。

然后生成结果。

如何使用：

首先创建虚拟环境。

install requirements.txt

下载词向量包。

http://nlp.stanford.edu/data/glove.6B.zip

解压到data文件夹。

cd ..\run

python sif_embedding.py

输入一个URL (仅使用过BBC NEWS进行测试)

然后可以得到一个表格。

表格会显示文章中的个人或组织发表的言论。