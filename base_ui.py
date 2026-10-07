"""
base_ui.py - Base Textual Layout with 100ms Debounced Lexer Execution
Coordinates a 4-panel dashboard layout displaying Code Input, AST View,
Symbol Table, and Intermediate Code/Status panels.
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.timer import Timer
from textual.widgets import Header, Footer, TextArea, Static, Label
from typing import Optional

from lexer import Lexer, TokenType


DEFAULT_CODE = """let a: int = 10;
let b: int = 20 + 5;
if (a < b) {
    let result: string = "passed";
}
"""

APP_CSS = """
Screen {
    background: #1e1e2e;
    layout: vertical;
}

#main-grid {
    height: 1fr;
    layout: grid;
    grid-size: 2 2;
    grid-columns: 1fr 1fr;
    grid-rows: 1fr 1fr;
    grid-gutter: 1;
    padding: 1;
}

.panel-container {
    border: round #89b4fa;
    background: #181825;
    padding: 0 1;
}

.panel-title {
    background: #313244;
    color: #cdd6f4;
    text-style: bold;
    padding: 0 1;
    dock: top;
    height: 1;
}

#editor {
    height: 1fr;
    background: #181825;
}

#ast-panel, #symbol-panel, #tac-panel {
    height: 1fr;
    overflow-y: auto;
    color: #a6adc8;
}
"""


class VisualCompilerApp(App):
    CSS = APP_CSS
    TITLE = "TUI Visual Compiler"
    SUB_TITLE = "Real-Time Pipeline Inspection"
    BINDINGS = [("escape", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        self._debounce_timer: Optional[Timer] = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main-grid"):
            # Top-Left: Code Input Panel
            with Vertical(classes="panel-container"):
                yield Label(" Source Editor (Keystroke Active)", classes="panel-title")
                yield TextArea(text=DEFAULT_CODE, language="python", id="editor")

            # Top-Right: AST View Panel (Placeholder for Lavanbarath)
            with Vertical(classes="panel-container"):
                yield Label(" Abstract Syntax Tree (AST View)", classes="panel-title")
                yield Static(
                    "[yellow]Awaiting Phase 2 Parser...[/yellow]\n\n"
                    "Will render green branches for valid nodes\n"
                    "and red nodes for recovered syntax errors.",
                    id="ast-panel",
                )

            # Bottom-Left: Symbol Table Panel (Placeholder for Lavanbarath)
            with Vertical(classes="panel-container"):
                yield Label(" Symbol Table (Scopes & Types)", classes="panel-title")
                yield Static(
                    "[yellow]Awaiting Phase 2 Semantic Analyzer...[/yellow]\n\n"
                    "Tracks identifier bindings, types, and scope depths.",
                    id="symbol-panel",
                )

            # Bottom-Right: TAC & Lexer Status Panel
            with Vertical(classes="panel-container"):
                yield Label(" Intermediate Code (TAC) & Diagnostics", classes="panel-title")
                yield Static("Initializing lexer feed...", id="tac-panel")
        yield Footer()

    def on_mount(self) -> None:
        # This line enables keyboard scrolling for the TAC panel
        self.query_one("#tac-panel").can_focus = True
        self.trigger_compilation_pipeline()

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if self._debounce_timer:
            self._debounce_timer.stop()
        self._debounce_timer = self.set_timer(0.1, self.trigger_compilation_pipeline)

    def trigger_compilation_pipeline(self) -> None:
        editor = self.query_one("#editor", TextArea)
        source = editor.text
        tac_panel = self.query_one("#tac-panel", Static)

        lexer = Lexer(source)
        tokens = lexer.tokenize()

        unknowns = [t for t in tokens if t.type == TokenType.UNKNOWN]
        total_tokens = len(tokens) - 1

        # 1. Put the Summary at the top so it is always visible
        output = [
            f"[bold green]✓ Lexer Active (Debounce: 100ms)[/bold green]",
            f"Total Tokens: {total_tokens} | Unknowns: {len(unknowns)}",
            "─" * 40,
        ]

        if unknowns:
            output.append("[bold red]Lexical Irregularities:[/bold red]")
            for u in unknowns:
                output.append(f" • '{u.value}' at Line {u.line}, Col {u.column}")
        else:
            output.append("[green]Stream clean without lexical faults.[/green]")

        # 2. Show only the first 5 tokens so everything fits on screen
        output.append("\n[dim]Recent Tokens (First 5):[/dim]")
        for tok in tokens[:5]:
            output.append(f"  {tok.type.name:<15} -> {tok.value!r}")

        tac_panel.update("\n".join(output))


if __name__ == "__main__":
    app = VisualCompilerApp()
    app.run()