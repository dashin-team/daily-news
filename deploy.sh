#!/usr/bin/env bash
# Daily refresh: rebuild index.html and push to dashin-team/daily-news (GitHub Pages)
set -euo pipefail
cd "$(dirname "$0")"
python3 build.py
[ -d .git ] || { git init -q -b main; git remote add origin https://github.com/dashin-team/daily-news.git; }
gh auth setup-git >/dev/null 2>&1 || true
git add -A index.html app.js data.json img build.py deploy.sh news-*-all.zip
git -c user.name="dashin-team" -c user.email="dashin-team@users.noreply.github.com" commit -qm "Daily update $(date +%F_%H%M)" || echo "nothing to commit"
git fetch -q origin main && git rebase -q origin/main 2>/dev/null || true
git push -q origin main
echo "Deployed: https://dashin-team.github.io/daily-news/"
