# Certificate Generator 🎓

A simple Python script to bulk generate certificates from a CSV file.

## 🚀 Features
- **Bulk Generation**: Generate hundreds of certificates in seconds.
- **Dynamic Text Fitting**: Text automatically shrinks to fit within specified bounding boxes.
- **Customizable**: Easily adjust positions, colors, and fonts.
- **Preview Mode**: Limit generation for quick testing.

## 📁 Project Structure
- `script.py`: The main logic for certificate generation.
- `data.csv`: Your data source (Name, Institute).
- `certificate.png`: The certificate template image.
- `arial_narrow_7.ttf`: Font used for the text.
- `certificates_output/`: Where the magic happens (generated certificates).

## 🛠️ Usage

### 1. Prepare your CSV
Create a file named `data.csv` (or edit the existing one) with the following format:
```csv
Name,Institute
John Doe,Tech University
Jane Smith,Science Institute
```

### 2. Run the Script
To generate **all** certificates:
```bash
python script.py
```

To generate a **limited number** (e.g., for testing):
```bash
python script.py --limit 4
```

### 3. Customizing Positions
Open `script.py` and modify the `NAME_BOX` and `INSTITUTE_BOX` dictionaries:
- `x`, `y`: Top-left coordinates.
- `width`, `height`: Bounding box dimensions.
- `color`: RGB color tuple.
- `max_font_size`: Starting font size.

## 📦 Requirements
- Python 3.x
- Pillow (`pip install Pillow`)

---
Created with ❤️ by Antigravity
