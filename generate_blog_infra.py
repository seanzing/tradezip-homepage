#!/usr/bin/env python3
"""
Generate blog infrastructure for TradeZIP:
- sitemap.xml (index)
- sitemap-pages.xml (homepage + industry pages)
- sitemap-blog.xml (blog pages)
- robots.txt
- blog/authors/index.html
- blog/authors/[slug]/index.html (8 author pages)
- blog/search/index.html
"""

import os

LASTMOD = "2026-08-19"
DOMAIN = "https://trade-zip.com"

BRAND_LOCKUP = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNjAwIiBoZWlnaHQ9IjU2MCIgdmlld0JveD0iMCAwIDE2MDAgNTYwIj4KICA8ZGVmcz4KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0idHJhZGV6aXBHcmFkaWVudCIgeDE9IjAiIHkxPSIwLjEiIHgyPSIxIiB5Mj0iMC43NSI+CiAgICAgIDxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzE2RDJFNSIvPjxzdG9wIG9mZnNldD0iMC40OCIgc3RvcC1jb2xvcj0iIzE2OENGRiIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzY5M0NGRiIvPgogICAgPC9saW5lYXJHcmFkaWVudD4KICAgIDxtYXNrIGlkPSJwaW5DdXRvdXQiPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9IiNmZmYiLz48cGF0aCBmaWxsPSIjMDAwIiBkPSJNMjMwIDE3NmMtMzcgMC02MyAyNy02MyA2MiAwIDM4IDMwIDY0IDYzIDk3IDMzLTMzIDYzLTU5IDYzLTk3IDAtMzUtMjYtNjItNjMtNjJ6Ii8+PC9tYXNrPgogIDwvZGVmcz4KICA8cGF0aCBmaWxsPSJ1cmwoI3RyYWRlemlwR3JhZGllbnQpIiBtYXNrPSJ1cmwoI3BpbkN1dG91dCkiIGQ9Ik0yMzAgMzFDMTE5IDMxIDQyIDExMiA0MiAyMjBjMCAxMTYgOTIgMTk2IDE4OCAyOTMgOTYtOTcgMTg4LTE3NyAxODgtMjkzQzQxOCAxMTIgMzQxIDMxIDIzMCAzMXoiLz4KICA8ZyBmaWxsPSIjZmZmIj4KICAgIDxwYXRoIGQ9Im01MTYuMzkyIDMzNGgyOS44NjZWMjAxLjQ1NmgyOS44NjZ2LTI4LjU1OGgtODkuNTk4djI4LjU1OGgyOS44NjZ6Ii8+CiAgICA8cGF0aCBkPSJtNTc0LjEgMzM0aDI4Ljk5NHYtNjcuMTQ0Yy0uNjU0LTE3Ljg3NiA4LjUwMi0yNy45MDQgMjUuOTQyLTI4LjU1OHYtMjcuOTA0aC0yLjE4Yy0xMi40MjYgMC0xOC41MyAzLjQ4OC0yNi4xNiAxNC42MDZ2LTExLjc3Mkg1NzQuMXoiLz4KICAgIDxwYXRoIGQ9Ik03NTMuNjcgMjEzLjIyOGgtMjYuNTk2djE2LjEzMmMtMTAuMDI4LTEzLjI5OC0yMi4wMTgtMTguOTY2LTM5LjQ1OC0xOC45NjYtMzUuNzUyIDAtNjEuNDc2IDI2LjgxNC02MS40NzYgNjMuNjU2IDAgMzYuNDA2IDI1LjUwNiA2Mi43ODQgNjAuODIyIDYyLjc4NCAxNy4wMDQgMCAyOC41NTgtNS4yMzIgNDAuMTEyLTE4LjUzVjMzNGgyNi41OTZ6bS02My4wMDIgMjMuNzYyYzIwLjcxIDAgMzUuNTM0IDE1LjQ3OCAzNS41MzQgMzcuNDk2IDAgOC43Mi0zLjQ4OCAxOC43NDgtOC43MiAyNC44NTItNS44ODYgNy4xOTQtMTUuMjYgMTAuOS0yNi4zNzggMTAuOS0yMS4xNDYgMC0zNS43NTItMTQuMzg4LTM1Ljc1Mi0zNS41MzQgMC0yMi4wMTggMTQuNjA2LTM3LjcxNCAzNS4zMTYtMzcuNzE0eiIvPgogICAgPHBhdGggZD0iTTg4OC4xMTQgMTcyLjg5OEg4NTkuMTJ2NTEuMDEyYy04LjUwMi05LjM3NC0yMi40NTQtMTUuMDQyLTM3LjQ5Ni0xNS4wNDItMzQuMDA4IDAtNjAuNjA0IDI4LjM0LTYwLjYwNCA2NC41MjggMCAzNS45NyAyNi4xNiA2My40MzggNjAuNjA0IDYzLjQzOCAxNi4zNSAwIDI4LjEyMi01LjQ1IDM5Ljg5NC0xOC41M1YzMzRoMjYuNTk2em0tNjIuNTY2IDYyLjU2NmMyMC4yNzQgMCAzNS43NTIgMTYuMTMyIDM1Ljc1MiAzNy40OTYgMCAyMC45MjgtMTUuNDc4IDM3LjI3OC0zNS4wOTggMzcuMjc4LTIwLjI3NCAwLTM1Ljk3LTE2LjU2OC0zNS45Ny0zOC4xNSAwLTIwLjcxIDE1LjQ3OC0zNi42MjQgMzUuMzE2LTM2LjYyNHoiLz4KICAgIDxwYXRoIGQ9Ik0xMDIwLjgxNCAyODYuNDc2Yy44NzItNC4zNiAxLjA5LTYuOTc2IDEuMDktMTEuMzM2IDAtMzcuMjc4LTI2LjM3OC02NC43NDYtNjIuMzQ4LTY0Ljc0Ni0zNS41MzQgMC02My42NTYgMjguMTIyLTYzLjY1NiA2My42NTYgMCAzNS4zMTYgMjguNTU4IDYyLjc4NCA2NS40IDYyLjc4NCAxOS44MzggMCAzNS4zMTYtNy4xOTQgNDcuOTYtMjEuOCA0LjU3OC01LjY2OCA3LjYzLTEwLjY4MiA5LjU5Mi0xNi43ODZoLTMxLjYxYy03LjQxMiA4LjcyLTE0LjYwNiAxMS45OS0yNi41OTYgMTEuOTktMTcuMjIyIDAtMjkuODY2LTkuMTU2LTMzLjM1NC0yMy43NjJ6bS05NC4zOTQtMjUuNTA2YzQuNTc4LTE1LjY5NiAxNi4zNS0yMy45OCAzMy41NzItMjMuOTggMTcuODc2IDAgMjkuNjQ4IDguNTAyIDMzLjM1NCAyMy45OHoiLz4KICAgIDxwYXRoIGQ9Ik0xMDIzLjgwNCAzMDguNzEyVjMzNGgxMDAuNzE2di0yOC41NThoLTY0Ljc0Nmw2MC42MDQtMTA1Ljczdi0yNi44MTRoLTkzLjMwNHYyOC41NThoNTcuNzd6Ii8+CiAgICA8cGF0aCBkPSJNMTEzMi41MjQgMzM0aDI4Ljk5NFYyMTMuMjI4aC0yOC45OTR6bTAtMTMzLjg1MmgyOC45OTR2LTI3LjI1aC0yOC45OTR6Ii8+CiAgICA8cGF0aCBkPSJNMTE3NS44NDQgMzc0LjMzaDI4Ljk5NHYtNTEuNjY2YzExLjExOCA5LjgxIDIyLjIzNiAxNC4xNyAzNy4wNiAxNC4xNyAzNC44OCAwIDYwLjM4Ni0yNy4wMzIgNjAuMzg2LTYzLjY1NiAwLTM2LjQwNi0yNS4yODgtNjIuNzg0LTU5Ljk1LTYyLjc4NC0xNi41NjggMC0zMC41MiA1Ljg4Ni0zOS44OTQgMTcuMDA0di0xNC4xN2gtMjYuNTk2em02Mi41NjYtMTM3LjM0YzE5LjYyIDAgMzQuNjYyIDE1LjkxNCAzNC42NjIgMzYuODQyIDAgMjAuNDkyLTE1LjA0MiAzNi40MDYtMzQuMjI2IDM2LjQwNi0yMC40OTIgMC0zNS43NTItMTUuNjk2LTM1Ljc1Mi0zNi44NDIgMC0yMC43MSAxNS4yNi0zNi40MDYgMzUuMzE2LTM2LjQwNnoiLz4KICA8L2c+Cjwvc3ZnPgo="

