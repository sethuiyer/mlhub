//Neural network in C++
// Author: Sethu Iyer 
//Sigmoid is used because the sigmoid function assumes 
//minimal structure and reflects our general state of ignorance about the underlying model.

//This code implements simple 3 layer feed forward neural network with no regularization.
// we use fast sigmoid approximation to speed up the calculation.

#include <iostream>
#include <armadillo>

using namespace std;
using namespace arma;

class Neural_Network
{
   private:
    //define the architecture of the network
    int inputLayerSize = 2;
    int  outputLayerSize = 1;
    int hiddenLayerSize = 3;

    // activation function and the weights
    arma::mat W1,W2;
    arma::mat z2,a2;
    arma::mat z3,a3;
    arma::mat delta3,delta2;
    arma::mat dJdW1, djdW2;

  public:
       Neural_Network()
     {
          //fills in random weights
        W1.randu(2,3);
        W2.randu(3,1);
    }

      //helper functions
        static double sigmoid(double x)
    {
      return x / (1 + abs(x));
    }
    static double sigmoidPrime(double x)
    {
      double f = sigmoid(x);
      return f * (1-f);
    }


    //forwarding function.
    arma::mat forward(arma::mat X)
    {
        z2 = X * W1;
        a2 = z2;
        a2.transform(*sigmoid);
        z3 = a2 * W2;
        a3 = z3;
        a3.transform(*sigmoid);
        return a3;
    }

    //cost function
    double costFunction(mat X,mat y)
    {
      mat yHat = forward(X);

      double cost = 0;
      for(int i = 0; i < outputLayerSize; i++)
      {
        cost =  cost + (yHat[i] - y[i])*(yHat[i] - y[i]);
      }
      cost = cost / 2;
      return cost;

    }

    //derivative of cost function 
    //backpropogation of errors can be understood in this code
    void computeGradients(mat X, mat y)
    {

      mat yHat = forward(X);
      mat z = z3;
      z.transform(*sigmoidPrime);
      delta3 = (yHat - y.t()) % z;
      djdW2 = a2.t() * delta3;

      z = z2;
      z.transform(*sigmoidPrime);
      delta2 = delta3 * W2.t()*z;
      dJdW1 = X.t() * delta2;

    }

    //alpha is our learning rate
    void gradientDescent(mat X,mat y,double alpha,int numIter)
    {
      int i;
      mat transdj1,transdj2;
      for(i=0;i<numIter;i++)
      {
        computeGradients(X,y);
        transdj1 = dJdW1;
        transdj1.transform([=] (double x) { return x * alpha;});
        W1 = W1 - transdj1;
    transdj2 = djdW2;
        transdj2.transform([=] (double x ) { return x *alpha;});
        W2 = W2 - transdj2;
      }
    }
};

int main()
{

    mat X = {{0.3,1},{0.5,0.2},{1,0.4}};
    mat y = {0.75,0.82,0.93};
    Neural_Network nn;
    cout<<"Initial Cost: "<<nn.costFunction(X,y)<<endl;
    nn.gradientDescent(X,y,0.01,400);
    cout<<"After 400 Iterations: "<<nn.costFunction(X,y)<<endl;
    nn.gradientDescent(X,y,0.01,400);
    cout<<"After 800 Iterations: "<<nn.costFunction(X,y)<<endl;
    return 0;
}