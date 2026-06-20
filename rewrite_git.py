import os
import subprocess

script = """
git filter-branch -f --env-filter '
export GIT_AUTHOR_NAME="Mohammed Adnan Mohiuddin"
export GIT_AUTHOR_EMAIL="adnan@example.com"
export GIT_COMMITTER_NAME="Mohammed Adnan Mohiuddin"
export GIT_COMMITTER_EMAIL="adnan@example.com"
' HEAD
"""

with open('rewrite.sh', 'w') as f:
    f.write(script)

print("Running filter-branch...")
subprocess.run(['bash', 'rewrite.sh'])
print("Force pushing to GitHub...")
subprocess.run(['git', 'push', '--force', 'origin', 'main'])
print("Done!")
