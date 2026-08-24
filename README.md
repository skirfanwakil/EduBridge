# EduBridge - Flask + Excel Database

EduBridge uses `data/EduBridge_Database_Data.xlsx` as its database.
No MySQL/Aiven connection is required.

## Local run

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Vercel deployment

1. Upload this project to GitHub.
2. Import the repository into Vercel.
3. Deploy. No database environment variables are required.
4. The Excel workbook is bundled with the project and is read by Flask.

## Important

This Excel setup is intended as a read-only database for deployment. Vercel's serverless filesystem should not be treated as a place to permanently write/update Excel records. To change data, edit the Excel file and redeploy.

## API endpoints

- `/` - main website
- `/search` - filters by pincode/category/keyword
- `/api/data` - returns all Excel records as JSON
- `/health` - deployment health check
