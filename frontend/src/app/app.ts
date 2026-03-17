import { Component, OnInit, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';


const EMPTY_GRID = (): number[][] =>
  Array.from({ length: 9 }, () => Array(9).fill(0));

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',
  styleUrls: ['./app.scss']
})
export class App implements OnInit {
  private API = 'http://localhost:5000/api';

  displayGrid: number[][] = EMPTY_GRID();
  originalGrid: number[][] = EMPTY_GRID();
  givenMask: boolean[][] = Array.from({ length: 9 }, () => Array(9).fill(false));

  selectedCell: { r: number; c: number } | null = null;
  loading = false;
  hasSolution = false;
  stats: any = null;
  errorMsg = '';

  constructor(private http: HttpClient) {}

  ngOnInit(): void { this.loadSample('easy'); }

  loadSample(level: string) {
    this.hasSolution = false; this.stats = null; this.errorMsg = '';
    this.http.get<any>(`${this.API}/sample?difficulty=${level}`).subscribe({
      next: (res) => this.setGrid(res.grid),
      error: () => this.setGrid([
        [5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9],
      ])
    });
  }

  setGrid(grid: number[][]) {
    this.displayGrid = grid.map(r => [...r]);
    this.originalGrid = grid.map(r => [...r]);
    this.givenMask = grid.map(r => r.map(v => v !== 0));
    this.hasSolution = false;
  }

  isGiven(r: number, c: number) { return this.givenMask[r][c]; }

  selectCell(r: number, c: number) {
    if (this.isGiven(r, c)) { this.selectedCell = null; return; }
    this.selectedCell = { r, c };
  }

  @HostListener('window:keydown', ['$event'])
  onKey(e: KeyboardEvent) {
    if (!this.selectedCell) return;
    const { r, c } = this.selectedCell;
    if (e.key >= '1' && e.key <= '9') this.inputDigit(+e.key);
    else if (e.key === 'Backspace' || e.key === 'Delete' || e.key === '0') this.inputDigit(0);
    else if (e.key === 'ArrowRight') this.move(r, c, 0, 1);
    else if (e.key === 'ArrowLeft')  this.move(r, c, 0, -1);
    else if (e.key === 'ArrowDown')  this.move(r, c, 1, 0);
    else if (e.key === 'ArrowUp')    this.move(r, c, -1, 0);
  }

  move(r: number, c: number, dr: number, dc: number) {
    const nr = (r+dr+9)%9, nc = (c+dc+9)%9;
    if (!this.givenMask[nr][nc]) this.selectedCell = { r: nr, c: nc };
  }

  inputDigit(n: number) {
    if (!this.selectedCell) return;
    const { r, c } = this.selectedCell;
    if (this.givenMask[r][c]) return;
    this.displayGrid[r][c] = n;
    this.hasSolution = false; this.stats = null; this.errorMsg = '';
  }

  hasConflict(r: number, c: number): boolean {
    const val = this.displayGrid[r][c];
    if (val === 0) return false;
    for (let i = 0; i < 9; i++) {
      if (i !== c && this.displayGrid[r][i] === val) return true;
      if (i !== r && this.displayGrid[i][c] === val) return true;
    }
    const br = Math.floor(r/3)*3, bc = Math.floor(c/3)*3;
    for (let dr = 0; dr < 3; dr++) for (let dc = 0; dc < 3; dc++) {
      const nr = br+dr, nc = bc+dc;
      if ((nr !== r || nc !== c) && this.displayGrid[nr][nc] === val) return true;
    }
    return false;
  }

  solvePuzzle() {
    this.loading = true; this.errorMsg = ''; this.stats = null;
    this.http.post<any>(`${this.API}/solve`, { grid: this.displayGrid }).subscribe({
      next: (res) => {
        this.loading = false;
        if (res.success) { this.displayGrid = res.solution; this.hasSolution = true; this.stats = res; }
        else this.errorMsg = res.error || 'No solution found.';
      },
      error: (err) => { this.loading = false; this.errorMsg = err?.error?.error || 'API error. Is the Flask server running?'; }
    });
  }

  clearBoard() {
    this.displayGrid = EMPTY_GRID(); this.originalGrid = EMPTY_GRID();
    this.givenMask = Array.from({ length: 9 }, () => Array(9).fill(false));
    this.hasSolution = false; this.stats = null; this.errorMsg = ''; this.selectedCell = null;
  }

  resetToOriginal() {
    this.displayGrid = this.originalGrid.map(r => [...r]);
    this.hasSolution = false; this.stats = null; this.errorMsg = ''; this.selectedCell = null;
  }
}
