import numpy as np
import pandas as pd
import math

class DocumentSimilarity():

    def __init__(self, file1, file2):

        self.file1 = file1
        self.file2 = file2

    #implement all the methods here (cosineSimilarity, jaccard, etc.)
    def cosineSimilarity(self):

        file1Hash = dict()
        file2Hash = dict()

        file1Words = self.file1.read().split()
        file2Words = self.file2.read().split()

        i = 0

        while i < max(len(file1Words), len(file2Words)):

            if i < len(file1Words):

                if not(file1Words[i] in file2Hash): file2Hash[file1Words[i]] = file2Words.count(file1Words[i])
                if not(file1Words[i] in file1Hash): file1Hash[file1Words[i]] = file1Words.count(file1Words[i])

            if i < len(file2Words):

                if not(file2Words[i] in file1Hash): file1Hash[file2Words[i]] = file1Words.count(file2Words[i])
                if not(file2Words[i] in file2Hash): file2Hash[file2Words[i]] = file2Words.count(file2Words[i])

            i += 1

        self.file1TermFrequency = [0] * len(file1Hash)
        self.file2TermFrequency = [0] * len(file1Hash)
        self.termFrequenciesMultiplied = 0

        self.file1EuclideanNorm = 0
        self.file2EuclideanNorm = 0

        x = 0

        for p in file1Hash:

            self.file1EuclideanNorm += (file1Hash.get(p) ** 2)
            self.file2EuclideanNorm += (file2Hash.get(p) ** 2)

            self.file1TermFrequency[x] = file1Hash.get(p)
            self.file2TermFrequency[x] = file2Hash.get(p)
            self.termFrequenciesMultiplied += (self.file1TermFrequency[x] * self.file2TermFrequency[x])

            x += 1

        self.file1EuclideanNorm = math.sqrt(self.file1EuclideanNorm)
        self.file2EuclideanNorm = math.sqrt(self.file2EuclideanNorm)

        cosineSimilarity = (self.termFrequenciesMultiplied) / (self.file1EuclideanNorm * self.file2EuclideanNorm)

        print(cosineSimilarity)


file1 = open("C:\\Users\\Administrator\\Documents\\GitHub\\clientSentimentAnalysis\\file1.txt", "r") #first document (doesn't acutally exist yet, use the path to the file)
file2 = open("C:\\Users\\Administrator\\Documents\\GitHub\\clientSentimentAnalysis\\file2.txt", "r") #second document (doesn't actually exist yet, use the path to the file)

documentAnalysis = DocumentSimilarity(file1, file2)
documentAnalysis.cosineSimilarity();
