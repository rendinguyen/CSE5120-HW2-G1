# CSE 5120 Homework 2

## Scored tic tac toe and constraint satisfaction

Implement minimax with alpha-beta pruning, negamax with alpha-beta pruning, a testable game controller, and executable CSP formulations. Use the supplied Pygame view to play against your search agent. Your grade comes from function behavior, including hidden test cases, rather than the appearance of your GUI or your ability to beat another student.

**Course:** CSE 5120 Introduction to Artificial Intelligence, Fall 2026. **Total:** 150 points. The original homework carries 15% of the course grade; the course syllabus and Canvas settings determine the final weight. Release date, deadline, late policy, and resubmission settings appear in Canvas. Work individually or in a group of up to four. Submit one packet per group and identify every member and their contributions in REPORT.md.

## 1  Setup and files

Use Python 3.10 or newer. Core code and public tests use only the standard library. Pygame is needed only for visualization. In a terminal inside the extracted starter folder:

```text
python -m unittest discover -s tests_public -v
python -m pip install -r requirements-gui.txt
python large_board_tic_tac_toe.py --size 4 --depth 2
```

The starter intentionally raises NotImplementedError in the functions you must write. Initial test failures are expected. Complete the state functions, search functions, and controller before launching the GUI. Test the CSP functions independently.

| File | Your work |
|---|---|
| GameStatus_5120.py | Complete S1 through S5: terminal test, moves, successors, counts, evaluation. |
| multiAgents.py | Complete M1 and N1: minimax and negamax. |
| game_controller.py | Complete C1 through C4: reset, human move, AI move, status. |
| csp.py | Complete K1, K2, V1 through V4. |
| large_board_tic_tac_toe.py | Supplied renderer. Do not edit or submit for credit. |
| tests_public/test_public.py | Visible checks. Do not edit or submit. Add your own tests separately. |
| REPORT.md and AI_USE.md | Complete the short explanations, testing evidence, contributions, and disclosure. |

Preserve filenames, signatures, and return formats. You may add helpers inside the four submitted Python files. Do not depend on extra modules, NumPy, Pygame, network access, file access, interactive input, or a display in your submitted code. Importing a module must not start a game, create a window, or run a long computation.

## 2  Game rules and score convention

This is **scored tic-tac-toe**, including on a 3 by 3 board. The game continues until every square is filled. A line of three does not end the game. The winner has the most completed length-three windows when the board is full. Equal counts produce a draw. Do not assume the optimal result must match ordinary tic-tac-toe.

The board is square with size 3 through 8. Core functions must support that range. The human chooses O or X and always moves first. The computer takes the other symbol. Moves use zero-based `(row, col)` coordinates, not screen `(x, y)` coordinates. Cell values are **+1 for O, -1 for X, and 0 for empty**. `turn_O=True` means O moves next. Tests may construct arbitrary valid boards and set the turn directly; do not reject a position because mark counts look unusual.

Count each length-three window once in four directions: horizontal, vertical, down-right diagonal, and down-left diagonal. Include off-center diagonals and overlapping windows. Four O marks in a row contain two O triplets. Five contain three. A 4 by 4 all-O board has 24 triplets across all directions. The provided `windows()` iterator already enumerates the windows for you.

`triplet_counts()` returns `(O_count, X_count)` using raw counts. `is_terminal()` returns a bool and does not change the board. `get_moves()` returns empty cells in row-major order. `get_new_state(move)` returns a separate state with one legal mark and a flipped turn. Reject malformed, out-of-range, or occupied moves with ValueError. Preserve the caller's state and all sibling states.

The search evaluation always measures O's advantage:

| Window content | Nonterminal contribution |
|---|---:|
| Three O marks | +100 |
| Two O marks and one empty cell | +10 |
| One O mark and two empty cells | +1 |
| Corresponding X-only patterns | -100, -10, or -1 |
| Both O and X, or entirely empty | 0 |

For `get_scores(False)`, add these contributions over every window. For `get_scores(True)`, return `100 * (O_count - X_count)` and ignore unfinished patterns. Honor the supplied flag even when a test calls the function directly. `get_negamax_scores()` is supplied and delegates to the same evaluation. Do not change the weights or make them depend on the human's chosen symbol.

## 3  Minimax and negamax

