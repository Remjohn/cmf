# 📚 CMF BATCH AUTOMATION GUIDE
## A Complete Beginner's Guide to Running CMF Workflows with Gemini CLI

**Version:** 3.0
**Word Count:** ~3200 words
**Audience:** Beginners to Advanced Users

---

## Table of Contents
1. [Understanding Gemini CLI](#understanding-gemini-cli)
2. [What is a Session and Why Does It Matter?](#what-is-a-session)
3. [Interactive vs Headless Mode](#interactive-vs-headless)
4. [Google Cloud Shell: Your Production Powerhouse](#cloud-shell)
5. [Starting a New Project: The Initialization](#initialization)
6. [The CMF Workflow Structure](#cmf-workflow-structure)
6. [Running Commands: Step-by-Step](#running-commands)
7. [Use Cases with Detailed Examples](#use-cases)
8. [Parallel Execution Explained](#parallel-execution)
9. [Phase 2: Image Generation Automation](#phase-2-images)
10. [Orchestrating 5 Projects Per Day](#five-projects)
11. [Batch Scripts Reference](#batch-scripts)
12. [Troubleshooting Common Issues](#troubleshooting)
13. [Managing "Lazy" AI & Quality Control](#lazy-ai)

---

## ⚡ QUICK REFERENCE CHEAT SHEET <a name="cheat-sheet"></a>

**1. CREATE A NEW PROJECT (The Factory)**
```powershell
# Standard (Coach Adele)
python tools/create_project.py --transcript "14_160-01 Monia.srt"

# Specific Coach
python tools/create_project.py --transcript "14_160-01 Monia.srt" --coach "Coach Jean"
```

**2. RUN THE PIPELINE (The Manager)**
*Go into the folder and run:*
```powershell
cd "inputs/Coach Adele/06_50-12 Monia"
.\RUN_PIPELINE.ps1
```

**3. FIX A MISTAKE (The Reset)**
*Delete the bad file and run the pipeline again.*
```powershell
rm "06_50-12 Monia_STORYBOARD_VISUAL_POETRY.md"
.\RUN_PIPELINE.ps1
```

---

## 1. Understanding Gemini CLI <a name="understanding-gemini-cli"></a>

Gemini CLI is a command-line interface that allows you to interact with Google's Gemini AI models directly from your terminal or PowerShell. Instead of opening a web browser and typing into a chat interface, you can type commands directly in your terminal and receive AI-generated responses. This is extremely powerful for automation because it allows you to script AI interactions, chain multiple AI calls together, and integrate AI into your existing workflows without manual intervention.

For the Conscious Movie Factory (CMF), Gemini CLI is the perfect tool because our production pipeline requires executing multiple sequential steps, each generating specific output files. Instead of manually opening the chat, typing a command, waiting for the output, then repeating this process seven or more times per project, you can automate the entire sequence with a single script. The CLI handles each step automatically, saving you hours of repetitive work. When you have five or more projects to process, this automation becomes absolutely essential for maintaining productivity and sanity.

The key advantage of Gemini CLI over web-based interfaces is control. You control exactly what context goes into each request, when each request happens, and how the outputs are handled. This level of control is what enables the batch processing and parallel execution techniques we will explore in this guide.

---

## 2. What is a Session and Why Does It Matter? <a name="what-is-a-session"></a>

A "session" in the context of AI assistants refers to a continuous conversation where the AI remembers everything that was said before. Think of it like a phone call: once you start the call, you can reference things you said earlier in the conversation, and the person on the other end remembers the context. When you end the call and start a new one, you're starting fresh with no memory of the previous conversation.

In Gemini CLI, when you type `gemini` and press Enter, you start an interactive session. Everything you type within that session builds up in what's called the "context window." The context window is like the AI's short-term memory—it can only hold so much information before it becomes overwhelmed. As you keep adding more instructions, loading more files, and receiving more responses, the context window fills up. When it gets too full, performance degrades: the AI becomes slower, may forget earlier instructions, and can produce lower-quality outputs.

For CMF, this is a critical problem because each workflow (like `/cmf-phase1a-diagnose` or `/cmf-phase1b-storyboard`) requires loading large agent files (900 to 4000 words each), transcripts, guides, and constitution documents. If you run all seven workflows in a single session, the context window becomes bloated with information from earlier workflows that is no longer relevant. The AI might confuse instructions from the Storyboard Architect with instructions from the GMG Composer, leading to incorrect outputs.

The solution is simple but powerful: run each workflow in its own fresh session. When you start a new session, the context window is completely empty. The AI has no memory of previous workflows, which means it can focus 100% of its attention on the current task. This is why we use the `gemini --prompt` or `gemini -p` command instead of interactive mode—each invocation is guaranteed to be a completely fresh session with an empty context window.

---

## 3. Interactive vs Headless Mode <a name="interactive-vs-headless"></a>

Gemini CLI can operate in two fundamentally different modes, and understanding the difference is crucial for effective automation.

**Interactive Mode** is what you get when you simply type `gemini` and press Enter. The CLI opens an ongoing conversation where you can type multiple messages, and the AI responds to each one while remembering everything said before. This mode is excellent for exploration, brainstorming, or when you need to iterate on a task with back-and-forth dialogue. However, it accumulates context over time, and you must manually exit (by typing `/exit` or pressing Ctrl+C) to end the session.

**Headless Mode** (also called non-interactive mode) is what happens when you use the `--prompt` or `-p` flag, like this: `gemini -p "Your instruction here"`. In headless mode, the CLI receives your single instruction, processes it, outputs the result, and then immediately exits. There is no ongoing conversation—the session ends automatically after the response. This is perfect for automation because each command is completely isolated. You don't need to worry about ending sessions manually, and you're guaranteed a fresh context window every time.

For CMF batch processing, we exclusively use headless mode. Here's why: when you run `gemini -p "Execute /cmf-phase1a-diagnose for Project Monia"`, the CLI starts fresh, loads only what's needed for that workflow, generates the outputs, and exits. When you then run `gemini -p "Execute /cmf-phase1a-narrative for Project Monia"`, it's a completely new session with no memory of the previous command. This isolation prevents context pollution and ensures each workflow operates at maximum performance.

---

## 4. Google Cloud Shell: Your Production Powerhouse <a name="cloud-shell"></a>

Google Cloud Shell is a free, browser-based Linux environment provided by Google. It's the ideal platform for running CMF workflows at scale because it provides all the infrastructure you need without any local setup or resource constraints. Understanding Cloud Shell is essential if you want to orchestrate 5 or more projects per day efficiently.

### What Cloud Shell Provides

When you open Cloud Shell, you get access to a full Linux virtual machine (VM) assigned to your Google account. This VM comes pre-configured with the Gemini CLI and many other development tools. The key features that make it perfect for CMF are:

**Multiple Terminal Tabs:** You can open multiple terminal tabs or windows within the same Cloud Shell session. Each tab acts as a completely separate shell environment. This means commands running in Tab 1 do not interfere with Tab 2—they operate in complete isolation. The only situation where tabs might conflict is if they both try to write to the exact same file at the same time, which our CMF workflow design specifically prevents by using unique output filenames per project.

**Free and Persistent:** Cloud Shell is completely free to use and provides 5GB of persistent storage in your home directory. This means your documents, scripts, and workflow outputs are saved across all your tabs and even across different Cloud Shell sessions. You can close your browser, come back the next day, and your files will still be there.

**Always Available:** Unlike running Gemini CLI on your local Windows machine where system resources might be limited, Cloud Shell runs on Google's infrastructure. You don't need to worry about your laptop overheating or running out of memory when processing multiple projects in parallel.

### The Three Rules for Isolation

To ensure your 12-15 agent documents and 7 workflow commands don't "pollute" each other's context, follow these three essential rules:

**Rule 1: Always Use Headless Mode.** Instead of running an interactive chat session, always use the `-p` flag for specific commands. For example: `gemini -p "/cmf-phase1a-diagnose --project=Monia"`. This ensures each command starts with a "fresh brain" and doesn't get confused by what happened in a previous tab's conversation. Every single time you invoke `gemini -p`, you're guaranteed a clean slate.

**Rule 2: Unique Output Files.** Our CMF workflows already follow this rule by design—every output file includes the project ID in its filename. For example, `06_50-12 Monia_strategy_brief.json` and `05_50-12 Fitou_strategy_brief.json` will never conflict because they have different names. When running parallel tasks across different projects, the outputs go to different files and different folders, so nothing gets overwritten.

**Rule 3: Separate Workspaces.** The Gemini CLI recognizes local context based on the directory you are currently in. Each project has its own subfolder within the inputs directory, so when you `cd` into a project folder before running a command, the CLI operates within that project's context. This provides an additional layer of isolation even when running multiple projects simultaneously.

### Setting Up Cloud Shell for CMF

To use Cloud Shell for CMF production, follow these steps:

1. Open your browser and go to `shell.cloud.google.com`
2. Sign in with your Google account
3. Wait for the VM to initialize (usually takes 10-30 seconds)
4. Clone or upload your CMF project files to the Cloud Shell environment
5. Open multiple terminal tabs using the "+" button in the Cloud Shell interface
6. In each tab, navigate to a different project folder
7. Run your workflows in parallel across all tabs

---

## 5. Starting a New Project: The Initialization <a name="initialization"></a>

For every new project, you must first "install" the intelligent project manager script into its folder. This only needs to be done once per project.

1.  **Create the Folder:** Inside `inputs/Coach Adele/`, create your new folder (e.g., `07_50-12 NewProject`).
2.  **Add Transcript:** Drop your `.srt` or `.txt` file into the folder.
3.  **Run Initialization:** In your root terminal, run:
    ```powershell
    python tools/generate_automator.py --project "07_50-12 NewProject"
    ```
4.  **Ready to Go:** Now open that folder, and you will see `RUN_PIPELINE.ps1`. You can now run the entire pipeline from inside this folder!

> [!TIP]
> If you create multiple new folders at once, you can run `python tools/generate_automator.py --all` to initialize all of them in one go.

---

## 6. The CMF Workflow Structure <a name="cmf-workflow-structure"></a>

The Conscious Movie Factory production pipeline is divided into two major phases, each containing multiple sequential workflows.

**Phase 1A: Script Generation** consists of three workflows that must be run in order:
*   `/cmf-phase1a-diagnose`: Determines the narrative arc and creates the Brand Avatar.
*   `/cmf-phase1a-narrative`: Extracts quotes and assembles the premise.
*   `/cmf-phase1a-script`: Formats the final production-ready script.

**Phase 1B: Visual Prompts** generates all visual specifications:
*   `/cmf-phase1b-sonic`: Generates music and sound prompts.
*   `/cmf-phase1b-storyboard`: Generates A-Roll hero frame prompts.
*   `/cmf-phase1b-motion`: Generates GMG (Motion Graphics) and CAC (Ambient Cinema) prompts.
*   `/cmf-phase1b-authorize`: The final quality audit for all prompts.

---

## 7. Running Commands: Step-by-Step <a name="running-commands"></a>

### Option A: The "Automatic Manager" (Recommended)
This uses the script generated in Step 5.
1.  Navigate to the project folder: `cd "inputs/Coach Adele/06_50-12 Monia"`
2.  Run the automator: `.\RUN_PIPELINE.ps1`
3.  The script will handle all 7 steps + image generation, skipping anything you've already finished.

### Option B: Manual Execution (For Debugging)
1.  Navigate to the project folder.
2.  Run a single step: `gemini -p "Execute workflow: /cmf-phase1a-diagnose"`
3.  Wait for it to finish, then run the next one.

---

## 8. Parallel Execution Explained <a name="parallel-execution"></a>

Parallel execution means running multiple projects at the same time by using multiple terminal tabs.

**How to Run Parallel:**
1.  Open 5 Terminal Tabs in Cloud Shell or Windows.
2.  In each tab, `cd` into a different project folder.
3.  In each tab, run `.\RUN_PIPELINE.ps1`.
4.  Each tab will show the live logs for that specific project.

---

## 9. Phase 2: Image Generation Automation <a name="phase-2-images"></a>

We use OpenRouter (`bytedance-seed/seedream-4.5`) for high-speed image generation.

**What the automator does:**
1.  Parses `STORYBOARD_VISUAL_POETRY.md` for A-Roll.
2.  Parses `GMG_PROMPTS.md` and `CAC_PROMPTS.md` for B-Roll.
3.  Detects the correct scenes and experts automatically.
4.  Saves images into organized scene folders (`W1/`, `W2/`, etc.).

---

## 10. Orchestrating 5 Projects Per Day <a name="five-projects"></a>

1.  **Initialize all folders:** `python tools/generate_automator.py --all`
2.  **Open 5 Tabs:** One for each project.
3.  **Launch Scripts:** Run `.\RUN_PIPELINE.ps1` in every tab.
4.  **Monitor:** Check the tabs periodically for errors.
5.  **Review:** Once finished, check the `generated_images/` folders.

---

## 11. Batch Scripts Reference <a name="batch-scripts"></a>

| Script | Location | Description |
|--------|----------|-------------|
| `tools/generate_automator.py` | Root/tools | The Factory: Creates the project scripts. |
| `RUN_PIPELINE.ps1` | Project Folder | The Manager: Runs the full pipeline for that project. |
| `cmf-batch-images.ps1` | Root | Utility: Runs image generation only for all projects. |

---

## 12. Troubleshooting Common Issues <a name="troubleshooting"></a>

**Issue: Pipeline stops or skips a step prematurely**
The script checks for specific output files. If a file exists from a previous failed run, it might skip it. Delete the partial output file to force a re-run.

**Issue: Image generation fails**
Verify your `OPENROUTER_API_KEY` is in the `.env` file and that you have Python installed with `openai` and `python-dotenv` packages.

---

## 13. Managing "Lazy" AI & Quality Control <a name="lazy-ai"></a>

AI can sometimes be "lazy"—it might cut a task short, omit certain details, or produce a file that is technically there but of low quality. Our "Self-Healing" script is designed to handle this through the **Delete-and-Rerun** pattern.

### The "Delete-and-Rerun" Pattern
If you notice that a step (e.g., the Storyboard) is missing scenes or looks "broken":

1.  **Identify the File:** Find the output file for that specific step (e.g., `06_50-12 Monia_STORYBOARD_VISUAL_POETRY.md`).
2.  **Delete It:** Manually delete that file from your project folder.
3.  **Rerun the Pipeline:** execute `./RUN_PIPELINE.ps1` again.
4.  **Result:** The script will scan the folder, see that all previous steps are done, but detect that the Storyboard file is "missing." It will then **re-run only that specific step** with a fresh sense of duty.

### When to use this:
*   **The "Half-Finished" File:** If the AI stopped generating halfway through a script.
*   **The "Low Quality" Output:** If you don't like the creative direction of a specific phase and want to give the AI another "roll of the dice."
*   **The "Missing Scene" Bug:** If the GMG or CAC prompts missed one or two scenes from the storyboard.

By deleting the file, you are essentially "forgetting" the lazy memory and forcing a fresh start for that exact moment in the pipeline.

---

**End of Guide**
