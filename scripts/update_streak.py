name: Update Consistency Streak

on:
  schedule:
    - cron: "0 18 * * *"   # runs daily at 18:00 UTC (~11:30 PM IST) — checks "yesterday"
  workflow_dispatch: {}     # lets you trigger it manually from the Actions tab

permissions:
  contents: write

jobs:
  update-streak:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install requests

      - name: Run streak tracker
        env:
          GH_USERNAME: aash1sh9
          # Optional: add a repo secret named GH_PAT (personal access token,
          # scope: repo) if you want private-repo commits to count too.
          GH_PAT: ${{ secrets.GH_PAT }}
        run: python scripts/update_streak.py

      - name: Commit and push changes
        run: |
          git config --local user.email "actions@github.com"
          git config --local user.name "streak-bot"
          git add stats.json progress_bar.svg calendar.svg
          git diff --quiet && git diff --staged --quiet || git commit -m "chore: update consistency streak [skip ci]"
          git push
