# OsztottRendszerekProjekt

## Git Strategy

To maintain a clean and organized codebase, we follow a branch-based development workflow:

1.  **Branching:** Always create a new branch for every feature, bug fix, or task. Do not work directly on the `main` branch.
2.  **Naming Convention:** Name your branches descriptively based on the work being done. Use prefixes for clarity:
    *   `feature/` for new features (e.g., `feature/user-authentication`)
    *   `bugfix/` for bug fixes (e.g., `bugfix/connection-timeout`)
    *   `docs/` for documentation changes (e.g., `docs/update-readme`)
3.  **Pull Requests (PRs):** Once your work is complete and tested, open a Pull Request to merge your branch into `main`.
4.  **Review and Merge:** At least one other team member should review the PR before it is merged. After merging, delete the feature branch.