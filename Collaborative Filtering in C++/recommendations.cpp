// recommendation system in c++ written in mlpack
// Author: Sethu Iyer
// compile it with these following flags
//g++ recommendations.cpp -std=c++11 -I/usr/include/libxml2 -lxml2 -L/usr/lib -larmadillo -L/usr/lockal/lib -lmlpack -L/usr/local/lib/ -lboost_serialization

//Generating recommendations for User 3
#include <iostream>
#include <vector>
#include <string>
#include <mlpack/methods/cf/cf.hpp>
using namespace std;
using namespace arma;
using namespace mlpack::cf;
std::vector<std::string> users = {"Aisha","Bob","Chandrika","User"};
std::vector<std::string> movies = {"Up","Skyfall","Thor","Amelie","Snatch","Casablanca","Bridesmaids","Grease"};
int main()
{
mat X;
X.load("dataset.csv",csv_ascii);
size_t neigh = 2;
size_t rank = 2;
int i;
cout <<"Based on your ratings, fetching your recommendations.."<<endl;

X = X.t();
CF cf(X,mlpack::amf::NMFALSFactorizer(),neigh,rank);
int mno,maxrate=0;
for(i=1;i<=7;i++)
{
int prediction = cf.Predict(3,i);
if (prediction >= maxrate)
{
  mno=i;
  maxrate=prediction;
}
}
cout <<"Most likely, you would like the move \""<<movies[mno]<<" \" and will probablity rate it with "<<maxrate<<" stars"<<endl<<endl;
return 0;
}
