# nmf-tipe

## Introduction
This project has been realized in 2012-2013 for the TIPE, a test in the competitive exam of the Ecole Normale Supérieure.
My subject was "The Non-negative Matrix Factorization algorithm", and was my first real contact with machine learning, and Python.

I reproduced the first expriments of Daniel D. Lee and H Sebastian Seung with the NMF algorithm : I first used the algorithm on faces pictures, using the same dataset than the authors. Then, I have reproduced the experiment they have done on a dictionnary dataset, but on the french version of wikipedia. This raised a lot of problem of big data manipulation, since the whole dataset's size was 8Go, and I was running the whole procedure on a small laptop.

This project was mainly a great way to learn Python, and some basics in machine learning. I have recoded as many thing as I could, trying not to use some machine learning libraries, because this was for a competitive exam, and I had to prove I was able to do it. This code is far from being optimal in speed.

The report I have done for this exam is in `report.pdf`. Some of the results are plotted there.

The best article to read about NMF : 
http://www.nature.com/nature/journal/v401/n6755/pdf/401788a0.pdf

## How it works

`ioFiles.py` is reading the dataset, parsing the file using ElementTree to be able to stream the file, since it can't be loaded entirely, parsing the texts (using some functions of `treatWiki.py`), and the stored version of the Wikipedia articles are some arrays of words.
The dataset is separed into a hundred of files, in order to be computed easily.

We then build the array of word, counting how many times a word is appearing in a article. This is done in `textStat.py`.

We delete a list of words which are supposed to be not significant, and then keep only the 10,000 most frequent words.
We also keep only the 10,000 longest articles (in term of number of words), supposing that they are the less noisy).

We run the NMF algorithm (in `nmf.py`)

Then, we plot the data by constructing some dendrograms of the articles.
