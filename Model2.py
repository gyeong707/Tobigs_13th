import numpy as np
import math

class TwoLayerNet():
    """
    2 Layer Network를 만드려고 합니다.

    해당 네트워크는 아래의 구조를 따릅니다.

    input - Linear - ReLU - Linear - Softmax

    Softmax 결과는 입력 N개의 데이터에 대해 개별 클래스에 대한 확률입니다.
    """

    def __init__(self, X, input_size, hidden_size, hidden_size2, output_size, std=1e-4):
         """
         네트워크에 필요한 가중치들을 initialization합니다.
         initialized by random values
         해당 가중치들은 self.params 라는 Dictionary에 담아둡니다.

         input_size: 데이터의 변수 개수 - D
         hidden_size: 히든 층의 H 개수 - H
         output_size: 클래스 개수 - C

         """

         self.params = {}
         self.params["W1"] = std * np.random.randn(input_size, hidden_size)
         self.params["b1"] = np.random.randn(hidden_size)
         self.params["W2"] = std * np.random.randn(hidden_size, hidden_size2)
         self.params["b2"] = np.random.randn(hidden_size2)
         self.params["W3"] = std * np.random.randn(hidden_size2, output_size)
         self.params["b3"] = np.random.randn(output_size)
        

    def forward(self, X, y=None):

        """

        X: input 데이터 (N, D)
        y: 레이블 (N,)

        Linear - ReLU - Linear - Softmax - CrossEntropy Loss

        y가 주어지지 않으면 Softmax 결과 p와 Activation 결과 a를 return합니다. p와 a 모두 backward에서 미분할때 사용합니다.
        y가 주어지면 CrossEntropy Error를 return합니다.

        """

        W1, b1 = self.params["W1"], self.params["b1"]
        W2, b2 = self.params["W2"], self.params["b2"]
        W3, b3 = self.params["W3"], self.params["b3"]

        N, D = X.shape

        # 여기에 p를 구하는 작업을 수행하세요.

        h = np.dot(X, W1) + b1
        a = np.maximum(0, h)
        h2 = np.dot(a, W2) + b2
        a2 = np.maximum(0, h2)
        o = np.dot(a2, W3) + b3
        p = np.exp(o)/np.sum(np.exp(o),axis=1).reshape(-1,1)

        if y is None:
            return p, a2, a
        
        # 여기에 Loss를 구하는 작업을 수행하세요.
        
        Loss = 0
        
        for i in range(y.shape[0]): #행
            for j in range(p.shape[1]): #열
                if y[i] == j:
                    Loss -= np.log(p[i][j])
#        print('loss : ',Loss)

        return Loss


    def backward(self, X, y, learning_rate=1e-5):
        """

        X: input 데이터 (N, D)
        y: 레이블 (N,)

        grads에는 Loss에 대한 W1, b1, W2, b2 미분 값이 기록됩니다.

        원래 backw 미분 결과를 return 하지만
        여기서는 Gradient Descent방식으로 가중치 갱신까지 합니다.

        """
        W1, b1 = self.params["W1"], self.params["b1"]
        W2, b2 = self.params["W2"], self.params["b2"]
        W3, b3 = self.params["W3"], self.params["b3"]

        N = X.shape[0] # 데이터 개수
        grads = {}

        p, a2, a = self.forward(X)

        # 여기에 파라미터에 대한 미분을 저장하세요.

        dp = p
        for i in range(p.shape[0]):
            for j in range(p.shape[1]):
                if(j==y[i]):
                    dp[i][j]-=1
        
        # p-y
        da = np.heaviside(a,0)
        da2 = np.heaviside(a2, 0)
        
        
        grads["W3"] = np.dot(a2.T, dp)
        grads["b3"] = np.sum(dp, axis=0)
        grads["W2"] = np.dot(a.T, da2*np.dot(dp, W3.T))
        grads["b2"] = np.sum(da2*np.dot(dp,W3.T), axis=0)
        grads["W1"] = np.dot(X.T, da*np.dot(da2*np.dot(dp, W3.T),W2.T))
        grads["b1"] = np.sum(da*np.dot(da2*np.dot(dp, W3.T),W2.T), axis=0)
        
        self.params["W3"] -= learning_rate * grads["W3"]
        self.params["b3"] -= learning_rate * grads["b3"]
        self.params["W2"] -= learning_rate * grads["W2"]
        self.params["b2"] -= learning_rate * grads["b2"]
        self.params["W1"] -= learning_rate * grads["W1"]
        self.params["b1"] -= learning_rate * grads["b1"]

        
        
    def accuracy(self, X, y):

        p, _, _ = self.forward(X)
        
        pre_p = np.argmax(p,axis=1)

        return np.sum(pre_p==y)/pre_p.shape[0]
