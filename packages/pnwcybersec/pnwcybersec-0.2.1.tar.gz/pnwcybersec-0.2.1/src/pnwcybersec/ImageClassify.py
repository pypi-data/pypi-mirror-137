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
    
def loadData(valid_pct, get_items=get_image_files, get_y = parent_label, item_tfms = Resize(224, ResizeMethod.Pad, pad_mode='zeros')):
    # parent_label -->> simply gets the name of the folder a file is in
    loader = DataBlock(
        blocks = (ImageBlock, CategoryBlock),
        get_items = get_items,
        splitter = RandomSplitter(valid_pct=valid_pct, seed=24),
        get_y = get_y,
        item_tfms = item_tfms
        #batch_tfms=aug_transforms()
        #item_tfms = Resize(224, ResizeMethod.pad, pad_mode='zeros'),   # by default it crops
        #RandomResizedCrop(224)
    )
    return loader

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
    
def confusionMatrix(model):
    interp = ClassificationInterpretation.from_learner(model)
    interp.plot_confusion_matrix()
    plt.show()

# model = the trained model, testPath = the path containing the test set of images, lbl_dict = the dictionary containing the labels, test_df = test set dataframe showing the actual class for each item
def predict(model, testPath):
    path = Path(testPath)
    files = get_image_files(path)
    for item in files:
        # Predict each file
        pred, pred_idx, probs = model.predict(item)
        print(f"Item: {item} | Prediction: {pred}; Probability: {probs[pred_idx]:.04f}")
