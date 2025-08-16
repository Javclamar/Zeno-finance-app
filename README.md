# Finance App

A full-stack personal finance management platform with budgeting, transaction tracking, and stock price prediction using LSTM neural networks.



## Features

- **User Authentication**: Secure login/register with JWT.

  <img width="1905" height="851" alt="image" src="https://github.com/user-attachments/assets/f58cc78d-5553-40c3-8151-d0c380c0bfd5" />

- **Budget Management**: Create and track budgets.

<img width="1651" height="647" alt="image" src="https://github.com/user-attachments/assets/92363e5b-15bc-4550-ab68-54dbeca1e5d9" />

- **Transaction Tracking**: Add, search, and visualize income/expenses.

<img width="1371" height="789" alt="image" src="https://github.com/user-attachments/assets/ec1bd589-383c-4d20-b9ba-9078ac3f3e4d" />

- **Dashboard**: Interactive charts and summaries.

  <img width="1908" height="778" alt="image" src="https://github.com/user-attachments/assets/fdcf1e64-61f5-4826-8568-923267befa64" />

- **Stock Prediction**: LSTM-based price forecasting (Python FastAPI backend).

  <img width="1897" height="795" alt="image" src="https://github.com/user-attachments/assets/37f9902c-ad5c-4882-b72e-d0470ad0c019" />

- **RESTful API**: Built with Express and Prisma ORM.
- **Modern Frontend**: Vue 3 + Pinia + Chart.js.

## Project Structure

```
finance-app/
│
├── backend/           # Node.js/Express/Prisma API
│   ├── src/
│   │   ├── controllers/
│   │   ├── middlewares/
│   │   ├── routes/
│   │   ├── services/
│   │   └── app.ts
│   └── prisma/
│
├── src/               # Vue 3 frontend
│   ├── components/
│   ├── views/
│   ├── router/
│   └── main.ts
│
├── lstm_backend/      # Python LSTM prediction service with FastAPI
│   ├── app/
│   │   ├── lstm_functions/
│   │   ├── lstm_utils/
│   │   └── main.py
│   └── requirements.txt
```  

Connected to a PostgreSQL database

## Getting Started

### 1. Backend (Node.js/Express)

```bash
cd backend
npm install
npx prisma migrate dev
npm run dev
```

### 2. Frontend (Vue 3)

```bash
cd src
npm install
npm run dev
```

### 3. LSTM Prediction Service (Python FastAPI)

```bash
cd lstm_backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd app
fastapi dev main.py
```
To execute the training script (after installing the requirements, the venv activated and the Alpaca API keys set up)  

```bash
cd lstm_backend
python -m app.lstm_functions.train
```
To execute the predicting script (after installing the requirements and with the venv activated)  

```bash
cd lstm_backend
python -m app.lstm_functions.predict
```
The training script is set to run everyday at 2am, but this would be in production since FastAPI needs to be running. 
The predictions script is also set to run at the same time, but if you dont run it, loading the stocks section on the app will run the script

## Environment Variables

- **backend/.env**: Set your database URL, JWT_SECRET, PORT to run the backend, CLIENT_ID, CLIENT_SECRET and REDIRECT_URI for Google Oauth2.
- **lstm_backend/.env**: Set your Alpaca API keys and DB connection.

## Usage

- The model is trained wit data until the 06/08/2025, so running the training script is advised to get updated predictions 
- Register/login to manage your finances (trough email and password if Google Oauth hasn't been set up).
- Add transactions and budgets.
- View charts and predictions on the dashboard.
- Use the stock prediction feature for market insights.

## Tech Stack

- **Frontend**: Vue 3, Pinia, Chart.js, FontAwesome, TypeScript
- **Backend**: Node.js, Express, Prisma, PostgreSQL, TypeScript
- **ML Service**: FastAPI, Python, TensorFlow/Keras, scikit-learn, SQLAlchemy

## License

MIT

---

*For questions or contributions, open an issue or pull request!*
