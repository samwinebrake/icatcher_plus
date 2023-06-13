from typing import Dict, Iterable
import uuid
import shutil
from inference import predict_from_video
from options import parse_arguments_for_testing
import os


class PipelineHandler:
    def __init__(self):
        self.guids_to_videos_paths = {}
        self.running_videos = {}

    def _assert_correct_input(self, json_data: Dict, keys: Iterable):
        missing_keys = [k for k in keys if k not in json_data.keys()]
        assert len(missing_keys) == 0, f"Keys missing form input: {missing_keys}"

    def handle_register(self, json_data: Dict):
        self._assert_correct_input(json_data, {"video_paths"})
        video_paths = json_data["video_paths"]
        video_guids = []

        for vp in video_paths:
            guid = str(uuid.uuid4())
            video_guids.append(guid)
            self.guids_to_videos_paths[guid] = vp

        return {
            "video_guids": video_guids,
            "success": True,
            "error": None,
        }

    def handle_input(self, json_data: Dict):
        self._assert_correct_input(json_data, {"video_path"})
        video_path = json_data["video_path"]
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        video_guid = str(uuid.uuid4())

        output_video_path = f"output/{video_name}"
        manual_args = ["--source", video_path]
        manual_args += ["--output_video_path", output_video_path]

        args = options.parse_arguments_for_testing(manual_args)
        predict_from_video(args)

        self.guids_to_videos_paths[video_guid] = output_video_path
        return {
            "video_guid": video_guid,
            "success": True,
            "error": None,
        }

    def handle_output_audit(self, json_data: Dict):
        """
        Start an audit for a video, auto-creating an audit file

        Args:
            json_data (Dict):
        """

        self._assert_correct_input(json_data, {"video_guid", "corrected_frames"})

        video_guid = json_data["video_guid"]
        corrected_frames = json_data["corrected_frames"]

        video_output_path = self.guids_to_videos_paths[video_guid]
        audited_labels_path = os.path.join(video_output_path, "labels_audit.txt")

        if not os.isfile(audited_labels_path):
            raise ValueError("Could not locate the output annotations file")

        with open(audited_labels_path) as f:
            lines = f.read().split("\n")
        for li in range(len(lines)):
            l = lines[i].replace(" ", ",")
            if not l:
                continue
            frame_num, annotation, confidence = l.split(",")
            if int(frame_num) in corrected_frames:
                annotation = corrected_frames[int(frame_num)]
                confidence = str(1.0)
            lines[li] = f"{frame_num}, {annotation}, {confidence}"
        new_lines = "\n".join(lines)
        with open(audited_labels_path, "w") as f:
            f.write(new_lines)

        return {
            "video_guid": video_guid,
            "success": True,
            "error": None,
        }

    def handle_output_annotations(self, json_data: Dict):
        self._assert_correct_input(json_data, {"video_guid"})
        video_guid = json_data["video_guid"]

        video_output_path = self.guids_to_videos_paths[video_guid]
        labels_path = os.path.join(video_output_path, "labels.txt")
        audited_labels_path = os.path.join(video_output_path, "labels_audit.txt")

        shutil.copy(labels_path, audited_labels_path)

        return {
            "video_guid": video_guid,
            "success": True,
            "error": None,
        }
