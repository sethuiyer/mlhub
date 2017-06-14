# Happy or Sad Webapp

A simple Flask based webapp where you paste the url of an image and it gives you the prediction wheather the person in the image is happy or sad
![image](output_image.PNG)

### Data Collection

Data was collected using [Fatkun Batch Download Image extension](https://chrome.google.com/webstore/detail/fatkun-batch-download-ima/nnjjahlikiabnchcpehcpkdeckfgnohf?hl=en). After downloading the images, the data directory should contain two folders, train and validation and inside each folder, happy_face and sad_face folder should be created.

The number of examples used is very low, so the model is not perfect.

## Dependencies

	Keras
	Opencv 3.1
	Flask
  	Tensorflow

## How to Run

	python app.py
