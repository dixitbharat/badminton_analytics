import cv2
import torch
from scipy.spatial import distance as dist
import time

# Load YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s_model.pt', source='local')

# Define classes
classes = ['player', 'shuttlecock', 'racket']

# Define boundaries of the badminton court quadrants (x_min, y_min, x_max, y_max)
court_quadrants = {
    'top_left': (0, 0, 500, 250),
    'top_right': (500, 0, 1000, 250),
    'bottom_left': (0, 250, 500, 500),
    'bottom_right': (500, 250, 1000, 500)
}

# Initialize variables to store time spent in each quadrant
quadrant_times = {quadrant: 0 for quadrant in court_quadrants.keys()}

# Function to detect objects using YOLOv5
def detect_objects(frame):
    results = model(frame)
    boxes = []
    confidences = []
    class_ids = []
    for label, box, conf in zip(results.names, results.xyxy[0], results.xyxy[0].scores):
        label = label.cpu().numpy()
        if label in [0, 1, 2]:  # Consider player, shuttlecock, and racket classes
            boxes.append(box[:4].cpu().numpy())
            confidences.append(conf.cpu().numpy())
            class_ids.append(label)
    return boxes, confidences, class_ids

# Function to calculate force exerted on the shuttlecock
def calculate_force(centroid_list, fps, mass=0.005, g=9.81):
    if len(centroid_list) < 2:
        return None
    displacement = dist.euclidean(centroid_list[0], centroid_list[-1])
    time = len(centroid_list) / fps
    velocity = displacement / time
    force = mass * g * velocity
    return force

# Function to calculate shuttle velocity
def calculate_shuttle_velocity(centroid_list, fps):
    if len(centroid_list) < 2:
        return None
    displacement = dist.euclidean(centroid_list[0], centroid_list[-1])
    time = len(centroid_list) / fps
    velocity = displacement / time
    return velocity

# Function to calculate time spent in each quadrant
def calculate_quadrant_times(centroid_list, fps):
    global quadrant_times
    if len(centroid_list) < 2:
        return
    for centroid1, centroid2 in zip(centroid_list[:-1], centroid_list[1:]):
        for quadrant, boundaries in court_quadrants.items():
            if is_within_quadrant(centroid2, boundaries) and not is_within_quadrant(centroid1, boundaries):
                quadrant_times[quadrant] += 1 / fps

# Function to check if a point is within a quadrant
def is_within_quadrant(point, boundaries):
    x, y = point
    x_min, y_min, x_max, y_max = boundaries
    return x_min <= x <= x_max and y_min <= y <= y_max

# Function to process video
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    prev_time = time.time()
    prev_shuttle_centroid = None
    shuttle_centroid_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        boxes, confidences, class_ids = detect_objects(frame)
        for i in range(len(boxes)):
            if classes[class_ids[i]] == 'shuttlecock' and confidences[i] > 0.5:
                shuttle_centroid = ((boxes[i][0] + boxes[i][2]) // 2, (boxes[i][1] + boxes[i][3]) // 2)
                shuttle_centroid_list.append(shuttle_centroid)
                force = calculate_force(shuttle_centroid_list, fps)
                if force is not None:
                    cv2.putText(frame, f"Force exerted on shuttle: {force:.2f} N", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                velocity = calculate_shuttle_velocity(shuttle_centroid_list, fps)
                if velocity is not None:
                    cv2.putText(frame, f"Shuttle Velocity: {velocity:.2f} m/s", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif classes[class_ids[i]] == 'player' and confidences[i] > 0.5:
                pass
            elif classes[class_ids[i]] == 'racket' and confidences[i] > 0.5:
                pass
        calculate_quadrant_times(shuttle_centroid_list, fps)
        for i, (quadrant, time) in enumerate(quadrant_times.items()):
            cv2.putText(frame, f"Time in {quadrant}: {time:.2f} s", (50, 150 + i * 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "input_video.mkv"  # Path to your video file
    process_video(video_path)
