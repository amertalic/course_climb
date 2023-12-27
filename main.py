import argparse
from course_statistics import CourseProgressCalculator

def main(root_folder):
    course_progress_calculator = CourseProgressCalculator(root_folder)
    course_progress_calculator._calculate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate course progress')
    parser.add_argument('root_folder', type=str, help='Root folder path for the course')
    args = parser.parse_args()

    main(args.root_folder)