BRAND_MARK = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0NjAiIGhlaWdodD0iNTUwIiB2aWV3Qm94PSIwIDAgNDYwIDU1MCI+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9InRyYWRlemlwR3JhZGllbnQiIHgxPSIwIiB5MT0iMC4xIiB4Mj0iMSIgeTI9IjAuNzUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiMxNkQyRTUiLz4KICAgICAgPHN0b3Agb2Zmc2V0PSIwLjQ4IiBzdG9wLWNvbG9yPSIjMTY4Q0ZGIi8+CiAgICAgIDxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzY5M0NGRiIvPgogICAgPC9saW5lYXJHcmFkaWVudD4KICAgIDxtYXNrIGlkPSJwaW5DdXRvdXQiPgogICAgICA8cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZmZmIi8+CiAgICAgIDxwYXRoIGZpbGw9IiMwMDAiIGQ9Ik0yMzAgMTc2Yy0zNyAwLTYzIDI3LTYzIDYyIDAgMzggMzAgNjQgNjMgOTcgMzMtMzMgNjMtNTkgNjMtOTcgMC0zNS0yNi02Mi02My02MnoiLz4KICAgIDwvbWFzaz4KICA8L2RlZnM+CiAgPHBhdGggZmlsbD0idXJsKCN0cmFkZXppcEdyYWRpZW50KSIgbWFzaz0idXJsKCNwaW5DdXRvdXQpIgogICAgICAgIGQ9Ik0yMzAgMzFDMTE5IDMxIDQyIDExMiA0MiAyMjBjMCAxMTYgOTIgMTk2IDE4OCAyOTMgOTYtOTcgMTg4LTE3NyAxODgtMjkzQzQxOCAxMTIgMzQxIDMxIDIzMCAzMXoiLz4KPC9zdmc+Cg=="

