# TradeZIP Blog Architecture and Build Brief

**Website:** https://trade-zip.com/
**Blog name shown to visitors:** The Contractor Growth Hub
**Permanent blog URL:** https://trade-zip.com/blog/
**Purpose:** Build an SEO-scalable editorial system capable of supporting thousands of articles without changing article URLs or creating duplicate and thin pages.

## 1. Current-site findings

The TradeZIP brand journey is:

1. Get searched
2. Get found
3. Get booked

The website's confirmed industry directory contains four groups and eleven industry hubs:

### Home Systems

- Plumbers
- Electricians
- HVAC

### Home Projects

- General Contractors
- Concrete & Masonry
- Flooring & Tile
- Painters

### Maintenance

- Cleaning & Pressure Wash
- Landscaping & Lawn
- Pool & Spa

### Auto

- Auto Repair & Services

The blog must use these exact public-facing groups and industry labels so its taxonomy matches the main website. The industries must still be maintained through a configurable CMS collection rather than hard-coded into templates.

TradeZIP products and capabilities currently represented on the site include:

- Contractor websites
- Local service-area landing pages
- Local SEO and directory listings
- Google Business Profile support
- Weekly blog content
- Social content
- Google review generation
- AI website chat
- AI voice receptionist
- Instant responses to Angi and Thumbtack leads
- Quotes, invoices and online payments
- Print the Street direct-mail campaigns
- Custom contractor automations

The blog architecture should lead readers naturally from educational content to one of these products or a pricing plan.

## 2. Final URL architecture

### Core routes

| Page type | URL pattern | Example |
| --- | --- | --- |
| Blog homepage | `/blog/` | `/blog/` |
| Individual article | `/blog/[content-type]/[article-slug]/` | `/blog/how-to/get-more-google-reviews-for-plumbers/` |
| Content-type hub | `/blog/[content-type]/` | `/blog/how-to/` |
| Topic hub | `/blog/topics/[topic-slug]/` | `/blog/topics/local-seo/` |
| Industry hub | `/blog/industries/[industry-slug]/` | `/blog/industries/plumbers/` |
| Author page | `/blog/authors/[author-slug]/` | `/blog/authors/tradezip-team/` |
| Blog pagination | `/blog/page/[number]/` | `/blog/page/2/` |
| Internal search | `/blog/search/?q=[query]` | `/blog/search/?q=reviews` |

### URL rules

- Place every article in exactly one approved, permanent content-type directory.
- Use lowercase words separated by hyphens.
- Use `/how-to/`, not `/howto/`.
- Use concise, descriptive article slugs that include the industry when the article is industry-specific.
- Do not include dates, years, topic categories, post IDs or `.html` in public URLs.
- Do not change an article URL when its title, topic, industry or publish date changes.
- If a URL must change, create a server-side 301 redirect from the old URL to the new one.
- Each article must have one self-referencing canonical URL.
- The same article may appear on several topic and industry hubs, but it must never be duplicated under multiple article URLs.

### Approved content-type directories

Each article must belong to one, and only one, permanent content type.

| Content type | URL | Use for | Example article URL |
| --- | --- | --- | --- |
| How-to | `/blog/how-to/` | A specific task with actionable steps | `/blog/how-to/get-more-google-reviews-for-plumbers/` |
| Guides | `/blog/guides/` | Broad, comprehensive education | `/blog/guides/local-seo-for-hvac-companies/` |
| Checklists | `/blog/checklists/` | Audits, setup lists and repeatable processes | `/blog/checklists/google-business-profile-for-electricians/` |
| Ideas | `/blog/ideas/` | Inspiration and lists of practical options | `/blog/ideas/landscaping-marketing-ideas/` |
| Comparisons | `/blog/comparisons/` | Product, platform or strategy comparisons | `/blog/comparisons/angi-vs-thumbtack-for-contractors/` |
| Costs | `/blog/costs/` | Pricing, budgeting and cost explanations | `/blog/costs/contractor-website-cost/` |
| Case studies | `/blog/case-studies/` | Genuine TradeZIP customer evidence and outcomes | `/blog/case-studies/how-a-plumber-expanded-local-visibility/` |
| Templates | `/blog/templates/` | Downloadable scripts, forms and worksheets | `/blog/templates/contractor-review-request-text-message/` |

