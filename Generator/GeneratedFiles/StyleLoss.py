import torch
import torch.nn as nn
import torchvision.models as models
import copy


def gram_matrix(input_tensor):
    """
    Compute the Gram matrix for style representation.
    """
    batch, channels, height, width = input_tensor.size()
    features = input_tensor.view(batch, channels, height * width)
    gram = torch.bmm(features, features.transpose(1, 2))
    return gram.div(channels * height * width)


class ContentLoss(nn.Module):
    """
    Content loss module.
    """
    def __init__(self, target):
        super(ContentLoss, self).__init__()
        self.target = target.detach()
        self.loss = 0

    def forward(self, input_tensor):
        self.loss = nn.functional.mse_loss(input_tensor, self.target, reduction='none')
        self.loss = self.loss.view(self.loss.size(0), -1).mean(dim=1)
        return input_tensor


class StyleLoss(nn.Module):
    """
    Style loss module.
    """
    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        self.target = gram_matrix(target_feature).detach()
        self.loss = 0

    def forward(self, input_tensor):
        gram = gram_matrix(input_tensor)
        self.loss = nn.functional.mse_loss(gram, self.target, reduction='none')
        self.loss = self.loss.view(self.loss.size(0), -1).mean(dim=1)
        return input_tensor


class Normalization(nn.Module):
    """
    Normalization module for VGG preprocessing.
    """
    def __init__(self, mean, std):
        super(Normalization, self).__init__()
        self.mean = mean.view(-1, 1, 1)
        self.std = std.view(-1, 1, 1)

    def forward(self, img):
        return (img - self.mean) / self.std


def get_style_model_and_losses(cnn, normalization_mean, normalization_std,
                               content_img, style_img,
                               content_layers=['conv_4'],
                               style_layers=['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']):
    """
    Build the style transfer model by inserting content and style loss modules.
    """
    cnn = copy.deepcopy(cnn)
    normalization = Normalization(normalization_mean, normalization_std).to(content_img.device)
    
    content_losses = []
    style_losses = []

    model = nn.Sequential(normalization)

    i = 0
    for layer in cnn.children():
        if isinstance(layer, nn.Conv2d):
            i += 1
            name = 'conv_{}'.format(i)
        elif isinstance(layer, nn.ReLU):
            name = 'relu_{}'.format(i)
            layer = nn.ReLU(inplace=False)
        elif isinstance(layer, nn.MaxPool2d):
            name = 'pool_{}'.format(i)
        else:
            continue

        model.add_module(name, layer)

        if name in content_layers:
            target = model(content_img).detach()
            content_loss = ContentLoss(target)
            model.add_module('content_loss_{}'.format(i), content_loss)
            content_losses.append(content_loss)

        if name in style_layers:
            target_feature = model(style_img).detach()
            style_loss = StyleLoss(target_feature)
            model.add_module('style_loss_{}'.format(i), style_loss)
            style_losses.append(style_loss)

    for i in range(len(model) - 1, -1, -1):
        if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
            break

    model = model[:(i + 1)]

    return model, content_losses, style_losses


def func_loss(input_img, content_img, style_img):
    """
    Calculate content loss and style loss.
    
    Args:
        input_img: Tensor of shape [batch, 3, 512, 512] - style transferred images
        content_img: Tensor of shape [batch, 3, 512, 512] - content images
        style_img: Tensor of shape [batch, 3, 512, 512] - style images
    
    Returns:
        content_score: Tensor of shape [batch] - content loss values
        style_score: Tensor of shape [batch] - style loss values
    """
    device = input_img.device
    batch_size = input_img.size(0)
    
    cnn = models.vgg19(pretrained=True).features.to(device).eval()
    
    normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
    normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(device)
    
    for param in cnn.parameters():
        param.requires_grad = False
    
    model, content_losses, style_losses = get_style_model_and_losses(
        cnn, normalization_mean, normalization_std, content_img, style_img)
    
    model(input_img)
    
    content_score = torch.zeros(batch_size).to(device)
    style_score = torch.zeros(batch_size).to(device)
    
    for cl in content_losses:
        content_score += cl.loss
    
    for sl in style_losses:
        style_score += sl.loss
    
    return content_score, style_score