# Base CSS shared across all blog pages
BASE_CSS = """
  *{box-sizing:border-box;margin:0;padding:0}
  :root{
    --navy:#050536;--navy-2:#080b3a;--navy-3:#11115b;
    --turquoise:#34e1d2;--cyan:#00aeff;--blue:#3a5aff;
    --violet:#9600ff;--purple:#6407fa;--pale:#f5faff;
    --white:#fff;--muted:#bdc6e0;--line:#ffffff1f;
    --gradient:linear-gradient(135deg,#34e1d2 0%,#00aeff 32%,#3a5aff 64%,#9600ff 100%)
  }
  html{scroll-behavior:smooth}
  body{background:var(--navy);color:var(--white);font-family:"Manrope","Avenir Next","Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.6}
  a{color:inherit;text-decoration:none}
  img{max-width:100%;display:block}

  /* ── HEADER ── */
  .site-header{z-index:20;border-bottom:1px solid var(--line);background:#050536fa;grid-template-columns:1fr auto 1fr;align-items:center;gap:38px;height:84px;padding:0 clamp(24px,4vw,64px);display:grid;position:relative;box-shadow:0 8px 30px #05053629}
  .brand{align-items:center;width:max-content;display:inline-flex}
  .brand-lockup{object-fit:contain;object-position:left center;width:174px;height:61px;display:block}
  .desktop-nav{color:#ffffffc7;align-items:center;gap:clamp(22px,2.4vw,42px);font-size:15px;font-weight:600;display:flex}
  .desktop-nav a,.login-link{transition:color .18s;position:relative}
  .desktop-nav a:after,.login-link:after{content:"";transform-origin:0;background:var(--gradient);height:2px;transition:transform .18s;position:absolute;bottom:-9px;left:0;right:0;transform:scaleX(0)}
  .desktop-nav a:hover,.login-link:hover{color:var(--white)}
  .desktop-nav a:hover:after,.login-link:hover:after{transform:scaleX(1)}
  .header-actions{justify-self:end;align-items:center;gap:24px;display:flex}
  .login-link{color:#ffffffc7;font-size:15px;font-weight:600}
  .button{min-height:62px;color:var(--white);background:var(--gradient);border-radius:14px;justify-content:center;align-items:center;gap:9px;padding:0 30px;font-size:17px;font-weight:700;transition:transform .18s,box-shadow .18s,filter .18s;display:inline-flex;box-shadow:0 14px 36px #3a5aff42}
  .button:hover{filter:brightness(1.08);transform:translateY(-2px);box-shadow:0 18px 42px #3a5aff57}
  .button--compact{border-radius:11px;min-height:50px;padding:0 24px;font-size:15px}
  .mobile-menu{justify-self:end;display:none;position:relative}
  .mobile-menu summary{cursor:pointer;align-content:center;gap:5px;width:44px;height:44px;padding:10px;list-style:none;display:grid}
  .mobile-menu summary::-webkit-details-marker{display:none}
  .mobile-menu summary span{background:#fff;width:100%;height:2px;display:block}
  .mobile-menu nav{border:1px solid var(--line);background:var(--navy-3);border-radius:14px;gap:8px;width:220px;padding:16px;display:grid;position:absolute;top:56px;right:0;box-shadow:0 20px 45px #0505364d}
  .mobile-menu nav a{border-radius:8px;padding:10px;display:block}
  .mobile-menu nav a:hover{background:#ffffff14}

  /* ── FOOTER ── */
  .site-footer{border-top:1px solid var(--line);padding:64px clamp(24px,6vw,96px) 40px;margin-top:0}
  .footer-brand{margin-bottom:48px}
  .footer-brand p{color:var(--muted);margin-top:14px;font-size:14px}
  .footer-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:40px;margin-bottom:48px}
  .footer-links>div{display:flex;flex-direction:column;gap:10px}
  .footer-links strong{color:#fff;font-size:13px;font-weight:700;margin-bottom:4px}
  .footer-links a{color:var(--muted);font-size:14px;transition:color .18s}
  .footer-links a:hover{color:#fff}
  .footer-bottom{border-top:1px solid var(--line);padding-top:24px;display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:13px;gap:16px;flex-wrap:wrap}

  /* ── PAGE HERO (dark navy) ── */
  .page-hero{background:linear-gradient(135deg,#080b3a 0%,#050536 100%);padding:80px clamp(24px,6vw,96px) 64px;position:relative;overflow:hidden}
  .page-hero::before{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 80% 20%,#16D2E520,transparent 60%),radial-gradient(ellipse at 20% 80%,#693CFF18,transparent 60%);pointer-events:none}
  .page-hero__inner{position:relative;z-index:1;max-width:1200px;margin:0 auto}

  /* ── BREADCRUMBS ── */
  .breadcrumbs{margin-bottom:28px}
  .breadcrumbs ol{list-style:none;display:flex;flex-wrap:wrap;align-items:center;gap:6px;font-size:13px;color:var(--muted)}
  .breadcrumbs li{display:flex;align-items:center;gap:6px}
  .breadcrumbs li+li::before{content:"›";color:#ffffff40}
  .breadcrumbs a{color:var(--muted);transition:color .15s}
  .breadcrumbs a:hover{color:var(--turquoise)}
  .breadcrumbs li:last-child span{color:#ffffff90}

  /* ── MAIN CONTENT AREA ── */
  .page-content{max-width:1200px;margin:0 auto;padding:64px clamp(24px,6vw,96px)}

  /* ── AVATAR ── */
  .author-avatar{width:120px;height:120px;border-radius:50%;background:linear-gradient(135deg,#16D2E5 0%,#168CFF 48%,#693CFF 100%);display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:700;color:#fff;flex-shrink:0;box-shadow:0 12px 32px #3a5aff4a}

  /* ── ARTICLE CARD GRID ── */
  .article-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;margin-top:32px}
  .article-card{background:#0e1a3a;border:1px solid var(--line);border-radius:16px;padding:28px;transition:transform .2s,box-shadow .2s,border-color .2s}
  .article-card:hover{transform:translateY(-3px);box-shadow:0 16px 40px #00000040;border-color:#ffffff22}
  .article-card__type{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--turquoise);margin-bottom:10px}
  .article-card__title{font-size:17px;font-weight:700;line-height:1.35;color:#fff;margin-bottom:12px}
  .article-card__link{font-size:13px;font-weight:600;color:var(--turquoise);display:inline-flex;align-items:center;gap:6px;transition:gap .15s}
  .article-card:hover .article-card__link{gap:10px}

  /* ── AUTHOR INDEX CARDS ── */
  .authors-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:24px;margin-top:48px}
  .author-card{background:#0e1a3a;border:1px solid var(--line);border-radius:20px;padding:32px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:16px;transition:transform .2s,box-shadow .2s,border-color .2s}
  .author-card:hover{transform:translateY(-3px);box-shadow:0 16px 40px #00000040;border-color:#ffffff22}
  .author-card__avatar{width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#16D2E5 0%,#168CFF 48%,#693CFF 100%);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:700;color:#fff;box-shadow:0 8px 20px #3a5aff40}
  .author-card__name{font-size:18px;font-weight:700;color:#fff}
  .author-card__role{font-size:13px;color:var(--muted)}
  .author-card__count{font-size:12px;color:var(--turquoise);font-weight:600}

  /* ── AUTHOR PROFILE PAGE ── */
  .author-profile{display:flex;align-items:flex-start;gap:36px;margin-bottom:48px}
  .author-info h1{font-size:clamp(28px,4vw,44px);font-weight:800;letter-spacing:-0.04em;line-height:1.1;margin-bottom:8px}
  .author-role-badge{display:inline-flex;align-items:center;gap:8px;background:linear-gradient(135deg,#16D2E515,#693CFF15);border:1px solid #16D2E530;border-radius:8px;padding:6px 14px;font-size:13px;font-weight:600;color:var(--turquoise);margin-bottom:20px}
  .author-bio{color:var(--muted);font-size:16px;line-height:1.7;max-width:640px}
  .section-label{font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--turquoise);margin-bottom:4px}

  /* ── SEARCH PAGE ── */
  .search-hero{padding:80px clamp(24px,6vw,96px) 40px;background:linear-gradient(135deg,#080b3a 0%,#050536 100%);position:relative;overflow:hidden}
  .search-hero::before{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 70% 30%,#16D2E518,transparent 60%);pointer-events:none}
  .search-hero__inner{position:relative;z-index:1;max-width:800px}
  .search-input-wrap{position:relative;margin-top:32px}
  .search-input{width:100%;background:#0e1a3a;border:1.5px solid var(--line);border-radius:14px;color:#fff;font-family:inherit;font-size:17px;padding:18px 24px 18px 56px;outline:none;transition:border-color .2s,box-shadow .2s}
  .search-input:focus{border-color:#16D2E5;box-shadow:0 0 0 3px #16D2E520}
  .search-input::placeholder{color:#ffffff50}
  .search-icon{position:absolute;left:20px;top:50%;transform:translateY(-50%);color:#ffffff50;pointer-events:none}
  .search-results{max-width:800px;margin:0 auto;padding:40px clamp(24px,6vw,96px) 64px}
  .search-placeholder{color:var(--muted);font-size:16px;padding:48px 0;text-align:center}

  @media (max-width:1040px){
    .desktop-nav,.header-actions .login-link{display:none}
    .site-header{grid-template-columns:1fr auto}
    .mobile-menu{display:block}
  }
  @media (max-width:680px){
    .site-header{height:72px;padding:0 18px}
    .brand-lockup{width:142px;height:50px}
    .header-actions .button{min-height:42px;padding:0 15px;font-size:13px}
    .author-profile{flex-direction:column;align-items:flex-start}
    .author-avatar{width:96px;height:96px;font-size:36px}
  }
"""

