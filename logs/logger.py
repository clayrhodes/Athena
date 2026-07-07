from datetime import datetime
import os


def save_report(report_text):

    logs_folder = "logs"

    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    file_name = f"athena_report_{timestamp}.txt"
    file_path = os.path.join(logs_folder, file_name)

    with open(file_path, "w") as file:
        file.write(report_text)

    return file_path