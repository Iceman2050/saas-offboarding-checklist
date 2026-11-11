# saas-offboarding-checklist

**Someone just quit. In 30 seconds, know exactly what to revoke — in the right order.**

When an employee leaves, teams forget half the access to revoke. The OAuth grant
they authorized 8 months ago keeps working. The API key in their dotfiles keeps
working. The shared 1Password vault they could see never gets rotated. This tool
turns "which tools did they touch?" into an **ordered revocation runbook**:
OAuth grants and SSO sessions first, then API keys, then shared credentials,
then data exports — with a checkbox for every step and a link to each vendor's
own how-to doc.

## Quickstart

```bash
# 30-second demo: sample ex-employee, 8 tools, full runbook to stdout
python -m offboarding --demo

# Real run: pick tools from the 25-tool catalog, save the runbook
python -m offboarding --employee "Jane Doe" --email jane@acme.com \
  --tools google-workspace,github,aws,slack,stripe \
  --out jane-doe-offboarding.md

# All 25 tools
python -m offboarding --employee "Jane Doe" --tools all --out full.md

# Add a tool that isn't in the catalog (repeatable)
python -m offboarding --employee "Jane Doe" \
  --custom "Acme CRM|oauth|Disable the user in Acme admin console" \
  --custom "Acme CRM|apikeys|Revoke their Acme API token"

# See the catalog
python -m offboarding --list
```

No dependencies beyond Python 3.9+ stdlib. No network calls, no accounts, no setup.

## Example output

Fresh from `python -m offboarding --demo --generated-date 2026-10-17`
(byte-for-byte verified — see "Verification" below):

