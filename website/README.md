# APEX32 Secure — Developer Projects integration

Use this folder as **publication-ready content**, not as evidence that the live website has already been modified.

## Intended location

- Developer Projects index: `/developer-projects`
- Proposed detail slug: `/developer-projects/wifi-password-studio`
- Project grouping: **Security Tools / Python / Open-source status pending license**
- Repository URL **after repository creation**: `https://github.com/32oeb32/WiFi-Password-Studio`

## Project card

**Title:** Wi-Fi Password Studio  
**Subtitle:** Offline WPA/WPA2 passphrase creation and security education  
**Short description:** A standard-library Python terminal utility for generating strong Wi-Fi passphrases, checking basic password weaknesses, and working with synthetic password-pattern datasets in authorized environments.  
**Tags:** Python · Kali Linux · Offline · Security Education  
**Status:** Community preview · v2  
**Primary CTA:** View project (detail page)  
**Secondary CTA:** View source (enable only after GitHub repository exists)

## Detail-page hero

**Headline:** Create stronger Wi-Fi passwords. Understand the patterns behind weaker ones.  
**Body:** Wi-Fi Password Studio is a lightweight offline CLI built for password creation and security education. Generate cryptographically random credentials, build memorable synthetic passphrases, assess obvious weaknesses, and explore password-format patterns without sending data to external services.

**Highlights:** No dependencies · Offline operation · Python 3.10+ · Six CLI options · Local-only output

**Technical limitations:** The evaluator is heuristic and cannot predict real crack times. Human-pattern datasets are research samples, not recommended new credentials. No handshake capture, verification or router interaction.

**Requirements:** Python 3.10+; Kali Linux recommended.  
**Installation:** `python3 wifi_password_studio_v2.py` after downloading verified source.  
**Developer:** `#DEV32#` — [dev32@apex32-secure.com](mailto:dev32@apex32-secure.com)

## Integration procedure

1. Identify the **current** APEX32 Secure frontend template/component that powers the Developer Projects index. Do not overwrite unrelated project cards.
2. Add a new project record with the text and metadata above; use existing design tokens, accessibility rules, header/footer components and SSR route patterns.
3. Add the detail page at `/developer-projects/wifi-password-studio` when that route is supported, including canonical metadata, basic structured data and an internal breadcrumb to the index.
4. Link to the exact published GitHub source, **not** to an assumed release ZIP or direct-download endpoint.
5. Verify site build, route response, mobile readability, outbound link, and cache/CDN refresh before announcing publication.

**Do not deploy this stub HTML as the live page without matching the website's actual source framework.**
