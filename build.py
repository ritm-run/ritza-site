# Builds index.html of ritza.app from i18n.json (Russian in the markup, the other languages switched by a small script).
import json, os, html
here = os.path.dirname(os.path.abspath(__file__))
t = json.load(open(os.path.join(here, "i18n.json"), encoding="utf-8"))
ru = t["ru"]
def s(k): return html.escape(ru[k])

# Front metals checked against the supplied art and ui/Medals.kt.
# Names/requirements come from core/Achievements.kt; LEGEND is a rank (8000 XP).
medals = [
    ("hare", "bronze", "FIRST_ESCAPE"),
    ("wolf", "silver", "PACK_LEADER"),
    ("shield", "gold", "UNTOUCHABLE"),
    ("lightning", "gold", "LIGHTNING"),
    ("steps", "gold", "STEPS_10K"),
    ("5k", "bronze", "FIVE_K"),
    ("half", "gold", "HALF_MARATHON"),
    ("owl", "bronze", "NIGHT_OWL"),
]

def medal_markup(key, metal, source, legend=False):
    name, desc = "trophy_" + key + "_name", "trophy_" + key + "_desc"
    tier = "trophy_rank" if legend else "trophy_" + metal
    return f'''<button type="button" class="medal-toggle {metal}" data-achievement="{source}"
          aria-pressed="false" aria-labelledby="medal-{key}-name" aria-describedby="medal-{key}-desc trophy-hint">
          <span class="medal-stage"><span class="medal-coin">
            <span class="medal-face medal-front" aria-hidden="true"><img src="img/medals/{key}.webp" alt="" width="360" height="360" loading="lazy"><span class="medal-glint"></span></span>
            <span class="medal-face medal-back" aria-hidden="true"><img src="img/medals/back-{metal}.webp" alt="" width="360" height="360" loading="lazy">
              <span class="medal-engraving"><strong data-t="{name}">{s(name)}</strong><span id="medal-{key}-desc" data-t="{desc}">{s(desc)}</span></span>
            </span>
          </span></span>
          <span class="medal-name" id="medal-{key}-name" data-t="{name}">{s(name)}</span>
          <span class="medal-tier" data-t="{tier}">{s(tier)}</span>
        </button>'''

trophy_grid = "\n".join(medal_markup(*m) for m in medals)
legend_medal = medal_markup("legend", "gold", "LEGEND", legend=True)

