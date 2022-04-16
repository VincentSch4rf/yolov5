from pathlib import Path

from yolov5.models.common import AutoShape, DetectMultiBackend
from yolov5.utils.general import LOGGER, logging
from yolov5.utils.torch_utils import torch


def load_model(model_path, device=None, autoshape=True, agnostic=False, fp16=False, verbose=False):
    """
    Creates a specified YOLOv5 model
    Arguments:
        model_path (str): path of the model
        device (str): select device that model will be loaded (cpu, cuda)
        pretrained (bool): load pretrained weights into the model
        autoshape (bool): make model ready for inference
        verbose (bool): if False, yolov5 logs will be silent
    Returns:
        pytorch model
    (Adapted from yolov5.hubconf.create)
    """
    # set logging
    if not verbose:
        LOGGER.setLevel(logging.WARNING)

    # set device if not given
    if device is None:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    elif type(device) is str:
        device = torch.device(device)

    model = DetectMultiBackend(model_path, device=device, fp16=fp16)

    if autoshape:
        model = AutoShape(model, agnostic=agnostic)  # for file/URI/PIL/cv2/np inputs and NMS
    return model.to(device)


class YOLOv5:
    def __init__(self, model_path, device=None, load_on_init=True, agnostic=False, fp16=False):
        self.model_path = model_path
        self.device = device
        self.agnostic = agnostic
        self.fp16 = fp16
        if load_on_init:
            Path(model_path).parents[0].mkdir(parents=True, exist_ok=True)
            self.model = load_model(model_path=model_path, device=device, autoshape=True, agnostic=self.agnostic,
                                    fp16=self.fp16)
        else:
            self.model = None

    def load_model(self):
        """
        Load yolov5 weight.
        """
        Path(self.model_path).parents[0].mkdir(parents=True, exist_ok=True)
        self.model = load_model(model_path=self.model_path, device=self.device, autoshape=True, agnostic=self.agnostic,
                                fp16=self.fp16)

    def predict(self,
                image_list,
                size=640,
                augment=False):
        """
        Perform yolov5 prediction using loaded model weights.
        Returns results as a yolov5.models.common.Detections object.
        """
        assert self.model is not None, "before predict, you need to call .load_model()"
        results = self.model(imgs=image_list, size=size, augment=augment)
        return results


if __name__ == "__main__":
    model_path = "yolov5/weights/yolov5s.pt"
    device = "cuda"
    model = load_model(model_path=model_path, config_path=None, device=device)

    from PIL import Image

    imgs = [Image.open(x) for x in Path("yolov5/data/images").glob("*.jpg")]
    results = model(imgs)