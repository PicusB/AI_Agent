# AI_Agent

This is a simple program that takes a prompt and works with the local file system in the specified working directory.
Boot.Dev project (course #8 Back-End Engineer)

## Usage

To set the working directory, change the working_dir variable in ./functions/call_function.py
Requires Python to run
Requires GenAI[https://aistudio.google.com/prompts/new_chat] API Key
"Python3 main.py 'args'" where args is a string for the LLM

## Config
System_prompt can be set in ./config.py, default:
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

For solutions with multiple steps, make a clear list of the steps taken.

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
