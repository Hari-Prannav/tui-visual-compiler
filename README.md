# TUI Visual Compiler

The TUI Visual Compiler is a real-time, terminal-based educational tool that visually renders the internal compilation pipeline—including abstract syntax trees and panic-mode error recovery—live on every keystroke.

This project addresses the gap between batch-mode student compilers (which hide their internal state and penalize syntax mistakes immediately) and the need for visible, real-time feedback inside a native developer terminal.

## Key Features

* **Live Debounced Re-parsing:** Every keystroke triggers an incremental update inside the terminal canvas, debounced by 100ms so it never floods the render loop or flickers the screen.


* **Visible Panic-Mode Recovery:** When the parser hits bad syntax, it isolates the failure into a distinct `ErrorNode`, synchronizes at the next statement delimiter, and keeps parsing the remaining valid statements. The terminal renders these error nodes in red while keeping the rest of the tree intact.


* **Four-Panel TUI Dashboard:** Coordinates a code buffer, Abstract Syntax Tree (AST), Symbol Table, and Three-Address Code (TAC) / Status panel in a single screen.


* **No External Dependencies:** A lexical analyzer, recursive-descent parser, scoped semantic analyzer, and intermediate code generator implemented entirely from scratch without parser-generator shortcuts.



## System Architecture

The pipeline processes code through four distinct phases, updating the Textual UI on every keystroke:

1. **Lexical Analyzer (`lexer.py`):** Converts raw text into a token stream (type, value, line, column) and applies an unknown-token marker on bad characters to keep scanning without crashing.


2. **Recursive-Descent Parser (`parser.py`):** Consumes tokens to build the AST and executes the `synchronize()` routine to isolate errors and resume parsing.


3. **Semantic Analyzer (`semantic_analyzer.py`):** Manages the scope stack, flags undeclared identifiers, detects type mismatches, and populates the Symbol Table.


4. **Intermediate Code Generator (`ir_generator.py`):** Translates valid AST nodes into Three-Address Code (TAC) with temporary variables and jump labels.



## Installation & Requirements

**Prerequisites:**

* Python 3.10+


* A terminal supporting 256-color or true color (e.g., Windows Terminal, macOS Terminal, Linux)


* Minimum Dual-core 1.5GHz+ processor, 2GB RAM


* Terminal window size of at least 120 columns × 35 rows



**Setup:**

```bash
# Clone the repository
git clone <YOUR_REPO_URL>
cd tui-visual-compiler

# Install the required Textual UI framework
pip install textual

# Run the application
python base_ui.py

```

## Usage & Controls

* **Interactive Editing:** Click inside the top-left "Source Editor" panel to begin typing. The diagnostic panels will update automatically within 100 milliseconds of your last keystroke.


* **Scrolling Panels:** Click on any of the output panels (like the TAC/Diagnostics panel) to grant it keyboard focus, allowing you to scroll through the token stream or generated code using your arrow keys.
* **Quit Application:** Press the `Esc` key to safely terminate the application and return to your standard command prompt.

## Team Members & Contributions

**BCSE307P - Compiler Design Lab**

| Register No | Name | Core Contributions |
| --- | --- | --- |
| **24BCE0659** | Hariprannav S | Lexer & Parser (recursive-descent grammar, panic-mode error recovery, `ErrorNode` synchronization).

 |
| **24BDS0155** | Lavanbarath B | Semantic Analyzer & Symbol Table (scope stack, type checking) + Terminal UI Engine & TAC Generator (Textual panels, live rendering).

 |
