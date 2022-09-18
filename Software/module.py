import gensim
import gensim.models.keyedvectors as word2vec
import nltk
from pyvi import ViTokenizer
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

def ReturnDistortions(sentences, vocabulary, w2v_model, K):
    X = []
    for sentence in sentences:
        sentence_tokenized = ViTokenizer.tokenize(sentence)
        words = sentence_tokenized.split(" ")
        sentence_vec = np.zeros((128))
        for word in words:
            if word in vocabulary:
                sentence_vec += w2v_model[word]
        X.append(sentence_vec)
    distortions = []
    if(K >= 10):
        K = 10
    for k in range(1,K):
        kmeanModel = KMeans(n_clusters=k, init='k-means++', random_state=42)
        kmeanModel.fit(X)
        distortions.append(kmeanModel.inertia_)

    return distortions,K

def KmeanTextSummary(inputText, K, model, vocabulary):
    #load model and preprocessing
    w2v_model = model
    contents_parsed = inputText.lower()
    contents_parsed = contents_parsed.replace('\n', ' ')
    contents_parsed = contents_parsed.strip()
    sentences = nltk.sent_tokenize(contents_parsed)

    #tokenize and split the input
    X = []
    for sentence in sentences:
        sentence_tokenized = ViTokenizer.tokenize(sentence)
        words = sentence_tokenized.split(" ")
        sentence_vec = np.zeros((128))
        for word in words:
            if word in vocabulary:
                sentence_vec += w2v_model[word]
        X.append(sentence_vec)

    #Fit model and return result
    try:
        n_clusters = K
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans = kmeans.fit(X)
        avg = []
        for j in range(n_clusters):
            idx = np.where(kmeans.labels_ == j)[0]
            avg.append(np.mean(idx))

        closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
        ordering = sorted(range(n_clusters), key=lambda k: avg[k])
        summary = ' '.join([sentences[closest[idx]] for idx in ordering])
        summary = '. '.join(map(lambda s: s.strip().capitalize(), summary.split('.')))
        return summary
    except Exception as e:
        stringException = f"Lỗi phần mềm!\nLỗi cụ thể: {e}"
        return stringException