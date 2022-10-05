import torch
import torchvision
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import time
import random

torch.manual_seed(42)
random.seed(42)

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

batch_size = 8

source_train = './024 Photos 64x64 train test split balanced/01_train'
source_test = './024 Photos 64x64 train test split balanced/02_test'

trainset = datasets.ImageFolder(root= source_train, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=2)

testset = datasets.ImageFolder(root= source_test, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=True, num_workers=2)

classes = ('01 Basic', '02 Pure', '03 S Pure', '04 X Pure', '05 GP 4')

print("Trainset: ", trainset)
print()
print("Testset: ", testset)


import matplotlib.pyplot as plt
import numpy as np


# functions to show an image
def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()


# get some random training images
dataiter = iter(trainloader)
images, labels = dataiter.next()


# print labels
print()
print("Random Traindata")
print(''.join('Class(Train): 'f'{classes[labels[j]]:5s}\n' for j in range(batch_size)))
# show images
#imshow(torchvision.utils.make_grid(images))

import torch.nn as nn
import torch.nn.functional as F

# Define Neural Network
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.conv1 = nn.Conv2d(in_channels = 3, out_channels = 6, kernel_size = 5, stride = 1, padding = 2, 
            bias = True, padding_mode = 'zeros')
        self.conv2 = nn.Conv2d(in_channels = 6, out_channels = 16, kernel_size = 5, stride = 1, padding = 2, 
            bias = True, padding_mode = 'zeros')
        
        self.pool = nn.MaxPool2d(kernel_size = 2, stride = 2)

        # Input Linear = (Anz Dim letzte Schicht x Höhe x Breite) / 2^(2 x Anz Pooling Layer)
        # Input Linear = (out_channels x Höhe x Breite) / 2^(2 x Anz Pool)

        self.fc1 = nn.Linear(4096, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 5)

    def forward(self, x):
        
        #print(x.size())
        x = self.pool(F.relu(self.conv1(x)))
        #print(x.size())   
        x = self.pool(F.relu(self.conv2(x)))     
        #print(x.size())   
        x = torch.flatten(x, 1) # flatten all dimensions except batch  
        #print(x.size())      
        x = F.relu(self.fc1(x))
        #print(x.size())        
        x = F.relu(self.fc2(x))        
        x = self.fc3(x)

        
        return x


net = Net()
print(net)

import torch.optim as optim

# Define Loss Function and Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

epoch = 400

print()
print("Start training... ")
start_time = time.time()

for epoch in range(epoch):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        #print("Shape Input: ", inputs.shape)
        #print("Shape Labels: ", labels.shape)
        #print("Inputs:", inputs)
        #print("Labels:", labels)
        #print()
       
        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 40 == 39:    # print every 20 mini-batches
            print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
            running_loss = 0.0

training_time = round((time.time() - start_time), 1)
print('Finished Training')
print()

PATH = './bora.net.pth'
torch.save(net.state_dict(), PATH)

dataiter = iter(testloader)
images, labels = dataiter.next()

# print images
print('GroundTruth: ', ' '.join(f'{classes[labels[j]]:5s}' for j in range(batch_size)))




net = Net()
net.load_state_dict(torch.load(PATH))

outputs = net(images)

_, predicted = torch.max(outputs, 1)

print('Predicted: ', ' '.join(f'{classes[predicted[j]]:5s}'
                              for j in range(batch_size)))

imshow(torchvision.utils.make_grid(images))


correct = 0
total = 0
# since we're not training, we don't need to calculate the gradients for our outputs
with torch.no_grad():
    for data in testloader:
        images, labels = data
        # calculate outputs by running images through the network
        outputs = net(images)
        # the class with the highest energy is what we choose as prediction
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print()
print("Epochs:", epoch+1)
print("Training Time: %.1f Seconds" % (training_time))
convert = time.strftime("%M:%S", time.gmtime(training_time))
print("Training Time: ", convert)

print(f'Accuracy of the network on the test images: {100 * correct // total} %')


# prepare to count predictions for each class
correct_pred = {classname: 0 for classname in classes}
total_pred = {classname: 0 for classname in classes}

# again no gradients needed
with torch.no_grad():
    for data in testloader:
        images, labels = data
        outputs = net(images)
        _, predictions = torch.max(outputs, 1)
        # collect the correct predictions for each class
        for label, prediction in zip(labels, predictions):
            if label == prediction:
                correct_pred[classes[label]] += 1
            total_pred[classes[label]] += 1


# print accuracy for each class
for classname, correct_count in correct_pred.items():
    accuracy = 100 * float(correct_count) / total_pred[classname]
    print(f'Accuracy for class: {classname:5s} is {accuracy:.1f} %')

print()
print("end.")