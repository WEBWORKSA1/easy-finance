# Easy.Finance — Phase-wise Build Prompt

**Concept:** a free personal-finance calculator and guide hub ("money, made easy"), monetized by AdSense on high-CPC finance traffic, with a qualified-lead funnel and reader support.

**Why this concept:**
- Calculator pages ("mortgage calculator", "EMI calculator", "compound interest calculator") are evergreen, high-volume search queries.
- Personal finance is one of the highest-paying AdSense verticals.
- Every calculator result is a natural hand-off to a "get expert help" lead form.

The prompts below rebuild or extend the site. Run them in order. Each phase is self-contained.

---

## Phase 1 — Foundation & compliance
> Build a static, dependency-free website for the domain **Easy.Finance** that can be hosted on GitHub Pages (free plan).
>
> **Stack and structure**
> - Plain HTML, CSS and JS with relative links.
> - A Python generator (`tools/build.py`) owns a shared header and footer.
>
> **Every page includes**
> - The AdSense head script for `ca-pub-6620975821265271`.
> - A top bar reading "Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership", linked to https://web.works/contact.
> - A cookie notice.
> - Canonical URL, Open Graph tags and JSON-LD.
> - Dark mode, a skip link and mobile navigation.
>
> **Compliance and SEO pages**
> - About, Contact, Privacy (with Google advertising-cookie disclosures and opt-out links), Cookie policy, Terms, Disclaimer.
> - How We Make Money, Editorial Guidelines, Accessibility, Trademark & Copyright disclosure, HTML sitemap.
> - `sitemap.xml`, `robots.txt`, `ads.txt` (`google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0`), a 404 page and `.nojekyll`.
>
> **Brand**
> - Use an ink-navy, emerald and gold palette.
> - Never use orange-on-white "easy" trade dress.
> - Add a non-affiliation notice covering easyGroup, easyJet and any "EasyFinance"-named business.

## Phase 2 — Calculator engine (traffic core)
> Build one reusable calculator engine (`assets/js/calc.js`) driven by declarative configs.
>
> **Engine features**
> - Paired slider and number inputs.
> - Currency switcher (USD, CAD, EUR, GBP, AUD, INR, LKR) with locale auto-detect and range scaling.
> - Live result card with a headline figure, a stacked bar and key/value rows.
> - SVG line chart and a collapsible year-by-year schedule.
> - A "Get free expert help" CTA that deep-links to the lead form with `?topic=`.
>
> **Ship 12 calculators**
> Mortgage (P&I + tax + insurance + amortisation), Compound Interest, Loan/EMI, Home Affordability (28/36 DTI), Retirement (inflation + safe withdrawal rate + shortfall), Savings Goal, Debt Payoff (avalanche vs snowball, 3 debts), Credit Card Payoff, 50/30/20 Budget, SIP with step-up, Inflation, and Emergency Fund.
>
> **Each calculator page includes**
> - About 300 words of original "how it works" text, including the formula.
> - An FAQ section with FAQPage schema and WebApplication schema.
> - Related guides and cross-links to other calculators.

## Phase 3 — Content (AdSense approval and SEO depth)
> Write 8 original 700–1,000 word guides.
>
> **Topics:** budgeting, credit scores, emergency fund, index funds, mortgage basics, debt payoff strategies, retirement planning, compound interest.
>
> **Each guide includes**
> - A key-takeaways box, table of contents, byline and updated date.
> - A worked numeric example.
> - An embedded verified YouTube video (privacy-enhanced, click-to-load facade).
> - An FAQ, plus Article, FAQPage and VideoObject schema.
> - Cross-links to calculators.
>
> **Also add**
> - A video library page.
> - A 40-term glossary with DefinedTermSet schema.
> - An 8-question "Money Check-up" quiz that scores out of 100 and routes users to the tools that address their weakest answers.
> - Client-side site search driven by a generated index.

## Phase 4 — Lead generation (primary revenue engine #2)
> Build `/get-help.html` as a 6-step wizard.
>
> **Steps**
> 1. Need — tap cards for 8 verticals: mortgage, loans, debt relief, credit repair, investing/retirement, insurance, tax, coaching.
> 2. Amount.
> 3. Credit band.
> 4. Timeline.
> 5. Country and postal code.
> 6. Contact details plus an explicit consent checkbox for sharing with up to 3 partners.
>
> **Behaviour and trust**
> - Show a progress bar with time remaining, and allow back navigation.
> - Show reassurance copy: no credit check, free, no obligation, HTTPS.
> - Include a honeypot field and topic pre-fill from calculators.
> - Add "Why us", "How we're paid" and "Your data" blocks, plus a FAQ.
> - Put a sticky mobile CTA on every page.

## Phase 5 — Support, sponsorship, contests, talent
> **Support page**
> - Donation tiers (5 / 25 / 100 / 500).
> - One-time or monthly toggle, currency selector, and an allocation selector (operations, promotion & marketing, hiring, contests & prizes).
> - Payment links configurable in `config.js` (PayPal, Stripe, Buy Me a Coffee, UPI), with a pledge-by-email fallback.
> - A transparent allocation chart.
>
> **Advertise page:** sponsorship packages, lead partnerships and domain acquisition, with an inquiry form.
>
> **Contests page:** 3 categories, a prize structure, an entry form, and official rules (no purchase necessary, skill-based judging criteria, 18+, void where prohibited, Quebec note).
>
> **Careers page:** 6 roles and an application form.

## Phase 6 — Forms without exposing the inbox
> Route every form through FormSubmit's AJAX endpoint.
> - The destination inbox is never written in HTML. It is assembled at runtime from an encoded value in `config.js`.
> - After the first submission is confirmed, replace it with FormSubmit's random alias (`formAlias`).
> - Show success and error states inline, and fall back to the web.works inquiry link on errors.

## Phase 7 — Deploy
> Push to `github.com/webworksa1/easy-finance`.
> - Publish via GitHub Pages: branch `gh-pages`, or `main` / root.
> - For the custom domain:
>   1. Add a `CNAME` file containing `easy.finance`.
>   2. Point DNS: apex A records to 185.199.108.153, .109.153, .110.153 and .111.153; `www` CNAME to `webworksa1.github.io`.
>   3. Enforce HTTPS.
> - Then apply to AdSense with the root domain and enable Google's certified CMP for EEA/UK traffic.

## Phase 8 — Growth backlog
1. Add calculators: rent vs buy, refinance, auto loan, FD/RD, PPF, TFSA/RRSP, paycheck/take-home pay, net worth, DTI, CD.
2. Add "Best X" comparison pages with an affiliate disclosure.
3. Add country hubs (/in/, /ca/, /us/) with localised guides.
4. Add a newsletter platform (Beehiiv or ConvertKit) and replace the email-capture endpoint.
5. Add short-form video channels that reuse guides.
6. Add Hindi, French and Spanish translations.
