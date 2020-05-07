import torchvision.transforms as transforms
from torch.utils.data import DataLoader,Subset
from torchvision.datasets import CIFAR10
from torchvision.datasets import SVHN

def transform_data(dataset, M= 0, train_batch_size= 128, test_batch_size= 10, validation= False, down= False):
    trainset, testset = load_data(dataset)

    num_classes = len(trainset.classes)
    validation_loader = None

    if down:
        trainset = downsample(trainset, M)
        #testset = downsample(testset, M)

    num_classes = len(trainset.classes)
    validation_loader = None

    if validation:
        size = len(trainset)
        train_size = int(0.9 * size)
        val_size = size-train_size
        trainset, valset = random_split(trainset, [train_size, val_size])
        validation_loader = DataLoader(validation_data, batch_size= test_batch_size, shuffle=True)

    # create data loaders
    trainloader = DataLoader(trainset, batch_size= train_batch_size, shuffle=True)
    testloader = DataLoader(testset, batch_size= test_batch_size, shuffle=True)

    return trainloader, testloader, validation_loader, num_classes


def load_data(dataset):
    if dataset.lower() == 'cifar10':
        # convert each image to tensor format
        transform_train = transforms.Compose([
            transforms.Pad(4),
            transforms.RandomHorizontalFlip(),
            transforms.RandomCrop(32),
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.247, 0.243, 0.261)),
            # source https://github.com/kuangliu/pytorch-cifar/issues/19
        ])

        transform_test = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.247, 0.243, 0.261)),
            # source https://github.com/kuangliu/pytorch-cifar/issues/19
        ])

        trainset = CIFAR10("./data", train=True, download=True, transform=transform_train)
        testset = CIFAR10("./data", train=False, download=True, transform=transform_test)

        return trainset, testset

    elif dataset.lower() == 'SVHN':
        transfrom = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.4377, 0.4438, 0.4728), (0.1980, 0.2010, 0.1970))
        ])

        trainset = torchvision.datasets.SVHN(root='./data', train=True,download=True, transform=transform)
        testset = torchvision.datasets.SVHN(root='./data', train=False,download=True, transform=transform)

        return trainset, testset
    else:
        raise ValueError('Dataset not specified.')


def downsample(dataset, M):
    labels = dataset.class_to_idx
    label_counts = {key:0 for key in labels.values()}
    samples_index = []

    for inx, item in enumerate(dataset):

        if all(count >= M for count in label_counts.values()):
            break
        else:
            data_item, label = item
            if label_counts[label] < M:
                label_counts[label] += 1
                samples_index.append(inx)

    data_subset = Subset(dataset, samples_index)
    return data_subset