trophy_css = r'''
/* Real two-sided medals: only the coin and its light band animate. */
.trophies { scroll-margin-top: 88px; }
.trophy-lead { display: grid; grid-template-columns: minmax(0, 1fr) 280px; gap: 48px; align-items: center; margin-bottom: 28px; }
.trophy-lead h2 { margin-bottom: 18px; }
.trophy-lead p { color: var(--ink-2); max-width: 38em; margin: 0 0 22px; font-size: 18px; }
.trophy-metals { display: flex; flex-wrap: wrap; gap: 8px; }
.trophy-metal { display: inline-flex; align-items: center; justify-content: center; gap: 7px; border: 1px solid var(--line); background: var(--card); border-radius: 999px; padding: 7px 13px; font-size: 13px; font-weight: 600; text-align: center; }
.trophy-metal::before { content: ""; width: 10px; height: 10px; border-radius: 50%; background: #BC784C; }
.trophy-metal.silver::before { background: #A5ADB6; }
.trophy-metal.gold::before { background: #DCB34B; }
.trophy-hint { display: block; color: var(--muted); font-size: 14px; margin-top: 18px; }
.trophy-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; }
.medal-toggle { appearance: none; width: 100%; min-width: 0; padding: 18px 14px; border: 1px solid var(--line); border-radius: var(--r-card); background: var(--card); color: var(--ink); font: inherit; cursor: pointer; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; text-align: center; -webkit-tap-highlight-color: transparent; }
.medal-toggle:focus-visible { outline: 3px solid var(--run); outline-offset: 4px; }
.medal-stage { display: block; width: 100%; max-width: 230px; aspect-ratio: 1; perspective: 1000px; container-type: inline-size; }
.medal-coin { position: relative; display: block; width: 100%; height: 100%; transform-style: preserve-3d; transform: rotateY(0deg); }
.medal-face { position: absolute; inset: 0; display: block; backface-visibility: hidden; -webkit-backface-visibility: hidden; }
.medal-face img { width: 100%; height: 100%; object-fit: contain; }
.medal-back { transform: rotateY(180deg); }
.medal-toggle[aria-pressed="true"] .medal-coin { transform: rotateY(180deg); }
.medal-engraving { position: absolute; inset: 18% 17%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; color: #211309; text-shadow: 0 1px 1px rgb(255 239 199 / .65), 0 -1px 1px rgb(48 23 4 / .4); }
.silver .medal-engraving { color: #20252B; text-shadow: 0 1px 1px rgb(255 255 255 / .75), 0 -1px 1px rgb(31 40 51 / .35); }
.gold .medal-engraving { color: #3A2607; }
.medal-engraving strong { font-size: clamp(11px, 6.7cqw, 16px); line-height: 1.15; font-weight: 800; }
.medal-engraving > span { font-size: clamp(10px, 6cqw, 14px); line-height: 1.25; font-weight: 600; }
.medal-name { width: 100%; min-height: 2.6em; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px; line-height: 1.3; margin-top: 10px; text-wrap: balance; }
.medal-tier { color: var(--muted); font-weight: 500; font-size: 12px; margin-top: 6px; }
.trophy-legend { background: radial-gradient(ellipse at 50% 30%, var(--lime-soft), var(--card) 75%); }
.trophy-legend .medal-stage { max-width: 250px; }
.trophy-legend .medal-name { font-size: 22px; min-height: auto; }
.medal-front { overflow: hidden; border-radius: 50%; }
.medal-glint { position: absolute; inset: 9%; border-radius: 50%; overflow: hidden; pointer-events: none; }
.medal-glint::after { content: ""; position: absolute; inset: -30%; background: linear-gradient(110deg, transparent 35%, rgb(255 255 255 / .55) 49%, transparent 63%); transform: translateX(-110%); opacity: 0; }
@keyframes medal-turn { from { transform: rotateY(0deg); } to { transform: rotateY(360deg); } }
@keyframes medal-glint { 0%, 52% { transform: translateX(-110%); opacity: 0; } 65% { opacity: .8; } 100% { transform: translateX(110%); opacity: 0; } }
@media (prefers-reduced-motion: no-preference) {
  .medal-toggle.is-visible:not(.is-turning) .medal-coin { transition: transform .55s ease-out; }
  .medal-toggle.is-turning .medal-coin { animation: medal-turn 1.5s cubic-bezier(.18,.65,.3,1) both; }
  .medal-toggle.is-turning .medal-glint::after { animation: medal-glint 1.5s ease-out both; }
}
.trophies.is-paused .medal-coin, .trophies.is-paused .medal-glint::after { animation: none; transition: none; }
@media (max-width: 959px) { .trophy-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } .trophy-lead { grid-template-columns: minmax(0, 1fr) 240px; gap: 24px; } }
@media (max-width: 600px) {
  .trophy-lead { grid-template-columns: minmax(0, 1fr); gap: 24px; }
  .trophy-legend { max-width: 280px; justify-self: center; }
  .trophy-grid { gap: 12px; }
  .medal-toggle { padding: 12px 8px; border-radius: var(--r-tile); }
  .medal-name { font-size: 14px; }
  .medal-tier { font-size: 11px; }
  .trophy-lead p { font-size: 17px; }
}
'''

