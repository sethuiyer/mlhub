//Neural network in C++
// Author: Sethu Iyer 
//Sigmoid is used because the sigmoid function assumes minimal structure and reflects our general state of ignorance about the underlying model.

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

};

int main()
{

    mat X = {{0.3,1},{0.5,0.2},{1,0.4}};
    mat y = {0.75,0.82,0.93};
  Neural_Network nn;
  cout<<nn.costFunction(X,y);
  return 0;
}