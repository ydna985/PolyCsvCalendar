# PolyCsvCalendar 📅

**PolyCsvCalendar** is a utility Python script designed for students at Polytechnique Montréal. It parses official PDF exam schedules (midterms and finals), filters your specific room assignments based on your last name, and generates a `.csv` file ready to import directly into **Google Calendar** or other calendar applications.

---

## ✨ Key Features

* **Smart Filtering:** Extracts your specific exam room or seating block by analyzing last-name ranges (the `Remarque` column) or universal room allocations.
* **Google Calendar Ready:** Outputs a correctly structured CSV file complete with headers (`Subject`, `Start Date`, `Description`, `Location`, etc.).
* **Built-in Motivation:** Randomly assigns an encouraging quote to your calendar event descriptions to keep your spirits high during exam season!

---

## 🛠️ Prerequisites & Installation

Make sure you have Python installed, along with the required libraries (`pdfplumber` and `pandas`).
Checkout the .txt at the root for dependencies.

---

## 🚀 Usage

Run the script from your terminal by providing your family name, your registered courses, and the paths to your PDF schedule files.

### Example Command

```bash
python main.py --name Koutou --classes CHE0501-01 ELE1001-01 --midtermsFile ./CP_Affichage.pdf --finalsFile ./EF-horaire_web.pdf
```

---

## 📋 Command-Line Options

| Option | Required? | Description | Example |
| :--- | :--- | :--- | :--- |
| `--name` | **Yes** | Your family (last) name used for room filtering. | `--name Koutou` |
| `--classes` | **Yes** | List of your courses in `sigle-group` format (space-separated). | `--classes MTH2304-1 CIV8185-1` |
| `--midtermsFile` | No | File path to the official midterm PDF schedule. | `--midtermsFile ./midterms.pdf` |
| `--finalsFile` | No | File path to the official final exam PDF schedule. | `--finalsFile ./finals.pdf` |

---

> **Note:** Once the script finishes execution, you will find your `calendar.csv` file generated right in the root directory, ready to be imported into your calendar app of choice!