trophy_script = r'''
// A single scheduler serves the entrance sequence and the quiet 4-second turns.
// Both observers must permit a turn: no animation runs outside the viewport.
const trophySection = document.getElementById("trophies");
const medalButtons = [...trophySection.querySelectorAll(".medal-toggle")];
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
const hoverDevice = matchMedia("(hover: hover) and (pointer: fine)");
const visibleMedals = new Set(), introducedMedals = new Set();
const pinnedMedals = new Set(), hoveredMedals = new Set();
let trophyInView = false, turningMedal = null, lastMedal = null, turnTimer = null;

function stopMedalTurn() {
  clearTimeout(turnTimer); turnTimer = null;
  if (turningMedal) turningMedal.classList.remove("is-turning");
  turningMedal = null;
}
function canTurnMedals() { return trophyInView && !document.hidden && !reducedMotion.matches; }
function availableMedals() {
  return medalButtons.filter(m => visibleMedals.has(m) && m.getAttribute("aria-pressed") !== "true" && m !== document.activeElement);
}
function scheduleMedalTurn(delay) {
  clearTimeout(turnTimer); turnTimer = null;
  if (!canTurnMedals() || turningMedal || !availableMedals().length) return;
  turnTimer = setTimeout(() => {
    turnTimer = null;
    if (!canTurnMedals()) return;
    const available = availableMedals();
    const first = available.find(m => !introducedMedals.has(m));
    const pool = available.filter(m => m !== lastMedal);
    const medal = first || (pool.length ? pool : available)[Math.floor(Math.random() * (pool.length || available.length))];
    if (!medal) return;
    introducedMedals.add(medal); lastMedal = medal; turningMedal = medal;
    medal.classList.add("is-turning");
  }, delay);
}
function refreshMedalMotion() {
  trophySection.classList.toggle("is-paused", !canTurnMedals());
  if (!canTurnMedals()) stopMedalTurn();
  else if (!turningMedal) scheduleMedalTurn(availableMedals().some(m => !introducedMedals.has(m)) ? 180 : 4000);
}
function setMedalBack(medal) {
  if (turningMedal === medal) stopMedalTurn();
  medal.setAttribute("aria-pressed", String(pinnedMedals.has(medal) || hoveredMedals.has(medal)));
  refreshMedalMotion();
}
medalButtons.forEach(medal => {
  medal.querySelector(".medal-coin").addEventListener("animationend", e => {
    if (e.animationName !== "medal-turn" || turningMedal !== medal) return;
    medal.classList.remove("is-turning"); turningMedal = null;
    scheduleMedalTurn(availableMedals().some(m => !introducedMedals.has(m)) ? 180 : 4000);
  });
  medal.addEventListener("pointerenter", e => {
    if (!hoverDevice.matches || e.pointerType !== "mouse") return;
    hoveredMedals.add(medal); setMedalBack(medal);
  });
  medal.addEventListener("pointerleave", () => { hoveredMedals.delete(medal); setMedalBack(medal); });
  medal.addEventListener("click", e => {
    // Mouse hover is momentary; touch and keyboard keep the back until next press.
    if (e.detail && hoveredMedals.has(medal)) return;
    if (pinnedMedals.has(medal)) pinnedMedals.delete(medal); else pinnedMedals.add(medal);
    setMedalBack(medal);
  });
  medal.addEventListener("blur", refreshMedalMotion);
});
const medalObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    const medal = entry.target;
    if (entry.isIntersecting && entry.intersectionRatio >= .6) {
      visibleMedals.add(medal); medal.classList.add("is-visible");
    } else {
      visibleMedals.delete(medal); medal.classList.remove("is-visible");
      if (turningMedal === medal) stopMedalTurn();
      hoveredMedals.delete(medal);
      medal.setAttribute("aria-pressed", String(pinnedMedals.has(medal)));
    }
  });
  refreshMedalMotion();
}, { threshold: [0, .6], rootMargin: "-68px 0px 0px 0px" });
medalButtons.forEach(m => medalObserver.observe(m));
new IntersectionObserver(entries => {
  trophyInView = entries[0].isIntersecting; refreshMedalMotion();
}, { threshold: 0, rootMargin: "-68px 0px 0px 0px" }).observe(trophySection);
document.addEventListener("visibilitychange", refreshMedalMotion);
reducedMotion.addEventListener("change", refreshMedalMotion);
'''

