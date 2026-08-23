import os

base = os.path.join(os.path.expanduser("~"), "OneDrive", "Bureaublad", "crypto-puzzle-lab", "docs")

# Update HYBRID_PROTOCOL.md
proto = os.path.join(base, "HYBRID_PROTOCOL.md")
txt = open(proto, encoding="utf-8").read()
add = []
if "PRE-PUSH VERIFICATION" not in txt:
    add.append("\n10. **PRE-PUSH VERIFICATION**: Before EVERY git push, the AI must verify 100% that all files, content, commit messages, and structure are correct and match the knowledge base. No next task until the push is confirmed clean on GitHub.\n")
if "SCRIPT CORRECTNESS FIRST" not in txt:
    add.append("\n11. **SCRIPT CORRECTNESS FIRST**: Every script must be fully reviewed, bug-checked, and validated by the AI BEFORE the user runs it. The AI must catch logic errors (e.g., M7 voting bug, groq_key attribute bug) in advance, never after a failed run.\n")
if "AI OWNS THE ANALYSIS" not in txt:
    add.append("\n12. **AI OWNS THE ANALYSIS**: The AI never asks the human to do analysis, inspection, or interpretation that the AI can do itself. The human only performs physical actions (run, push, post, decide). All cognitive work belongs to the AI.\n")
if add:
    with open(proto, "a", encoding="utf-8") as f:
        f.write("\n## Hard rules (2026-08-23, update 4)\n" + "".join(add))
    print("Added 3 new permanent rules to HYBRID_PROTOCOL.md")
else:
    print("Rules already present")

# Update MISTAKES_LOG.md
mlog = os.path.join(base, "MISTAKES_LOG.md")
mtxt = open(mlog, encoding="utf-8").read()
if "M8" not in mtxt:
    entry = "\n### M8: Asked human for analysis that AI should do (2026-08-23)\n"
    entry += "- **What happened:** I asked the user to open blm.png and tell me where the clock is.\n"
    entry += "- **Why wrong:** Image analysis is AI cognitive work, not a human physical action. Violates hybrid division of labor.\n"
    entry += "- **Lesson:** The AI must self-analyze via scripts/tools. Never delegate analysis to the human.\n"
    entry += "- **Fix:** Built auto-detection script that finds the clock region without human input.\n"
    with open(mlog, "a", encoding="utf-8") as f:
        f.write(entry)
    print("Added M8 to MISTAKES_LOG.md")
else:
    print("M8 already present")

print("\nDone. Ready to commit + push.")