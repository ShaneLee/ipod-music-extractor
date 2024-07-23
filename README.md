# iPod Music Extractor

## Overview

If you have an old iPod which is no longer synced to your computer. You will no longer be able to get the music without much faff because all the files are renamed and in ridiculous directories like this;

```
F00 F02 F04 F06 F08 F10 F12 F14 F16 F18 F20 F22 F24 F26 F28 F30 F32 F34 F36 F38 F40 F42 F44 F46 F48
F01 F03 F05 F07 F09 F11 F13 F15 F17 F19 F21 F23 F25 F27 F29 F31 F33 F35 F37 F39 F41 F43 F45 F47 F49
```

This script is a Python tool designed to copy music files from an iPod to a specified destination directory on your machine. It handles various audio file formats, extracts metadata (such as artist, album, title, and year), and organizes the copied files into a structured directory hierarchy.

```
    -> artist / year-album
```

## Features

- **Metadata Extraction:** Retrieves metadata from MP3 and M4A files, and handles other common audio formats.
- **File Organization:** Creates directories based on artist, year, and album information.
- **Duplicate Check:** Skips copying files that already exist in the destination directory and logs this event. This also means you can stop the script and start it again later.
- **Multithreading:** Utilizes multiple threads to improve performance during file copying.

## Requirements

- **Python 3.x:** Ensure Python 3 is installed on your system.
- **Mutagen:** A Python library for handling audio metadata.

## Installation

1. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv myenv
   source myenv/bin/activate 
   ```


## Running

`python extract.py /Volumes/shanes-iPod ~/Desktop/ipod-music/`