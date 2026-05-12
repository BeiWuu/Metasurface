import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models
import copy


def gram_matrix(input_tensor):
    """
    Compute the Gram matrix for style representation.
    """
    batch, channels, height, width = input_tensor.size()
    features = input_tensor.view(batch * channels, height * width)
    gram = torch.mm(features, features.t())
    return gram.div(batch * channels * height * width)


class ContentLoss(nn.Module):
    """
    Content loss module.
    """
    def __init__(self, target):
        super(ContentLoss, self).__init__()
        self.target = target.detach()
        self.loss = 0

    def forward(self, input_tensor):
        self.loss = nn.functional.mse_loss(input_tensor, self.target)
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
        self.loss = nn.functional.mse_loss(gram, self.target)
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


def run_style_transfer_single(cnn, normalization_mean, normalization_std,
                              content_img, style_img, num_steps=300,
                              style_weight=1e6, content_weight=1):
    """
    Run style transfer for a single content-style pair.
    """
    input_img = content_img.clone()
    
    model, content_losses, style_losses = get_style_model_and_losses(
        cnn, normalization_mean, normalization_std, content_img, style_img)
    
    optimizer = optim.LBFGS([input_img.requires_grad_()])

    run = [0]
    while run[0] <= num_steps:
        def closure():
            input_img.data.clamp_(0, 1)

            optimizer.zero_grad()
            model(input_img)
            
            style_score = 0
            content_score = 0

            for sl in style_losses:
                style_score += sl.loss
            for cl in content_losses:
                content_score += cl.loss

            style_score *= style_weight
            content_score *= content_weight

            loss = style_score + content_score
            loss.backward()

            run[0] += 1

            return loss

        optimizer.step(closure)

    input_img.data.clamp_(0, 1)

    return input_img


def run_style_transfer(content, style):
    """
    Main function for style transfer.
    
    Args:
        content: Tensor of shape [batch, 3, 512, 512]
        style: Tensor of shape [batch, 3, 512, 512]
    
    Returns:
        Tensor of shape [batch, 3, 512, 512] with style-transferred images
    """
    device = content.device
    batch_size = content.size(0)
    
    cnn = models.vgg19(pretrained=True).features.to(device).eval()
    
    normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
    normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(device)
    
    for param in cnn.parameters():
        param.requires_grad = False
    
    results = []
    
    for i in range(batch_size):
        content_img = content[i:i+1]
        style_img = style[i:i+1]
        
        output_img = run_style_transfer_single(
            cnn, normalization_mean, normalization_std,
            content_img, style_img,
            num_steps=300,
            style_weight=1e6,
            content_weight=1
        )
        
        results.append(output_img)
    
    output = torch.cat(results, dim=0)
    
    return output