HEADER_HTML = f"""<header class="site-header">
  <a class="brand" href="/">
    <img class="brand-lockup" src="{BRAND_LOCKUP}" alt="TradeZIP" width="174" height="61"/>
  </a>
  <nav class="desktop-nav" aria-label="Main navigation">
    <a href="/#platform">How it works</a>
    <a href="/#pricing">Pricing</a>
    <a href="/blog/" aria-current-section="true">Resources</a>
  </nav>
  <div class="header-actions">
    <a class="login-link" href="/#login">Log in</a>
    <a class="button button--compact" href="/#contact">Get started</a>
  </div>
  <div class="mobile-menu">
    <details>
      <summary aria-label="Open navigation menu">
        <span></span><span></span><span></span>
      </summary>
      <nav>
        <a href="/#platform">How it works</a>
        <a href="/#pricing">Pricing</a>
        <a href="/blog/">Resources</a>
        <a href="/#login">Log in</a>
        <a href="/#contact">Get started</a>
      </nav>
    </details>
  </div>
</header>"""

FOOTER_HTML = f"""<footer class="site-footer">
  <div class="footer-brand">
    <a class="brand" href="/">
      <img class="brand-lockup" src="{BRAND_LOCKUP}" alt="TradeZIP" width="174" height="61"/>
    </a>
    <p>Local growth, done for you.</p>
  </div>
  <div class="footer-links">
    <div>
      <strong>Platform</strong>
      <a href="/#platform">How it works</a>
      <a href="/#pricing">Pricing</a>
      <a href="/#results">Growth loop</a>
    </div>
    <div class="footer-industries">
      <strong>Industries</strong>
      <a href="/websites/plumbers/">Plumbers</a>
      <a href="/websites/electricians/">Electricians</a>
      <a href="/websites/hvac/">HVAC</a>
      <a href="/websites/general-contractors/">General Contractors</a>
      <a href="/websites/concrete/">Concrete &amp; Masonry</a>
      <a href="/websites/flooring/">Flooring &amp; Tile</a>
      <a href="/websites/">All industries →</a>
    </div>
    <div>
      <strong>Resources</strong>
      <a href="/blog/">Contractor Growth Hub</a>
      <a href="/blog/how-to/">How-To Guides</a>
      <a href="/blog/guides/">In-Depth Guides</a>
      <a href="/blog/checklists/">Checklists</a>
      <a href="/blog/costs/">Costs &amp; Pricing</a>
      <a href="/blog/authors/">Meet the Team</a>
    </div>
    <div>
      <strong>Company</strong>
      <a href="/#contact">Contact</a>
      <a href="/#resources">FAQs</a>
    </div>
    <div>
      <strong>Account</strong>
      <a href="/#login">Log in</a>
      <a href="/#contact">Get started</a>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 TradeZIP. All rights reserved.</span>
    <span>Privacy · Terms</span>
  </div>
</footer>"""