page = f"""<!doctype html>
<html lang="ru" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{s("title")}</title>
<meta name="description" content="{s("hero_sub")}">
<meta property="og:title" content="Рица · Ritza · ריצה">
<meta property="og:description" content="{s("hero_sub")}">
<meta property="og:image" content="https://ritza.app/img/chase.webp">
<link rel="icon" href="img/favicon.png">
<link rel="apple-touch-icon" href="img/icon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700;800&display=swap">
<style>
:root {{
  --lime: #B8F66B; --lime-soft: #E4FBC7; --ink: #17202D; --ink-2: #3A4656; --muted: #5F6B7B;
  --page: #F6F8F2; --card: #FFFFFF; --line: #E2E8DC; --run: #1FAE82; --walk: #3B82F6; --sun: #ED8A3B;
  --r-card: 24px; --r-tile: 16px; --gutter: 20px;
  --font: "Rubik", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --page: #0E1418; --card: #18212A; --ink: #F1F4F8; --ink-2: #C9D2DC; --muted: #9AA6B5; --line: #26313B; --lime-soft: #22311A; }}
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{ margin: 0; background: var(--page); color: var(--ink); font: 17px/1.55 var(--font); -webkit-font-smoothing: antialiased; }}
img {{ max-width: 100%; height: auto; display: block; }}
figure {{ margin: 0; }}
a {{ color: inherit; }}
.wrap {{ max-width: 1160px; margin: 0 auto; padding-inline: var(--gutter); }}

/* header */
header {{ position: sticky; top: 0; z-index: 10; background: color-mix(in srgb, var(--page) 88%, transparent); backdrop-filter: blur(10px); border-bottom: 1px solid var(--line); }}
.bar {{ display: flex; align-items: center; gap: 18px; height: 68px; }}
.brand {{ display: flex; align-items: center; gap: 10px; text-decoration: none; }}
.brand img.mark {{ width: 46px; height: 46px; }}
.brand .wm {{ height: 26px; width: auto; }}
.brand .wm.dark {{ display: none; }}
@media (prefers-color-scheme: dark) {{ .brand .wm.light {{ display: none; }} .brand .wm.dark {{ display: block; }} }}
nav {{ display: flex; gap: 22px; margin-inline-start: auto; font-weight: 500; font-size: 15px; }}
nav a {{ text-decoration: none; color: var(--ink-2); }}
nav a:hover {{ color: var(--ink); }}
.lang {{ display: inline-flex; background: var(--card); border: 1px solid var(--line); border-radius: 999px; padding: 3px; gap: 2px; }}
.lang button {{ font: 600 13px/1 var(--font); color: var(--ink-2); background: transparent; border: 0; border-radius: 999px; min-width: 42px; height: 32px; padding: 0 10px; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; }}
.lang button[aria-pressed="true"] {{ background: var(--lime); color: #17202D; }}
.lang button:focus-visible, .btn:focus-visible {{ outline: 3px solid var(--run); outline-offset: 2px; }}
@media (max-width: 960px) {{ nav {{ display: none; }} .lang {{ margin-inline-start: auto; }} .brand .wm {{ height: 22px; }} }}

/* hero */
.hero {{ position: relative; overflow: hidden; }}
.hero::before {{ content: ""; position: absolute; inset: 0; background: radial-gradient(1200px 620px at 78% 40%, var(--lime-soft), transparent 70%); pointer-events: none; }}
.hero .wrap {{ position: relative; display: grid; grid-template-columns: 1fr 1.15fr; align-items: center; gap: 28px; padding-block: 56px 40px; }}
.eyebrow {{ display: inline-flex; align-items: center; gap: 8px; font-weight: 600; font-size: 14px; letter-spacing: .02em; color: var(--ink-2); background: var(--card); border: 1px solid var(--line); border-radius: 999px; padding: 6px 14px; }}
.eyebrow i {{ width: 8px; height: 8px; border-radius: 50%; background: var(--run); }}
h1 {{ font-weight: 800; font-size: clamp(40px, 6.2vw, 74px); line-height: 1.02; letter-spacing: -.02em; margin: 18px 0 18px; text-wrap: balance; }}
h1 .hl {{ background: linear-gradient(transparent 62%, var(--lime) 62%); }}
.sub {{ font-size: clamp(17px, 1.6vw, 20px); color: var(--ink-2); max-width: 34em; margin: 0 0 28px; }}
.ctas {{ display: flex; flex-wrap: wrap; gap: 12px; }}
.btn {{ display: inline-flex; align-items: center; justify-content: center; gap: 10px; min-height: 54px; padding: 0 26px; border-radius: 999px; font: 700 16px/1 var(--font); text-decoration: none; border: 0; text-align: center; }}
.btn.primary {{ background: #17202D; color: #fff; }}
@media (prefers-color-scheme: dark) {{ .btn.primary {{ background: var(--lime); color: #17202D; }} }}
.btn.primary svg {{ width: 20px; height: 20px; }}
.btn.ghost {{ background: var(--card); color: var(--ink); border: 1px solid var(--line); }}
.hero-art img {{ width: 100%; height: auto; filter: drop-shadow(0 24px 40px rgba(23,32,45,.10)); }}
@media (max-width: 900px) {{ .hero .wrap {{ grid-template-columns: 1fr; padding-block: 28px 8px; }} .hero-art {{ order: -1; max-width: 560px; margin-inline: auto; }} }}

/* the route to the goal */
.route .wrap {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 48px; align-items: center; }}
.route .lead {{ color: var(--ink-2); font-size: 18px; margin: 14px 0 20px; }}
.route .ticks {{ list-style: none; padding: 0; margin: 0 0 18px; display: grid; gap: 12px; }}
.route .ticks li {{ display: flex; gap: 12px; align-items: flex-start; font-weight: 500; }}
.route .ticks b {{ flex: none; width: 26px; height: 26px; border-radius: 999px; background: var(--lime); color: #17202D; display: inline-flex; align-items: center; justify-content: center; font-size: 14px; }}
.route .small {{ color: var(--ink-2); font-size: 14px; margin: 0; }}
.route-shots {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; justify-items: center; }}
@media (max-width: 860px) {{ .route .wrap {{ grid-template-columns: 1fr; gap: 32px; }} }}
@media (max-width: 480px) {{ .route-shots {{ gap: 12px; }} }}

/* sections */
section {{ padding-block: 64px; }}
.kicker {{ font-weight: 700; font-size: 13px; letter-spacing: .12em; text-transform: uppercase; color: var(--run); }}
h2 {{ font-weight: 800; font-size: clamp(28px, 3.6vw, 44px); line-height: 1.1; letter-spacing: -.015em; margin: 8px 0 28px; text-wrap: balance; }}
.grid-2, .grid-3 {{ display: grid; gap: 20px; }}
.grid-2 {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
.grid-3 {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
@media (max-width: 900px) {{ .grid-3 {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
@media (max-width: 640px) {{ .grid-2, .grid-3 {{ grid-template-columns: 1fr; }} }}
.card {{ background: var(--card); border: 1px solid var(--line); border-radius: var(--r-card); padding: 26px; display: flex; flex-direction: column; gap: 8px; height: 100%; }}
.card h3 {{ margin: 0; font-weight: 700; font-size: 21px; }}
.card p {{ margin: 0; color: var(--ink-2); }}
.hunt .card {{ padding: 0; overflow: hidden; }}
.hunt .card .pic {{ background: radial-gradient(circle at 50% 60%, var(--lime-soft), transparent 70%); aspect-ratio: 4 / 3; display: grid; place-items: center; }}
.hunt .card .pic img {{ width: 92%; }}
.hunt .card .txt {{ padding: 22px 26px 26px; display: grid; gap: 6px; }}
.ico {{ width: 46px; height: 46px; border-radius: 14px; background: var(--lime-soft); display: grid; place-items: center; margin-bottom: 6px; }}
.ico svg {{ width: 24px; height: 24px; fill: none; stroke: var(--ink); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}

/* screenshots */
.shots {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 28px; justify-items: center; }}
.phone {{ width: 100%; max-width: 280px; display: grid; gap: 14px; justify-items: center; text-align: center; }}
.phone .frame {{ width: 100%; border-radius: 34px; padding: 9px; background: #10161D; box-shadow: 0 22px 44px rgba(23,32,45,.18); }}
.phone .frame img {{ border-radius: 26px; width: 100%; aspect-ratio: 540 / 1104; object-fit: cover; }}
.phone span {{ font-weight: 600; color: var(--ink-2); }}
.phone > span {{ min-height: 3.1em; display: flex; align-items: center; justify-content: center; text-wrap: balance; }}
@media (max-width: 480px) {{
  .route-shots .frame {{ padding: 6px; border-radius: 24px; }}
}}
@media (max-width: 760px) {{ .shots {{ grid-template-columns: 1fr; }} .phone {{ max-width: 300px; }} }}

/* privacy */
.priv {{ background: #17202D; color: #F1F4F8; border-radius: 32px; padding: clamp(28px, 5vw, 56px); display: grid; grid-template-columns: 1fr 1fr; gap: 28px; align-items: center; }}
.priv h2 {{ color: #fff; margin-bottom: 0; }}
.priv .kicker {{ color: var(--lime); }}
.pills {{ display: grid; gap: 12px; }}
.pill {{ display: flex; align-items: center; justify-content: center; text-align: center; gap: 14px; background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.10); border-radius: var(--r-tile); padding: 16px 18px; font-weight: 500; min-height: 64px; }}
.pill span {{ flex: 1; }}
.pill b {{ flex: 0 0 auto; width: 30px; height: 30px; border-radius: 50%; background: var(--lime); color: #17202D; display: grid; place-items: center; font-size: 16px; }}
@media (max-width: 760px) {{ .priv {{ grid-template-columns: 1fr; }} }}

/* final */
.end .wrap {{ display: grid; grid-template-columns: 1fr 1fr; gap: 28px; align-items: center; }}
.end img {{ width: 100%; max-width: 520px; margin-inline: auto; }}
.end p {{ color: var(--ink-2); margin: 0 0 22px; font-size: 19px; }}
@media (max-width: 760px) {{ .end .wrap {{ grid-template-columns: 1fr; }} }}

footer {{ border-top: 1px solid var(--line); padding-block: 28px 40px; color: var(--muted); font-size: 14px; }}
footer .wrap {{ display: flex; flex-wrap: wrap; gap: 10px 24px; align-items: center; }}
footer .note {{ flex-basis: 100%; }}
{trophy_css}
[dir="rtl"] .btn.primary svg {{ transform: scaleX(-1); }}
@media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior: auto; }} }}
</style>
</head>
<body>
<header>
  <div class="wrap bar">
    <a class="brand" href="#top" aria-label="Рица">
      <img class="mark" src="img/mark.webp" alt="" width="46" height="46">
      <img class="wm light" id="wm-light" src="img/wordmark-ru.svg" alt="Рица">
      <img class="wm dark" id="wm-dark" src="img/wordmark-ru-dark.svg" alt="Рица">
    </a>
    <nav>
      <a href="#hunt" data-t="nav_hunt">{s("nav_hunt")}</a>
      <a href="#route" data-t="nav_route">{s("nav_route")}</a>
      <a href="#features" data-t="nav_features">{s("nav_features")}</a>
      <a href="#privacy" data-t="nav_privacy">{s("nav_privacy")}</a>
    </nav>
    <div class="lang" role="group" aria-label="{s("lang_label")}" id="lang">
      <button type="button" data-lang="ru" aria-pressed="true" title="Русский">RU</button>
      <button type="button" data-lang="en" aria-pressed="false" title="English">EN</button>
      <button type="button" data-lang="he" aria-pressed="false" title="עברית">HE</button>
    </div>
  </div>
</header>

<main id="top">
  <div class="hero">
    <div class="wrap">
      <div>
        <span class="eyebrow"><i></i><span data-t="hero_eyebrow">{s("hero_eyebrow")}</span></span>
        <h1 data-t="hero_h1">{s("hero_h1")}</h1>
        <p class="sub" data-t="hero_sub">{s("hero_sub")}</p>
        <div class="ctas">
          <span class="btn primary" aria-disabled="true"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 3.5v17a.8.8 0 0 0 1.2.7l14.6-8.5a.8.8 0 0 0 0-1.4L5.2 2.8A.8.8 0 0 0 4 3.5z"/></svg><span data-t="cta_soon">{s("cta_soon")}</span></span>
          <a class="btn ghost" href="mailto:ritza.support@gmail.com" data-t="cta_write">{s("cta_write")}</a>
        </div>
      </div>
      <div class="hero-art"><img src="img/chase.webp" alt="" width="1400" height="1050" fetchpriority="high"></div>
    </div>
  </div>

  <section id="hunt" class="hunt">
    <div class="wrap">
      <div class="kicker" data-t="hunt_kicker">{s("hunt_kicker")}</div>
      <h2 data-t="hunt_h2">{s("hunt_h2")}</h2>
      <div class="grid-2">
        <article class="card"><div class="pic"><img src="img/hunt-hare.webp" alt="" width="900" height="675" loading="lazy"></div>
          <div class="txt"><h3 data-t="hunt_hare_h">{s("hunt_hare_h")}</h3><p data-t="hunt_hare_p">{s("hunt_hare_p")}</p></div></article>
        <article class="card"><div class="pic"><img src="img/hunt-wolf.webp" alt="" width="900" height="675" loading="lazy"></div>
          <div class="txt"><h3 data-t="hunt_wolf_h">{s("hunt_wolf_h")}</h3><p data-t="hunt_wolf_p">{s("hunt_wolf_p")}</p></div></article>
      </div>
    </div>
  </section>

  <section id="trophies" class="trophies is-paused" aria-labelledby="trophy-heading">
    <div class="wrap">
      <div class="trophy-lead">
        <div>
          <div class="kicker" data-t="trophy_kicker">{s("trophy_kicker")}</div>
          <h2 id="trophy-heading" data-t="trophy_h2">{s("trophy_h2")}</h2>
          <p data-t="trophy_p">{s("trophy_p")}</p>
          <div class="trophy-metals">
            <span class="trophy-metal bronze" data-t="trophy_bronze">{s("trophy_bronze")}</span>
            <span class="trophy-metal silver" data-t="trophy_silver">{s("trophy_silver")}</span>
            <span class="trophy-metal gold" data-t="trophy_gold">{s("trophy_gold")}</span>
          </div>
          <span class="trophy-hint" id="trophy-hint" data-t="trophy_hint">{s("trophy_hint")}</span>
        </div>
        {legend_medal.replace('medal-toggle gold', 'medal-toggle gold trophy-legend')}
      </div>
      <div class="trophy-grid">
        {trophy_grid}
      </div>
    </div>
  </section>

  <section id="route" class="route">
    <div class="wrap">
      <div class="route-text">
        <div class="kicker" data-t="route_kicker">{s("route_kicker")}</div>
        <h2 data-t="route_h2">{s("route_h2")}</h2>
        <p class="lead" data-t="route_p">{s("route_p")}</p>
        <ul class="ticks">
          <li><b>✓</b><span data-t="route_b1">{s("route_b1")}</span></li>
          <li><b>✓</b><span data-t="route_b2">{s("route_b2")}</span></li>
          <li><b>✓</b><span data-t="route_b3">{s("route_b3")}</span></li>
          <li><b>✓</b><span data-t="route_b4">{s("route_b4")}</span></li>
        </ul>
        <p class="small" data-t="route_note">{s("route_note")}</p>
      </div>
      <div class="route-shots">
        <figure class="phone"><div class="frame"><img data-shot="plan" src="img/screen-plan-ru.webp" alt="" width="540" height="1104" loading="lazy"></div><span data-t="shot_plan">{s("shot_plan")}</span></figure>
        <figure class="phone"><div class="frame"><img data-shot="today" src="img/screen-today-ru.webp" alt="" width="540" height="1104" loading="lazy"></div><span data-t="shot_today">{s("shot_today")}</span></figure>
      </div>
    </div>
  </section>

  <section id="features">
    <div class="wrap">
      <div class="kicker" data-t="feat_kicker">{s("feat_kicker")}</div>
      <h2 data-t="feat_h2">{s("feat_h2")}</h2>
      <div class="grid-3">
FEATURES
      </div>
    </div>
  </section>

  <section id="shots">
    <div class="wrap">
      <h2 data-t="shots_h2">{s("shots_h2")}</h2>
      <div class="shots">
        <figure class="phone"><div class="frame"><img data-shot="hunt" src="img/screen-hunt-ru.webp" alt="" width="540" height="1104" loading="lazy"></div><span data-t="shot_hunt">{s("shot_hunt")}</span></figure>
        <figure class="phone"><div class="frame"><img data-shot="summary" src="img/screen-summary-ru.webp" alt="" width="540" height="1104" loading="lazy"></div><span data-t="shot_summary">{s("shot_summary")}</span></figure>
        <figure class="phone"><div class="frame"><img data-shot="start" src="img/screen-start-ru.webp" alt="" width="540" height="1104" loading="lazy"></div><span data-t="shot_start">{s("shot_start")}</span></figure>
      </div>
    </div>
  </section>

  <section id="privacy">
    <div class="wrap">
      <div class="priv">
        <div><div class="kicker" data-t="priv_kicker">{s("priv_kicker")}</div><h2 data-t="priv_h2">{s("priv_h2")}</h2></div>
        <div class="pills">
          <div class="pill"><b>✓</b><span data-t="p1">{s("p1")}</span></div>
          <div class="pill"><b>✓</b><span data-t="p2">{s("p2")}</span></div>
          <div class="pill"><b>✓</b><span data-t="p3">{s("p3")}</span></div>
        </div>
      </div>
    </div>
  </section>

  <section class="end">
    <div class="wrap">
      <img src="img/finish.webp" alt="" width="900" height="675" loading="lazy">
      <div>
        <h2 data-t="end_h2">{s("end_h2")}</h2>
        <p data-t="end_p">{s("end_p")}</p>
        <a class="btn primary" href="mailto:ritza.support@gmail.com" data-t="cta_write">{s("cta_write")}</a>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <a href="https://ritm-run.github.io/privacy/" data-t="foot_privacy">{s("foot_privacy")}</a>
    <span><span data-t="foot_support">{s("foot_support")}</span>: <bdi dir="ltr">ritza.support@gmail.com</bdi></span>
    <span>© 2026</span>
    <span class="note" data-t="foot_note">{s("foot_note")}</span>
  </div>
</footer>

<script>
const T = I18N;
const html = document.documentElement;
function apply(lang) {{
  const d = T[lang] || T.ru;
  html.lang = lang; html.dir = lang === "he" ? "rtl" : "ltr";
  document.title = d.title;
  document.querySelectorAll("[data-t]").forEach(el => {{ const k = el.dataset.t; if (d[k]) setTranslation(el, d[k], lang); }});
  document.querySelector('meta[name="description"]').content = d.hero_sub;
  document.querySelector('meta[property="og:description"]').content = d.hero_sub;
  document.querySelectorAll("img[data-shot]").forEach(i => {{ i.src = "img/screen-" + i.dataset.shot + "-" + lang + ".webp"; }});
  document.getElementById("wm-light").src = "img/wordmark-" + lang + ".svg";
  document.getElementById("wm-dark").src = "img/wordmark-" + lang + "-dark.svg";
  const brandName = lang === "he" ? "ריצה" : lang === "en" ? "Ritza" : "Рица";
  document.querySelector(".brand").setAttribute("aria-label", brandName);
  document.getElementById("wm-light").alt = brandName;
  document.getElementById("wm-dark").alt = brandName;
  document.querySelectorAll("#lang button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.lang === lang)));
  document.getElementById("lang").setAttribute("aria-label", d.lang_label);
  try {{ localStorage.setItem("ritza-lang", lang); }} catch (e) {{}}
}}
// Keep Latin brands, decimal numbers, times and Roman tiers together in RTL.
// Text stays in JSON; bdi is created as DOM, never as translated HTML.
function setTranslation(el, value, lang) {{
  el.replaceChildren();
  if (lang !== "he") {{ el.textContent = value; return; }}
  const mixed = /Google (?:Play|Drive)|[0-9]+(?:[.,:][0-9]+)*(?:\\s?%|\\sXP)?|\\b(?:III|II|I)\\b/g;
  let at = 0;
  for (const match of value.matchAll(mixed)) {{
    el.append(document.createTextNode(value.slice(at, match.index)));
    const isolated = document.createElement("bdi"); isolated.dir = "ltr"; isolated.textContent = match[0];
    el.append(isolated); at = match.index + match[0].length;
  }}
  el.append(document.createTextNode(value.slice(at)));
}}
document.querySelectorAll("#lang button").forEach(b => b.addEventListener("click", () => apply(b.dataset.lang)));
let start = (location.hash || "").replace("#", "");
if (!T[start]) {{ try {{ start = localStorage.getItem("ritza-lang"); }} catch (e) {{}} }}
if (!T[start]) {{ const n = (navigator.language || "ru").toLowerCase(); start = n.startsWith("he") || n.startsWith("iw") ? "he" : n.startsWith("ru") ? "ru" : "en"; }}
apply(start);
{trophy_script}
</script>
</body>
</html>
"""

