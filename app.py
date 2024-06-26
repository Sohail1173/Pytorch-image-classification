import cv2
from torch.utils.data import DataLoader,Dataset
from torchvision import transforms
import os
import torch.nn as nn

images=[]
labels=[]
datapath=r"C:\Users\91808\Downloads\chest-ctscan"
subfolder=os.listdir(datapath)
# print(subfolder)
for folder in subfolder:
    label=subfolder.index(folder)
    path=os.path.join(datapath,folder)
    for imglist in os.listdir(path):
        image=cv2.imread(os.path.join(path,imglist))
        images.append(image)
        labels.append(label)

class DataPrep(Dataset):
    def __init__(self,features,labels,transform=None):
        self.features=features
        self.labels=labels
        self.transform=transform
    
    def __getitem__(self,item):
        image=self.features[item]
        label=self.labels[item]
        if self.transform:
            image=self.transform(image)

        return image,label
    

    def __len__(self):
        return len(self.labels)
    
data_trans=transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((200,200))
])

dataset=DataPrep(images,labels,data_trans)
data_loader=DataLoader(dataset,batch_size=4,shuffle=True)
data_sample=next(iter(data_loader))
# print(dataset.__len__())
# # print(dataset.__getitem__())

class Disease(nn.Module):
    def __init__(self):
        super(Disease,self).__init__()
        self.conv1=nn.Conv2d(in_channels=3,out_channels=64,kernel_size=2,stride=2,padding=0)
        self.maxpool=nn.MaxPool2d(kernel_size=2,stride=2,padding=0)
        self.activation=nn.ReLU()
        self.linear=nn.Linear(64*50*50,2)
        self.flatten=nn.Flatten()

    def forward(self,data):
        out=self.conv1(data)
        out=self.activation(data)
        out=self.maxpool(data)
        out=self.activation(data)
        out=self.flatten(data)
        out=self.linear(data)
        return out
    
model=Disease()
print(model.eval())
print(model.forward(data_loader))

