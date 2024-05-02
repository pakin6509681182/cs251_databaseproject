# Stray Home Install Instructions
![strayhome_hoepage](/README_photo/strayhome_homepage.png)
## Dependencies สิ่งที่ต้องใช้ ก่อนที่จะติดตั้ง Stray Home
- Python 3.10.12
- Flask 3.0.3
- Flask_Bcrypt 1.0.1
- pyodbc 5.1.0
- ODBC Driver 17 for SQL Server
- Internet Connection
- Windows / Linux / macOS Computer

## What you need to know สิ่งที่ควรรู้ก่อนการติดตั้ง
Database ของ Stray Home ถูกสร้างขึ้นบน Azure SQL Database ดังนั้นจำเป็นต้องมี Internet Connection ในการเชื่อมต่อกับฐานข้อมูล และต้องได้รับการอนุญาตให้เข้าถึงฐานข้อมูลจากแอดมินด้วย

ซึ่งหากไม่มีสิทธิการเข้าถึง สามารถใช้ Local Database ในเครื่องได้เช่นกัน โดยต้องเปลี่ยน Connection String ในไฟล์ `app.py` จาก `azure` เป็น `local` และต้องสร้าง Table ตามที่ระบุในไฟล์ `query/CreateTable.sql`
## How to install dependencies วิธีการติดตั้ง Dependencies
Windows:
1. Install Python 3.10.12 from [Python Official Website](https://www.python.org/downloads/release/python-31012/)
2. Check if Python 3.10.12 and pip is installed by running `python --version` and `pip --version` in Command Prompt
1. Clone Repository using git `git clone https://github.com/pakin6509681182/cs251_databaseproject.git`
2. Install all required packages by running `pip install -r requirements.txt` in the project directory
3. Install ODBC Driver 17 for SQL Server (Windows) from [Microsoft Official Website](https://go.microsoft.com/fwlink/?linkid=2266337)
4. Done!

Linux :
1. Check if Python 3.10.12 is installed by running `python3 --version` in terminal
1. Clone Repository using git `git clone https://github.com/pakin6509681182/cs251_databaseproject.git`
2. Install all required packages by running `pip install -r requirements.txt` in the project directory
3. Follow instructions on [Microsoft Official Website](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=alpine18-install%2Cubuntu17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline#17) to install ODBC Driver 17 for SQL Server in different Linux distributions
4. Done!

## How to run Stray Home วิธีการเริ่มต้นใช้งาน Stray Home
1. Open Command Prompt / Terminal
2. Change directory to the project directory
3. Run `python app.py` in Command Prompt / `python3 app.py` in Terminal
4. Open your web browser and go to `http://127.0.0.1:5000/homepage`