# ─────────────────────────────────────────────
# 1. SITEMAP INDEX
# ─────────────────────────────────────────────
sitemap_index = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>{DOMAIN}/sitemap-pages.xml</loc>
    <lastmod>{LASTMOD}</lastmod>
  </sitemap>
  <sitemap>
    <loc>{DOMAIN}/sitemap-blog.xml</loc>
    <lastmod>{LASTMOD}</lastmod>
  </sitemap>
</sitemapindex>
"""

# ─────────────────────────────────────────────
# 2. PAGES SITEMAP (homepage + industry pages)
# ─────────────────────────────────────────────
page_urls = [
    "/",
    "/websites/",
    "/websites/plumbers/",
    "/websites/electricians/",
    "/websites/hvac/",
    "/websites/general-contractors/",
    "/websites/concrete/",
    "/websites/flooring/",
    "/websites/painters/",
    "/websites/cleaners/",
    "/websites/landscapers/",
    "/websites/pool-service/",
    "/websites/auto/",
]

def sitemap_url(path, changefreq="monthly", priority="0.7"):
    return f"""  <url>
    <loc>{DOMAIN}{path}</loc>
    <lastmod>{LASTMOD}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""

pages_entries = []
for i, path in enumerate(page_urls):
    cf = "weekly" if path == "/" else "monthly"
    pr = "1.0" if path == "/" else ("0.8" if path == "/websites/" else "0.7")
    pages_entries.append(sitemap_url(path, cf, pr))

sitemap_pages = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(pages_entries)}
</urlset>
"""

# ─────────────────────────────────────────────
# 3. BLOG SITEMAP
# ─────────────────────────────────────────────
blog_urls = []

# Blog homepage
blog_urls.append(sitemap_url("/blog/", "weekly", "0.9"))

# Indexable content-type hubs (only those with articles at launch)
for ct in ["how-to", "guides", "checklists", "costs"]:
    blog_urls.append(sitemap_url(f"/blog/{ct}/", "weekly", "0.8"))

# Industry hubs (all 11)
industry_slugs = [
    "plumbers", "electricians", "hvac",
    "general-contractors", "concrete-masonry", "flooring-tile",
    "painters", "cleaning-pressure-washing", "landscaping-lawn-care",
    "pool-spa-services", "auto-repair-services",
]
for slug in industry_slugs:
    blog_urls.append(sitemap_url(f"/blog/industries/{slug}/", "monthly", "0.7"))

# 10 launch articles
articles = [
    "/blog/costs/contractor-website-cost/",
    "/blog/guides/contractor-website-mistakes/",
    "/blog/guides/local-seo-for-contractors/",
    "/blog/guides/service-area-pages-for-contractors/",
    "/blog/checklists/google-business-profile-for-contractors/",
    "/blog/guides/best-online-directories-for-contractors/",
    "/blog/how-to/get-more-google-reviews-for-contractors/",
    "/blog/guides/ai-receptionist-for-contractors/",
    "/blog/guides/angi-thumbtack-lead-response-time/",
    "/blog/how-to/get-more-neighborhood-jobs/",
]
for article in articles:
    blog_urls.append(sitemap_url(article, "monthly", "0.7"))

# 8 author pages (indexable)
author_slugs = [
    "amy-bourke", "elliot-farmer", "elizabeth-adams", "eric-stark",
    "emily-smith", "caden-wightman", "jon-alcon", "zach-meade",
]
for slug in author_slugs:
    blog_urls.append(sitemap_url(f"/blog/authors/{slug}/", "monthly", "0.6"))

sitemap_blog = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(blog_urls)}
</urlset>
"""

# ─────────────────────────────────────────────
# 4. ROBOTS.TXT
# ─────────────────────────────────────────────
robots_txt = f"""User-agent: *
Allow: /

# Block internal search results (noindex pages)
Disallow: /blog/search/
Disallow: /blog/page/

# Block filter/query combinations
Disallow: /blog/industries/*?*
Disallow: /blog/topics/*?*

Sitemap: {DOMAIN}/sitemap.xml
"""

