from fastai.vision.all import *
from fastai.metrics import accuracy
import pandas as pd
import numpy as np
import os
import PIL.Image as Image
import matplotlib.pyplot as plt

Image.MAX_IMAGE_PIXELS = 933120000 # Change the max pixels to avoid warnings
#lbldict = {1: 'Ramnit', 2:'Lollipop', 3:'Kelihos_ver3', 4:'Vundo', 5:'Simda', 6:'Tracur', 7:'Kelihos_ver1', 8:'Obfuscator.ACY', 9:'Gatak'}

# src = Path to the folder containing the files you want to become images. dst = Path to folder where you want the images saved.
def convertToImage(src, dst):
    files=os.listdir(src)
    print('Source:', src)
    print('Destination', dst)
    print('Converting...')
    for file in files:
        srcPath = src+file
        dstPath = dst+file+'.png'
        f = open(srcPath, 'rb')
        ln = os.path.getsize(srcPath)
        width = int(ln**0.5)
        a = bytearray(f.read())
        f.close()
        g = np.reshape(a[:width * width], (width, width))
        g = np.uint8(g)
        img = Image.fromarray(g)
        img.save(dstPath)
    print('Files converted successfully')

# csv = Path to train csv file, path = path to train images, validpct = percent of data for validation, label_col = column number for labels in csv, splitter = how the data should be splitted for train/validation, item_tfms = item transforms for data augmentation, device = what device should be used (cpu/gpu)
# Returns the DataLoaders
def loadData(csv, path, validpct=None, label_col=1, seed=None, splitter=None, item_tfms = None, device = None):
    df = pd.read_csv(csv, sep=',', header=0)
    dls = ImageDataLoaders.from_df(df, path, label_col=label_col, valid_pct=validpct, seed=seed, splitter = splitter, item_tfms = item_tfms, device=device)
    return dls

# dls = DataLoaders object, arch = architecture, path = path to where the trained model should be exported, epoch_ct = number of iterations, metrics = the metrics used to train the model, pretrained = whether or not to use a pretrained model (False = Create model from scratch)
def trainModel(dls, arch, path, epoch_ct=1, metrics=error_rate, pretrained=True):
    model = cnn_learner(dls, arch, metrics=metrics, pretrained=pretrained)
    model.fine_tune(epochs=epoch_ct)
    model.dls.train = dls.train
    model.dls.valid = dls.valid
    model.export(path)
    return model

# exportPath = path to the exported model, cpu = whether the model should use the cpu or gpu
def loadModel(exportPath, cpu=False):
    model = load_learner(exportPath, cpu)
    return model

# directory = path you want to check whether it is a directory or file
# Returns True if it is a directory, False if it is not.
def isDir(directory):
    isDir = os.path.isdir(directory)
    if isDir == False:
        print("Error: Directory not found, please try again")
    return isDir
    
# item = the specific image you want to show
def showImages(item):
    # Show the images that are being predicted
    img = plt.imread(item)
    plt.imshow(img)
    plt.axis('off')
    plt.title(item)
    plt.show()

# model = the trained model, testPath = the path containing the test set of images, lbl_dict = the dictionary containing the labels
def predict(model, testPath, lbl_dict, test_df=None):
    files = os.listdir(testPath)
    for item in files:
        # Predict each file
        pred, pred_idx, probs = model.predict(testPath+item)
        if(test_df is None):
            print(f"Item: {item} | Prediction: {lbl_dict[int(pred)]}; Probability: {probs[pred_idx]:.04f}")
        elif(test_df is not None):
           print(f"Item: {item} | Prediction: {lbl_dict[int(pred)]}; Probability: {probs[pred_idx]:.04f} | Actual: {lbl_dict[test_df.loc[item][0]]}")
        #showImges(testPath+item)
