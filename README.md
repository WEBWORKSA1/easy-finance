# Easy.Finance

Free financial calculators, plain-English guides, and free expert matching. This is a static site with no build server, designed for GitHub Pages on the free plan.

## What's inside
- **12 calculators** (`/calculators/`): mortgage, compound interest, loan/EMI, home affordability, retirement, savings goal, debt payoff (avalanche vs snowball), credit card payoff, 50/30/20 budget, SIP, inflation and emergency fund. All of them support 7 currencies.
- **8 guides** (`/guides/`), each with a verified YouTube video, an FAQ and schema markup.
- **Get free help** (`get-help.html`): a 6-step lead wizard with consent capture.
- **Support** (`support.html`): donations, sponsorship, contests, careers and an advertise page.
- **Tools**: a money check-up quiz, a 40-term glossary and site search.
- **Compliance pages**: privacy, cookies, terms, disclaimer, how we make money, editorial guidelines, trademark and copyright, accessibility, plus `ads.txt`, `robots.txt` and `sitemap.xml`.

## Edit and rebuild
Page content lives in `tools/build.py`, `tools/guides.py` and `tools/calcs.py`. After editing, run:

```bash
python3 tools/build.py   # regenerates every HTML page, sitemap.xml and the search index
```

Site settings are in `assets/js/config.js`. That file holds the form alias, the donation links (PayPal, Stripe, Buy Me a Coffee, UPI) and the default currency.

## Forms
Forms post to FormSubmit through AJAX. The inbox address is never written in the HTML.

The first submission triggers an activation email to the inbox:
1. Click the activation link in that email.
2. Copy the random alias FormSubmit gives you.
3. Paste it into `formAlias` in `config.js`.

## Custom domain
1. Add a file named `CNAME` containing `easy.finance`.
2. At your registrar, create A records for `@` pointing to `185.199.108.153`, `185.199.109.153`, `185.199.110.153` and `185.199.111.153`.
3. Add a CNAME record for `www` pointing to `webworksa1.github.io`.
4. In repo **Settings → Pages**, enable **Enforce HTTPS**.

Once the custom domain is live, `ads.txt` will be served at the domain root, which AdSense requires.

## Legal
© Easy.Finance. This site is independent and is not affiliated with easyGroup Ltd, easyJet, or any business trading as "EasyFinance". See `trademark.html` for the full notice.
