import numpy as np
import math
import face_recognition

class FaceRec:
    """
    Encapsulates entity recognition and all data associated with it
    Should be used in the following logic:
        if it passes age detection, no reference image, and has 100% confidence, set reference image for current video
        if number of faces in changed from this frame to last, call facerec check
    """

    def __init__(self):
        self.ref_img_path = None
        self.selected_bbox = None
        self.known_faces = list()
        self.moving_avg_bboxes = list()
        self.window = 0

    def convert_bounding_boxes(self, bboxes):
        """
        Converts pipeline bounding box for use in face recognition
        param bbox: bounding boxes in [left, top, width, height] form
        :return: bboxes in [top, right, bottom, left]
        """
        faces = []
        for bbox in bboxes:
            left = bbox[0]
            top = bbox[1]
            w = bbox[2]
            h = bbox[3]
                        
            right = w + left
            bottom = top - h

            faces.append([top, right, bottom, left])
        return faces
        

    def get_ref_image(self, img_path):
        """
        If the user passes a reference image file path to the command line, it will be grabbed from here
        param img_path: Path to the reference image to be used by face recognition
        """
        img = face_recognition.load_image_file(img_path)
        self.known_faces.append(face_recognition.face_encodings(img)[0])

    def generate_ref_image(self, bbox, frame):
        """
        Save a bounded location as a reference image

        param bbox: The bounding box that contains the user's reference image
        param frame: The frame that the bounding box is being used in
        """
        self.selected_bbox = bbox
        self.known_faces.append(
            face_recognition.face_encodings(frame, known_face_locations=[bbox])[0]
        )


    def replace_generated_ref(self, bbox, frame):
        cur_top = self.selected_bbox[0]
        cur_left = self.selected_bbox[1]
        cur_bot = self.selected_bbox[2]
        cur_right = self.selected_bbox[3]

        new_top = bbox[0]
        new_bot = bbox[2]

        if new_top < cur_top and new_bot < cur_bot:
            self.selected_bbox = bbox
            self.known_faces = list()
            print("Swapping reference")
            self.known_faces.append(face_recognition.face_encodings(frame, known_face_locations=[bbox])[0])

    def facerec_check(self, frame, device="cpu"):
        face_locations = []
        face_encodings = []


        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s), note that tolerance is low
            match = face_recognition.compare_faces(
                self.known_faces, face_encoding, tolerance=0.10
            )

            if match[0]:
                #returns in [top, right, bottom, left] format
                top = face_locations[0][0]
                right = face_locations[0][1]
                bottom = face_locations[0][2]
                left = face_locations[0][3]
                
                h = top - bottom
                w =  right - left
                
                #We want left, top, width, height
                return (top, left, w, h)
            else:
                return None
    
    def get_moving_avg_dist(self, frame):
        
        if len(self.moving_avg_bboxes) > self.window: #If there are enough bboxes to form a window
            avg_bbox = [sum(sub_list)/len(sub_list) for sub_list in zip(*self.moving_avg_bboxes)[-(self.window):]]
            
        else: #Take average of available bounding boxes
            avg_bbox = [sum(sub_list)/len(sub_list) for sub_list in zip(*self.moving_avg_bboxes)]
        
        avg_bbox = list(map(int, avg_bbox))
        
        face_encodings = face_recognition.face_encodings(frame, known_face_locations=[avg_bbox])[0]
            
        distance = face_recognition.face_distance(self.known_faces, face_encodings)[0]
        
        return distance, avg_bbox

    def get_window_distances(self, current_bbox):
        distances = None
        if len(self.moving_avg_bboxes) == 0:
            return None

        current_bbox_center = self.get_bbox_center(current_bbox)
        
        center = self.get_bbox_center(self.moving_avg_bboxes[-1])
        distance = math.dist(current_bbox_center, center)

        return distance

    def get_bbox_center(self, bbox):
        x_center = bbox[0] + int((bbox[2]-bbox[0])/2)
        y_center = bbox[1] + int((bbox[3]-bbox[1])/2)
        return (x_center, y_center)

    def get_bbox_area(self, bbox):
        cur_top = bbox[0]
        cur_left = bbox[1]
        w  = bbox[2]
        h = bbox[3]

        return w * h

    def select_face(self, bboxes, frame, opt):
        """
        selects a correct face from candidates bbox in frame
        :param bboxes: the bounding boxes of candidates
        :param frame: the frame
        :return: the cropped face and its bbox data
        """
        
        target_distance = None
        target_index = 0
        feature_distances = list()

        if opt.use_facerec == "reference" and len(self.known_faces) == 0:
                fr.get_ref_image(opt.facerec_ref)

        #encode new bounding boxes
        for i, bbox in enumerate(bboxes):
            area = self.get_bbox_area(bbox)
            if area < 1000:
                if len(bboxes) == 1:
                    return None
                continue
            if area > 1000: #Ensures that bounding box is not a reflection based on its area
                print(area)
                if opt.use_facerec == "bbox" and len(self.known_faces) == 0: #If no known faces, generate a reference image
                    self.generate_ref_image(bbox, frame)
            
                distance = self.get_window_distances(bbox)
            
                if distance is None or distance < 1.0:
                 #if len(self.selected_bbox) > 0:
                  #  self.replace_generated_ref(bbox, frame)
                    face_encodings = face_recognition.face_encodings(frame, known_face_locations=[bbox])[0]

                    feature_distance = face_recognition.face_distance(self.known_faces, face_encodings)[0]
                    feature_distances.append(feature_distance)
 
                    if target_distance == None or feature_distance < target_distance:
                        target_distance = feature_distance
                        print(target_distance)
                        target_index = i

        if len(self.known_faces) == 0 or (target_distance is not None and target_distance > 0.45) or target_index == None:
            print("Returning None")
            return None
        
        self.moving_avg_bboxes.append(bboxes[target_index])
        return bboxes[target_index]
                
    def select_face_preprocessing(self, bboxes, frame):
        
        face_encodings = face_recognition.face_encodings(frame, known_face_locations=bboxes)
        target_distance = None
        target_index = 0

        for i, bbox in enumerate(bboxes):
            face_encoding = face_recognition.face_encodings(frame, known_face_locations=[bbox])[0]
            distance = face_recognition.face_distance(self.known_faces, face_encoding)[0]

            if target_distance == None or distance < target_distance:
                target_distance = distance
                target_index = i
        
        face = bbox[target_index]
        selected_face = target_index

        crop_img = frame[face[1]:face[1] + face[3], face[0]:face[0] + face[2]]
                                        # resized_img = cv2.resize(crop_img, (100, 100))
        resized_img = crop_img  # do not lose information in pre-processing step!
        face_box = np.array([face[1], face[1] + face[3], face[0], face[0] + face[2]])
        img_shape = np.array(frame.shape)
        ratio = np.array([face_box[0] / img_shape[0], face_box[1] / img_shape[0],
                    face_box[2] / img_shape[1], face_box[3] / img_shape[1]])
        face_size = (ratio[1] - ratio[0]) * (ratio[3] - ratio[2])
        face_ver = (ratio[0] + ratio[1]) / 2
        face_hor = (ratio[2] + ratio[3]) / 2
        face_height = ratio[1] - ratio[0]
        face_width = ratio[3] - ratio[2]
        feature_dict = {
            'face_box': face_box,
            'img_shape': img_shape,
            'face_size': face_size,
            'face_ver': face_ver,
            'face_hor': face_hor,
            'face_height': face_height,
            'face_width': face_width
            }
        return selected_face, feature_dict, resized_img