Both functions return `(value, best_move)`. A move is a `(row, col)` tuple. At depth zero or a terminal node, return the appropriate evaluation and `None` for the move. **One depth unit is one move by one player.** Depth two examines the current player's move and the opponent's reply. Decrement depth on every recursive call.

`minimax(state, depth, maximizingPlayer, alpha, beta)` returns an O-perspective value. O maximizes; X minimizes. The caller supplies `maximizingPlayer == state.turn_O`. Use alpha-beta pruning in both branches.

`negamax(state, depth, turn_multiplier, alpha, beta)` returns a value from the player-to-move's perspective. The multiplier is +1 for O and -1 for X. Multiply the O-perspective leaf evaluation by that sign. Recursion switches the sign, negates the child's returned value, and passes reversed negated bounds `(-beta, -alpha)`. Implement this negamax recursion yourself; do not delegate it to minimax. For the same state, depth, and unlimited root bounds, the negamax value equals `turn_multiplier * minimax_value`.

For both algorithms:

1. Process `get_moves()` in its given order. Keep the first move when values tie by updating the best move only on strict improvement.
2. Generate each successor only when you are about to search it. Stop immediately when `alpha >= beta`. Return the best value actually found, rather than clamping it to the bound; this is fail-soft alpha-beta.
3. Use the caller's bounds, including finite bounds. A cutoff result may be a bound rather than an exact minimax value.
4. Do not reorder moves, prebuild successors, cache search results, or use random tie-breaking in the graded implementation. These restrictions make expansion tests reproducible. You may explore such optimizations separately after finishing the homework.
5. Access search states through `is_terminal`, `get_scores`, `get_negamax_scores`, `get_moves`, `get_new_state`, and `turn_O`. Tests also use small artificial game trees with this interface. Do not inspect `board_state` or require the exact concrete state class inside the algorithms.
6. Assume valid search inputs: nonnegative integer depth, consistent turn/sign, and alpha less than beta. The core search has no fixed depth cap. The GUI limits selectable depth to keep interaction practical.

A completed game and a nonterminal depth cutoff use different evaluations. Explain that distinction in your report. Larger boards branch quickly; begin with depth one or two. A depth-limited agent is not guaranteed to play a perfect full game.

## 4  Controller and visualization

The supplied constructor validates size, symbol, algorithm, and depth, then calls your `reset()`. The controller supports size 3 through 8 and depth 1 through 4. The human always starts. Complete these methods using the exact contracts in their docstrings:

| Method | Required behavior |
|---|---|
| reset() | Empty the board, restore human's turn, preserve size/symbol/algorithm/depth. Return None. |
| human_move(row, col) | Apply exactly one legal human move and return True. Return False for wrong turn, terminal, invalid, or occupied coordinates without changing the state. Do not invoke AI. |
| ai_move() | On an active AI turn, call the selected search function with the correct depth and bool/sign, apply its returned legal move, and return that move. Otherwise return None with no search or state change. An illegal AI result raises ValueError without changing the state. |
| status() | Return exactly `{'terminal': bool, 'turn': 'O'/'X'/None, 'O': raw_count, 'X': raw_count, 'winner': 'O'/'X'/'Draw'/None}`. The turn is None only at terminal states; the winner is None while active. |

Use `import multiAgents` and call its functions through the module so the controller can be tested with a stubbed search. The grader replaces dependencies for unit tests, then runs your real modules together in integration tests. A scoring bug should not automatically cost all search points.

The GUI uses your controller. Click an empty square to move. Press **3, 4, or 5** to change size, **O or X** to change the human symbol, **M or N** to select minimax or negamax, **Up or Down** to change depth, **R** to reset, and **Escape** to quit. Changing a setting starts a new game. Sizes 6 through 8 can be selected with `--size` at launch. AI search runs in a separate process so Reset and Quit stay responsive. If a search exceeds 15 seconds, the supplied view resets with a lower depth. This GUI guard is separate from the grading timeout.

You are responsible for testing a playable game, but you do not need to design graphics or submit a video. GUI appearance carries no manual points. Functional controller calls are automatically graded without opening a window.

## 5  Constraint satisfaction problems

### Knights

