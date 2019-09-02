## Automatically extract the views of people in news articles

#### version 0.2

The objectives of this project are:

Extraction of views of people or organizations in the news

The specific implementation process of this project is:

The user enters a news URL. E.g:https://www.bbc.co.uk/news/uk-england-london-49307088

The program will automatically read the contents of this URL and traverse all the sentences in the news.

Divide the article into different blocks. The value of the sentence vector in each block is less than a certain value. This means that all the sentences in this block are related.

Then iterate through the blocks. Look for which blocks have synonyms for 'said'.

Then extract these blocks with the synonym of 'said'.

Analyze these blocks.

Then generate the result.

how to use:

First create a virtual environment.

install requirements.txt

Download the word vector package.

http://nlp.stanford.edu/data/glove.6B.zip

Unzip to the data folder.

cd ..\run

python sif_embedding.py

Enter a URL (any news site article is fine)

Then you can get a form.

The table shows the views published by people or organizations in the article.

