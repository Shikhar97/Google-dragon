import torch
import torch.nn as nn
from torchvision import models


def create_test_model(model_name="resnet", all_path_v0="model/dino.pth"):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    if model_name == "swin":
        model_all_v0 = models.swin_s(weights="IMAGENET1K_V1")
        for param in model_all_v0.parameters():  # freeze model
            param.requires_grad = False

        n_inputs = model_all_v0.head.in_features
        model_all_v0.head = nn.Sequential(
            nn.Linear(in_features=n_inputs, out_features=3, bias=True),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Softmax(dim=1))
    else:
        model_all_v0 = models.resnet50(weights="IMAGENET1K_V2")
        model_all_v0.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        fc_in_size = model_all_v0.fc.in_features
        model_all_v0.fc = nn.Sequential(
            nn.Linear(in_features=fc_in_size, out_features=3, bias=True),
            nn.Softmax(dim=1))

    model_all_v0 = model_all_v0.to(device)
    model_all_v0.load_state_dict(torch.load(all_path_v0))
    return model_all_v0


def resnet_classification(model, img):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    img = img.float().to(device)

    model.eval()

    with torch.no_grad():
        target_class = model(img).detach()
        target_class = torch.argmax(target_class, dim=1).cpu().numpy()

    return img, target_class
