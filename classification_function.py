from outlier_function import *
import operator
import random
# Given a 2d array into a 1d array row wise. 
def flatten_2d(a):
    output=[]
    for i in a:
        output=output+i
    return output
# A Naive Bayes Classifier, the labels must be intergers and so must the vector
# Having multiple values don't matter
class naive_bayes:
    def __init__(self,n):
        self.prior = {}
        self.categories = n
        self.label_counts = Counter()
        for i in range(n):
            self.label_counts[i] = 0
        self.is_fitted = False
        self.probability_matrix=[[]]
        
    def fit(self, X, y):
        self.probability_matrix = np.zeros(( self.categories , len(X[0]) ))
        for i, example in enumerate(X):
            label=y[i]
            self.label_counts[label] += 1
            for j in range(len(example)):
               if(example[j] != 0):
                    self.probability_matrix[label,j] += 1
        for i in range(len(self.probability_matrix)):
            if(self.label_counts[i] != 0):
                self.probability_matrix[i] /= self.label_counts[i]        
        total_examples = len(y)
        for label in set(y):
            self.prior[label] = float(self.label_counts[label]) / total_examples
        self.is_fitted = True
        return self
    
    def predict(self, test_set):
        self._check_fitted()
        predictions = []
        for i in range(len(test_set)):
            result = self.predict_record(test_set[i])
            predictions.append(result)
        return predictions
    
    def predict_record(self, test_case):
        log_likelihood = {k: log(v) for k, v in self.prior.items()}
        for label in self.label_counts:
            for i in range(len(test_case)):
                if(test_case[i] != 0):
                    probability = self.probability_matrix[label,i]
                    try:
                        log_likelihood[label] += log(probability)
                    except:
                        continue
        return max(log_likelihood, key=log_likelihood.get)
    
    def _check_fitted(self):
        if not self.is_fitted:
            raise NotFittedError(self.__class__.__name__)
            
class knn():
    def __init__(self, n):
        self.data = []
        self.results = []
        self.number = n
    
    def fit(self,X,y):
        self.data = X
        self.results = y
        return self
    
    def predict(self, test_set):
        predictions = []
        for i in range(len(test_set)):
            result = self.predict_record(test_set[i])
            predictions.append(result)
        return predictions
        
    def predict_record(self, test_case):
        distances = self.distance_array(test_case)
        distances.sort()
        distances = distances[:self.number]
        dictionary = {}
        for i in distances:
            if(i[1] in dictionary.keys()):
                dictionary[i[1]] += 1
            else:
                dictionary[i[1]] = 1
        prediction = max(dictionary.iteritems(), key=operator.itemgetter(1))[0]
        return prediction
    
    def distance_array(self, test_case):
        distances = []
        for i in range(len(self.data)):
            to_append = (self.distance(test_case, self.data[i]), self.results[i])
            distances.append(to_append)
        return distances
        
    def distance(self, x1, x2):
        distance = 0
        for i in range(len(x1)):
            distance += np.square(x1[i] - x2[i])
        return np.sqrt(distance)

def cross_validation(model,train_data,train_result,test_data, test_result):
    model = model.fit(train_data,train_result)
    predictions = model.predict(test_data)
    correct = 0.0
    for i in range(len(predictions)):
        if(predictions[i] == test_result[i]):
            correct = correct + 1
    return correct/(len(predictions))

'''
from classification_function import *
X=[[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1], [10,10,10],[10,10,11],[10,11,10],[10,11,11],[11,10,10],[11,10,11],[11,11,10],[11,11,11]]
y=[1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2]
clf=knn(2)
clf=clf.fit(X,y)
clf.predict([[2,2,2],[12,12,12]])

'''    
