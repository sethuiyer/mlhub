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
arma::mat forward(arma::mat X)
{
    z2 = X * W1;
    a2 = z2;
    a2.transform([](double x) {return x / (1 + abs(x)); });
    z3 = a2 * W2;
    a3 = z3;
    a3.transform([] (double x) { return x / (1+abs(x));});
    return a3;
}

};

int main()
{

    mat X = {{0.3,1},{0.5,0.2},{1,0.4}};
    mat y = {0.75,0.82,0.93};
  Neural_Network nn;
  mat yHat = nn.forward(X);
  cout<<yHat[0]<<" "<<y[0]<<endl;
  cout<<yHat[1]<<" "<<y[1]<<endl;
  cout<<yHat[2]<<" "<<y[2]<<endl;
}