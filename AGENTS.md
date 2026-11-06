# Shared class project instructions

Multiple students develop this application in separate Codex chats connected to
the same GitHub repository. Follow these rules for every task:

1. Before making changes, retrieve the latest repository version. Check for local
   changes first, fetch from the shared remote, and safely incorporate updates
   from the target branch without discarding local work.
2. Preserve all existing application functionality.
3. Do not overwrite or discard another student's work, including uncommitted
   changes or commits made in another chat.
4. After completing a task, test the changes with relevant checks and commit the
   completed changes with a descriptive commit message. Stage only files intended
   for the task, and report test results and any limitations.
5. Push completed changes to the shared GitHub repository.
6. Immediately before pushing, fetch again and check whether other students have
   pushed new changes to the target branch. If they have, incorporate those
   changes safely and rerun relevant tests before pushing. If a normal push is
   rejected because the branch advanced, repeat this check and integration.
7. If conflicting changes cannot be safely combined, stop and explain the
   conflict rather than overwriting anyone's work.
8. Never force-push to the shared repository, including with --force-with-lease.

Use the existing checkout; each cloud task is already isolated. Do not create a
Git worktree unless the user explicitly requests one.
