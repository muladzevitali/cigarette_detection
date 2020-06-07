from typing import List

import numpy
import torch

from src.config import resnet_config
from .resnet import resnet18, resnet101
from .transforms import transform_images

batch_size = resnet_config.batch_size
softmax = torch.nn.Softmax(dim=0)


class Resnet:
    def __init__(self):
        self.cigarette_classifier = self.load_model()
        self.category_map = ['camel', 'kent', 'lm', 'malboro', 'sobranie', 'winston']

    @staticmethod
    def load_model():
        """Load classifier model"""
        cigarette_classifier = resnet101(pretrained=True)
        cigarette_classifier.load_state_dict(torch.load(resnet_config.weights_file, map_location=torch.device('cpu')))

        if resnet_config.cuda:
            cigarette_classifier = cigarette_classifier.cuda()

        cigarette_classifier = cigarette_classifier.eval()

        return cigarette_classifier

    def predict_classes(self, images_array: List[numpy.array]):
        """Get predictions"""
        predictions: List[dict] = list()

        for index_ in range(len(images_array) // batch_size + 1):
            # Slice batch
            images_batch = images_array[batch_size * index_: batch_size * (index_ + 1)]

            if not len(images_batch):
                continue
            # Transform images
            transformed_images = transform_images(images_batch)
            # Apply to model
            with torch.no_grad():
                outputs = self.cigarette_classifier(transformed_images)
                outputs_with_probability = softmax(outputs)
            # Apply names to indices and get top k predictions
            batch_prediction = self.handle_predictions(outputs_with_probability)

            predictions.extend(batch_prediction)

        return predictions

    def handle_predictions(self, predictions: torch.Tensor) -> List[dict]:
        """Prettify predictions"""
        results: List[dict] = list()
        # Get Top K results with probabilities
        top_probabilities, top_labels = torch.topk(predictions, resnet_config.top_k)
        top_probabilities, top_labels = top_probabilities.cpu().numpy(), top_labels.cpu().numpy()
        # Prettify predictions and map indices to names
        for labels, probabilities in zip(top_labels, top_probabilities):
            results.append(
                {'predictions': [{'class': self.category_map[label_index], 'probability': float(probability)} for
                                 label_index, probability in zip(labels, probabilities)]})

        return results
