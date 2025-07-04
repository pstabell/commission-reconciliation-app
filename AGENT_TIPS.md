# Agent Tips and Tricks

This file contains insights and lessons learned to improve agent performance and avoid common issues.

---

## Tip: Handling Output Truncation from `read_file`

**Issue:** When using `read_file`, the output can be truncated (indicated by "[File content truncated...]"). This prevents the agent from seeing the full content, especially critical for `replace` operations that require exact `old_string` matches.

**Solution:**
1.  **Increase `limit` parameter:** When reading large files or sections where full context is crucial, significantly increase the `limit` parameter in `read_file` (e.g., `limit = 1000` or more) to ensure the entire relevant block is retrieved.
2.  **Verify `old_string`:** Before using `replace`, always verify the `old_string` against the *full, untruncated* content from `read_file` to ensure an exact match, including all whitespace and line breaks.
3.  **Context is Key:** For `replace` operations, include sufficient surrounding context (at least 3 lines before and after) in the `old_string` to make it unique and prevent multiple matches.

---

## Template for New Tips:

### Tip: [Brief, descriptive title of the tip]

**Issue:** [Description of the problem or challenge the tip addresses.]

**Solution:** [Actionable advice or steps to resolve/avoid the issue.]

---
