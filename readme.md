# 🧠 String Analyzer Service

A Django REST API that analyzes text strings and stores computed properties such as length, palindrome status, unique characters, and character frequency.

---

## 🚀 Overview

The **String Analyzer Service** accepts a string input, computes its characteristics, and stores the results in a database.  
It also supports listing all analyzed strings, filtering results, and deleting strings by their value.

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework  
- **Database:** SQLite (default)  
- **Environment:** Python 3.12+  
- **Hosting:** Compatible with Railway, Render, Heroku, AWS, etc. 
---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/string-analyzer-service.git
cd string-analyzer-service
2. Create and Activate Virtual Environment
bash
Copy code
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # Mac/Linux
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Run Migrations
bash
Copy code
python manage.py migrate
5. Start the Server
bash
Copy code
python manage.py runserver
🔐 Environment Variables
No external environment variables are required for local development.

🧪 API Endpoints
Method	Endpoint	Description
POST	/api/strings/create/	Analyze and store a new string
GET	/api/strings/	Retrieve all analyzed strings (supports filtering)
DELETE	/api/strings/{string_value}/	Delete a specific string by its text value

🧩 Example Request & Response
✅ Create / Analyze String
POST /api/strings/create/

Request Body

json
Copy code
{
  "value": "madam"
}
Response (201 Created)

json
Copy code
{
  "id": "765cc52b3dbc1bb8ec279ef9c8ec3d0f251c0c92a6ecdc1870be8f7dc7538b21",
  "value": "madam",
  "properties": {
    "length": 5,
    "is_palindrome": true,
    "unique_characters": 3,
    "word_count": 1,
    "sha256_hash": "765cc52b3dbc1bb8ec279ef9c8ec3d0f251c0c92a6ecdc1870be8f7dc7538b21",
    "character_frequency_map": {
      "m": 2,
      "a": 2,
      "d": 1
    }
  },
  "created_at": "2025-10-22"
}
📜 List All Strings
GET /api/strings/

Response

json
Copy code
[
  {
    "id": "3b74dd038604835b4f7cde257ad2f74bf1d607fdb7614fc7dee0a46166ab270b",
    "value": "madman",
    "properties": {
      "length": 6,
      "is_palindrome": false,
      "unique_characters": 4,
      "word_count": 1,
      "sha256_hash": "3b74dd038604835b4f7cde257ad2f74bf1d607fdb7614fc7dee0a46166ab270b",
      "character_frequency_map": {
        "m": 2,
        "a": 2,
        "d": 1,
        "n": 1
      }
    },
    "created_at": "2025-10-22"
  }
]
🗑️ Delete String
DELETE /api/strings/madam/

Response (204 No Content)

css
Copy code
(no content)
Error (404 Not Found)

json
Copy code
{
  "detail": "String does not exist in the system"
}


]
👨‍💻 Author
Buchi Rex-David
📧 rhexmilia06@gmail.com
🔗 GitHub: RexDavid06

🧾 License
This project is open source and available under the MIT License.