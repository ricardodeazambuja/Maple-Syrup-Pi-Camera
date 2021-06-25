# Usage examples for Maple-Syrup-Pi-Camera

The [Google Coral USB Accelerator](https://coral.ai/products/accelerator) used in the Maple-Syrup-Pi-Camera can only run [TFLite models that were compiled by the EdgeTPU compiler](https://coral.ai/docs/edgetpu/models-intro/). However, there are plenty of TFLite models already available ready to be used. In addition to that, Google doesn't officially support the use of the Coral USB Accelerator with the Raspberry Pi Zero anymore, therefore I had to manually adapt the [PyCoral API](https://github.com/google-coral/pycoral) (already available in the SDCard image). Still, if you try a script that uses the PyCoral API, it may need small adaptations.

Using the supplied SDCard image, you can go to ```/home/pi/coral/``` and try:


#### **Detection**:

##### [90 different things](https://github.com/google-coral/test_data/raw/master/coco_labels.txt) - Using SSD MobileNet V1
```
python object_detection_from_cam.py --model test_data/ssd_mobilenet_v1_coco_quant_postprocess_edgetpu.tflite --labels test_data/coco_labels.txt
```

##### [90 different things](https://github.com/google-coral/test_data/raw/master/coco_labels.txt) - Using SSD MobileNet V2
```
python object_detection_from_cam.py --model test_data/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite --labels test_data/coco_labels.txt
```

##### [90 different things](https://github.com/google-coral/test_data/raw/master/coco_labels.txt) - Using SSDLite MobileDet
```
python object_detection_from_cam.py --model test_data/ssdlite_mobiledet_coco_qat_postprocess_edgetpu.tflite --labels test_data/coco_labels.txt
```

##### [Faces](https://coral.ai/models/all/#detection) - Using SSD MobileNet V2
```
python object_detection_from_cam.py --model test_data/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite --labels test_data/coco_labels.txt
```

I 
#### **Classification**:

##### [1000 different things](https://github.com/google-coral/test_data/raw/master/imagenet_labels.txt) - Using Inception V1
```
python classify_from_cam.py   --model test_data/inception_v1_224_quant_edgetpu.tflite  --labels test_data/imagenet_labels.txt
```

##### [1000 different things](https://github.com/google-coral/test_data/raw/master/imagenet_labels.txt) - Using Inception V2
```
python classify_from_cam.py   --model test_data/inception_v2_224_quant_edgetpu.tflite  --labels test_data/imagenet_labels.txt
```

##### [1000 different things](https://github.com/google-coral/test_data/raw/master/imagenet_labels.txt) - Using Inception V3
```
python classify_from_cam.py   --model test_data/inception_v3_299_quant_edgetpu.tflite  --labels test_data/imagenet_labels.txt
```

##### [1000 different things](https://github.com/google-coral/test_data/raw/master/imagenet_labels.txt) - Using MobileNet V1
```
python classify_from_cam.py   --model test_data/mobilenet_v1_1.0_224_quant_edgetpu.tflite  --labels test_data/imagenet_labels.txt
```

##### [1000 different things](https://github.com/google-coral/test_data/raw/master/imagenet_labels.txt) - Using MobileNet V2
```
python classify_from_cam.py   --model test_data/mobilenet_v2_1.0_224_quant_edgetpu.tflite  --labels test_data/imagenet_labels.txt
```

##### [1000 different things](https://github.com/google-coral/test_data/raw/master/imagenet_labels.txt) - Using MobileNet V3
```
python classify_from_cam.py   --model test_data/tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite  --labels test_data/imagenet_labels.txt
```

##### Pets
```
python classify_from_cam.py   --model test_data/ssd_mobilenet_v1_fine_tuned_pet_edgetpu.tflite  --labels test_data/pet_labels.txt
```
##### [900+ Birds](https://github.com/google-coral/test_data/raw/master/inat_bird_labels.txt)
```
python classify_from_cam.py --model test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite --labels test_data/inat_bird_labels.txt
```
##### [1000+ insects](https://github.com/google-coral/test_data/raw/master/inat_insect_labels.txt)
```
python classify_from_cam.py   --model test_data/mobilenet_v2_1.0_224_inat_insect_quant_edgetpu.tflite  --labels test_data/inat_insect_labels.txt
```

##### [2000+ plants](https://github.com/google-coral/test_data/raw/master/inat_plant_labels.txt)
```
python classify_from_cam.py   --model test_data/mobilenet_v2_1.0_224_inat_plant_quant_edgetpu.tflite  --labels test_data/inat_plant_labels.txt
```

## Models prepared for this camera:
* [MultiPose](https://github.com/ricardodeazambuja/MultiPose-EdgeTPU-RPI0)
* [Automatic License Plate Recognition](https://github.com/ricardodeazambuja/ALPR-EdgeTPU-RPI0)
* [Face Mask Detection (Mask, No Mask, Poor Mask)](https://github.com/ricardodeazambuja/MaskDetection-EdgeTPU-RPI0)

## Other possible sources for TFLite models:
* https://coral.ai/models/all/
* https://coral.ai/examples/
* https://modelplace.ai/models
* https://github.com/Qengineering
* https://www.tensorflow.org/lite/guide/hosted_models
