
git filter-branch -f --env-filter '
export GIT_AUTHOR_NAME="Mohammed Adnan Mohiuddin"
export GIT_AUTHOR_EMAIL="adnan@example.com"
export GIT_COMMITTER_NAME="Mohammed Adnan Mohiuddin"
export GIT_COMMITTER_EMAIL="adnan@example.com"
' HEAD
