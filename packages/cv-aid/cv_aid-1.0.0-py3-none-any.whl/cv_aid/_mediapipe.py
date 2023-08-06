# pylint: disable=C0103

import numpy as np
import mediapipe as mp


class _Mediapipe:
    """Provides a class for loading and using mediapipe models."""

    def __init__(self, torso_size_multiplier=2.5):
        """Initializes Mediapipe."""

        # Multiplier to apply to the torso to get minimal body size.
        self._torso_size_multiplier = torso_size_multiplier
        "Multiplier to apply to the torso to get minimal body size."

        self.face_detector = mp.solutions.face_detection
        """Face detector."""

        self.hands_detector = mp.solutions.hands
        """Hands detector."""

        self.pose_detector = mp.solutions.pose
        """Pose detector."""
        self.pose_landmark_names = [
            "nose",
            "left_eye_inner",
            "left_eye",
            "left_eye_outer",
            "right_eye_inner",
            "right_eye",
            "right_eye_outer",
            "left_ear",
            "right_ear",
            "mouth_left",
            "mouth_right",
            "left_shoulder",
            "right_shoulder",
            "left_elbow",
            "right_elbow",
            "left_wrist",
            "right_wrist",
            "left_pinky_1",
            "right_pinky_1",
            "left_index_1",
            "right_index_1",
            "left_thumb_2",
            "right_thumb_2",
            "left_hip",
            "right_hip",
            "left_knee",
            "right_knee",
            "left_ankle",
            "right_ankle",
            "left_heel",
            "right_heel",
            "left_foot_index",
            "right_foot_index",
        ]

    def detect_faces(self, image: np.ndarray, **kwargs):
        """Detects faces in an image.

        Args:
          image: image to detect faces in
          kwargs: kwargs for process
          image: np.ndarray:
          **kwargs:

        Returns:
          list of rectangles containing faces

        """

        # Get faces and scores
        faces_ = self.face_detector.process(image, **kwargs)
        if faces_.detections:
            return faces_.detections
        return []

    def detect_hands(self, image: np.ndarray, **kwargs):
        """Detects hands in an image.

        Args:
          image: image to detect hands in
          kwargs: kwargs for process
          image: np.ndarray:
          **kwargs:

        Returns:
          list of rectangles containing hands

        """

        # Get hands and scores
        results = self.hands_detector.process(image, **kwargs)
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks
        return []

    def detect_pose(self, image: np.ndarray, **kwargs):
        """Detects pose in an image.

        Args:
          image: image to detect pose in
          kwargs: kwargs for process
          image: np.ndarray:
          **kwargs:

        Returns:
          list of rectangles containing pose

        """

        # Get pose and scores
        results = self.pose_detector.process(image, **kwargs)
        if results.pose_landmarks:
            return results.pose_landmarks
        return []

    def left_wrist_angle(self, landmarks):
        """Calculates left wrist angle.

        Args:
          landmarks: pose landmarks

        Returns:
          float: wrist angle in degrees

        """

        # Get wrist and elbow.
        wrist = landmarks[self.pose_landmark_names.index("left_wrist")]
        elbow = landmarks[self.pose_landmark_names.index("left_elbow")]

        # Calculate angle.
        angle = np.arctan2(
            self._get_distance(wrist, elbow)[1], self._get_distance(wrist, elbow)[0]
        )
        return angle * 180 / np.pi

    def right_wrist_angle(self, landmarks):
        """Calculates right wrist angle.

        Args:
          landmarks: pose landmarks

        Returns:
          float: wrist angle in degrees

        """

        # Get wrist and elbow.
        wrist = landmarks[self.pose_landmark_names.index("right_wrist")]
        elbow = landmarks[self.pose_landmark_names.index("right_elbow")]

        # Calculate angle.
        angle = np.arctan2(
            self._get_distance(wrist, elbow)[1], self._get_distance(wrist, elbow)[0]
        )
        return angle * 180 / np.pi

    def is_left_hand_open(self, landmarks, threshold=90):
        """Checks if left hand is open.

        Args:
          landmarks: pose landmarks
          threshold: threshold for hand openness

        Returns:
          bool: True if left hand is open

        """

        angle = self.left_wrist_angle(landmarks)
        return angle > threshold

    def is_right_hand_open(self, landmarks, threshold=90):
        """Checks if right hand is open.

        Args:
          landmarks: pose landmarks
          threshold: threshold for hand openness

        Returns:
          bool: True if right hand is open

        """

        angle = self.right_wrist_angle(landmarks)
        return angle > threshold

    def head_angle(self, landmarks):
        """Calculates head angle.

        Args:
          landmarks: pose landmarks

        Returns:
          float: head angle in degrees

        """

        # Get head and neck.
        head = landmarks[self.pose_landmark_names.index("nose")]
        neck = landmarks[self.pose_landmark_names.index("left_shoulder")]

        # Calculate angle.
        angle = np.arctan2(
            self._get_distance(head, neck)[1], self._get_distance(head, neck)[0]
        )
        return angle * 180 / np.pi

    def is_head_down(self, landmarks, threshold=90):
        """Checks if head is down.

        Args:
          landmarks: pose landmarks
          threshold: threshold for head angle

        Returns:
          bool: True if head is down

        """

        angle = self.head_angle(landmarks)
        return angle < threshold

    def is_head_up(self, landmarks, threshold=90):
        """Checks if head is up.

        Args:
          landmarks: pose landmarks
          threshold: threshold for head angle

        Returns:
          bool: True if head is up

        """

        angle = self.head_angle(landmarks)
        return angle > threshold
    

    def _normalize_pose_landmarks(self, landmarks):
        """Normalizes landmarks translation and scale."""
        landmarks = np.copy(landmarks)

        # Normalize translation.
        pose_center = self._get_pose_center(landmarks)
        landmarks -= pose_center

        # Normalize scale.
        pose_size = self._get_pose_size(landmarks, self._torso_size_multiplier)
        landmarks /= pose_size
        # Multiplication by 100 is not required, but makes it eaasier to debug.
        landmarks *= 100

        return landmarks

    def _get_pose_center(self, landmarks):
        """Calculates pose center as point between hips."""
        left_hip = landmarks[self.pose_landmark_names.index("left_hip")]
        right_hip = landmarks[self.pose_landmark_names.index("right_hip")]
        center = (left_hip + right_hip) * 0.5
        return center

    def _get_pose_size(self, landmarks, torso_size_multiplier):
        """Calculates pose size.

        It is the maximum of two values:
        * Torso size multiplied by `torso_size_multiplier`
        * Maximum distance from pose center to any pose landmark
        """
        # This approach uses only 2D landmarks to compute pose size.
        landmarks = landmarks[:, :2]

        # Hips center.
        left_hip = landmarks[self.pose_landmark_names.index("left_hip")]
        right_hip = landmarks[self.pose_landmark_names.index("right_hip")]
        hips = (left_hip + right_hip) * 0.5

        # Shoulders center.
        left_shoulder = landmarks[self.pose_landmark_names.index("left_shoulder")]
        right_shoulder = landmarks[self.pose_landmark_names.index("right_shoulder")]
        shoulders = (left_shoulder + right_shoulder) * 0.5

        # Torso size as the minimum body size.
        torso_size = np.linalg.norm(shoulders - hips)

        # Max dist to pose center.
        pose_center = self._get_pose_center(landmarks)
        max_dist = np.max(np.linalg.norm(landmarks - pose_center, axis=1))

        return max(torso_size * torso_size_multiplier, max_dist)

    def _get_average_by_names(self, landmarks, name_from, name_to):
        lmk_from = landmarks[self.pose_landmark_names.index(name_from)]
        lmk_to = landmarks[self.pose_landmark_names.index(name_to)]
        return (lmk_from + lmk_to) * 0.5

    def _get_distance_by_names(self, landmarks, name_from, name_to):
        lmk_from = landmarks[self.pose_landmark_names.index(name_from)]
        lmk_to = landmarks[self.pose_landmark_names.index(name_to)]
        return self._get_distance(lmk_from, lmk_to)

    def _get_distance(self, lmk_from, lmk_to):
        return lmk_to - lmk_from

    def _get_pose_distance_embedding(self, landmarks):
        """Converts pose landmarks into 3D embedding.

        We use several pairwise 3D distances to form pose embedding. All distances
        include X and Y components with sign. We different types of pairs to cover
        different pose classes. Feel free to remove some or add new.

        Args:
        landmarks - NumPy array with 3D landmarks of shape (N, 3).

        Result:
        Numpy array with pose embedding of shape (M, 3) where `M` is the number of
        pairwise distances.
        """
        embedding = np.array(
            [
                # One joint.
                self._get_distance(
                    self._get_average_by_names(landmarks, "left_hip", "right_hip"),
                    self._get_average_by_names(
                        landmarks, "left_shoulder", "right_shoulder"
                    ),
                ),
                self._get_distance_by_names(landmarks, "left_shoulder", "left_elbow"),
                self._get_distance_by_names(landmarks, "right_shoulder", "right_elbow"),
                self._get_distance_by_names(landmarks, "left_elbow", "left_wrist"),
                self._get_distance_by_names(landmarks, "right_elbow", "right_wrist"),
                self._get_distance_by_names(landmarks, "left_hip", "left_knee"),
                self._get_distance_by_names(landmarks, "right_hip", "right_knee"),
                self._get_distance_by_names(landmarks, "left_knee", "left_ankle"),
                self._get_distance_by_names(landmarks, "right_knee", "right_ankle"),
                # Two joints.
                self._get_distance_by_names(landmarks, "left_shoulder", "left_wrist"),
                self._get_distance_by_names(landmarks, "right_shoulder", "right_wrist"),
                self._get_distance_by_names(landmarks, "left_hip", "left_ankle"),
                self._get_distance_by_names(landmarks, "right_hip", "right_ankle"),
                # Four joints.
                self._get_distance_by_names(landmarks, "left_hip", "left_wrist"),
                self._get_distance_by_names(landmarks, "right_hip", "right_wrist"),
                # Five joints.
                self._get_distance_by_names(landmarks, "left_shoulder", "left_ankle"),
                self._get_distance_by_names(landmarks, "right_shoulder", "right_ankle"),
                self._get_distance_by_names(landmarks, "left_hip", "left_wrist"),
                self._get_distance_by_names(landmarks, "right_hip", "right_wrist"),
                # Cross body.
                self._get_distance_by_names(landmarks, "left_elbow", "right_elbow"),
                self._get_distance_by_names(landmarks, "left_knee", "right_knee"),
                self._get_distance_by_names(landmarks, "left_wrist", "right_wrist"),
                self._get_distance_by_names(landmarks, "left_ankle", "right_ankle"),
                # Body bent direction.
                # self._get_distance(
                #     self._get_average_by_names(landmarks, 'left_wrist', 'left_ankle'),
                #     landmarks[self._landmark_names.index('left_hip')]),
                # self._get_distance(
                #     self._get_average_by_names(landmarks, 'right_wrist', 'right_ankle'),
                #     landmarks[self._landmark_names.index('right_hip')]),
            ]
        )

        return embedding


