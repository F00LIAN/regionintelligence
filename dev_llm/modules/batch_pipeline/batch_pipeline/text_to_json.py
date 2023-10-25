import json
import re
import os
from pathlib import Path
from datetime import datetime
import glob
from utils import JSON_DATA_DIR, RAW_DATA_DIR


# San Jose send to JSON
class San_Jose_to_JSON:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def get_latest_file(self):
        try:
            files = list(self.input_dir.glob("*.txt"))
            if not files:
                return None
            latest_file = max(files, key=os.path.getctime)
            return latest_file
        except Exception as e:
            print(f"Error while getting the latest file: {str(e)}")
            return None

    def extract_from_file(self, filename: Path):
        stack = []
        chapters = []
        try:
            with filename.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line == "":
                        continue
                    # Check for section ID.
                    if re.match(r"\d+\.\d+.*", line):
                        parts = line.split(" ", 1)
                        section_id = parts[0]
                        title = parts[1] if len(parts) > 1 else ""
                        new_section = {
                            "section_id": section_id,
                            "title": title,
                            "content": "",
                            "subsections": [],
                        }

                        # If section_id starts with a new number, start a new chapter.
                        if (
                            len(stack) == 0
                            or section_id.split(".")[0] != stack[0]["section_id"].split(".")[0]
                        ):
                            chapter = {
                                "chapter": section_id.split(".")[0],
                                "sections": [new_section],
                            }
                            chapters.append(chapter)
                            stack = [new_section]
                        else:
                            # Add section to the correct parent.
                            while len(stack) > 1 and (
                                section_id.count(".") <= stack[-1]["section_id"].count(".")
                                or (
                                    section_id.count(".") - stack[-1]["section_id"].count(".")
                                    > 1
                                )
                            ):
                                stack.pop()

                            # Append to parent section's subsections.
                            stack[-1]["subsections"].append(new_section)

                            # Update current section.
                            stack.append(new_section)
                    elif stack:
                        # Otherwise, append line to content.
                        stack[-1]["content"] += (line + "\n") if line else ""

        except Exception as e:
            print(f"Error reading from {filename}: {str(e)}")
        return chapters

    def process_files(self):
        latest_file = self.get_latest_file()
        if not latest_file:
            print("No text files found in the directory.")
            return

        chapters = self.extract_from_file(latest_file)

        # Fetching the current date and formatting it as YYYY-MM-DD
        current_date = datetime.now().strftime('%Y-%m-%d')

        output_filename = "san_jose_" + f"{current_date}.json"
        output_file = self.output_dir / output_filename

        try:
            with output_file.open("w") as f:
                json.dump(chapters, f, indent=4)
            print(f"Data processed and saved to {output_file}")
        except Exception as e:
            print(f"Error writing to {output_file}: {str(e)}")

