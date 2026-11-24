# SAIF social profiles and marketing campaigns

Completed MGMT 3450 Team 2 class-project materials. These supplement the existing files in [marketing](../README.md); those files and the website/customer-management work are preserved.

## Open these first

- [Instagram post mockups](instagram-campaign/instagram-post-mockups-v3.html): the final standalone Instagram-style posts.
- [Rendered Instagram post preview](instagram-campaign/instagram-post-mockups-v3.jpg): ready to view on GitHub or use in a group presentation.
- [Instagram ads and strategy](instagram-campaign/instagram-feed-ads-and-strategy.html): scrolling feed, two ads, captions, targeting assumptions, and rollout.
- [LinkedIn ads and strategy](linkedin-campaign/linkedin-strategy-and-ads.html): customer ad and investor/strategic-partner awareness ad.
- [Full company-profile mockups](social-media-mockups/index.html): LinkedIn profile plus Instagram profile with six original posts and six aerospace concepts.

GitHub displays HTML source rather than running these previews. Download the folder or clone the repository, then open the HTML files in a browser. Keep the three sibling folders and their assets together. The checked-in previews use local image files to avoid duplicating large base64 images; the source build scripts can generate self-contained copies.

## Strategies, copy, and editable files

- [LinkedIn strategy](linkedin-campaign/strategy.txt), [ad copy](linkedin-campaign/campaign-data.json), and [results template](linkedin-campaign/measurement-template.csv).
- [Instagram strategy](instagram-campaign/strategy.txt), [ad copy](instagram-campaign/campaign-data.json), and [results template](instagram-campaign/measurement-template.csv).
- [Profile biographies and post captions](social-media-mockups/profile-copy-and-captions.txt) and [original Instagram captions](social-media-mockups/original-instagram-captions.txt).
- Each assets directory contains the image-only graphics. Build sources, generation prompts, and validation metadata accompany the outputs. Superseded experiments, downloaded website code, duplicate delivery folders, and ZIP archives are excluded.

## Rebuild

With Node.js, run these from this folder, in order:

```sh
node linkedin-campaign/build.mjs
node instagram-campaign/build.mjs
node instagram-campaign/build-posts-v3.mjs
node social-media-mockups/build.mjs
```

The optional PowerShell graphics scripts use Windows System.Drawing. The existing source graphics are checked in, so these scripts are not needed to view the work. Rebuilding overwrites generated previews in this folder; preserve edits before rebuilding.

## Status and sources

No live social account, ad publication, media spending, real engagement, investor commitment, or customer outcome is represented. Handles are proposals. The aircraft/components concepts are AI-generated and labeled; they do not document actual SAIF inventory or facilities. The LinkedIn investor creative uses SAIF's actual website facility photograph and does not assert an active fundraising offer.

Company facts, logo, and facility photo: [SAIF Industries](https://www.saifindustries.com/). Platform references and assumptions are recorded in the strategy files. Generation prompts record use of the built-in image generation tool.

## Repository safety check

The local folder initially had no commits or remote, so a commit-to-commit comparison against its original state was unavailable. The shared main history was fetched and reviewed before saving. Base commit: `0722b2f6a3dc644e5af3a9b2c1bdc5f0455f3fde` (November 20, 2026 UTC), predating this work. This package occupies a new directory; no pre-existing tracked files are replaced. A final fetch is required immediately before pushing.