# ─────────────────────────────────────────────
# 5. AUTHOR DATA
# ─────────────────────────────────────────────
AUTHORS = [
    {
        'name': 'Amy Bourke',
        'slug': 'amy-bourke',
        'role': 'Founder',
        'initials': 'AB',
        'meta_description': 'Amy Bourke is the Founder of TradeZIP. She writes about contractor growth strategy, websites, and the systems that help local trades businesses get found and win more work.',
        'bio': "Amy founded TradeZIP to give local contractors a real system for getting found, building trust, and winning more work online. She brings deep experience in local business growth and leads the company's overall strategic direction. When she's not building the product, she's working directly with contractors to understand what actually moves the needle.",
        'articles': [
            {'title': 'Contractor Website Mistakes That Cost You Leads', 'url': '/blog/guides/contractor-website-mistakes/', 'type': 'Guide'},
        ],
        'article_count': '1 article',
    },
    {
        'name': 'Elliot Farmer',
        'slug': 'elliot-farmer',
        'role': 'Head of Sales',
        'initials': 'EF',
        'meta_description': 'Elliot Farmer is Head of Sales at TradeZIP. He writes about lead generation, review strategies, and how contractors can respond faster and win more jobs.',
        'bio': "Elliot spends every day in conversations with contractors across the country, helping them understand why leads aren't converting and what to do about it. He's seen the full range of what works and what doesn't when it comes to online presence, lead response, and reputation — and he writes from that experience.",
        'articles': [
            {'title': 'How Contractors Can Get More Google Reviews', 'url': '/blog/how-to/get-more-google-reviews-for-contractors/', 'type': 'How-To'},
            {'title': 'How Quickly Should You Respond to Angi and Thumbtack Leads?', 'url': '/blog/guides/angi-thumbtack-lead-response-time/', 'type': 'Guide'},
        ],
        'article_count': '2 articles',
    },
    {
        'name': 'Elizabeth Adams',
        'slug': 'elizabeth-adams',
        'role': 'Head of GTM & Enablement',
        'initials': 'EA',
        'meta_description': 'Elizabeth Adams leads GTM and Enablement at TradeZIP. She writes about neighborhood marketing, turning completed jobs into new leads, and practical contractor growth strategies.',
        'bio': "Elizabeth leads go-to-market strategy and enablement at TradeZIP, which means she thinks constantly about how contractors can turn their existing work and relationships into more of both. She focuses on the practical side of growth — the moves that are actually repeatable and don't require a big budget or a marketing team.",
        'articles': [
            {'title': 'How to Turn One Completed Job Into More Work From the Neighborhood', 'url': '/blog/how-to/get-more-neighborhood-jobs/', 'type': 'How-To'},
        ],
        'article_count': '1 article',
    },
    {
        'name': 'Eric Stark',
        'slug': 'eric-stark',
        'role': 'Senior Business Advisor',
        'initials': 'ES',
        'meta_description': 'Eric Stark is a Senior Business Advisor at TradeZIP. He writes about technology, lead flow, and operational tools that help contractors run smarter businesses.',
        'bio': "Eric is a Senior Business Advisor at TradeZIP who helps contractors make smarter decisions about technology, lead flow, and daily operations. He focuses on cutting through the hype to identify the tools and systems that make a real difference for growing service businesses — and explains them in plain language.",
        'articles': [
            {'title': 'AI Receptionists for Contractors: What They Can and Cannot Do', 'url': '/blog/guides/ai-receptionist-for-contractors/', 'type': 'Guide'},
        ],
        'article_count': '1 article',
    },
    {
        'name': 'Emily Smith',
        'slug': 'emily-smith',
        'role': 'Marketing Leader',
        'initials': 'Em',
        'meta_description': 'Emily Smith leads marketing at TradeZIP. She writes about local SEO, contractor websites, content strategy, and building a digital presence that generates consistent leads.',
        'bio': "Emily leads marketing at TradeZIP with a focus on local SEO, content strategy, and helping contractors build a digital presence that actually generates leads. She writes from experience running campaigns for service businesses and watching what translates into real results — not just traffic, but calls and booked jobs.",
        'articles': [
            {'title': 'How Much Does a Contractor Website Cost?', 'url': '/blog/costs/contractor-website-cost/', 'type': 'Costs'},
            {'title': 'Local SEO for Contractors: A Practical Guide', 'url': '/blog/guides/local-seo-for-contractors/', 'type': 'Guide'},
        ],
        'article_count': '2 articles',
    },
    {
        'name': 'Caden Wightman',
        'slug': 'caden-wightman',
        'role': 'Business Advisor',
        'initials': 'CW',
        'meta_description': 'Caden Wightman is a Business Advisor at TradeZIP. He writes about local SEO, service-area pages, and how contractors can show up more consistently in local search.',
        'bio': "Caden is a Business Advisor at TradeZIP who works with contractors looking to grow their local footprint and show up more consistently in search. He focuses on practical strategies around websites, local SEO, and service-area visibility — the kind of work that can be put into action quickly and compounds over time.",
        'articles': [
            {'title': 'Do Service-Area Pages Help Contractors Rank Locally?', 'url': '/blog/guides/service-area-pages-for-contractors/', 'type': 'Guide'},
        ],
        'article_count': '1 article',
    },
    {
        'name': 'Jon Alcon',
        'slug': 'jon-alcon',
        'role': 'Business Advisor',
        'initials': 'JA',
        'meta_description': 'Jon Alcon is a Business Advisor at TradeZIP. He writes about Google Business Profile, local listings, and the changes that generate more calls and bookings for contractors.',
        'bio': "Jon is a Business Advisor at TradeZIP who helps contractors optimize their Google presence so their business shows up where local customers are actually searching. He focuses on the details of Google Business Profile, local listings, and the small improvements that add up to more calls and booked jobs.",
        'articles': [
            {'title': 'Google Business Profile Optimization Checklist for Contractors', 'url': '/blog/checklists/google-business-profile-for-contractors/', 'type': 'Checklist'},
        ],
        'article_count': '1 article',
    },
    {
        'name': 'Zach Meade',
        'slug': 'zach-meade',
        'role': 'Business Advisor',
        'initials': 'ZM',
        'meta_description': 'Zach Meade is a Business Advisor at TradeZIP. He writes about online directories, local citations, and how contractors can build a stronger presence across search platforms.',
        'bio': "Zach is a Business Advisor at TradeZIP who guides contractors through building a stronger online presence across search platforms and business directories. He's focused on practical, no-hype advice on how to get your business listed and trusted in the right places — and why it matters for local visibility.",
        'articles': [
            {'title': 'The Best Online Directories for Contractors', 'url': '/blog/guides/best-online-directories-for-contractors/', 'type': 'Guide'},
        ],
        'article_count': '1 article',
    },
]