def san_jose_json():
    INPUT_DIRECTORY = RAW_DATA_DIR / 'san_jose_building_codes'
    OUTPUT_DIRECTORY = JSON_DATA_DIR / 'san_jose_building_codes_json'

    extractor = San_Jose_to_JSON(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
    extractor.process_files()

# San Francisco send to JSON
class San_Francisco_to_JSON:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def get_latest_file(self):
        try:
            files = list(self.input_dir.glob("*.txt"))
            if not files:
                return None
            latest_file = max(files, key=os.path.getctime)
            return latest_file
        except Exception as e:
            print(f"Error while getting the latest file: {str(e)}")
            return None

    def extract_from_file(self, filename: Path):
        stack = []
        chapters = []
        try:
            with filename.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line == "":
                        continue
                    # Check for section ID.
                    if re.match(r"\d+\.\d+.*", line):
                        parts = line.split(" ", 1)
                        section_id = parts[0]
                        title = parts[1] if len(parts) > 1 else ""
                        new_section = {
                            "section_id": section_id,
                            "title": title,
                            "content": "",
                            "subsections": [],
                        }

                        # If section_id starts with a new number, start a new chapter.
                        if (
                            len(stack) == 0
                            or section_id.split(".")[0] != stack[0]["section_id"].split(".")[0]
                        ):
                            chapter = {
                                "chapter": section_id.split(".")[0],
                                "sections": [new_section],
                            }
                            chapters.append(chapter)
                            stack = [new_section]
                        else:
                            # Add section to the correct parent.
                            while len(stack) > 1 and (
                                section_id.count(".") <= stack[-1]["section_id"].count(".")
                                or (
                                    section_id.count(".") - stack[-1]["section_id"].count(".")
                                    > 1
                                )
                            ):
                                stack.pop()

                            # Append to parent section's subsections.
                            stack[-1]["subsections"].append(new_section)

                            # Update current section.
                            stack.append(new_section)
                    elif stack:
                        # Otherwise, append line to content.
                        stack[-1]["content"] += (line + "\n") if line else ""

        except Exception as e:
            print(f"Error reading from {filename}: {str(e)}")
        return chapters

    def process_files(self):
        latest_file = self.get_latest_file()
        if not latest_file:
            print("No text files found in the directory.")
            return

        chapters = self.extract_from_file(latest_file)

        # Fetching the current date and formatting it as YYYY-MM-DD
        current_date = datetime.now().strftime('%Y-%m-%d')

        output_filename = "san_francisco_" + f"{current_date}.json"
        output_file = self.output_dir / output_filename

        try:
            with output_file.open("w") as f:
                json.dump(chapters, f, indent=4)
            print(f"Data processed and saved to {output_file}")
        except Exception as e:
            print(f"Error writing to {output_file}: {str(e)}")

def san_francisco_json():
    INPUT_DIRECTORY = RAW_DATA_DIR / 'san_francisco_building_codes'
    OUTPUT_DIRECTORY = JSON_DATA_DIR / 'san_francisco_building_codes_json'

    extractor = San_Francisco_to_JSON(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
    extractor.process_files()

# Los Angeles County send to JSON
class Los_Angeles_County_to_JSON:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def get_latest_file(self):
        try:
            files = list(self.input_dir.glob("*.txt"))
            if not files:
                return None
            latest_file = max(files, key=os.path.getctime)
            return latest_file
        except Exception as e:
            print(f"Error while getting the latest file: {str(e)}")
            return None

    def extract_from_file(self, filename: Path):
        stack = []
        chapters = []
        try:
            with filename.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line == "":
                        continue
                    # Check for section ID.
                    if re.match(r"\d+\.\d+.*", line):
                        parts = line.split(" ", 1)
                        section_id = parts[0]
                        title = parts[1] if len(parts) > 1 else ""
                        new_section = {
                            "section_id": section_id,
                            "title": title,
                            "content": "",
                            "subsections": [],
                        }

                        # If section_id starts with a new number, start a new chapter.
                        if (
                            len(stack) == 0
                            or section_id.split(".")[0] != stack[0]["section_id"].split(".")[0]
                        ):
                            chapter = {
                                "chapter": section_id.split(".")[0],
                                "sections": [new_section],
                            }
                            chapters.append(chapter)
                            stack = [new_section]
                        else:
                            # Add section to the correct parent.
                            while len(stack) > 1 and (
                                section_id.count(".") <= stack[-1]["section_id"].count(".")
                                or (
                                    section_id.count(".") - stack[-1]["section_id"].count(".")
                                    > 1
                                )
                            ):
                                stack.pop()

                            # Append to parent section's subsections.
                            stack[-1]["subsections"].append(new_section)

                            # Update current section.
                            stack.append(new_section)
                    elif stack:
                        # Otherwise, append line to content.
                        stack[-1]["content"] += (line + "\n") if line else ""

        except Exception as e:
            print(f"Error reading from {filename}: {str(e)}")
        return chapters

    def process_files(self):
        latest_file = self.get_latest_file()
        if not latest_file:
            print("No text files found in the directory.")
            return

        chapters = self.extract_from_file(latest_file)

        # Fetching the current date and formatting it as YYYY-MM-DD
        current_date = datetime.now().strftime('%Y-%m-%d')

        output_filename = "los_angeles_county_" + f"{current_date}.json"
        output_file = self.output_dir / output_filename

        try:
            with output_file.open("w") as f:
                json.dump(chapters, f, indent=4)
            print(f"Data processed and saved to {output_file}")
        except Exception as e:
            print(f"Error writing to {output_file}: {str(e)}")

def los_angeles_county_json():
    INPUT_DIRECTORY = RAW_DATA_DIR / 'los_angeles_county_building_codes'
    OUTPUT_DIRECTORY = JSON_DATA_DIR / 'los_angeles_county_building_codes_json'

    extractor = Los_Angeles_County_to_JSON(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
    extractor.process_files()

# Los Angeles send to JSON
class Los_Angeles_to_JSON:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def get_latest_file(self):
        try:
            files = list(self.input_dir.glob("*.txt"))
            if not files:
                return None
            latest_file = max(files, key=os.path.getctime)
            return latest_file
        except Exception as e:
            print(f"Error while getting the latest file: {str(e)}")
            return None

    def extract_from_file(self, filename: Path):
        stack = []
        chapters = []
        try:
            with filename.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line == "":
                        continue
                    # Check for section ID.
                    if re.match(r"\d+\.\d+.*", line):
                        parts = line.split(" ", 1)
                        section_id = parts[0]
                        title = parts[1] if len(parts) > 1 else ""
                        new_section = {
                            "section_id": section_id,
                            "title": title,
                            "content": "",
                            "subsections": [],
                        }

                        # If section_id starts with a new number, start a new chapter.
                        if (
                            len(stack) == 0
                            or section_id.split(".")[0] != stack[0]["section_id"].split(".")[0]
                        ):
                            chapter = {
                                "chapter": section_id.split(".")[0],
                                "sections": [new_section],
                            }
                            chapters.append(chapter)
                            stack = [new_section]
                        else:
                            # Add section to the correct parent.
                            while len(stack) > 1 and (
                                section_id.count(".") <= stack[-1]["section_id"].count(".")
                                or (
                                    section_id.count(".") - stack[-1]["section_id"].count(".")
                                    > 1
                                )
                            ):
                                stack.pop()

                            # Append to parent section's subsections.
                            stack[-1]["subsections"].append(new_section)

                            # Update current section.
                            stack.append(new_section)
                    elif stack:
                        # Otherwise, append line to content.
                        stack[-1]["content"] += (line + "\n") if line else ""

        except Exception as e:
            print(f"Error reading from {filename}: {str(e)}")
        return chapters

    def process_files(self):
        latest_file = self.get_latest_file()
        if not latest_file:
            print("No text files found in the directory.")
            return

        chapters = self.extract_from_file(latest_file)

        # Fetching the current date and formatting it as YYYY-MM-DD
        current_date = datetime.now().strftime('%Y-%m-%d')

        output_filename = "los_angeles_" + f"{current_date}.json"
        output_file = self.output_dir / output_filename

        try:
            with output_file.open("w") as f:
                json.dump(chapters, f, indent=4)
            print(f"Data processed and saved to {output_file}")
        except Exception as e:
            print(f"Error writing to {output_file}: {str(e)}")

def los_angeles_json():
    INPUT_DIRECTORY = RAW_DATA_DIR / 'los_angeles_building_codes'
    OUTPUT_DIRECTORY = JSON_DATA_DIR / 'los_angeles_building_codes_json'

    extractor = Los_Angeles_to_JSON(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
    extractor.process_files()
    
# California send to JSON
class CaliforniaCodeExtractor:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def get_latest_file(self):
        try:
            files = list(self.input_dir.glob("*.txt"))
            if not files:
                return None
            latest_file = max(files, key=os.path.getctime)
            return latest_file
        except Exception as e:
            print(f"Error while getting the latest file: {str(e)}")
            return None

    def extract_from_file(self, filename: Path):
        stack = []
        chapters = []
        try:
            with filename.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line == "":
                        continue
                    # Check for section ID.
                    if re.match(r"\d+\.\d+.*", line):
                        parts = line.split(" ", 1)
                        section_id = parts[0]
                        title = parts[1] if len(parts) > 1 else ""
                        new_section = {
                            "section_id": section_id,
                            "title": title,
                            "content": "",
                            "subsections": [],
                        }

                        # If section_id starts with a new number, start a new chapter.
                        if (
                            len(stack) == 0
                            or section_id.split(".")[0] != stack[0]["section_id"].split(".")[0]
                        ):
                            chapter = {
                                "chapter": section_id.split(".")[0],
                                "sections": [new_section],
                            }
                            chapters.append(chapter)
                            stack = [new_section]
                        else:
                            # Add section to the correct parent.
                            while len(stack) > 1 and (
                                section_id.count(".") <= stack[-1]["section_id"].count(".")
                                or (
                                    section_id.count(".") - stack[-1]["section_id"].count(".")
                                    > 1
                                )
                            ):
                                stack.pop()

                            # Append to parent section's subsections.
                            stack[-1]["subsections"].append(new_section)

                            # Update current section.
                            stack.append(new_section)
                    elif stack:
                        # Otherwise, append line to content.
                        stack[-1]["content"] += (line + "\n") if line else ""

        except Exception as e:
            print(f"Error reading from {filename}: {str(e)}")
        return chapters

    def process_files(self):
        latest_file = self.get_latest_file()
        if not latest_file:
            print("No text files found in the directory.")
            return

        chapters = self.extract_from_file(latest_file)

        output_filename = latest_file.stem + ".json"
        output_file = self.output_dir / output_filename

        try:
            with output_file.open("w") as f:
                json.dump(chapters, f, indent=4)
            print(f"Data processed and saved to {output_file}")
        except Exception as e:
            print(f"Error writing to {output_file}: {str(e)}")

def california_json():
    INPUT_DIRECTORY = RAW_DATA_DIR / 'california_building_codes'
    OUTPUT_DIRECTORY = JSON_DATA_DIR / 'california_building_codes_json'

    extractor = CaliforniaCodeExtractor(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
    extractor.process_files()
