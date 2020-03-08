# imageCaptionGenerator
This project creates a NN that uses features extracted from the pretrained Xception network to generate image captions.

The dataset used is the Flickr_8K dataset. It can be downloaded here:

[Flickr8k_Dataset](https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_Dataset.zip)
[Flickr8k_text](https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_text.zip)

The project uses Keras.

## The NN
The network has two input:

### Features
1. **Input layer** (, 2048), this are the features extrated by the Xception network
2. **Dropout layer** (, 2048), keep_prob 0.5
3. **Dense layer** (, 256)

### Captions
1. **Input layer** (, 34), the input sequence to create a caption
2. **Embedding layer** (, 34, 256)
3. **Dropout layer** (, 34, 256), keep_prob 0.5
4. **LSTM layer** (, 256)

### Final layers
Take the output of the last two sections as input
1. **Add layer** (, 256)
2. **Dense layer** (, 256)
3. **Dense layer** (, 7612)

## To use the trained run 
```bash
python gui.py
```

And then either selet an image of let the program randomly choose an image from the test dataset

You can then see the predicted caption of the NN.
