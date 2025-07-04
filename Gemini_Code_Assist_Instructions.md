# Gemini Code Assist Operational Instructions

This document outlines specific protocols for interacting with the user to ensure clarity and prevent errors.

## Manual Code Replacement Protocol

When the automated diff/patch tool fails and a manual code replacement is necessary, the following multi-step process must be followed to avoid mistakes:

1.  **Step 1: State the Action Clearly.** Always begin by stating the primary action, such as "Find and Delete", "Find and Replace", or "Paste New Code".

2.  **Provide the Code to be Found/Deleted.**
    *   If replacing or deleting, provide the *exact* block of code that the user needs to find and delete.
    *   If pasting new code without deleting, provide the code block that the new code should be pasted *after* or *before*.

3.  **Provide the New Code to be Pasted.** Provide the new block of code to be inserted.

4.  **Clarify Placement and Spacing.**
    *   Explicitly state where to paste the new code (e.g., "in the exact same spot", "on a new line immediately after the block you found").
    *   If pasting after a found block, specify whether a blank line is needed. If no blank line is needed for correct indentation and structure, state that. If it is needed, state that.

**Example Interaction (Replacing Code):**

"Of course. To fix this, we'll need to manually replace a function.

### Step 1: Find and Delete

Please find and delete this entire function from `your_file.py`:

```python
def old_buggy_function():
    # old, buggy logic
    return False
```

### Step 2: Paste New Code

Now, in the exact same spot where you deleted the old function, please paste the following new code. No extra blank line is needed.

```python
def new_function_with_fix():
    # new, corrected logic
    return True
```

Once you've updated the file, we can continue.

<!--
[PROMPT_SUGGESTION]Okay, the instructions are updated. Let's continue.[/PROMPT_SUGGESTION]
-->


