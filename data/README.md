# Dataset
Please download the data files from [this tSpace file directory](https://tspace.web.att.com/communities/service/html/communityview?communityUuid=fb400868-b17c-44d8-8b63-b445d26a0be4#fullpageWidgetId=W403a0d6f86de_45aa_8b67_c52cf90fca16&folder=8c4ff1ee-8eb8-4584-8c22-3018a24cdf54).

At a minimum, you will need these files...
- `reviews_Office_Products_10.json.gz` - contains the reviews for a category of Amazon products
- `meta_Office_Products.json.gz` - contains product metadata for a category of Amazon products


# Core Tasks

The data for this workshop was built on a number of ardously collected and maintained data sources.  If you use this data in other tutorials or experiments, you should follow the respective authors' requests to include paper citations.


## Amazon Product Reviews

* Primary textual description - http://jmcauley.ucsd.edu/data/amazon/index.html
* Paper Citations

"""
R. He, J. McAuley. "Modeling the visual evolution of fashion trends with one-class collaborative filtering." WWW, 2016
J. McAuley, C. Targett, J. Shi, A. van den Hengel. "Image-based recommendations on styles and substitutes". SIGIR, 2015
"""

* We also downloaded the metadata from the same site.  It is strongly recommended to grab the pre-partitioned sets of data instead of the full draw, which may be GBs.

* Primary Reviews for Amazon Office Products - http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Office_Products_10.json.gz
* Primary Metadata for Amazon Office Products - http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/meta_Office_Products.json.gz

## Sentiment Classification
Sentiment models help to assign a numerical sentiment for mood, emotion, intent, etc. to text, images, etc.  In this workshop, we use a sentiment model to process the textual columns of our data in hopes of getting additional insights that improve our overall review prediction service.

In the workshop, sentiment classifiers that have been pretrained are utilized to show the power of standing on others shoulders -- even for model building!


# Advanced Tasks
Here you'll find a few advanced topics that demonstrate the utility of sharing and reusing others models in your own.  While we only officially integrated the sentiment model examples, embedding of text (or other numerical features) is another cool topic that you might investigate on your own to ramp up performance!


## Training a Sentiment Model
Repeated from above, sentiment models help to assign a numerical sentiment for mood, emotion, intent, etc. to text, images, etc.  In this workshop, we use a sentiment model to process the textual columns of our data in hopes of getting additional insights that improve our overall review prediction service.

As an advanced topic, you may consider training your own sentiment model because you have a special dataset.  One example of this is the training of a model for a specific domain like customer care, technician interactions, bot interactions, or product reviews.

The most commmon open source datasets here are those around public resources like twitter (human sentiment for "good" or "bad"), Amazon (for "positive or negative"), and IMDB.  Starting generically from the [UCI dataset list](https://archive.ics.uci.edu/ml/datasets.html?view=list), this [product dataset](https://archive.ics.uci.edu/ml/datasets/Sentiment+Labelled+Sentences) lists good and bad sentiment from many scraped examples.  One of the most famous content datasets is the [IMDB sentiment dataset](http://ai.stanford.edu/~amaas/data/sentiment/) that has many reviews from high polar movies.  Datasets are increasingly provided for academic papers, so now even [wikipedia](https://en.wikipedia.org/wiki/List_of_datasets_for_machine-learning_research) lists a number of relevant starting points.


## Embedding Models
Embedding models are a way to take complex data in one high-dimensional space and learn a mapping to go to a reduced dimensional space.  They are also a way to capture some rich correlation data for a particular dataset into a dense form.

In the first case, numerical features can be embedded with almost any method - one article on [local linear embedding (LLE)](https://en.wikipedia.org/wiki/Feature_learning#Local_linear_embedding) describes one method to do this using distances between samples.  There are other more complex, but similar methods that utilize [non-linear dimentionality reduction](https://en.wikipedia.org/wiki/Nonlinear_dimensionality_reduction) through clustering that can create interesting "manifolds"; manifolds can be thought of as a way to "project" complex data into more tractable planes or lower dimensionality.  In plain English, if you looked at points in space around the Earth (e.g. landmark locations on the globe), you may get a scattering of 3D volumes; if you used a manifold that mapped to the Earth's surface, you could probably make this 2D (lat, long) and prevent a lot of headaches!

In the second case, textual embedding has gained a lot of great contributions and OSS.  Starting from origins like [word2vec](https://en.wikipedia.org/wiki/Word2vec), models can be learned from large corpora that will start to make semantic relationships.  The most common example of this is realizing the text equation `queen - woman = king` in numerical vectors and seeing the results "add" up.  In python model libraries like [gensim](https://radimrehurek.com/gensim/models/word2vec.html) and [gloVe](https://nlp.stanford.edu/projects/glove/) may be the most popular with varying sizes of models (50d, 300d, etc from billions of web pages or even twitter messages).  In Java, [h2o](http://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-science/word2vec.html) also features pretrained models that may prove useful.