Do not add new content types casually. If an article could fit more than one type, select the format that best matches its dominant search intent before publication. The assigned type becomes part of the permanent URL.

Content-type hubs should be indexable once they contain a useful original introduction and enough articles to serve visitors. Empty content-type hubs should not be published or indexed.

### Good article URLs

- `/blog/costs/contractor-website-cost/`
- `/blog/guides/local-seo-for-roofers/`
- `/blog/checklists/google-business-profile-for-plumbers/`
- `/blog/guides/ai-receptionist-for-hvac-companies/`
- `/blog/how-to/market-a-landscaping-job-to-the-neighborhood/`

### URLs to avoid

- `/blog/2026/08/contractor-website-cost/`
- `/blog/howto/get-reviews/`
- `/blog/local-seo/plumbers/article-name/`
- `/blog/post-84729/`
- `/blog/contractor-website-cost.html`
- Multiple URLs that display the same article

## 3. Visitor-facing information architecture

The main blog navigation should reflect the TradeZIP growth journey rather than exposing a confusing list of SEO categories.

### Get Searched

Contains content that creates awareness and gives more local customers a reason to search for the business:

- Print the Street
- Contractor direct mail
- Neighborhood marketing
- Social-media marketing
- Referral generation
- Customer follow-up
- Turning completed work into content

### Get Found

Contains content about:

- Contractor websites
- Local SEO
- Service-area landing pages
- Google Business Profile
- Directory listings and citations
- Blogging and content
- Being discovered in Google and AI search

### Get Booked

Contains content about:

- Google reviews
- Reputation management and social proof
- Website trust and conversion
- Lead response time
- Angi and Thumbtack leads
- AI receptionists
- Missed-call recovery
- Website chat
- Online booking
- Quotes, invoices and online payments
- Contractor automation
- Repetitive admin work
- Invoice follow-up
- Lead routing
- Contractor productivity
- Connecting business software

These three labels should be the primary visual navigation groups. The indexable SEO topic hubs beneath them should use clear search-oriented names.

## 4. Indexable topic hubs

Create these initial topic hub pages:

| Navigation group | Topic hub | URL |
| --- | --- | --- |
| Get Searched | Direct Mail and Neighborhood Marketing | `/blog/topics/neighborhood-marketing/` |
| Get Searched | Social Media for Contractors | `/blog/topics/contractor-social-media/` |
| Get Searched | Referrals and Customer Follow-Up | `/blog/topics/customer-follow-up/` |
| Get Found | Contractor Websites | `/blog/topics/contractor-websites/` |
| Get Found | Local SEO | `/blog/topics/local-seo/` |
| Get Found | Service-Area Pages | `/blog/topics/service-area-pages/` |
| Get Found | Google Business Profile | `/blog/topics/google-business-profile/` |
| Get Found | Business Directories | `/blog/topics/business-directories/` |
| Get Found | Content and AI Search | `/blog/topics/content-and-ai-search/` |
| Get Booked | Contractor Lead Generation | `/blog/topics/contractor-lead-generation/` |
| Get Booked | Reviews and Reputation | `/blog/topics/reviews-and-reputation/` |
| Get Booked | Website Conversion | `/blog/topics/website-conversion/` |
| Get Booked | Lead Response | `/blog/topics/lead-response/` |
| Get Booked | AI Receptionists | `/blog/topics/ai-receptionists/` |
| Get Booked | Quotes and Payments | `/blog/topics/quotes-and-payments/` |
| Get Booked | Contractor Automation | `/blog/topics/contractor-automation/` |
| Get Booked | Contractor Business Operations | `/blog/topics/contractor-operations/` |

### Topic-hub requirements

Every indexable topic hub must include:

