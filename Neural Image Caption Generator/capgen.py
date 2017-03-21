# download caffe model from http://www.robots.ox.ac.uk/~vgg/research/very_deep/
# download checkpoint model from http://cs.stanford.edu/people/karpathy/neuraltalk/

import caffe
import os.path
import numpy as np
from scipy.misc import imread, imresize
from neuraltalk.imagernn.imagernn_utils import decodeGenerator
import cPickle as pickle
import numpy as np

caffe.set_mode_cpu()
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
CAFFE_MODEL_DEF_PATH = os.path.join(FILE_DIR, 'python_features/deploy_features.prototxt')
CAFFE_MODEL_PATH = os.path.join(FILE_DIR, 'python_features/vgg_16_weights.caffemodel')
CHECKPOINT_PATH = os.path.join(FILE_DIR, 'model/flickr8k_cnn_lstm_v1.p')
BEAM_SIZE = 1


class CaptionGenerator:
    def __init__(self):
        self.net = caffe.Net(CAFFE_MODEL_DEF_PATH, CAFFE_MODEL_PATH, caffe.TEST)

        # load the checkpoint
        # print 'loading checkpoint %s' % (CHECKPOINT_PATH, )
        self.checkpoint = pickle.load(open(CHECKPOINT_PATH, 'rb'))
        self.checkpoint_params = self.checkpoint['params']
        self.model = self.checkpoint['model']
        self.ixtoword = self.checkpoint['ixtoword']

    def extract(self, in_data):
        """
        Get the features for a batch of data using network
        Inputs:
        in_data: data batch
        """

        out = self.net.forward_all(**{self.net.inputs[0]: in_data})
        print out
        features = out[self.net.outputs[0]]
        return features

    def batch_extract(self, filenames):
        """
        Get the features for all images from filenames using a network
        Inputs:
        filenames: a list of names of image files
        Returns:
        an array of feature vectors for the images in that file
        """

        N, C, H, W = self.net.blobs[self.net.inputs[0]].data.shape
        F = self.net.blobs[self.net.outputs[0]].data.shape[1]
        Nf = len(filenames)
        Hi, Wi, _ = imread(filenames[0]).shape
        allftrs = np.zeros((Nf, F))
        for i in range(0, Nf, N):
            in_data = np.zeros((N, C, H, W), dtype=np.float32)

            batch_range = range(i, min(i + N, Nf))
            batch_filenames = [filenames[j] for j in batch_range]
            Nb = len(batch_range)

            batch_images = np.zeros((Nb, 3, H, W))
            for j, fname in enumerate(batch_filenames):
                im = imread(fname)
                #print im
                if len(im.shape) == 2:
                    im = np.tile(im[:, :, np.newaxis], (1, 1, 3))
                # RGB -> BGR
                im = im[:, :, (2, 1, 0)]
                # mean subtraction
                im = im - np.array([103.939, 116.779, 123.68])
                # resize
                im = imresize(im, (H, W), 'bicubic')
                # get channel in correct dimension
                im = np.transpose(im, (2, 0, 1))
                batch_images[j, :, :, :] = im

            # insert into correct place
            in_data[0, :, :, :] = batch_images
            print in_data
            # predict features
            ftrs = self.extract(in_data[0])
            print ftrs
            for j in range(len(batch_range)):
                allftrs[i + j, :] = ftrs[j, :]

                # print 'Done %d/%d files' % (i+len(batch_range), len(filenames))

        return allftrs

    def predict(self, features):

        # iterate over all images and predict sentences
        BatchGenerator = decodeGenerator(CHECKPOINT_PATH)
	print features
        # encode the image
        img = {}
        img['feat'] = features[:, 0]

        # perform the work. heavy lifting happens inside
        kwparams = {'beam_size': BEAM_SIZE}
        Ys = BatchGenerator.predict([{'image': img}], self.model, self.checkpoint_params, **kwparams)

        # encode the top prediction
        top_predictions = Ys[0]  # take predictions for the first (and only) image we passed in
        top_prediction = top_predictions[0]  # these are sorted with highest on top
	print top_predictions
        candidate = ' '.join(
            [self.ixtoword[ix] for ix in top_prediction[1] if ix > 0])  # ix 0 is the END token, skip that
        # print 'PRED: (%f) %s' % (top_prediction[0], candidate)

        return candidate

    # absolute file path
    def get_caption(self, file):
        allftrs = self.batch_extract([file])
        features = np.transpose(allftrs)
        caption = self.predict(features)
        return caption


if __name__ == "__main__":
    net = caffe.Net(CAFFE_MODEL_DEF_PATH, CAFFE_MODEL_PATH, caffe.TEST)
    img = caffe.io.load_image("img4.jpg")
    img = img[:,:,::-1]*255.0
    avg =  np.array([103.939, 116.779, 123.68])
    img = img - avg
    im = imresize(img, (224, 224), 'bicubic')
    im = np.transpose(im, (2, 0, 1))
    im = np.expand_dims(im,axis=0)
    im.astype(float)
    out = net.forward(data=im)
    print (net.params['conv1_1'][0].data)
    
