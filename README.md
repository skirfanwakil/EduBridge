# EduBridge

## Scholarship & Educational Assistance Directory

EduBridge is a web-based scholarship and educational assistance platform designed to help students discover relevant scholarship opportunities in a simple and organized way.

The project provides scholarship-related information in one place and allows students to find relevant opportunities using filters such as category and PinCode.

---

## Problem Statement

Students often have difficulty finding suitable scholarships because scholarship information is scattered across different organizations and sources.

The major problems are:

- Scholarship information is available across multiple sources.
- Students may not know which scholarships are relevant to them.
- Finding opportunities based on location can be difficult.
- Students have to spend time searching through different websites.
- Important information such as category, amount, contact details, address and website may not be available in one place.
- Students can miss suitable scholarship opportunities because of the difficulty in discovering them.

EduBridge aims to solve this problem by providing a centralized platform for scholarship and educational assistance information.

---

## Proposed Solution

EduBridge collects scholarship and educational assistance information and presents it through a single web interface.

The platform allows students to:

- View available scholarship opportunities.
- Filter scholarships based on category.
- Search records using PinCode.
- View scholarship and organization details.
- Check scholarship amounts.
- View contact information when available.
- Access the provided website for more information.

The main objective is to reduce the time and effort required to discover relevant scholarship opportunities.

---

## How EduBridge Helps Students

A student can use EduBridge in a simple process:

1. Open the EduBridge website.
2. View the available scholarship records.
3. Select a category from the filter.
4. Enter a PinCode when required.
5. The system retrieves matching records.
6. The student can view the available details.
7. The student can visit the provided website for further information.

This makes scholarship discovery more organized and easier to navigate.

---

## Data Used in EduBridge

The current version of EduBridge uses an Excel file as the data source.

The file is:

`data/EduBridge_Database_Data.xlsx`

The project contains scholarship and educational assistance related information.

The data includes fields such as:

| Field | Description |
|---|---|
| Name | Name of the organization or scholarship-related entity |
| Address | Address associated with the record |
| PinCode | Location PinCode |
| Contact | Contact information |
| Website | Website of the organization |
| Category | Category of the opportunity |
| Amount | Scholarship or assistance amount |

If information is not available for a particular field, it is kept empty/NULL rather than inventing information.

---

## Main Features

### Scholarship Directory

Students can view the available scholarship and educational assistance records in one place.

### Category Filter

Students can filter records according to their category.

Example categories include:

- Education
- Engineering
- Girls
- Merit
- Photography
- Other available categories in the dataset

`All` is used as the default option to display all records.

### PinCode Search

Students can enter a six-digit PinCode to find relevant records associated with that location.

### Scholarship Information

Each record can provide information such as:

- Name
- Address
- PinCode
- Category
- Amount
- Contact
- Website

### Website Access

When a website is available in the database, the student can open it for additional information.

---

## Backend

EduBridge uses **Python Flask** as its backend.

The backend is responsible for:

- Loading the data.
- Reading records from the Excel file.
- Processing search requests.
- Applying category filters.
- Applying PinCode filters.
- Returning filtered results to the frontend.
- Providing API data.

The main backend file is:

`app.py`

---

## How Filtering Works

The filtering process works between the frontend, Flask backend and data source.

```text
Student
   ↓
Selects Filter / Enters PinCode
   ↓
Frontend sends request
   ↓
Python Flask Backend
   ↓
Reads EduBridge Database
   ↓
Applies Filter
   ↓
Matching Records
   ↓
Frontend Displays Results text'''


## File Structure

EduBridge/
│
├── app.py
├── requirements.txt
├── vercel.json
├── README.md
│
├── data/
│   └── EduBridge_Database_Data.xlsx
│
└── templates/
    └── index.html