- A unique H1
- A useful editorial introduction written specifically for that topic
- A featured cornerstone guide
- Latest articles
- Most useful or popular articles
- Relevant industries
- A CTA to the closest TradeZIP service page
- Pagination when necessary
- A unique SEO title and meta description
- A self-referencing canonical URL
- `BreadcrumbList` structured data

Do not index an empty or nearly empty hub. A hub should generally remain unpublished or set to `noindex,follow` until it contains enough useful articles and original editorial context to serve visitors.

## 5. Industry taxonomy

The blog must use the same four groups and eleven industries shown on the TradeZIP website.

| Industry group | Public industry label | Industry hub URL |
| --- | --- | --- |
| Home Systems | Plumbers | `/blog/industries/plumbers/` |
| Home Systems | Electricians | `/blog/industries/electricians/` |
| Home Systems | HVAC | `/blog/industries/hvac/` |
| Home Projects | General Contractors | `/blog/industries/general-contractors/` |
| Home Projects | Concrete & Masonry | `/blog/industries/concrete-masonry/` |
| Home Projects | Flooring & Tile | `/blog/industries/flooring-tile/` |
| Home Projects | Painters | `/blog/industries/painters/` |
| Maintenance | Cleaning & Pressure Wash | `/blog/industries/cleaning-pressure-washing/` |
| Maintenance | Landscaping & Lawn | `/blog/industries/landscaping-lawn-care/` |
| Maintenance | Pool & Spa | `/blog/industries/pool-spa-services/` |
| Auto | Auto Repair & Services | `/blog/industries/auto-repair-services/` |

Industry hubs must be generated from a CMS collection or configuration file so future industries can be added without creating new templates.

### Combined-industry handling

Keep the website's combined labels as the main public hubs, but allow articles to carry more specific internal classification values. For example:

- Cleaning & Pressure Wash can contain `cleaning` and `pressure-washing` article tags.
- Landscaping & Lawn can contain `landscaping`, `lawn-care` and `lawn-maintenance` article tags.
- Pool & Spa can contain `pool-service`, `pool-cleaning` and `spa-service` article tags.
- Auto Repair & Services can contain `auto-repair`, `auto-detailing`, `tire-service` and other approved service tags.

These internal tags are for content organization and recommendations. Do not automatically create indexable tag archives. A separate public industry hub should only be created later if TradeZIP adds that industry to the main website navigation and has enough unique content to support it.

### Industry-hub requirements

Each industry hub must contain more than a filtered article grid. Include:

- A unique industry-specific H1 and introduction
- The primary marketing challenges for that industry
- Recommended starting guides
- Articles grouped by Get Searched, Get Found and Get Booked
- A link to the matching commercial industry page, such as `/contractor-websites/plumbers/`
- A relevant product CTA
- Unique title, description, canonical URL and breadcrumb data

Do not automatically create indexable pages for every combination of industry and topic. Filtered combinations such as `/blog/industries/plumbers/?topic=reviews` should be usable by visitors but set to `noindex,follow` and canonicalized appropriately. A combined landing page should become indexable only when it is intentionally curated and provides substantial unique value.

## 6. Blog homepage design

### Header

Use the standard TradeZIP site header. Add **Blog** or **Resources** to the main navigation. If a Resources dropdown is used, it should include:

- Contractor Growth Hub
- Get Searched
- Get Found
- Get Booked
- Browse by Industry

### Blog hero

**Eyebrow:** The Contractor Growth Hub
**H1:** Practical ways to get searched, get found and get booked.
**Supporting copy:** Straightforward advice on contractor websites, local SEO, reviews, lead response and the tools that keep your business moving.

Include a prominent search field with placeholder text:

`What do you want help with?`

### Homepage section order

1. Hero and blog search
2. Featured cornerstone article
3. Three journey cards: Get Searched, Get Found and Get Booked
4. Browse by Industry grid, grouped as Home Systems, Home Projects, Maintenance and Auto
5. Latest articles
6. Most popular or editor-selected guides
7. Product-connected CTA
8. Newsletter or practical tips signup, only if TradeZIP will actively maintain it