Formulate k labeled knights on an n by n board, with no two attacking. Use variables K0 through K{k-1}. Each variable's domain contains all `(row, col)` cells, in row-major order. The binary constraint for each pair requires distinct cells and forbids absolute coordinate differences `(1,2)` and `(2,1)`.

Implement `knight_domains(n,k)` and `knights_consistent(assignment,n,k)`. The consistency function accepts partial assignments, including `{}`. Check variable names, domain membership, occupied-square conflicts, and attacks among assigned knights. Invalid dimensions cause ValueError in the domain function and False in the consistency function. A zero-knight domain is `{}`. You do not need to solve the general placement problem. Explain the variables, domains, and formal pairwise predicate in REPORT.md.

### Vehicle scheduling

Each of A, B, C, D, and E reserves one `(stop, slot)`. Stops are CGI and JB; slots are 1 through 4. A, B, C use CGI. D and E use JB. B must use slot 1. D must use slot 3 or later. A must use slot 2 or earlier. D must arrive strictly before C leaves, so D's slot is less than C's. No two vehicles may reserve the same slot at the same stop. Vehicles at different stops may share a slot unless the D-before-C constraint prohibits that combination.

Implement:

- `vehicle_domains()`: apply unary restrictions only, before propagating binary constraints. Return domains in increasing slot order.
- `vehicles_consistent(assignment)`: validate partial assignments. Apply a binary constraint only when both variables are assigned. Do not reject a partial assignment merely because inference could show it has no completion.
- `constraint_edges()`: return the undirected constraint graph as sorted pairs with the alphabetically smaller name first. Include each nontrivial binary relation before inference exactly once. Do not include unary restrictions or self-edges.
- `solve_vehicles()`: enumerate all complete valid assignments, without duplicates, using the domain and consistency functions. The grader also replaces those functions with another small finite model to check that the solver does not memorize the five-vehicle answer. Use the dictionary's variable names; do not hard-code a fixed name list inside the solver. Solution order is not graded.

In REPORT.md, express the unary and binary constraints formally and describe the graph. The returned edge list is the automatically graded graph representation; a drawn diagram is optional.

## 6  Testing and rubric

Run the public tests frequently. They illustrate the contract and do not expose all grading cases. Hidden tests include overlap/off-diagonal scoring, both player signs, odd/even depths, terminal and cutoff cases, ties, observed successor-generation traces, invalid actions, resets, partial CSP assignments, all schedules, and complete headless games.

Each graded check runs in a fresh subprocess with a six-second wall-clock limit. Grading uses modest search trees and late-game board positions; it does not require solving an empty 8 by 8 board to completion. Partial credit is proportional to checks passed within each published subcategory. Timeouts and exceptions fail the affected check, not unrelated categories.

| Category | Points |
|---|---:|
| State rules 8 and scoring 12 | 20 |
| Minimax values/moves 25 and pruning 10 | 35 |
| Negamax values/moves 18 and pruning 7 | 25 |
| Controller unit behavior 16 and integration 4 | 20 |
| Knight domains 10 and constraints 15 | 25 |
| Vehicle domains 8, constraints 8, graph 4, enumeration 5 | 25 |
| Total | 150 |

The default grade is fully automated functional credit. REPORT.md and AI_USE.md remain required learning and disclosure evidence. The grader flags missing files but does not pretend to judge explanation quality, GUI aesthetics, or authorship automatically. The instructor may inspect selected submissions or request an explanation under the course policies.

## 7  Submission and academic practice

Upload exactly these six files individually or at the root of one ZIP:

```text
GameStatus_5120.py
multiAgents.py
game_controller.py
csp.py
REPORT.md
AI_USE.md
```

Use the Canvas assignment's selected submission route: Gradescope through Canvas, or a Canvas file upload for local grading. Do not submit both unless instructed. Do not upload the renderer, tests, environments, dependencies, caches, executables, or any instructor-only files. Keep the ZIP under 5 MB. Preserve the file layout so imports work on Linux, where capitalization matters.

Complete the work with your declared group. Do not copy another group's code, a solution key, or hidden tests. Follow the course academic-integrity policy. As in Homework 1, disclose any generative-AI assistance and verify every line you submit. Do not submit a full implementation generated by a tool. If you used no generative AI, say so explicitly. Bring small failing examples and public-test messages to office hours when asking for help.
