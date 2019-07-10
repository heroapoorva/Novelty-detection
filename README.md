# Motivation

The idea of the project is to use news article gathered from the web to calculate novelty of a news article compared to a set of news article and do even more analysis such as outlier detection, classification based on keywords, comparing classification techniques for news articles.

# Details
Novelty detection for news articles can be thought of as how different a news article is compared to a set of news article(s). This will be formalized shortly. A news article is assumed to have 4 fields/ keys; text, title, url, dop. Novelty detection is going to use the text of a news article and not the title or date of publishing (dop) or the url of the news article.

### Frequency Vector
Given the corpus of news article keep a dictionary of the words which appear in the corpus. Now this will be used to create a vector for the text field of each news article. The vector represent how many times a particular word appears in the news article. This vector for every news article will be of equal length. So this vector represents the news article in a n-dimensional space. This vector notation is used for novelty detection.

### Frequency matrix
It is possible to get a vector any given news article, hence it is easy to create a matrix of vectors representing a set of news article. This matirx of vectors is used to compare against a given vector(news). As each news has a date (dop), for a given time frame get all the news article and create the matrix which is then used to calculate the novelty of the next news article just outside the time frame. Slide this window and calculate novelty for each news article for a given time frame(window size)

### Calculating novelty from a given frequency matrix and a frequency vector.
Use the frequency matrix to get a TF-IDF matrix. Each row in this TF-IDF matrix still represents a news article but with a certain weight. Calculate the dot product of the frequency vector with each vector in the TF-IDF matrix, these dot product represent the novelty value of a news for a given time frame, we say the news article whose TF-IDF vector has the highest dot product with the frequency vector is the most similar news article and vice versa.

### Changes/Tweaks
        - It is not required to use all words in the corpus to create a vector, it is fine to use top k words. Experiment with different k values.
        - The vector produced via this method is a sparse one, can use dimensionality reduction to perhaps improve the results.
        - The dot product used is simple 1 metric, use any other metric.
        - Try out different window size.

## Outlier Detection
Calculate the novelty values of news articles just of a particular company. These values can provide insight towards the situation of the company and how to it represented in the news.

### Keywords
Reaching this part of the project, it is possible to implement a sliding window novelty detection algorithm for a given data set and for a given window size. The goal now is to filter out news articles based on certain keywords, by checking if they appear in the title of the news article and using sliding window novelty detection on this subset. 

### Data Analysis
Using our algorithm in part 1(Novelty Calculation) we end up an array of novelty values for different keywords/categories. Use these set of values to run different types of analysis, such as outlier detection, correlation, etc. 

### Changes/Tweaks
        - Try various filtering methods.
        - Try various keywords.
        - Try various tests on the novelty values.

## Classification
Using the filter it is possible to gather subset of news articles for a particular keyword from a set of news articles. With this it is possible to train a classifier to predict which category a news article belongs.

### Training classfier
At this point this step is quite straight forward as we just create a TF-IDF matrix for news article, their labels are also given. Pass this into a classfier to train. 

### Testing and Cross-Validation
This is a crucial step, use a k-fold cross validation to obtain an optimal model. 

### Performance measures
Calculate performance  measures such as Precision, Recall, Specificity for different classifiers.

### Changes/Tweaks
        - Use different classification algorithms
        - Try different prior
        
# Implementation

# Execution
The execution will take place in 5 steps:

        - `cleaning` - Making the news data json parseable.
        - `dictionary` - extracting the dictionary of words from the corpus.
        - `novelty calculation` - Calculating novelty values given news articles.
        - `outlier detection` - Doing various analysis on the novelty values for certain keywords.
        - `classification` - Use ML techniques to predict 

The step can be run regardless of the previous steps, provided the input for the given step is provided in proper format as stated.

## Input format

### Cleaning
The input for this step should be
1. A json file, which contains the news articles. 
2. The output file.

The json news articles must have these 4 keys:

        - `text` - The text of the news article.
        - `title` - The title of the news article.
        - `url` - The urls from where the news article was gathered.
        - `dop` - The date of publishing of the news article.

The output of this step is a cleaned the data, i.e  json parseable file, removed stopwords, converted everything to smaller case, lemmatized.

### Dictionary
The input to this step should be
1. A json parseable file with cleaning done.
2. The output file.

The json news articles must have these 4 keys:

        - `text` - The text of the news article.
        - `title` - The title of the news article.
        - `url` - The urls from where the news article was gathered.
        - `dop` - The date of publishing of the news article.
        
The output of this step is a json object(a dictionary) which contains all the words appearing in the corpus and how many time they appear in the corpus. 

### Novelty Detection
The input to this step should be 
1. Json parseable file with cleaning done with the 4 keys
2. A dictionary of all the words and their number of occurance in the json file, as another json file
3. A number indicating the number of topwords which should be used.
4. The output file.

The output of this step is an array of novelty values.

### Outlier Detection
The input to this step should be 
1. Json parseable file with cleaning done with the 4 keys
2. A dictionary of all the words and their number of occurance in the json file, as another json file
3. A number indicating the number of topwords which should be used.
4. A file containing the keywords for filtering

The output of this step is an array of arrays of novelty values. Each array contains novelty values for a keyword based on the window size.

### Classification
The input to this step should be 
1. Json parseable file with cleaning done with the 4 keys.
2. A dictionary of all the words and their number of occurance in the json file, as another json file
3. A number indicating the number of topwords which should be used.
4. A file containing the keywords for filtering.
5. Another Json parseable file with cleaning done with the 4 keys for prediction.

The output of this step is the classification of each news article based on the prediction.

# Results
This section is about results for the dataset I am using.

# Further work