icons = {
  "f1": '<path d="M12 21s-6-5.4-6-10a6 6 0 0 1 12 0c0 4.6-6 10-6 10z"/><circle cx="12" cy="11" r="2.2"/>',
  "f2": '<path d="M4 10v4"/><path d="M8 7v10"/><path d="M12 4v16"/><path d="M16 7v10"/><path d="M20 10v4"/>',
  "f3": '<circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/>',
  "f4": '<path d="M4 19h16"/><path d="M6 15l4-5 3 3 5-7"/>',
  "f5": '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
  "f6": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17"/><path d="M12 3.5c2.5 2.5 3.5 5.5 3.5 8.5s-1 6-3.5 8.5c-2.5-2.5-3.5-5.5-3.5-8.5s1-6 3.5-8.5z"/>',
}
cards = []
for k in ("f1", "f2", "f3", "f4", "f5", "f6"):
    cards.append(f'        <article class="card"><div class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">{icons[k]}</svg></div>'
                 f'<h3 data-t="{k}_h">{s(k + "_h")}</h3><p data-t="{k}_p">{s(k + "_p")}</p></article>')
page = page.replace("FEATURES", "\n".join(cards)).replace("I18N", json.dumps(t, ensure_ascii=False))
open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(page)
print("ok", len(page))
