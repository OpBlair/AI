# ♟️ Chess AI

A full-stack chess application featuring a custom-built **Minimax Engine**. This project demonstrates the intersection of classic game theory and modern web development.

## 🚀 Features

* **Custom Chess Engine:** Built from scratch in Python (no external chess libraries).
* **Minimax Algorithm:** AI looks ahead 3+ moves to determine the optimal strategy.
* **Validation System:** Complete move validation for all pieces (Pawns, Knights, Sliding pieces, etc.).
* **Interactive UI:** Clean, responsive board built with TypeScript and Tailwind CSS.
* **Real-time Communication:** Flask-based REST API handles the heavy computational logic.

---

## 🛠️ Tech Stack

| Component | Technology |
| --- | --- |
| **Frontend** | TypeScript, Tailwind CSS, HTML5 |
| **Backend** | Python, Flask, Flask-CORS |
| **AI Logic** | Minimax Algorithm |

---

## 📁 Project Structure

```text
.
├── backend/
│   ├── app.py             # Flask API routes
│   ├── chessEngine.py     # AI Logic & Move Validation
├── public/
│   ├── board.ts           # UI Logic & Move Handling
│   ├── index.html         # Main Entry Point
│   └── assets/            # Chess Piece SVGs
└── README.md
|__ requirement.txt        #Game dependencies and other external libs

```

---

## ⚡ Getting Started

### 1. Backend Setup

```bash
cd backend
# Create and activate virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip install flask flask-cors

# Start the server
python app.py

```

### 2. Frontend Setup

1. Open `public/index.html` in your browser (or use a Live Server extension in VS Code).
2. Ensure the backend is running on `http://127.0.0.1:5000`.
3. To compile the typescript file: run ```tsc``` in the folder the .tsc file is located
---

## 🧠 How the AI Thinks

The engine uses the **Minimax Algorithm** to evaluate the board. It assigns values to pieces:

* **Pawn:** 100 | **Knight:** 320 | **Bishop:** 330 | **Rook:** 500 | **Queen:** 900 | **King:** 20,000

It simulates every possible move, then simulates every possible response from the opponent, building a "Search Tree" to find the move that maximizes its own score while minimizing the opponent's.

---

## 🚧 Roadmap

* [ ] Implement **Alpha-Beta Pruning** to increase search depth.
* [ ] Add **Castling** and **En Passant** rules.
* [ ] **Piece-Square Tables** (making the AI prefer the center of the board).
* [ ] Checkmate and Stalemate UI indicators.

---
## Troubleshooting
* **Backend Error 500:** Check the terminal for Python Tracebacks.

* **CORS Error:** Ensure the Flask server is running and flask-cors is installed.

## 📄 License

MIT License - Feel free to use this for your own learning!

---
