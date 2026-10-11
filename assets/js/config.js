/* Easy.Finance — site configuration. Edit this file only; no other code changes needed. */
window.EF_CONFIG = {
  siteName: "Easy.Finance",
  adsenseClient: "ca-pub-6620975821265271",
  inquiryUrl: "https://web.works/contact",

  /* Form delivery (FormSubmit.co, free, no backend).
     The destination inbox is never written in the HTML; it is assembled at submit time.
     After the FIRST submission, FormSubmit emails an activation link to the inbox.
     Click it once. FormSubmit then shows a random alias string — paste it below to
     stop using the inbox address in requests entirely. */
  formAlias: "",           // e.g. "a1b2c3d4e5f6..." from FormSubmit activation
  _k: "bW9jLmxpYW1nQDFhc2tyb3diZXc=",

  /* Donation / payment links. Leave blank to fall back to the pledge form
     (pledges arrive by email and you reply with a payment link). */
  donate: {
    paypal: "",            // e.g. "https://www.paypal.com/donate/?hosted_button_id=XXXX"
    stripe: "",            // e.g. "https://buy.stripe.com/XXXX"
    buymeacoffee: "",      // e.g. "https://www.buymeacoffee.com/yourname"
    upi: ""                // e.g. "yourname@okaxis" (shown for Indian supporters)
  },

  /* Default calculator currency (auto-detected from browser locale if blank) */
  currency: ""
};
