# Git Quick Guide for Code Backup & Restore

## 1. Create a Backup Point (Commit)
Whenever you want to save your current code state:

```
git add .
git commit -m "Describe your change or backup point"
```

- Use a clear message for each backup point (e.g., "Added new report feature").

---
## 2. View Backup History
See all your previous backup points:

```
git log --oneline
```

- Shows a list of commits (backup points) with their IDs and messages.

---
## 3. Restore/Roll Back to a Previous Version
To view or restore a previous backup point:

- See the commit ID using `git log --oneline`.
- To temporarily view a previous version:
  ```
  git checkout <commit-id>
  ```
- To permanently roll back (reset) to a previous backup point:
  ```
  git reset --hard <commit-id>
  ```
  **Warning:** This will discard all changes after that commit.

---
## 4. Common Git Commands
- See file changes:  
  `git status`
- Undo changes to a file:  
  `git checkout -- filename`
- Remove a file from tracking:  
  `git rm filename`

---
## 5. Troubleshooting
- If you get stuck, you can always ask for help or search for "Git cheat sheet" online.
- You do NOT need to use GitHub for local backups—everything stays on your computer unless you choose to push to a remote.

---
## 6. More Help
- This file is always available in your project folder.
- For more, see: https://git-scm.com/docs or https://www.atlassian.com/git/tutorials

---
**Tip:**
You can open this file in VS Code anytime for a quick reference!
