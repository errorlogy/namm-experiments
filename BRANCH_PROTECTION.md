# Branch protection for `main`

Branch protection could **not** be applied via the GitHub REST API on this repository. The API returns HTTP **403**:

> Upgrade to GitHub Pro or make this repository public to enable this feature.

Apply the settings below in the GitHub web UI (Settings → Branches), or upgrade the account / make the repo public if you want API or Rulesets at the org level.

## Required CI check (from `.github/workflows/ci.yml`)

| Item | Value |
|------|--------|
| Workflow file | `.github/workflows/ci.yml` |
| Workflow `name` | `CI` |
| Job ID | `test` |
| Job display name (status check) | **`Test (Python 3.12)`** |

After at least one successful run on `main`, the check may also appear as **`CI / Test (Python 3.12)`** in the branch protection picker. Select whichever matches your Actions runs.

## Manual setup (GitHub UI)

1. Open [Branch protection rules](https://github.com/errorlogy/namm-experiments/settings/branches) for **errorlogy/namm-experiments**.
2. Click **Add rule** (or edit the existing rule for `main`).
3. **Branch name pattern:** `main`
4. Enable **Require status checks to pass before merging**.
5. Enable **Require branches to be up to date before merging** (strict; matches CI re-run on latest commit).
6. In **Status checks that are required**, search for and add **`Test (Python 3.12)`** (or **`CI / Test (Python 3.12)`**).
7. **Pull requests (optional, recommended even for solo repos):** enable **Require a pull request before merging**. You do not need required reviewers for a private solo repo; the rule still blocks direct pushes to `main` and forces CI on the PR.
8. Leave **Restrict who can push** empty unless you need deploy keys or bots with direct push.
9. Save changes.

## Verify

1. Open a test PR into `main` and confirm the **Test (Python 3.12)** check runs and is required.
2. Confirm merge is blocked if the check fails or is pending.

## API reference (when plan allows)

If branch protection becomes available (Pro, public repo, or Enterprise), equivalent REST configuration:

```bash
gh api -X PUT repos/errorlogy/namm-experiments/branches/main/protection \
  --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["Test (Python 3.12)"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null
}
EOF
```

Adjust `contexts` if the UI shows **`CI / Test (Python 3.12)`** instead.
