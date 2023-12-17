from ultralytics import YOLO
from django.conf import settings


def pred(img):
    model = YOLO("yolov8m.pt")
    results = model.predict(str(settings.MEDIA_ROOT)+'/'+img)
    
    return results[0].tojson()