# ♟️ Chess AI Project: Minimax with Alpha-Beta Pruning

This project aims to implement a fully functional Chess game with a strong AI opponent, built to demonstrate core concepts of Artificial Intelligence, specifically **Adversarial Search** and **Heuristic Evaluation**.

-----

## 🚀 Getting Started

### Project Structure

This project follows a clean separation of concerns:

  * `/frontend`: Contains the web interface (HTML, CSS, JavaScript, TypeScript) for the board and user interaction.
  * `/backend`: Contains the Python code that handles game logic, move validation, and the core AI engine.

### Prerequisites

You will need the following installed:

  * **Python 3.x**
  * **A Python Web Framework** (e.g., Flask or Django, as listed in `backend/requirements.txt`)
  * **Web Browser** (for the frontend)
  * **TypeScript**

### Installation and Setup

1.  **Clone the Repository:**
    ```bash
    git clone [this repo]
    cd chess_ai_project
    ```
2.  **Setup Backend Environment:**
    ```bash
    # Create a virtual environment (recommended)
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    # Install dependencies
    pip install -r backend/requirements.txt

    #Install TypeScript
    npm install typescript --save-dev

    #compile it later
    npx tsc
    ```
3.  **Run the Server:**
    ```bash
    # Navigate to the backend directory
    cd backend
    python app.py  # Or the appropriate command to run your Flask/Django app
    ```
4.  **Access the Game:**
    Open your web browser and navigate to the local server address (usually `http://127.0.0.1:5000/` or similar).

-----

## ✨ Features

### Core Game Implementation

  * **Visual Board:** Interactive $8 \times 8$ board implemented with **HTML/CSS (Tailwind)** and high-quality **SVG assets**.
  * **Full Ruleset:** Implements all standard Chess rules, including:
      * Castling (King-side and Queen-side)
      * En Passant
      * Pawn Promotion
      * Check and Checkmate detection
  * **Client-Server Communication:** Uses a RESTful API (Flask) to handle user moves and request the AI's response.

### 🧠 AI Components (The Focus of the Course)

| AI Concept | Implementation Details |
| :--- | :--- |
| **Adversarial Search** | Implemented using the **Minimax Algorithm** to explore the game tree. |
| **Optimization** | Utilizes **Alpha-Beta Pruning** to drastically improve search efficiency and reduce the effective branching factor. |
| **Heuristics** | The AI uses an **Evaluation Function** to score board positions, considering: |
| | - **Material Value** (Standard piece point system) |
| | - **Positional Score** (Control of the center, piece mobility) |
| | - **King Safety** |

-----

## 🛠️ Technology Stack

  * **Frontend:** HTML5, Tailwind CSS, JavaScript ES6
  * **Backend & Logic:** Python 3.x
  * **Framework:** Flask (or chosen framework)

-----

## 📝 Folder Structure Guide

| Folder/File | Purpose |
| :--- | :--- |
| `/backend/chess_engine.py` | **Core AI:** Contains the Minimax, Alpha-Beta, and Evaluation functions. |
| `/backend/app.py` | Server setup, API endpoints (`/move`, `/reset`), and integration of the AI. |
| `/frontend/index.html` | The main game interface HTML. |
| `/frontend/assets/js/chess_script.js` | Handles mouse clicks, move requests to the backend, and updating the board state. |
| `/frontend/assets/images` | Contains the 12 SVG files for the chess pieces. |

-----

## 🤝 Next Steps / Future Enhancements

  * **Iterative Deepening:** Implement ID search for time management.
  * **Transposition Table:** Add a table to store and recall previously searched positions.
  * **Opening Book:** Implement a small database of initial moves for better opening play.

-----
