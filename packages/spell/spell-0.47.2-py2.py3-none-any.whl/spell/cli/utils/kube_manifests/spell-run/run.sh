#!/usr/bin/env bash
set -e

git_remote_url=$1
git_commit_hash=$2
user_cmd=$3
log_fwd_path=$4

echo "checking out code from git remote at ${git_remote_url}..."
git init
git remote add origin ${git_remote_url}
GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no" git fetch --depth 1 origin ${git_commit_hash}
git checkout FETCH_HEAD

# wait for metrics-fw to start
bash -c "while ! curl http://localhost/spellcheck ; do sleep 0.1 ; done"
${user_cmd} | ${log_fwd_path}
curl http://localhost/shutdown