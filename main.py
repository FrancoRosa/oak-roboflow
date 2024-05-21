from roboflowoak import RoboflowOak
import cv2
import time
import numpy as np


def draw_predictions(frame, predictions, depth):
    for pred in predictions:

        x = int(pred.x)
        y = int(pred.y)
        width = int(pred.width)
        height = int(pred.height)
        class_name = pred.class_name
        confidence = pred.confidence

        # Calculate the depth at the center of the bounding box
        depth_value = depth[y, x] if depth is not None else 0

        # Draw bounding box
        cv2.rectangle(frame, (x - width // 2, y - height // 2),
                      (x + width // 2, y + height // 2), (0, 255, 0), 2)

        # Create label text
        label = f'{class_name}: {confidence:.2f}, Depth: {depth_value:.2f}'

        # Draw label
        label_size, base_line = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top_left = (x - width // 2, y - height // 2 - label_size[1])
        bottom_right = (x - width // 2 + label_size[0], y - height // 2)

        cv2.rectangle(
            frame, top_left, (bottom_right[0], bottom_right[1] + base_line), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, label, (x - width // 2, y - height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)


if __name__ == '__main__':
    # instantiating an object (rf) with the RoboflowOak module
    rf = RoboflowOak(model="trees-88tmr", confidence=0.05, overlap=0.5,
                     version="3", api_key="i28RMMt0uydRjy7g8Pq0", rgb=True,
                     depth=True, device=None, blocking=True)
    # Running our model and displaying the video output with detections
    while True:
        t0 = time.time()
        # The rf.detect() function runs the model inference
        result, frame, raw_frame, depth = rf.detect()
        predictions = result["predictions"]

        # Draw predictions on the frame
        draw_predictions(frame, predictions, depth)

        # timing: for benchmarking purposes
        t = time.time() - t0
        print("FPS ", 1 / t)
        print("PREDICTIONS ", [p for p in predictions])

        # setting parameters for depth calculation
        # comment out the following 2 lines out if you're using an OAK without Depth
        if depth is not None:
            max_depth = np.amax(depth)
            cv2.imshow("depth", depth / max_depth)

        # displaying the video feed as successive frames
        cv2.imshow("frame", frame)

        # how to close the OAK inference window / stop inference: CTRL+q or CTRL+c
        if cv2.waitKey(1) == ord('q'):
            break

    # Clean up
    cv2.destroyAllWindows()