<!-- EXAMPLE-OUTPUT-START -->
```markdown
# Offboarding runbook - Alex Rivera

Generated 2026-10-17 - 8 tools, 43 steps. Work the phases in order: OAuth/SSO first, then API keys, then shared credentials, then data.
Employee: alex.rivera@example.com

## Revoke OAuth grants & SSO sessions (do first)

### Google Workspace
Vendor how-to: [Delete or remove a user from your organization - Google Workspace Admin Help](https://support.google.com/a/answer/33314)
- [ ] Suspend the user immediately: Admin console > Users > select user > More > Suspend user (kills all sessions)
- [ ] Security > API controls > Manage third-party access: revoke the user's OAuth grants

### Okta
Vendor how-to: [Deactivate and delete user accounts - Okta Help](https://help.okta.com/en-us/Content/topics/users-groups-profiles/usgp-deactivate-user-account.htm)
- [ ] Directory > People > select user > Deactivate (kills SSO sessions everywhere)
- [ ] Clear their active sessions explicitly after deactivation

### GitHub
Vendor how-to: [Removing a member from your organization - GitHub Docs](https://docs.github.com/en/organizations/managing-membership-in-your-organization/removing-a-member-from-your-organization)
- [ ] Remove from every organization: People > select user > Remove from organization
- [ ] Organization Settings > Third-party access: revoke their OAuth app authorizations

### AWS (IAM)
Vendor how-to: [Deleting an IAM user - AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_remove.html)
- [ ] IAM > Users > select user: deactivate console access (remove console password, ends console sessions)
- [ ] Remove the user from all groups and detach managed/inline policies

### Slack
Vendor how-to: [Deactivate a member's account - Slack Help Center](https://slack.zendesk.com/hc/en-us/articles/204475027-Deactivate-a-member-s-account)
- [ ] Deactivate the account: Administration > Manage members > Deactivate (ends all sessions)
- [ ] Manage apps: review and revoke OAuth apps the user installed or authorized

### Stripe
Vendor how-to: [Manage access to your organization - Stripe Docs](https://docs.stripe.com/get-started/account/orgs/team)
- [ ] Settings > Team: remove the team member (revokes dashboard sessions)
- [ ] Review and revoke OAuth authorizations for connected apps they installed

### Notion
Vendor how-to: [Manage members, admins & guests in Notion - Notion Help](https://www.notion.com/help/add-members-admins-guests-and-groups)
- [ ] Settings & members > Members > remove the member (ends sessions)
- [ ] Review their OAuth connections under Settings > Connections and revoke

### 1Password
Vendor how-to: [Offboard a team member - 1Password Support](https://support.1password.com/offboarding/)
- [ ] Suspend then remove the team member (ends all sessions and device access)
- [ ] Revoke their OAuth/SSO provisioning link if SCIM was used

## Revoke API keys & tokens

### Google Workspace
Vendor how-to: [Delete or remove a user from your organization - Google Workspace Admin Help](https://support.google.com/a/answer/33314)
- [ ] APIs & Services > Credentials: delete OAuth clients and API keys they created

### Okta
Vendor how-to: [Deactivate and delete user accounts - Okta Help](https://help.okta.com/en-us/Content/topics/users-groups-profiles/usgp-deactivate-user-account.htm)
- [ ] Revoke API tokens and OAuth clients they created
- [ ] Remove them from groups, admin roles, and app assignments

### GitHub
Vendor how-to: [Removing a member from your organization - GitHub Docs](https://docs.github.com/en/organizations/managing-membership-in-your-organization/removing-a-member-from-your-organization)
- [ ] User Settings > SSH and GPG keys: delete their SSH keys and GPG keys
- [ ] Developer settings: revoke personal access tokens (classic and fine-grained)
- [ ] Remove them from teams, repository collaborators, and GitHub App installations

### AWS (IAM)
Vendor how-to: [Deleting an IAM user - AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_remove.html)
- [ ] Security credentials tab: deactivate, then delete every access key
- [ ] Delete any IAM roles or instance profiles they created for personal use

### Slack
Vendor how-to: [Deactivate a member's account - Slack Help Center](https://slack.zendesk.com/hc/en-us/articles/204475027-Deactivate-a-member-s-account)
- [ ] Revoke user tokens, bot tokens, and app-level tokens they created

### Stripe
Vendor how-to: [Manage access to your organization - Stripe Docs](https://docs.stripe.com/get-started/account/orgs/team)
- [ ] Developers > API keys: roll every secret/publishable key they had access to
- [ ] Delete restricted keys they created; review webhook endpoints they added

### Notion
Vendor how-to: [Manage members, admins & guests in Notion - Notion Help](https://www.notion.com/help/add-members-admins-guests-and-groups)
- [ ] Delete internal integrations and API tokens they created

### 1Password
Vendor how-to: [Offboard a team member - 1Password Support](https://support.1password.com/offboarding/)
- [ ] Delete service-account and Connect API tokens they created

## Rotate shared credentials

### Google Workspace
Vendor how-to: [Delete or remove a user from your organization - Google Workspace Admin Help](https://support.google.com/a/answer/33314)
- [ ] Rotate shared service-account passwords and SMTP credentials they knew

### Okta
Vendor how-to: [Deactivate and delete user accounts - Okta Help](https://help.okta.com/en-us/Content/topics/users-groups-profiles/usgp-deactivate-user-account.htm)
- [ ] Rotate shared admin credentials and enrollment policies they touched

### GitHub
Vendor how-to: [Removing a member from your organization - GitHub Docs](https://docs.github.com/en/organizations/managing-membership-in-your-organization/removing-a-member-from-your-organization)
- [ ] Rotate deploy keys and webhook secrets on repositories they administered

### AWS (IAM)
Vendor how-to: [Deleting an IAM user - AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_remove.html)
- [ ] Rotate credentials in Secrets Manager and Parameter Store they could read

### Slack
Vendor how-to: [Deactivate a member's account - Slack Help Center](https://slack.zendesk.com/hc/en-us/articles/204475027-Deactivate-a-member-s-account)
- [ ] Rotate shared webhook URLs and integration credentials posted in channels

### Stripe
Vendor how-to: [Manage access to your organization - Stripe Docs](https://docs.stripe.com/get-started/account/orgs/team)
- [ ] Rotate shared API keys stored in code, CI, or shared vaults

### Notion
Vendor how-to: [Manage members, admins & guests in Notion - Notion Help](https://www.notion.com/help/add-members-admins-guests-and-groups)
- [ ] Rotate shared integration tokens posted in team wikis

### 1Password
Vendor how-to: [Offboard a team member - 1Password Support](https://support.1password.com/offboarding/)
- [ ] CRITICAL: rotate every shared vault password they had access to
- [ ] Review vault access reports for vaults they viewed

## Transfer / export data

### Google Workspace
Vendor how-to: [Delete or remove a user from your organization - Google Workspace Admin Help](https://support.google.com/a/answer/33314)
- [ ] Transfer Drive/Docs ownership: Users > select user > Transfer data, then delete the account

### AWS (IAM)
Vendor how-to: [Deleting an IAM user - AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_remove.html)
- [ ] Check CloudTrail for resources they launched; transfer ownership or terminate

### Slack
Vendor how-to: [Deactivate a member's account - Slack Help Center](https://slack.zendesk.com/hc/en-us/articles/204475027-Deactivate-a-member-s-account)
- [ ] Export message history first if retention/compliance requires it

### Notion
Vendor how-to: [Manage members, admins & guests in Notion - Notion Help](https://www.notion.com/help/add-members-admins-guests-and-groups)
- [ ] Transfer ownership of private pages they need to keep before removal

### 1Password
Vendor how-to: [Offboard a team member - 1Password Support](https://support.1password.com/offboarding/)
- [ ] Transfer ownership of items in their Private vault if needed

---
_Generated by saas-offboarding-checklist. Verify each step in the vendor's current docs - admin consoles change._
```
<!-- EXAMPLE-OUTPUT-END -->

