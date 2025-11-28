import typer
from pathlib import Path
from rich.console import Console
from src.core.llm import llm_client
from src.core.config import Config
from src.agents.ingestor import ingestor_agent
from src.agents.analyzer import analyzer_agent
import json

# Initialize CLI and Rich Console
app = typer.Typer()
console = Console()

@app.callback()
def callback():
    """
    AI Job Application Agent CLI
    """
    pass

@app.command(name="test-connection")
def test_connection():
    """
    Simple command to verify Google API connection.
    """
    console.print("[bold yellow]Testing Gemini Connection...[/bold yellow]")
    try:
        response = llm_client.generate("Are you online?")
        console.print(f"[bold green]Gemini Says:[/bold green] {response}")
    except Exception as e:
        console.print(f"[bold red]Generation Error:[/bold red] {e}")

@app.command(name="ingest")
def ingest_file(filename: str):
    """
    Test the Ingestion Agent. reads a file from data/input/ and prints the start of it.
    """
    file_path = Config.INPUT_DIR / filename
    
    console.print(f"[bold yellow]Attempting to read:[/bold yellow] {file_path}")
    
    try:
        text = ingestor_agent.file_to_text(file_path)
        if text:
            console.print(f"[bold green]Success![/bold green] Read {len(text)} characters.")
            console.print("[bold]Preview:[/bold]")
            console.print(text[:500] + "...") # Show first 500 chars
        else:
            console.print("[bold red]Failed to extract text or file is empty.[/bold red]")
            
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@app.command(name="analyze-job")
def analyze_job(filename: str):
    """
    Feature 1: Analyzes a Job Description file and outputs structured data.
    """
    file_path = Config.INPUT_DIR / filename
    
    # 1. Ingest
    console.print(f"[bold yellow]1. Reading File:[/bold yellow] {filename}")
    text = ingestor_agent.file_to_text(file_path)
    
    if not text:
        console.print("[bold red]Aborting: Empty file.[/bold red]")
        return

    # 2. Analyze
    console.print(f"[bold yellow]2. Analyzing with Gemini...[/bold yellow]")
    analysis = analyzer_agent.analyze_jd(text)
    
    # 3. Output
    console.print("[bold green]Analysis Complete! Here is the structured data:[/bold green]")
    console.print_json(json.dumps(analysis))



if __name__ == "__main__":
    app()