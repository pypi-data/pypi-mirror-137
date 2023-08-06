import random
import numpy as np

class DatasetAnnotator():
    """docstring for Annotator"""
    def __init__(self, dataset):
        self.dataset = dataset
        
    def _compute_bounding_boxes(self, experiment_id, padding=10):
        particles, p_types = self.dataset.load_experiment_trajs(experiment_id)
        boxes = []
        for i, p in enumerate(particles):
            x = p[:, 0]
            y = p[:, 1]
            xmin = max(0, int(np.min(x) * 2304/350) - padding)    #TODO: Read this from metadata
            ymin = max(0, int(np.min(y) * 2304/350) - padding)    #TODO: Read this from metadata
            xmax = min(int(np.max(x) * 2304/350) + padding, 2304) #TODO: Read this from metadata
            ymax = min(int(np.max(y) * 2304/350) + padding, 2304) #TODO: Read this from metadata
            class_id = p_types[i]
            boxes.append((xmin, ymin, xmax, ymax, class_id))
        return boxes
 
    def _normalize_bounding_box(self, box):        
        img_width = 2304 #TODO: Read this from metadata
        img_height = 2304 #TODO: Read this from metadata
        xmin, ymin, xmax, ymax, class_id = box 
        return xmin/img_width, ymin/img_height, xmax/img_width, ymax/img_height, class_id

    def _convert_bounding_box_to_xywh(self, box):        
        xmin, ymin, xmax, ymax, class_id = box 
        width = xmax - xmin
        height = ymax - ymin
        x_center  = xmax + xmin
        y_center  = ymax + ymin
        return x_center, y_center, width, height, class_id

    def _process_bounding_boxes(self, boxes, normalize=True, center=True):
        new_boxes = []
        for box in boxes:
            if normalize:
                box = self._normalize_bounding_box(box)
            if center:
                box = self._convert_bounding_box_to_xywh(box)
            new_boxes.append(box)
        return new_boxes

    def _export_yolov5_label(self, experiment_id):
        boxes = self._compute_bounding_boxes(experiment_id)
        boxes = self._process_bounding_boxes(boxes)
        flines = ''
        for x_center, y_center, width, height, class_id in boxes:
            flines += f'{class_id} {x_center} {y_center} {width} {height}\n'
        label_name = self.label_path / f'{experiment_id}.txt'
        with open(label_name, "w") as label_file:
            label_file.write(flines)

    def _create_yolov5_label_folder(self, label_folder_name):
        base_path = self.dataset.path
        self.label_path = base_path / label_folder_name
        self.label_path.mkdir(parents=True, exist_ok=True)

    def _generate_yolov5_labels(self, label_folder_name):
        self._create_yolov5_label_folder(label_folder_name)
        all_experiments = self.dataset.list_all_experiments()
        for experiment_id in all_experiments:
            self._export_yolov5_label(experiment_id)

    def _export_yolov5_imagelist(self, image_list, file_name, prefix=''):
        text = ''
        for image in image_list:
            text += f"{prefix}{image}\n"

        file_path = self.dataset.path / file_name
        # Save the text files with the images lists
        with open(file_path, "w") as text_file:
            text_file.write(text) 

    def _read_image_list(self, shuffled=True):
        # Read all image filenames
        all_experiments = self.dataset.list_all_experiments()
        all_images = [f'{experiment_id}.png' for experiment_id in all_experiments]

        # Shuffle the image list before split it
        if shuffled:
            random.shuffle(all_images)

        return all_images

    def _generate_yolov5_split(self, train, test, val):
        # Check the split adds up to 100% the dataset
        assert abs((train + test + val) - 1) <= 0.00001

        all_images = self._read_image_list()

        # Compute the number of images on each cut
        image_count = len(all_images)
        train_count = int(train * image_count)
        test_count = int(test * image_count)
        val_count = image_count - train_count - test_count

        # Split according the given parameters
        train_images = all_images[:val_count]
        test_images = all_images[val_count:val_count+train_count]
        val_images = all_images[val_count+train_count:]

        # Export each image list to its own text file
        self._export_yolov5_imagelist(train_images, 'images_train.txt', prefix='./images/')
        self._export_yolov5_imagelist(test_images, 'images_test.txt', prefix='./images/')
        self._export_yolov5_imagelist(val_images, 'images_val.txt', prefix='./images/')


    def _generate_yolov5_yaml(self, file_name='cygno.yaml'):
        classes = list(self.dataset.classes.keys())
        Template = f"""
# Train/val/test sets as 1) dir: path/to/imgs, 2) file: path/to/imgs.txt, or 3) list: [path/to/imgs1, path/to/imgs2, ..]
path: {self.dataset.path}  # dataset root dir
train: images_train.txt  # train images (relative to 'path') 128 images
val: images_val.txt  # val images (relative to 'path') 128 images
test: images_test.txt # test images (optional)

# Classes
nc: {len(classes)}  # number of classes
names: {classes}
"""
        file_path = self.dataset.path / file_name
        # Save the text files with the images lists
        with open(file_path, "w") as text_file:
            text_file.write(Template) 

    def create_yolov5_annotations(self, train, test, val, label_folder_name='labels'):
        self._generate_yolov5_labels(label_folder_name)
        self._generate_yolov5_split(train, test, val)
        self._generate_yolov5_yaml()



