"""Catalog of SaaS tools with ordered revocation steps.

Each tool entry: slug, display name, vendor doc URL (verified to load),
and steps as (phase, text) tuples. Phases:
  oauth   - revoke OAuth grants & SSO sessions (do first)
  apikeys - revoke API keys & tokens
  shared  - rotate shared credentials the person knew
  data    - transfer / export their data
"""

PHASES = ("oauth", "apikeys", "shared", "data")

PHASE_TITLES = {
    "oauth": "Revoke OAuth grants & SSO sessions (do first)",
    "apikeys": "Revoke API keys & tokens",
    "shared": "Rotate shared credentials",
    "data": "Transfer / export data",
}

TOOLS = [
    {
        "slug": "google-workspace",
        "name": "Google Workspace",
        "doc_url": "https://support.google.com/a/answer/33314",
        "doc_title": "Delete or remove a user from your organization - Google Workspace Admin Help",
        "steps": [
            ("oauth", "Suspend the user immediately: Admin console > Users > select user > More > Suspend user (kills all sessions)"),
            ("oauth", "Security > API controls > Manage third-party access: revoke the user's OAuth grants"),
            ("apikeys", "APIs & Services > Credentials: delete OAuth clients and API keys they created"),
            ("shared", "Rotate shared service-account passwords and SMTP credentials they knew"),
            ("data", "Transfer Drive/Docs ownership: Users > select user > Transfer data, then delete the account"),
        ],
    },
    {
        "slug": "microsoft-365",
        "name": "Microsoft 365",
        "doc_url": "https://learn.microsoft.com/en-us/microsoft-365/admin/add-users/remove-former-employee",
        "doc_title": "Remove a former employee from Microsoft 365",
        "steps": [
            ("oauth", "Block sign-in: Users > Active users > select user > Block this user from signing in"),
            ("oauth", "Revoke sessions on the user's account page (forces re-auth everywhere)"),
            ("apikeys", "Microsoft Entra > App registrations: remove client secrets and certificates they created"),
            ("shared", "Rotate shared mailbox and admin credentials they knew"),
            ("data", "Convert the mailbox to a shared mailbox or grant manager access, then delete the user"),
        ],
    },
    {
        "slug": "slack",
        "name": "Slack",
        "doc_url": "https://slack.zendesk.com/hc/en-us/articles/204475027-Deactivate-a-member-s-account",
        "doc_title": "Deactivate a member's account - Slack Help Center",
        "steps": [
            ("oauth", "Deactivate the account: Administration > Manage members > Deactivate (ends all sessions)"),
            ("oauth", "Manage apps: review and revoke OAuth apps the user installed or authorized"),
            ("apikeys", "Revoke user tokens, bot tokens, and app-level tokens they created"),
            ("shared", "Rotate shared webhook URLs and integration credentials posted in channels"),
            ("data", "Export message history first if retention/compliance requires it"),
        ],
    },
    {
        "slug": "github",
        "name": "GitHub",
        "doc_url": "https://docs.github.com/en/organizations/managing-membership-in-your-organization/removing-a-member-from-your-organization",
        "doc_title": "Removing a member from your organization - GitHub Docs",
        "steps": [
            ("oauth", "Remove from every organization: People > select user > Remove from organization"),
            ("oauth", "Organization Settings > Third-party access: revoke their OAuth app authorizations"),
            ("apikeys", "User Settings > SSH and GPG keys: delete their SSH keys and GPG keys"),
            ("apikeys", "Developer settings: revoke personal access tokens (classic and fine-grained)"),
            ("apikeys", "Remove them from teams, repository collaborators, and GitHub App installations"),
            ("shared", "Rotate deploy keys and webhook secrets on repositories they administered"),
        ],
    },
    {
        "slug": "gitlab",
        "name": "GitLab",
        "doc_url": "https://docs.gitlab.com/ee/administration/moderate_users.html",
        "doc_title": "Moderate users (block / deactivate) - GitLab Docs",
        "steps": [
            ("oauth", "Block the user: Admin area > Users > select user > Block user (ends sessions)"),
            ("oauth", "Remove them from all groups and projects (or set membership to expire)"),
            ("apikeys", "Revoke their personal, project, and group access tokens"),
            ("apikeys", "Delete their SSH keys and deploy keys"),
            ("shared", "Rotate deploy tokens and runner registration tokens they handled"),
            ("data", "Reassign their issues and merge requests before deactivation"),
        ],
    },
    {
        "slug": "aws",
        "name": "AWS (IAM)",
        "doc_url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_remove.html",
        "doc_title": "Deleting an IAM user - AWS IAM User Guide",
        "steps": [
            ("oauth", "IAM > Users > select user: deactivate console access (remove console password, ends console sessions)"),
            ("oauth", "Remove the user from all groups and detach managed/inline policies"),
            ("apikeys", "Security credentials tab: deactivate, then delete every access key"),
            ("apikeys", "Delete any IAM roles or instance profiles they created for personal use"),
            ("shared", "Rotate credentials in Secrets Manager and Parameter Store they could read"),
            ("data", "Check CloudTrail for resources they launched; transfer ownership or terminate"),
        ],
    },
    {
        "slug": "gcp",
        "name": "Google Cloud (GCP)",
        "doc_url": "https://cloud.google.com/iam/docs/granting-changing-revoking-access",
        "doc_title": "Grant, change, and revoke access - Google Cloud IAM Docs",
        "steps": [
            ("oauth", "IAM > select the member > Remove access (revokes all project/folder/org bindings)"),
            ("oauth", "Remove them from Google Groups that grant IAM roles"),
            ("apikeys", "IAM > Service accounts: delete keys they created and disable service accounts they owned"),
            ("apikeys", "APIs & Services > Credentials: delete API keys and OAuth clients they created"),
            ("shared", "Rotate secrets in Secret Manager they had access to"),
        ],
    },
    {
        "slug": "azure",
        "name": "Microsoft Azure (Entra ID)",
        "doc_url": "https://learn.microsoft.com/en-us/entra/fundamentals/how-to-create-delete-users",
        "doc_title": "How to create or delete users in Microsoft Entra ID - Microsoft Learn",
        "steps": [
            ("oauth", "Entra ID > Users > select user: Block sign-in, then Revoke sessions"),
            ("oauth", "Remove app role assignments and OAuth consent grants"),
            ("apikeys", "App registrations: delete client secrets and certificates they created"),
            ("apikeys", "Remove them from privileged roles (Global Admin, etc.) first, then all groups"),
            ("shared", "Rotate shared service-principal credentials they knew"),
            ("data", "Transfer OneDrive data to their manager before deleting the account"),
        ],
    },
    {
        "slug": "stripe",
        "name": "Stripe",
        "doc_url": "https://docs.stripe.com/get-started/account/orgs/team",
        "doc_title": "Manage access to your organization - Stripe Docs",
        "steps": [
            ("oauth", "Settings > Team: remove the team member (revokes dashboard sessions)"),
            ("oauth", "Review and revoke OAuth authorizations for connected apps they installed"),
            ("apikeys", "Developers > API keys: roll every secret/publishable key they had access to"),
            ("apikeys", "Delete restricted keys they created; review webhook endpoints they added"),
            ("shared", "Rotate shared API keys stored in code, CI, or shared vaults"),
        ],
    },
    {
        "slug": "salesforce",
        "name": "Salesforce",
        "doc_url": "https://help.salesforce.com/s/articleView?id=sf.users_understanding_user_admin.htm",
        "doc_title": "Manage Users - Salesforce Help",
        "steps": [
            ("oauth", "Deactivate the user: Setup > Users > uncheck Active (ends sessions)"),
            ("oauth", "Setup > Connected Apps OAuth Usage: revoke their OAuth tokens"),
            ("apikeys", "Reset their security token and revoke API-only sessions"),
            ("apikeys", "Remove them from permission sets, roles, and public groups"),
            ("shared", "Rotate integration user credentials and named credentials they knew"),
            ("data", "Transfer record ownership (accounts, opportunities) to their manager"),
        ],
    },
    {
        "slug": "hubspot",
        "name": "HubSpot",
        "doc_url": "https://knowledge.hubspot.com/settings/add-and-remove-users",
        "doc_title": "Add and remove HubSpot users - HubSpot Knowledge Base",
        "steps": [
            ("oauth", "Settings > Users & Teams > remove the user (ends sessions)"),
            ("oauth", "Review connected private apps and revoke their authorizations"),
            ("apikeys", "Delete private app access tokens they created"),
            ("apikeys", "Remove them from teams, permission sets, and content access groups"),
            ("data", "Reassign their contacts, companies, deals, and tickets"),
        ],
    },
    {
        "slug": "zendesk",
        "name": "Zendesk",
        "doc_url": "https://support.zendesk.com/hc/en-us/articles/4408844129946-Removing-or-replacing-a-team-member",
        "doc_title": "Removing or replacing a team member - Zendesk Help",
        "steps": [
            ("oauth", "Suspend then delete the team member: Team > select user > Delete (ends sessions)"),
            ("oauth", "Revoke their OAuth tokens under API > OAuth clients if they built integrations"),
            ("apikeys", "Admin Center > Apps and integrations > API: delete API tokens they created"),
            ("apikeys", "Remove them from groups, roles, and triggers/automations they owned"),
            ("data", "Reassign their open tickets before deletion"),
        ],
    },
    {
        "slug": "notion",
        "name": "Notion",
        "doc_url": "https://www.notion.com/help/add-members-admins-guests-and-groups",
        "doc_title": "Manage members, admins & guests in Notion - Notion Help",
        "steps": [
            ("oauth", "Settings & members > Members > remove the member (ends sessions)"),
            ("oauth", "Review their OAuth connections under Settings > Connections and revoke"),
            ("apikeys", "Delete internal integrations and API tokens they created"),
            ("shared", "Rotate shared integration tokens posted in team wikis"),
            ("data", "Transfer ownership of private pages they need to keep before removal"),
        ],
    },
    {
        "slug": "figma",
        "name": "Figma",
        "doc_url": "https://help.figma.com/hc/en-us/articles/360039965493-Remove-access-to-teams",
        "doc_title": "Remove someone from your team - Figma Help",
        "steps": [
            ("oauth", "Admin settings > Members > remove the member (ends sessions)"),
            ("oauth", "Revoke OAuth authorizations for plugins/apps they connected"),
            ("apikeys", "Delete personal access tokens they generated"),
            ("shared", "Rotate shared library or plugin credentials"),
            ("data", "Transfer ownership of their files and projects to the team"),
        ],
    },
    {
        "slug": "atlassian",
        "name": "Atlassian (Jira/Confluence)",
        "doc_url": "https://support.atlassian.com/user-management/docs/deactivate-a-managed-account/",
        "doc_title": "Deactivate a managed account - Atlassian Support",
        "steps": [
            ("oauth", "admin.atlassian.com > Directory > Users > Deactivate user (ends sessions)"),
            ("oauth", "Review connected apps under their account and revoke OAuth access"),
            ("apikeys", "Delete API tokens they created (account settings > Security > API tokens)"),
            ("apikeys", "Remove them from groups, project roles, and space permissions"),
            ("data", "Reassign their issues and transfer Confluence page ownership"),
        ],
    },
    {
        "slug": "okta",
        "name": "Okta",
        "doc_url": "https://help.okta.com/en-us/Content/topics/users-groups-profiles/usgp-deactivate-user-account.htm",
        "doc_title": "Deactivate and delete user accounts - Okta Help",
        "steps": [
            ("oauth", "Directory > People > select user > Deactivate (kills SSO sessions everywhere)"),
            ("oauth", "Clear their active sessions explicitly after deactivation"),
            ("apikeys", "Revoke API tokens and OAuth clients they created"),
            ("apikeys", "Remove them from groups, admin roles, and app assignments"),
            ("shared", "Rotate shared admin credentials and enrollment policies they touched"),
        ],
    },
    {
        "slug": "1password",
        "name": "1Password",
        "doc_url": "https://support.1password.com/offboarding/",
        "doc_title": "Offboard a team member - 1Password Support",
        "steps": [
            ("oauth", "Suspend then remove the team member (ends all sessions and device access)"),
            ("oauth", "Revoke their OAuth/SSO provisioning link if SCIM was used"),
            ("apikeys", "Delete service-account and Connect API tokens they created"),
            ("shared", "CRITICAL: rotate every shared vault password they had access to"),
            ("shared", "Review vault access reports for vaults they viewed"),
            ("data", "Transfer ownership of items in their Private vault if needed"),
        ],
    },
    {
        "slug": "lastpass",
        "name": "LastPass",
        "doc_url": "https://blog.lastpass.com/posts/steps-to-effective-employee-offboarding",
        "doc_title": "8 Essential Steps to Effective Employee Offboarding - LastPass Blog",
        "steps": [
            ("oauth", "Admin Console > Users > delete or disable the user (ends sessions)"),
            ("apikeys", "Revoke provisioning/API credentials they created"),
            ("shared", "CRITICAL: rotate every shared-folder password they had access to"),
            ("shared", "Run a security report on shared folders they viewed"),
            ("data", "Transfer their vault items to a manager before deletion"),
        ],
    },
    {
        "slug": "zoom",
        "name": "Zoom",
        "doc_url": "https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061173",
        "doc_title": "Deleting users - Zoom Support",
        "steps": [
            ("oauth", "User Management > Users > delete the user (ends meetings and sessions)"),
            ("oauth", "Revoke OAuth authorizations for Marketplace apps they installed"),
            ("apikeys", "Marketplace > manage: delete JWT/Server-to-Server OAuth credentials they created"),
            ("apikeys", "Remove them from groups, roles, and admin privileges"),
            ("shared", "Rotate shared meeting/webinar credentials and API secrets"),
            ("data", "Transfer their cloud recordings to a manager before deletion"),
        ],
    },
    {
        "slug": "dropbox",
        "name": "Dropbox",
        "doc_url": "https://www.dropbox.com/help/business/delete-member",
        "doc_title": "How to delete a member from a Dropbox team - Dropbox Help",
        "steps": [
            ("oauth", "Admin console > Members > remove the member (ends sessions; choose remote wipe)"),
            ("oauth", "Revoke OAuth app authorizations under their account"),
            ("apikeys", "Delete API app tokens they generated"),
            ("shared", "Rotate shared links they created (disable or expire them)"),
            ("data", "Transfer their files to a manager; remote-wipe linked devices"),
        ],
    },
    {
        "slug": "box",
        "name": "Box",
        "doc_url": "https://support.box.com/hc/en-us/articles/360043694514-Deleting-Managed-Users",
        "doc_title": "Deleting Managed Users - Box Support",
        "steps": [
            ("oauth", "Admin Console > Users > deactivate the user (ends sessions)"),
            ("oauth", "Revoke OAuth tokens for apps they authorized"),
            ("apikeys", "Developer Console: delete custom apps and API tokens they created"),
            ("shared", "Rotate shared-link passwords and expire public shared links they made"),
            ("data", "Transfer content ownership to their manager before deletion"),
        ],
    },
    {
        "slug": "heroku",
        "name": "Heroku",
        "doc_url": "https://devcenter.heroku.com/articles/collaborating",
        "doc_title": "Collaborating with Other Developers on Your App - Heroku Dev Center",
        "steps": [
            ("oauth", "Remove them as collaborator from every app: Access tab > remove"),
            ("oauth", "Remove them from the Heroku Team (Team > Members > remove)"),
            ("apikeys", "Have them revoke API tokens; rotate any tokens stored in CI they touched"),
            ("apikeys", "Remove their SSH keys from the team account"),
            ("shared", "Rotate config vars (database URLs, API secrets) for apps they accessed"),
        ],
    },
    {
        "slug": "vercel",
        "name": "Vercel",
        "doc_url": "https://vercel.com/docs/teams-and-accounts/create-or-join-a-team",
        "doc_title": "Account management (team membership) - Vercel Docs",
        "steps": [
            ("oauth", "Team Settings > Members > remove the member (ends sessions)"),
            ("oauth", "Revoke OAuth authorizations for integrations they installed"),
            ("apikeys", "Delete tokens they created (Account Settings > Tokens)"),
            ("apikeys", "Remove them from projects and shared environments"),
            ("shared", "Rotate environment variables and webhook secrets on projects they accessed"),
        ],
    },
    {
        "slug": "cloudflare",
        "name": "Cloudflare",
        "doc_url": "https://developers.cloudflare.com/fundamentals/setup/manage-members/",
        "doc_title": "Manage account members - Cloudflare Docs",
        "steps": [
            ("oauth", "Manage Account > Members > remove the member (ends sessions)"),
            ("oauth", "Revoke their SSO/OAuth sessions explicitly"),
            ("apikeys", "My Profile > API Tokens: revoke tokens they created; rotate the Global API key if shared"),
            ("apikeys", "Remove them from super-admin and scoped roles"),
            ("shared", "Rotate origin certificates, Tunnel tokens, and webhook secrets they knew"),
        ],
    },
    {
        "slug": "pagerduty",
        "name": "PagerDuty",
        "doc_url": "https://support.pagerduty.com/docs/offboarding",
        "doc_title": "Offboarding - PagerDuty Support",
        "steps": [
            ("oauth", "Configuration > Users > delete the user (ends sessions)"),
            ("oauth", "Revoke OAuth app authorizations they granted"),
            ("apikeys", "Delete API keys and integration keys they created"),
            ("apikeys", "Remove them from teams, escalation policies, and schedules"),
            ("shared", "Rotate shared integration keys on services they owned"),
            ("data", "Reassign their open incidents before deletion"),
        ],
    },
]


def get_tool(slug):
    """Return the tool dict for a slug, or None."""
    for tool in TOOLS:
        if tool["slug"] == slug:
            return tool
    return None


def list_slugs():
    """All tool slugs in catalog order."""
    return [t["slug"] for t in TOOLS]
