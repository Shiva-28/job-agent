import typer
import json
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from src.core.llm import llm_client
from src.core.config import Config
from src.agents.ingestor import ingestor_agent
from src.agents.analyzer import analyzer_agent
from src.agents.strategist import strategist_agent
from src.agents.writer import writer_agent
from src.agents.tailor import tailor_agent
from src.agents.coach import coach_agent

# Initialize CLI and Rich Console
app = typer.Typer()
console = Console()

@app.callback()
def callback():
    """
    🚀 AI Job Application Agent - The Ultimate Career Copilot
    """
    pass

@app.command(name="test-connection")
def test_connection():
    """Verify Google API connection."""
    console.print("[bold yellow]Testing Gemini Connection...[/bold yellow]")
    try:
        response = llm_client.generate("Are you online?")
        console.print(f"[bold green]Gemini Says:[/bold green] {response}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@app.command(name="prepare-interview")
def prepare_interview(resume_file: str, jd_file: str):
    """
    Feature 6: Generates Interview Questions & Answers.
    """
    resume_path = Config.INPUT_DIR / resume_file
    jd_path = Config.INPUT_DIR / jd_file
    
    resume_text = ingestor_agent.file_to_text(resume_path)
    jd_text = ingestor_agent.file_to_text(jd_path)
    if not resume_text or not jd_text: return

    console.print("[bold yellow]Coach is predicting questions...[/bold yellow]")
    prep_data = coach_agent.generate_interview_prep(resume_text, jd_text)
    
    # Save to JSON
    out_path = Config.OUTPUT_DIR / "Interview_Prep.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(prep_data, f, indent=2)
    
    console.print("\n[bold]🎤 Technical Question Preview:[/bold]")
    for item in prep_data.get('technical_questions', [])[:2]:
        console.print(f"Q: {item['question']}")
        console.print(f"[italic]Tip: {item['ideal_answer'][:100]}...[/italic]")
    
    console.print(f"\n[green]💾 Full Guide Saved to {out_path}[/green]")

@app.command(name="process-all")
def process_all(resume_file: str, jd_file: str):
    """
    Feature 8: ONE COMMAND to rule them all. Runs the entire pipeline.
    """
    resume_path = Config.INPUT_DIR / resume_file
    jd_path = Config.INPUT_DIR / jd_file
    
    console.rule("[bold red]🚀 STARTING FULL JOB PREP WORKFLOW[/bold red]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        
        # Step 1: Ingestion
        task1 = progress.add_task("Reading Files...", total=None)
        resume_text = ingestor_agent.file_to_text(resume_path)
        jd_text = ingestor_agent.file_to_text(jd_path)
        time.sleep(0.5) 
        
        if not resume_text or not jd_text:
            console.print("[bold red]Failed to read files. Aborting.[/bold red]")
            return

        # Step 2: Analysis & Strategy
        progress.update(task1, description="Analyzing Fitment...")
        fitment = strategist_agent.calculate_fitment(resume_text, jd_text)
        
        # Step 3: Content Generation
        progress.update(task1, description="Drafting Cover Letter & Email...")
        cl = writer_agent.write_cover_letter(resume_text, jd_text)
        
        # Need basic JD analysis for the email context
        jd_analysis = analyzer_agent.analyze_jd(jd_text)
        email = writer_agent.write_email("Cold Outreach", jd_analysis)
        
        # Step 4: Tailoring
        progress.update(task1, description="Tailoring Resume...")
        tailored_data = tailor_agent.tailor_resume(resume_text, jd_text)
        
        # Step 5: Interview Prep
        progress.update(task1, description="Preparing Interview Guide...")
        interview_data = coach_agent.generate_interview_prep(resume_text, jd_text)
        
        progress.update(task1, completed=True)

    # --- FINAL REPORT GENERATION ---
    console.rule("[bold blue]🎉 WORKFLOW COMPLETE[/bold blue]")
    
    # 1. Fitment
    score = fitment['match_percentage']
    score_color = "green" if score > 75 else "yellow"
    console.print(f"\n📊 [bold]Match Score:[/bold] [{score_color}]{score}%[/{score_color}]")
    
    # 2. Saving Files
    console.print("\n[bold]💾 Saving artifacts...[/bold]")
    
    (Config.OUTPUT_DIR / "1_Cover_Letter.txt").write_text(cl, encoding="utf-8")
    (Config.OUTPUT_DIR / "2_Recruiter_Email.txt").write_text(email, encoding="utf-8")
    
    with open(Config.OUTPUT_DIR / "3_Tailored_Resume_Data.json", "w", encoding="utf-8") as f:
        json.dump(tailored_data, f, indent=2)

    with open(Config.OUTPUT_DIR / "4_Interview_Prep.json", "w", encoding="utf-8") as f:
        json.dump(interview_data, f, indent=2)
        
    console.print(f"[green]✔ All files saved in {Config.OUTPUT_DIR}[/green]")
    console.print("[bold]Good luck with the application! 🚀[/bold]")

if __name__ == "__main__":
    app()