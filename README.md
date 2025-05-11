# BuzzHeavier Python Uploader (`buzz.py`)

**Version:** 1.0.0
**Author:** AnonGhostID
**Last Updated:** 2025-05-11

## Overview

`buzz.py` is a Python script designed to upload files to `buzzheavier.com` anonymously. It offers parallel uploads, progress bars for each file, and saves the generated download links to a local file. File names are automatically cleaned by removing spaces and hyphens before uploading.

## Features

*   **Anonymous Uploads:** Uploads files to `w.buzzheavier.com`.
*   **Filename Cleaning:** Automatically removes spaces and hyphens from filenames before uploading (e.g., "My File - 01.mkv" becomes "MyFile01.mkv").
*   **Parallel Uploads:** Uploads multiple files concurrently (default: 4 at a time) to speed up the process.
*   **Individual Progress Bars:** Displays a progress bar for each concurrent upload, showing real-time status.
*   **Link Aggregation:** Collects all successful upload links and saves them to a file named `links.txt` in the same directory as the script.
*   **Wildcard Support:** Easily upload multiple files using shell wildcards (e.g., `*`, `*.mkv`).
*   **Cross-Platform:** Should work on any system with Python 3 and `pip`.

## Prerequisites

Before you can run this script, you need:

1.  **Python 3:** The script is written for Python 3. You can download it from [python.org](https://www.python.org/).
2.  **pip:** Python's package installer. It usually comes with Python 3.

## Installation

1.  **Save the Script:**
    Download or copy the `bhuploader.py` script to a directory on your computer.

2.  **Install Dependencies:**
    The script requires the `requests` and `tqdm` libraries. Open your terminal or command prompt, navigate to the directory where you saved `bhuploader.py`, and run:
    ```bash
    pip install requests tqdm
    ```
    Or, if you have multiple Python versions:
    ```bash
    python3 -m pip install requests tqdm
    ```

## Usage

You can run the script from your terminal or command prompt.

### Basic Command Structure

```bash
python3 bhuploader.py [file1] [file2] ... [fileN]
```

### Examples

1.  **Upload a Single File:**
    ```bash
    python3 bhuploader.py "My Video Episode 01.mp4"
    ```

2.  **Upload Multiple Specific Files:**
    ```bash
    python3 bhuploader.py "document_v1.pdf" "archive_backup.zip" "image-final.jpg"
    ```

3.  **Upload All Files in the Current Directory (using wildcard):**
    ```bash
    python3 bhuploader.py *
    ```
    *Note: The `*` wildcard is expanded by your shell (like Bash or Zsh) into a list of all non-hidden files in the current directory.*

4.  **Upload All `.mkv` Files in the Current Directory:**
    ```bash
    python3 bhuploader.py *.mkv
    ```

### How it Works During Execution

*   The script will process the list of files you provide.
*   It will start uploading files in parallel, up to the configured maximum number of workers (default is 4).
*   You will see individual progress bars for each file being actively uploaded. These bars will appear on separate lines in your terminal.
*   As uploads complete, new files from the queue will begin uploading, maintaining the concurrent upload limit.
*   If a file is not found or an upload fails, an error message will be printed to the standard error stream (stderr), but the script will continue with other files.
*   After all files have been attempted, a file named `links.txt` will be created (or overwritten if it already exists) in the same directory as the script. This file will contain one download link per line for all successfully uploaded files.

### Output

*   **Progress Bars:** Displayed in the terminal during uploads.
*   **`links.txt`:** A text file created upon completion, containing the direct download links. Example content:
    ```
    https://buzzheavier.com/abc123xyz789
    https://buzzheavier.com/def456uvw456
    https://buzzheavier.com/ghi789rst123
    ```

## Configuration

The primary configuration is within the script itself:

*   **Number of Parallel Uploads:**
    You can change the number of concurrent uploads by modifying the `max_workers` variable in the `if __name__ == '__main__':` block of the script.
    ```python
    # ...
    if __name__ == '__main__':
        # ...
        max_workers = 4  # Change this value to your desired number of parallel uploads
        # ...
    ```
    A higher number might speed up uploads if your internet connection and the server can handle it, but it will also consume more resources.

## Troubleshooting

*   **`pip` or `python3` command not found:**
    Ensure Python 3 is installed and its directory (and the Scripts subdirectory for pip) is added to your system's PATH environment variable.
*   **SSL Errors / Connection Errors:**
    These might be due to network issues, firewalls, or temporary problems with `buzzheavier.com`. Check your internet connection. The script uses HTTPS.
*   **Permission Denied (for `links.txt`):**
    Make sure the script has write permissions in the directory where it is located, as it needs to create `links.txt`.
*   **Progress Bars Overlapping (Rare):**
    The script is designed to give each progress bar its own line using the `position` argument in `tqdm`. If you still see issues, it might be related to your specific terminal emulator. `dynamic_ncols=True` helps with resizing.

## Contributing

Feel free to fork this script and suggest improvements or fix bugs.

## License

This script is provided as-is. You are free to use, modify, and distribute it. Consider adding a specific open-source license (e.g., MIT License) if you plan to share it more broadly.

---
