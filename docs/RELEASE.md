# Release procedure

## Current state

The source is prepared as a **v2 community preview**. The availability of a GitHub release, website deployment, signed packages or OS-specific qualification is **not yet asserted**.

## Before publication

- [ ] Confirm repository name and owner (`32oeb32/WiFi-Password-Studio` proposed).
- [ ] Choose and add a license file (MIT, GPL-3.0 or another approved license). No license is selected in this package.
- [ ] Review source and documentation for accidental credentials, identifying data and unsupported claims.
- [ ] Run Python compile, internal self-test and external unit tests on Kali Linux.
- [ ] Confirm script is still offline and has six options.
- [ ] Review optional plaintext export instructions and candidate-data safety language.
- [ ] Confirm GitHub Actions are green after first push.
- [ ] Decide release tag, e.g. `v2.0.0` only when qualification and repository are ready.
- [ ] Prepare SHA-256 checksum of release artifact and verify from a clean download.
- [ ] Publish repository/release before enabling live links on the APEX32 Secure website.

## GitHub flow

```bash
# after you have created an empty repository in GitHub:
git init
git branch -M main
git add .
git commit -m "feat: publish Wi-Fi Password Studio v2 source and docs"
git remote add origin git@github.com:32oeb32/WiFi-Password-Studio.git
git push -u origin main
```

A repository creation action is separate from this guide. Do not try to push to a URL until the repository exists and your GitHub credentials are configured.

## Website publication gate

Only advertise the project as **Available on GitHub** once the repository URL works. Only advertise a **Download v2** button when a real release asset exists. A plain **View source** link can point to a published repository even before the first tagged release.
