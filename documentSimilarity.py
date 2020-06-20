import numpy as np
import pandas as pd

class DocumentSimilarity():

    def __init__(self, file1, file2):

        self.file1 = file1
        self.file2 = file2

    #implement all the methods here (cosineSimilarity, jaccard, etc.)


file1 = open("file1", "r") #first document (doesn't acutally exist yet)
file2 = open("file2", "r") #second document (doesn't actually exist yet)

documentAnalysis = DocumentSimilarity(file1, file2)
