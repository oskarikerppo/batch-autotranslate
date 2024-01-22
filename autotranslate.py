import os
from googletrans import Translator
from tqdm import tqdm


def translate_text(text, target_language="en"):
    # translate text with Google translate
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    translated_text = translation.text
    return translated_text


def read_and_translate_write_file(input_folder, input_file, output_folder):
    input_file_path = os.path.join(input_folder, input_file)

    # Check if the input file exists
    if not os.path.exists(input_file_path):
        print(f"File {input_file} not found in folder {input_folder}")
        return

    # Construct the output file path
    output_file = (
        f"{os.path.splitext(input_file)[0]}-translated{os.path.splitext(input_file)[1]}"
    )
    output_file_path = os.path.join(output_folder, output_file)

    # Open the input file for reading and the output file for writing
    with open(input_file_path, "r") as input_file, open(
        output_file_path, "w"
    ) as output_file:
        # Initialize a variable to store adjacent non-empty lines
        adjacent_lines = []

        # Read lines and count total lines for progress bar
        total_lines = sum(1 for line in input_file)

        # Return to the beginning of the file
        input_file.seek(0)

        with tqdm(total=total_lines, desc="Translating") as pbar:
            for line_number, line in enumerate(input_file, start=1):
                # Special treatment for the first line (replace "fi" with "en" but don't translate)
                if line_number == 1:
                    line = line.replace("fi", "en")
                    output_file.write(line)
                else:
                    # Check if the line contains text (non-empty) and does not start with a number
                    if line.strip() and not line.strip()[0].isdigit():
                        adjacent_lines.append(line.strip())
                    else:
                        # Translate and write the adjacent non-empty lines to the output file
                        if adjacent_lines:
                            translated_line = translate_text(" ".join(adjacent_lines))
                            output_file.write(f"{translated_line}\n")
                            adjacent_lines = []

                        # Write the original line to the output file
                        output_file.write(line)
                pbar.update(1)

        # Translate and write any remaining adjacent non-empty lines at the end of the file
        if adjacent_lines:
            translated_line = translate_text(" ".join(adjacent_lines))
            output_file.write(f"{translated_line}\n")

    print(f"Translated text written to {output_file_path}")


def translate_files_in_folder(input_folder, output_folder, target_language="en"):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List all files in the input folder
    file_list = [
        f
        for f in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, f))
    ]
    print(file_list)

    # Create an overall progress bar for all files
    with tqdm(total=len(file_list), desc="Overall Progress") as pbar:
        # Iterate over all files in the input folder
        for input_file_name in file_list:
            input_file_path = os.path.join(input_folder, input_file_name)

            # Construct the output file path
            output_file_name = f"{os.path.splitext(input_file_name)[0]}-translated{os.path.splitext(input_file_name)[1]}"
            output_file_path = os.path.join(output_folder, output_file_name)

            # Skip directories, process only files, skip already translated files
            if os.path.isfile(output_file_path):
                print("Already translated!")
                pbar.update(1)
            elif os.path.isfile(input_file_path):
                pbar.set_postfix(file=input_file_name)
                read_and_translate_write_file(
                    input_folder, input_file_name, output_folder
                )
                pbar.update(1)


if __name__ == "__main__":
    # Specify the input and output folder paths
    input_folder = "tekstitykset_suomi"
    output_folder = "tekstitykset_englanti"
    target_language = "en"

    # Call the function to translate all files in the input folder
    translate_files_in_folder(input_folder, output_folder, target_language)


"""if __name__ == "__main__":
    # Specify the input and output folder paths and the input file name
    input_folder = "tekstitykset suomi"
    output_folder = "tekstitykset englanti"
    input_file = "t0-esittely.txt"

    # Call the function to read, translate, and write the translated text to a new file
    read_and_translate_write_file(input_folder, input_file, output_folder)"""