### Visual direction

- Use the established dark navy TradeZIP background and cyan-to-purple gradient.
- Use the TradeZIP pin icon as an accent, not as a repeated decorative element on every card.
- Use real contractor and job-site imagery for featured articles.
- Keep article cards clean, with one image, category, title, short excerpt and reading time.
- Use a denser editorial layout than the sales homepage while retaining the same typography and buttons.
- Make search and Browse by Industry highly visible on mobile.

## 7. Article-page template

Every article page should contain:

1. Breadcrumbs
2. Topic label and optional trade label
3. One H1
4. Short summary or standfirst
5. Author, publish date, updated date and reading time
6. Featured image
7. Table of contents for longer articles
8. Main article content
9. Contextual product CTA placed after the problem has been explained
10. Key-takeaways box
11. Optional FAQs when they genuinely help the reader
12. Author box
13. Related articles
14. Final CTA connected to the article's intent

### Article layout rules

- Use one H1 only.
- Use logical H2 and H3 headings.
- Keep paragraphs short and mobile-readable.
- Use descriptive internal-link anchor text, not "click here."
- Support claims with sources and link to primary sources where available.
- Use original examples, checklists, images, data or first-hand TradeZIP experience.
- Do not write to an arbitrary word count.
- Do not add FAQs merely to create keyword variations.
- Avoid exaggerated rankings, revenue claims and guarantees.

## 8. Article CMS/content model

The article content type should include:

- `title`
- `slug`
- `excerpt`
- `bodyHtml` or structured rich-text body
- `seoTitle`
- `metaDescription`
- `canonicalUrl`
- `primaryKeyword`
- `secondaryKeywords`
- `searchIntent`
- `contentTypeId`
- `author`
- `datePublished`
- `dateModified`
- `featuredImage`
- `featuredImageAlt`
- `topicIds`
- `industryIds`
- `featured`
- `cornerstone`
- `readingTime`
- `relatedArticleIds`
- `relatedProduct`
- `ctaHeading`
- `ctaCopy`
- `ctaLabel`
- `ctaUrl`
- `faqItems`
- `sources`
- `status`

Topics, industries and authors must each be separate structured collections rather than free-text labels.

## 9. Internal-linking system

Every published article must link to:

- Its primary topic hub
- Its relevant industry hub when industry-specific
- At least two genuinely related articles
- One relevant TradeZIP commercial service or industry page
- One relevant next step or CTA

Every topic and industry hub must link back to its cornerstone articles. Related articles should be chosen editorially or by shared topic and industry data, not purely by publication date.

### Commercial destinations

Use these commercial page patterns:

- `/contractor-websites/`
- `/contractor-websites/[trade]/`
- `/local-seo-for-contractors/`
- `/google-reviews-for-contractors/`
- `/ai-receptionist-for-contractors/`
- `/contractor-quoting-software/`
- `/print-your-street/`
- `/contractor-automation/`
- `/pricing/`

The build should not create these pages automatically if they do not yet exist. Until built, CTA URLs should be configurable and should point to the most relevant existing destination.

## 10. SEO and technical requirements

### Rendering and crawlability

- Article and hub content must be present in the server-rendered or statically generated HTML.
- Do not rely on browser-only JavaScript to inject primary article content.
- All links must use real crawlable `<a href>` elements.
- Maintain one canonical version of each URL.
- Include new articles and hubs in XML sitemaps.
- Connect the production domain to Google Search Console.

### Structured data

Article pages should include valid JSON-LD for:

- `BlogPosting`
- `BreadcrumbList`
- The TradeZIP organization as publisher
- The real author or editorial team

Use accurate `headline`, `description`, `image`, `datePublished`, `dateModified`, `author`, `publisher` and `mainEntityOfPage` values. Only include FAQ structured data if the visible page contains the same genuine FAQ content and current Google eligibility requirements are met.

### Metadata

Every indexable page needs:

- Unique SEO title
- Unique meta description
- Canonical URL
- Open Graph title, description, image and URL
- Social sharing metadata
- Descriptive image alt text

### Pagination, filters and search

- Use crawlable paginated archive pages.
- Each pagination page should have its own canonical URL.
- Set internal search-result pages to `noindex,follow`.
- Set query-parameter filter combinations to `noindex,follow` unless an individual combination has been deliberately turned into a curated landing page.
- Do not generate millions of crawlable combinations of topics, trades, dates and tags.

### Sitemaps

Use a sitemap index with separate files for:

- Articles
- Topic hubs
- Industry hubs
- Authors and other editorial pages if indexable

Sitemaps may be split into manageable shards as volume grows. Only canonical, indexable, successful 200-status URLs should appear in the sitemap.

### Images and mobile performance

- Standard featured-image ratio: 1200 × 630.
- Supply responsive image sizes and explicit width and height values.
- Prefer optimized WebP or AVIF with a JPG fallback when required.
- Lazy-load below-the-fold images.
- Do not lazy-load the main article image when it is the page's largest above-the-fold content element.
- Keep buttons, filters and article cards touch-friendly.
- Avoid intrusive popups on mobile.

## 11. Editorial and indexing controls

### Content statuses

- Draft
- In review
- Scheduled
- Published
- Updating
- Archived

### Quality controls before publication

Confirm that each article:

- Answers a real contractor question
- Has a specific intended reader and search intent
- Adds something beyond a summary of existing search results
- Contains no fabricated statistics, testimonials or outcomes
- Has been fact-checked
- Includes a useful internal-link path
- Has a relevant CTA
- Is not competing with an existing article targeting the same intent
- Has correct metadata, image, canonical URL and schema

### Handling old content

- Update genuinely outdated information and display an accurate modified date.
- Do not change dates solely to make content appear fresh.
- Consolidate overlapping weak articles into the strongest canonical article.
- Redirect consolidated URLs to the retained article.
- Keep evergreen URLs even when the year in the visible title changes.

## 12. Initial launch content

Launch with the blog homepage, the required topic hubs, confirmed industry hubs and at least these ten foundational articles:

| Article | Permanent URL |
| --- | --- |
| How Much Does a Contractor Website Cost? | `/blog/costs/contractor-website-cost/` |
| Contractor Website Mistakes That Cost You Leads | `/blog/guides/contractor-website-mistakes/` |
| Local SEO for Contractors: A Practical Guide | `/blog/guides/local-seo-for-contractors/` |
| Do Service-Area Pages Help Contractors Rank Locally? | `/blog/guides/service-area-pages-for-contractors/` |
| Google Business Profile Optimization Checklist for Contractors | `/blog/checklists/google-business-profile-for-contractors/` |
| The Best Online Directories for Contractors | `/blog/guides/best-online-directories-for-contractors/` |
| How Contractors Can Get More Google Reviews | `/blog/how-to/get-more-google-reviews-for-contractors/` |
| AI Receptionists for Contractors: What They Can and Cannot Do | `/blog/guides/ai-receptionist-for-contractors/` |
| How Quickly Should You Respond to Angi and Thumbtack Leads? | `/blog/guides/angi-thumbtack-lead-response-time/` |
| How to Turn One Completed Job Into More Work From the Neighborhood | `/blog/how-to/get-more-neighborhood-jobs/` |

The visible title may include a year when useful, but the URL should remain evergreen.

## 13. Build acceptance checklist

The blog build is complete only when:

- `/blog/` is live and linked from the main site navigation and footer.
- Article, content-type, topic, industry and author templates work on desktop and mobile.
- All article URLs use one approved permanent content-type directory.
- Blog search works.
- Topic and industry filtering works without creating indexable duplicate URLs.
- Breadcrumbs are visible and valid.
- Article and breadcrumb structured data pass Google's Rich Results Test where applicable.
- Canonicals, titles and meta descriptions are present and unique.
- XML sitemaps include all intended indexable editorial URLs.
- Search and filter pages are excluded from indexing.
- Related articles and commercial CTAs are populated.
- Pages are server rendered or statically generated and function with JavaScript disabled for primary content.
- Mobile layout has no horizontal scrolling, clipped headings or undersized tap targets.
- A 301 redirect mechanism exists for any future slug changes.
- Google Search Console is connected after the production domain is live.