def article_type_from_url(url):
    """Extract content type from URL path."""
    parts = url.strip('/').split('/')
    if len(parts) >= 2:
        ct = parts[1]
        return ct.replace('-', ' ').title()
    return 'Article'

def article_cards_html(articles):
    cards = []
    for article in articles:
        article_type = article.get('type', article_type_from_url(article['url']))
        cards.append(f"""<a href="{article['url']}" class="article-card">
          <div class="article-card__type">{article_type}</div>
          <div class="article-card__title">{article['title']}</div>
          <span class="article-card__link">Read article <span aria-hidden="true">→</span></span>
        </a>""")
    return "\n".join(cards)

def monogram_avatar(initials, size=120, font_size=44):
    return f"""<div class="author-avatar" style="width:{size}px;height:{size}px;font-size:{font_size}px;" aria-hidden="true">{initials}</div>"""

def breadcrumbs_html(crumbs):
    """crumbs = list of (label, url) tuples; last one has no url"""
    items = []
    for i, (label, url) in enumerate(crumbs):
        if i < len(crumbs) - 1:
            items.append(f'<li><a href="{url}">{label}</a></li>')
        else:
            items.append(f'<li><span>{label}</span></li>')
    return f"""<nav class="breadcrumbs" aria-label="Breadcrumb">
  <ol>
    {''.join(items)}
  </ol>
</nav>"""

def page_head(title, description, canonical, og_image=None, extra_meta=""):
    if og_image is None:
        og_image = f"{DOMAIN}/assets/og-default.jpg"
    return f"""<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title}</title>
  <meta name="description" content="{description}"/>
  <link rel="canonical" href="{canonical}"/>
  <meta property="og:type" content="website"/>
  <meta property="og:title" content="{title}"/>
  <meta property="og:description" content="{description}"/>
  <meta property="og:url" content="{canonical}"/>
  <meta property="og:image" content="{og_image}"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{title}"/>
  <meta name="twitter:description" content="{description}"/>
  {extra_meta}
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
  <style>{BASE_CSS}</style>
</head>"""

# ─────────────────────────────────────────────
# 6. AUTHORS INDEX PAGE
# ─────────────────────────────────────────────
def gen_authors_index():
    cards = []
    for author in AUTHORS:
        card = f"""<a href="/blog/authors/{author['slug']}/" class="author-card">
      <div class="author-card__avatar" aria-hidden="true">{author['initials']}</div>
      <div class="author-card__name">{author['name']}</div>
      <div class="author-card__role">{author['role']}</div>
      <div class="author-card__count">{author['article_count']}</div>
    </a>"""
        cards.append(card)

    json_ld = """{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Meet the TradeZIP Team",
  "description": "The advisors and leaders behind the Contractor Growth Hub — practical advice from people who work with contractors every day.",
  "url": "https://trade-zip.com/blog/authors/",
  "publisher": {
    "@type": "Organization",
    "name": "TradeZIP",
    "url": "https://trade-zip.com"
  }
}"""

    head = page_head(
        title="Meet the Team — TradeZIP",
        description="The advisors and leaders behind the Contractor Growth Hub. Practical advice from people who work with contractors every day.",
        canonical=f"{DOMAIN}/blog/authors/",
        extra_meta='<meta name="robots" content="noindex,follow"/>'
    )

    return f"""<!DOCTYPE html>
<html lang="en">
{head}
<body>
{HEADER_HTML}
<main>
  <section class="page-hero">
    <div class="page-hero__inner">
      {breadcrumbs_html([("Home", "/"), ("Blog", "/blog/"), ("Authors", None)])}
      <p style="font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--turquoise);margin-bottom:16px;">The Contractor Growth Hub</p>
      <h1 style="font-size:clamp(32px,4vw,52px);font-weight:800;letter-spacing:-0.04em;line-height:1.1;margin-bottom:16px;">Meet the Team</h1>
      <p style="color:var(--muted);font-size:17px;max-width:560px;line-height:1.6;">Practical advice from the advisors and leaders who work with contractors every day.</p>
    </div>
  </section>
  <div class="page-content" style="padding-top:0;margin-top:-24px;">
    <div class="authors-grid">
      {''.join(cards)}
    </div>
  </div>
</main>
{FOOTER_HTML}
<script type="application/ld+json">
{json_ld}
</script>
</body>
</html>"""

