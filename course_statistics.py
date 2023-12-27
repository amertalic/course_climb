import os
import re
from typing import List, Union

from moviepy.editor import VideoFileClip


class VideoProcessor:
    """Processes video files and calculates their duration in hours."""

    def __init__(self, video_path):
        """
        :param video_path: The path to the video file.
        """
        self.video_path = video_path

    def get_duration(self) -> Union [int, float]:
        """
        :return: The duration of the video file in hours.
        """
        try:
            video_clip = VideoFileClip(self.video_path)
            return video_clip.duration / 3600  # Convert to hours
        except Exception as e:
            print(f"Error processing {self.video_path}: {e}")
            return 0


class CourseFolderProcessor:
    """Processes a course folder, calculating the total duration of video files in it."""

    def __init__(self, course_folder: str):
        """
        :param course_folder: The path to the course folder.
        """
        self.course_folder = course_folder

    def _process(self) -> int:
        """
        :return: The total duration of video files in the course folder in hours.
        """
        total_duration = 0
        for root, dirs, files in os.walk(self.course_folder):
            for file in files:
                video_path = os.path.join(root, file)
                if any(video_path.lower().endswith(ext) for ext in ('.mp4', '.avi', '.mkv', '.mov', '.wmv')):
                    video_processor = VideoProcessor(video_path)
                    total_duration += video_processor.get_duration()
        return total_duration


class CourseProgressCalculator:
    """Calculates the progress of a course by analyzing the duration of video sections."""

    def __init__(self, root_folder: str):
        """
        :param root_folder: The path to the root folder containing course sections.
        """
        self.root_folder = root_folder

    @staticmethod
    def format_duration(duration_in_decimal_hours):
        """
        :param duration_in_decimal_hours: Duration in decimal hours.
        :return: Formatted duration string (e.g., '05h 30m').
        """
        total_minutes = duration_in_decimal_hours * 60
        hours = int(total_minutes // 60)
        minutes = int(total_minutes % 60)
        return f"{hours:02d}h {minutes:02d}m"

    def _calculate(self):
        """
        Calculate and print course progress, including section durations and remaining time.
        """
        total_duration = 0
        done_duration = 0
        pattern = r"^\d+" # starts numerically
        sections = set()

        for item in os.listdir(self.root_folder):
            item_path = os.path.join(self.root_folder, item)
            if os.path.isdir(item_path):
                match = re.match(pattern, item)
                course_folder_processor = CourseFolderProcessor(item_path)
                i = course_folder_processor._process()

                if item.startswith('[Done] '):
                    done_duration += i
                    total_duration += i
                elif match:
                    total_duration += i

                if i:
                    sections.add(f"Section duration: {item.split('/')[-1]}: {self.format_duration(i)}")

        def extract_section_number(section: str):
            """Sorts list of strings"""
            match = re.search(r'\d+', section)
            return int(match.group()) if match else 0

        sorted_sections: list[str] = sorted(sections, key=extract_section_number)

        self.print_results(done_duration, total_duration, sorted_sections)

    def print_results(self, done_duration: int, total_duration: int, sorted_sections: list):
        """
        Loops through "formatted" results and prints an end report.
        """
        remaining_duration = total_duration - done_duration
        total_percentage = (done_duration / total_duration) * 100
        remaining_percentage = 100 - total_percentage

        for section in sorted_sections:
            print(section)
        print()
        print(" " * 31 + "|   hours    percentage")
        print("-" * 55)
        print(f"Total course duration (hours): | {self.format_duration(total_duration)}")
        print(f"Done duration (hours):         | {self.format_duration(done_duration)}    - {total_percentage:6.2f}%")
        print(
            f"Remaining duration (hours):    | {self.format_duration(remaining_duration)}    - {remaining_percentage:6.2f}%")
        print("-" * 55)



