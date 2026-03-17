"""
Flask REST API for the AI-Based Sudoku Solver
Endpoints:
  POST /api/solve   — solve a puzzle
  POST /api/validate — validate a puzzle input
  GET  /api/health  — health check
  GET  /api/sample  — return sample puzzles
"""

import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from solver import solve, validate_grid, is_valid_solution, difficulty, count_filled

app = Flask(__name__)
CORS(app)  # Enable CORS for Angular frontend

# ---------------------------------------------------------------------------
# Sample puzzles
# ---------------------------------------------------------------------------
SAMPLES = {
    "easy": {
        "label": "Easy",
        "grid": [
            [5,3,0, 0,7,0, 0,0,0],
            [6,0,0, 1,9,5, 0,0,0],
            [0,9,8, 0,0,0, 0,6,0],

            [8,0,0, 0,6,0, 0,0,3],
            [4,0,0, 8,0,3, 0,0,1],
            [7,0,0, 0,2,0, 0,0,6],

            [0,6,0, 0,0,0, 2,8,0],
            [0,0,0, 4,1,9, 0,0,5],
            [0,0,0, 0,8,0, 0,7,9],
        ]
    },
    "medium": {
        "label": "Medium",
        "grid": [
            [0,0,0, 2,6,0, 7,0,1],
            [6,8,0, 0,7,0, 0,9,0],
            [1,9,0, 0,0,4, 5,0,0],

            [8,2,0, 1,0,0, 0,4,0],
            [0,0,4, 6,0,2, 9,0,0],
            [0,5,0, 0,0,3, 0,2,8],

            [0,0,9, 3,0,0, 0,7,4],
            [0,4,0, 0,5,0, 0,3,6],
            [7,0,3, 0,1,8, 0,0,0],
        ]
    },
    "hard": {
        "label": "Hard",
        "grid": [
            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,3, 0,8,5],
            [0,0,1, 0,2,0, 0,0,0],

            [0,0,0, 5,0,7, 0,0,0],
            [0,0,4, 0,0,0, 1,0,0],
            [0,9,0, 0,0,0, 0,0,0],

            [5,0,0, 0,0,0, 0,7,3],
            [0,0,2, 0,1,0, 0,0,0],
            [0,0,0, 0,4,0, 0,0,9],
        ]
    }
}

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "sudoku-solver-api"})


@app.route("/api/sample", methods=["GET"])
def sample():
    key = request.args.get("difficulty", "easy").lower()
    puzzle = SAMPLES.get(key, SAMPLES["easy"])
    return jsonify({
        "difficulty": puzzle["label"],
        "grid": puzzle["grid"],
        "filled": count_filled(puzzle["grid"])
    })


@app.route("/api/samples", methods=["GET"])
def all_samples():
    return jsonify({
        k: {"label": v["label"], "grid": v["grid"], "filled": count_filled(v["grid"])}
        for k, v in SAMPLES.items()
    })


@app.route("/api/validate", methods=["POST"])
def validate():
    data = request.get_json(force=True)
    grid = data.get("grid")
    valid, msg = validate_grid(grid)
    result = {"valid": valid, "message": msg}
    if valid:
        result["difficulty"] = difficulty(grid)
        result["filled"] = count_filled(grid)
    return jsonify(result)


@app.route("/api/solve", methods=["POST"])
def solve_puzzle():
    data = request.get_json(force=True)
    grid = data.get("grid")

    # Validate
    valid, msg = validate_grid(grid)
    if not valid:
        return jsonify({"success": False, "error": msg}), 400

    diff = difficulty(grid)

    # Solve and time it
    start = time.perf_counter()
    solution = solve(grid)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    if solution is None:
        return jsonify({
            "success": False,
            "error": "No solution exists for this puzzle.",
            "solve_time_ms": elapsed_ms
        }), 422

    verified = is_valid_solution(solution)

    return jsonify({
        "success": True,
        "solution": solution,
        "difficulty": diff,
        "solve_time_ms": elapsed_ms,
        "algorithm": "Constraint Propagation (AC-3) + Backtracking (MRV)",
        "verified": verified
    })


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