## How it works

1. You list the SaaS tools the departing employee touched (25 in the catalog:
   Google Workspace, Microsoft 365, Slack, GitHub, GitLab, AWS, GCP, Azure,
   Stripe, Salesforce, HubSpot, Zendesk, Notion, Figma, Atlassian, Okta,
   1Password, LastPass, Zoom, Dropbox, Box, Heroku, Vercel, Cloudflare,
   PagerDuty — plus unlimited `--custom` entries).
2. The generator sorts every step into four phases, **in this order**:
   1. Revoke OAuth grants & SSO sessions (do first — kills live sessions)
   2. Revoke API keys & tokens
   3. Rotate shared credentials
   4. Transfer / export data
3. You get a markdown runbook with checkboxes and per-tool links to the
   vendor's own documentation.

## Verification

- `python -m pytest tests/ -q` — 21 tests, all green.
- Every vendor doc URL in the catalog was fetched and confirmed HTTP 200
  (`python scripts/verify_urls.py`; 24 via curl, 1 via live browser fetch —
  LastPass's CDN blocks bots).
- The example above is regenerated from a fresh tool run and diffed against
  this README by `scripts/embed_example.py`; CI-style check: extract the
  fenced block and `diff` it against a fresh `--demo` run — empty diff required.

## What it does NOT do

- **It cannot revoke anything itself.** This is a runbook generator, not an
  integration. Every step is performed by a human (or your IdP/SCIM automation)
  following the checklist.
- It does not discover which tools the employee used — you tell it.
- It does not store employee data; the runbook is written to a file you control.
- Vendor admin consoles change; the doc links were verified working on
  2026-10-17, but always confirm against the vendor's current UI.

## Built by Ingenious AI
- DisclosureGuard — https://wa.me/5016691053?text=Hi%20Ingenious%20AI%21%20I%20want%20early%20access%20to%20DisclosureGuard.
- ModelMinder — https://wa.me/5016691053?text=Hi%20Ingenious%20AI%21%20I%20want%20early%20access%20to%20ModelMinder.
- TermsWatch — https://wa.me/5016691053?text=Hi%20Ingenious%20AI%21%20I%20want%20early%20access%20to%20TermsWatch.
- Vibe-Code Audit — https://wa.me/5016691053?text=Hi%20Ingenious%20AI%21%20I%20want%20early%20access%20to%20Vibe-Code%20Audit.
- Rogue-Agent Defense — https://wa.me/5016691053?text=Hi%20Ingenious%20AI%21%20I%20want%20early%20access%20to%20Rogue-Agent%20Defense.
- BreachHunter — https://wa.me/5016691053?text=Hi%20Ingenious%20AI%21%20I%20want%20early%20access%20to%20BreachHunter.
- ChatBreaker — https://wa.me/5016691053?text=Hi%20Ingenious%20AI%21%20I%20want%20early%20access%20to%20ChatBreaker.
- Agent Flight Recorder — https://wa.me/5016691053?text=Hi%20Ingenious%20AI%21%20I%20want%20early%20access%20to%20Agent%20Flight%20Recorder.
- Agent Auth Gateway — https://wa.me/5016691053?text=Hi%20Ingenious%20AI%21%20I%20want%20early%20access%20to%20Agent%20Auth%20Gateway.
- DomainGuard — https://wa.me/5016691053?text=Hi%20Ingenious%20AI%21%20I%20want%20early%20access%20to%20DomainGuard.
- ContentCraft AI — https://wa.me/5016691053?text=Hi%20Ingenious%20AI%21%20I%20want%20early%20access%20to%20ContentCraft%20AI.
Built — try it free: invite code

## License

MIT — see [LICENSE](LICENSE).
