# Happy or Sad Webapp

A simple Flask based webapp where you paste the url of an image and it gives you the prediction whether the person in the image is happy or sad
![image](output_image.PNG)

### Demo
[Happy or Sad Predictor - A Web application built using Deep Learning](https://www.youtube.com/watch?v=Ol_N0fkcEBs)

### Tutorial
Refer the IPython notebook, Code is self explanatory.

### Data Collection

Data was collected using [Fatkun Batch Download Image extension](https://chrome.google.com/webstore/detail/fatkun-batch-download-ima/nnjjahlikiabnchcpehcpkdeckfgnohf?hl=en). After downloading the images, the data directory should contain two folders, train and validation and inside each folder, happy_face and sad_face folder should be created.

The number of examples used is very low, so the model is not perfect.

``` train.py ``` parses the data directory and produces .npy files which is used for training the classifier.

``` predict_cli.py``` is the command line version of the classifier. The network is retrained VGG16.

``` app.py ``` is the main Flask code which renders the files present in ```static/``` folder. JavaScript is used to trigger a GET request when Go button is clicked. The GET request triggers the python program which then submits the result back to javascript program.

## Dependencies

	Keras
	Opencv 3.1
	Flask
  	Tensorflow

## How to Run

	python app.py or python predict_cli.py --image path_to_image_file
	
### Possible improvements
Using OpenCV and Python to extract faces in image and aligining it. [Face Alignment with OpenCV and Python](http://www.pyimagesearch.com/2017/05/22/face-alignment-with-opencv-and-python/) is a good tutorial to learn about the same. The network can be extended to detect more emotional states through facial expressions. For that, we need to replace sigmoid in Read out Layer by softmax and use categorical_crossentropy instead of binary_crossentropy.