## 14. Important implementation decision

Do not build thousands of static category combinations in advance. Build three reusable content systems:

1. Articles with one permanent content-type URL
2. Curated content-type hubs
3. Curated topic hubs
4. Curated industry hubs

An article can belong to several topics and industries through CMS relationships. This gives TradeZIP unlimited editorial scale without duplicate articles, unstable URLs or a crawlable maze of low-value filter pages.

## 15. Official implementation references

- Google SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Helpful, reliable, people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google AI search optimization guidance: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Structured data introduction: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- Article structured data: https://developers.google.com/search/docs/appearance/structured-data/article
- Breadcrumb structured data: https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
- Crawlable link guidance: https://developers.google.com/search/docs/crawling-indexing/links-crawlable

---

## Author roster (approved by Amy 2026-08-19)

- **Amy Bourke** — Founder — slug: `amy-bourke`
- **Elliot Farmer** — Head of Sales — slug: `elliot-farmer`
- **Elizabeth Adams** — Head of GTM & Enablement — slug: `elizabeth-adams`
- **Eric Stark** — Senior Business Advisor — slug: `eric-stark`
- **Emily Smith** — Marketing Leader — slug: `emily-smith`
- **Caden Wightman** — Business Advisor — slug: `caden-wightman`
- **Jon Alcon** — Business Advisor — slug: `jon-alcon`
- **Zach Meade** — Business Advisor — slug: `zach-meade`

## Author-to-article assignment (launch 10)

Distribute across all 8 authors, matching person to article topic:

1. How Much Does a Contractor Website Cost? — **Emily Smith** (Marketing Leader)
2. Contractor Website Mistakes That Cost You Leads — **Amy Bourke** (Founder)
3. Local SEO for Contractors: A Practical Guide — **Emily Smith** (Marketing Leader)
4. Do Service-Area Pages Help Contractors Rank Locally? — **Caden Wightman** (Business Advisor)
5. Google Business Profile Optimization Checklist for Contractors — **Jon Alcon** (Business Advisor)
6. The Best Online Directories for Contractors — **Zach Meade** (Business Advisor)
7. How Contractors Can Get More Google Reviews — **Elliot Farmer** (Head of Sales)
8. AI Receptionists for Contractors: What They Can and Cannot Do — **Eric Stark** (Senior Business Advisor)
9. How Quickly Should You Respond to Angi and Thumbtack Leads? — **Elliot Farmer** (Head of Sales)
10. How to Turn One Completed Job Into More Work From the Neighborhood — **Elizabeth Adams** (Head of GTM & Enablement)

(Emily and Elliot each get two because they map most naturally to two topics.)

## Branding — CRITICAL

**Do NOT use "ZING" anywhere in the blog.** TradeZIP is the standalone brand. All copy, meta descriptions, JSON-LD publisher name, footer credits, everything = TradeZIP.

## Build approach (current sprint)

Hand-written static HTML on GitHub Pages. Astro migration comes later. Templates must be consistent enough that they can be converted to Astro markdown without changing URLs.

## Existing site style

- CSS is INLINE in `index.html` (no separate stylesheet)
- Dark navy background: `#0A1229` / `#0e2350`
- Cyan accent: `#34e1d2`
- Cyan→blue→purple gradient: `#16D2E5 → #168CFF → #693CFF`
- Page background (light sections): `#f5f6f8`
- Font: Manrope (loaded via next.js layout in existing site)
- Header/footer are inline HTML at top and bottom of each page
- Rounded corners: 24-32px on hero sections, 14-20px on cards
- Existing hero pattern uses `border-radius:32px` with subtle shadow `0 30px 80px rgba(10,23,53,0.25)`
