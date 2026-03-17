🌐 Live Demo: https://sudoku-ai-frontend.onrender.com

# 🧩 AI-Based Sudoku Solver

> Intelligent Sudoku solving using **Constraint Propagation (AC-3)** + **Backtracking with MRV Heuristic**
> Flask REST API · Angular Frontend · Real-time solutions in milliseconds

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=flat-square&logo=flask)
![Angular](https://img.shields.io/badge/Angular-17+-DD0031?style=flat-square&logo=angular)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 Project Overview

Sudoku is a classic **Constraint Satisfaction Problem (CSP)**. Each row, column, and 3×3 box must contain unique digits 1–9. This solver applies two-phase AI reasoning:

1. **Constraint Propagation (AC-3)** — eliminates impossible candidate values from each empty cell by propagating constraints across peers (row, column, box). Solves ~80% of standard puzzles alone.
2. **Backtracking + MRV Heuristic** — for remaining ambiguity, the algorithm selects the cell with the **Minimum Remaining Values** and explores possibilities recursively.

The result: even "Expert"-level puzzles solve in **< 5 ms**.

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────┐
│         Angular Frontend             │
│  SudokuGrid · NumPad · StatPanel     │
└───────────────┬──────────────────────┘
                │ HTTP POST /api/solve
                │ { grid: number[][] }
┌───────────────▼──────────────────────┐
│         Flask REST API               │
│  /api/solve  /api/validate           │
│  /api/sample /api/health             │
└───────────────┬──────────────────────┘
                │
┌───────────────▼──────────────────────┐
│       Solver Engine (Python)         │
│  AC-3 Constraint Propagation         │
│  → Backtracking + MRV Heuristic      │
└───────────────┬──────────────────────┘
                │ { solution, difficulty,
                │   solve_time_ms, verified }
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 AC-3 Constraint Propagation | Eliminates impossible candidates cell-by-cell |
| 🔁 MRV Backtracking | Minimum Remaining Values heuristic for fast search |
| ⚡ Real-time API | Flask REST endpoint returns solution in < 5ms |
| 🎮 Interactive Grid | Click cells, use keyboard or numpad to input |
| ✅ Live Conflict Detection | Red highlight on duplicate values instantly |
| 📊 Solution Stats | Difficulty, algorithm used, solve time, verification |
| 🎯 Sample Puzzles | Easy / Medium / Hard preloaded puzzles |
| 🔍 Input Validation | Rejects malformed or unsolvable grids gracefully |

---

## 🛠️ Tech Stack

**Backend:** Python 3.11+ · Flask 3.0 · Flask-CORS · Gunicorn
**Frontend:** Angular 17 · TypeScript · SCSS · HttpClientModule
**Algorithms:** AC-3 (Arc Consistency) · Backtracking · MRV Heuristic

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+, Node.js 18+, Angular CLI

### 1. Clone
```bash
git clone https://github.com/YOUR_USERNAME/sudoku-solver-ai.git
cd sudoku-solver-ai
```

### 2. Backend
```bash
cd backend
pip install -r requirements.txt
python app.py        # http://localhost:5000
```

### 3. Frontend
```bash
cd frontend
npm install
ng serve             # http://localhost:4200
```

---

## 📡 API Reference

### POST /api/solve
```json
// Request
{ "grid": [[5,3,0,0,7,0,0,0,0], ...] }   // 0 = empty

// Response
{
  "success": true,
  "solution": [[5,3,4,...], ...],
  "difficulty": "Medium",
  "solve_time_ms": 1.34,
  "algorithm": "Constraint Propagation (AC-3) + Backtracking (MRV)",
  "verified": true
}
```

### GET /api/sample?difficulty=easy|medium|hard
Returns a preloaded puzzle.

### POST /api/validate — Validate grid format
### GET /api/health — Health check

---

## 🧠 Algorithm Deep Dive

### Phase 1 — Constraint Propagation (AC-3)
Each cell maintains a set of possible candidates (1–9). On each assignment:
- Digit is eliminated from all peers (row, column, box)
- Peer reduced to one candidate → propagated recursively
- Unit with one place for a digit → forced assignment

### Phase 2 — Backtracking with MRV
When propagation stalls: select cell with fewest candidates, try each, recurse, backtrack on contradiction.

---

## 📁 Project Structure

```
sudoku-solver-ai/
├── backend/
│   ├── app.py           # Flask API routes
│   ├── solver.py        # Core AI solving engine
│   └── requirements.txt
├── frontend/
│   ├── src/app/
│   │   ├── app.ts       # Component logic
│   │   ├── app.html     # Grid + numpad + stats
│   │   └── app.scss     # Component styles
│   └── ...
└── README.md
```

---

## 🔮 Future Improvements
- [ ] Sudoku puzzle generator with controllable difficulty
- [ ] Step-by-step solving animation
- [ ] Difficulty classifier using ML
- [ ] 16×16 Sudoku support
- [ ] PWA for offline use

---

## 👩‍💻 Author

**Sunidhi** · Dept. of Computer Applications, PES University, Bengaluru
Under the guidance of **Dr. C. Meenaka**

---
MIT License
