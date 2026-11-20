# Saif Industries website

A responsive, standalone website for Saif Industries LLC, a surplus military and aviation parts sourcing and supply business. Built with semantic HTML, CSS, JavaScript, and Vite. Fonts and the generated aviation image are served locally; there are no required third-party runtime requests.

## Run locally

Use Node.js 22.12+ (Node 24 was used for validation).

```sh
cd /workspace/MGMT-3450-Team-2/website
npm ci --cache /tmp/saif-npm-cache
npm run dev -- --port 3000
```

Open the local URL reported by Vite in a browser. The explicit npm cache path works around an unwritable default cache in the cloud environment; it can be omitted on a machine with a writable npm cache. Use the existing repository checkout; cloud tasks are already isolated.

## Build and preview

```sh
npm run build
npm run preview -- --port 4173
```

The production output is in `dist/`, which can be hosted as a static website. Run the commands from this `website` directory. No deployment to the existing company domain has been performed.

## Website features

- Responsive desktop, tablet, and phone layouts with mobile navigation.
- Aviation hero image, company history, six service cards, a sourcing process, FAQs, and contact details.
- Part-number/description inquiry that pre-fills a quote dialog.
- Required-field and email validation, editable inquiry preview, email draft link, and copy-to-clipboard option.
- Native dialog focus handling, Escape dismissal, labeled forms, skip navigation, visible focus states, and reduced-motion support.

The inquiry flow prepares a `mailto:` draft for **sales@saifind.com**. A visitor must review and send it using an email application, or copy the inquiry into an email service. The website does not send email, store submissions, submit orders, or query live inventory. Availability, condition, pricing, and delivery need confirmation from the sales team. A backend or email provider would be separate integration work.

## Browser checks

```sh
npx playwright install chromium
npm test
```

If using an existing cloud Chromium installation instead of downloading a Playwright browser:

```sh
PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm test
```

The Playwright suite runs on desktop and mobile Chromium configurations. It checks asset loading, company contact information, internal anchors, form validation, generated email details, editing, copying, dialog dismissal/focus restoration, mobile navigation, FAQs, and horizontal overflow at 320, 390, 768, 1024, and 1440 pixels. It starts a development server automatically or reuses an existing server on port 3000. It does not send email or establish a connection to real inventory.

## Content and imagery

Business details come from the About Us, services, and contact text the user supplied from https://www.saifindustries.com/. See [the recorded source information](../marketing/company-information.md). Direct access to the reference website returned HTTP 403 in this environment, so this is an original design using that supplied information rather than a verified reproduction of the current website.

`public/assets/aviation-hero.png` is an AI-generated conceptual aviation image, not a photograph of Saif's facility, stock, or customers. The design uses a text wordmark and a letter-S favicon. The earlier uploaded circular logo was not available as a local file; the wordmark is not represented as the original logo. Replace the image and wordmark with approved production assets when available.

The CAGE code is displayed as an identifier. No specific certifications or part airworthiness claims are added. No analytics, social-account links, fabricated stock results, or customer endorsements are included. The existing marketing package, customer database, workbook, CSVs, and scripts remain separate and unchanged by this website.