# ─────────────────────────────────────────────
# 7. INDIVIDUAL AUTHOR PAGES
# ─────────────────────────────────────────────
def gen_author_page(author):
    canonical = f"{DOMAIN}/blog/authors/{author['slug']}/"

    # Build JSON-LD
    same_as = []
    authored_works = []
    for article in author['articles']:
        authored_works.append(f"""    {{
      "@type": "Article",
      "headline": "{article['title']}",
      "url": "{DOMAIN}{article['url']}"
    }}""")

    person_ld = f"""{{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "{author['name']}",
  "jobTitle": "{author['role']}",
  "worksFor": {{
    "@type": "Organization",
    "name": "TradeZIP",
    "url": "https://trade-zip.com"
  }},
  "url": "{canonical}",
  "description": "{author['meta_description']}"
}}"""

    breadcrumb_ld = f"""{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type":"ListItem","position":1,"name":"Home","item":"{DOMAIN}/"}},
    {{"@type":"ListItem","position":2,"name":"Blog","item":"{DOMAIN}/blog/"}},
    {{"@type":"ListItem","position":3,"name":"Authors","item":"{DOMAIN}/blog/authors/"}},
    {{"@type":"ListItem","position":4,"name":"{author['name']}","item":"{canonical}"}}
  ]
}}"""

    head = page_head(
        title=f"{author['name']} — TradeZIP",
        description=author['meta_description'],
        canonical=canonical,
    )

    article_count_word = author['article_count']

    return f"""<!DOCTYPE html>
<html lang="en">
{head}
<body>
{HEADER_HTML}
<main>
  <section class="page-hero">
    <div class="page-hero__inner">
      {breadcrumbs_html([
          ("Home", "/"),
          ("Blog", "/blog/"),
          ("Authors", "/blog/authors/"),
          (author['name'], None)
      ])}
      <div class="author-profile">
        {monogram_avatar(author['initials'])}
        <div class="author-info">
          <h1>{author['name']}</h1>
          <div class="author-role-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            {author['role']}, TradeZIP
          </div>
          <p class="author-bio">{author['bio']}</p>
        </div>
      </div>
    </div>
  </section>
  <div class="page-content">
    <p class="section-label">{article_count_word} published</p>
    <div class="article-grid">
      {article_cards_html(author['articles'])}
    </div>
  </div>
</main>
{FOOTER_HTML}
<script type="application/ld+json">
{person_ld}
</script>
<script type="application/ld+json">
{breadcrumb_ld}
</script>
</body>
</html>"""

# ─────────────────────────────────────────────
# 8. SEARCH PAGE SCAFFOLD
# ─────────────────────────────────────────────
def gen_search_page():
    breadcrumb_ld = f"""{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type":"ListItem","position":1,"name":"Home","item":"{DOMAIN}/"}},
    {{"@type":"ListItem","position":2,"name":"Blog","item":"{DOMAIN}/blog/"}},
    {{"@type":"ListItem","position":3,"name":"Search","item":"{DOMAIN}/blog/search/"}}
  ]
}}"""

    head = page_head(
        title="Search — Contractor Growth Hub — TradeZIP",
        description="Search the TradeZIP Contractor Growth Hub for guides, how-to articles, checklists and practical advice for contractors.",
        canonical=f"{DOMAIN}/blog/search/",
        extra_meta='<meta name="robots" content="noindex,follow"/>'
    )

    return f"""<!DOCTYPE html>
<html lang="en">
{head}
<body>
{HEADER_HTML}
<main>
  <section class="search-hero">
    <div class="search-hero__inner">
      {breadcrumbs_html([("Home", "/"), ("Blog", "/blog/"), ("Search", None)])}
      <h1 style="font-size:clamp(28px,4vw,44px);font-weight:800;letter-spacing:-0.04em;line-height:1.1;margin-bottom:8px;">Search the Growth Hub</h1>
      <p style="color:var(--muted);font-size:16px;margin-bottom:0;">Find guides, how-tos, checklists and practical advice for contractors.</p>
      <div class="search-input-wrap">
        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          class="search-input"
          type="search"
          id="search-input"
          name="q"
          placeholder="What do you want help with?"
          aria-label="Search the Contractor Growth Hub"
          autocomplete="off"
        />
      </div>
    </div>
  </section>
  <div class="search-results">
    <div id="search-results-container">
      <p class="search-placeholder" id="search-placeholder">Enter a search term above to find articles.</p>
      <!-- TODO: wire Pagefind or Algolia after launch -->
    </div>
  </div>
</main>
{FOOTER_HTML}
<script>
  (function() {{
    var params = new URLSearchParams(window.location.search);
    var q = params.get('q') || '';
    var input = document.getElementById('search-input');
    var placeholder = document.getElementById('search-placeholder');
    if (q) {{
      input.value = q;
      placeholder.textContent = 'Search results for "' + q + '" will appear here once search is connected.';
    }}
  }})();
</script>
<script type="application/ld+json">
{breadcrumb_ld}
</script>
</body>
</html>"""

# ─────────────────────────────────────────────
# WRITE ALL FILES
# ─────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))

def write(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ {path}")

print("\nGenerating TradeZIP blog infrastructure...\n")

write("sitemap.xml", sitemap_index)
write("sitemap-pages.xml", sitemap_pages)
write("sitemap-blog.xml", sitemap_blog)
write("robots.txt", robots_txt)
write("blog/authors/index.html", gen_authors_index())
write("blog/search/index.html", gen_search_page())

for author in AUTHORS:
    path = f"blog/authors/{author['slug']}/index.html"
    write(path, gen_author_page(author))

print(f"\nDone. {4 + 1 + 1 + len(AUTHORS)} files written.")
