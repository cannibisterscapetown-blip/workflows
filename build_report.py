import json, base64, os

with open('/tmp/templates.json') as f:
    templates = json.load(f)

with open('/home/user/workflows/Canni Logo.png', 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode()

# Re-engagement combined: Mar 20 + Mar 21 + Mar 24 (cancelled partial)
reeng_recipients = 13128 + 13103 + 8741
reeng_delivered  = 11610 + 11742 + 8197
reeng_opens      = 987 + 1000 + 558
reeng_clicks     = 33 + 40 + 16
reeng_unsubs     = 12 + 23 + 9
reeng_convs      = 1 + 4 + 0
reeng_revenue    = 3562.90
reeng_del_rate   = reeng_delivered / reeng_recipients * 100
reeng_open_rate  = reeng_opens / reeng_delivered * 100
reeng_click_rate = reeng_clicks / reeng_delivered * 100

campaigns = [
    {
        'name': 'March Newsletter',
        'date': 'Mar 5',
        'status': 'Sent', 'sc': 'sent',
        'subject': 'March specials just landed \U0001f33f',
        'audience': 'Diamond/Platinum \u00b7 Engaged \u00b7 Active Hub \u00b7 2\u00d7 Buyers',
        'recipients': 7103, 'delivered': 6814, 'delivery_rate': 95.9,
        'opens': 1513, 'open_rate': 22.2, 'clicks': 42, 'click_rate': 0.62,
        'unsubscribes': 35, 'conversions': 52, 'revenue': 54559.80, 'aov': 529.71,
        'templates': [{'label': 'View Email', 'key': 'march_newsletter'}], 'ab': False,
    },
    {
        'name': 'Membership Offer',
        'date': 'Mar 5',
        'status': 'Sent', 'sc': 'sent',
        'subject': 'Become a Cannibisters member today \U0001f33f',
        'audience': 'New Contacts',
        'recipients': 3716, 'delivered': 3396, 'delivery_rate': 91.4,
        'opens': 71, 'open_rate': 2.1, 'clicks': 8, 'click_rate': 0.24,
        'unsubscribes': 0, 'conversions': 0, 'revenue': 0, 'aov': 0,
        'templates': [{'label': 'View Email', 'key': 'membership_campaign'}], 'ab': False,
    },
    {
        'name': 'Loyalty: 1M Points Redeemed',
        'date': 'Mar 12',
        'status': 'Sent', 'sc': 'sent',
        'subject': 'One member got R9,070 off their order \U0001f62e',
        'audience': 'Diamond/Platinum \u00b7 Engaged \u00b7 Active Hub \u00b7 2\u00d7 Buyers',
        'recipients': 7104, 'delivered': 6996, 'delivery_rate': 98.5,
        'opens': 1811, 'open_rate': 25.9, 'clicks': 49, 'click_rate': 0.70,
        'unsubscribes': 19, 'conversions': 61, 'revenue': 73378.75, 'aov': 527.90,
        'templates': [{'label': 'View Email', 'key': 'loyalty_1m_points'}], 'ab': False,
    },
    {
        'name': 'Happy Hour March',
        'date': 'Mar 17',
        'status': 'Sent', 'sc': 'sent',
        'subject': '24% Off Flower from 9PM till closing \U0001f33f',
        'audience': 'Diamond/Platinum \u00b7 Active Members \u00b7 Engaged \u00b7 2\u00d7 Buyers',
        'recipients': 7135, 'delivered': 6982, 'delivery_rate': 97.9,
        'opens': 1512, 'open_rate': 21.7, 'clicks': 52, 'click_rate': 0.74,
        'unsubscribes': 38, 'conversions': 28, 'revenue': 34717.50, 'aov': 655.05,
        'templates': [{'label': 'View Email', 'key': 'happy_hour_march'}], 'ab': False,
    },
    {
        'name': 'Loyalty Kiosk Launch',
        'date': 'Mar 19',
        'status': 'Sent', 'sc': 'sent',
        'subject': 'Your points are worth more than you think',
        'audience': 'Diamond/Platinum \u00b7 Active Members \u00b7 Engaged \u00b7 2\u00d7 Buyers',
        'recipients': 7095, 'delivered': 6997, 'delivery_rate': 98.6,
        'opens': 1734, 'open_rate': 24.8, 'clicks': 49, 'click_rate': 0.70,
        'unsubscribes': 32, 'conversions': 62, 'revenue': 63398.40, 'aov': 480.29,
        'templates': [{'label': 'View Email', 'key': 'loyalty_kiosk'}], 'ab': False,
    },
    {
        'name': 'Re-engagement Campaign',
        'date': 'Mar 20\u201324',
        'status': '3 Sends', 'sc': 'multi',
        'subject': "We've missed you \U0001f33f Claim your FREE 30-Day Membership",
        'audience': 'Not bought in 90 days',
        'recipients': reeng_recipients,
        'delivered': reeng_delivered,
        'delivery_rate': round(reeng_del_rate, 1),
        'opens': reeng_opens,
        'open_rate': round(reeng_open_rate, 1),
        'clicks': reeng_clicks,
        'click_rate': round(reeng_click_rate, 2),
        'unsubscribes': reeng_unsubs,
        'conversions': reeng_convs,
        'revenue': reeng_revenue,
        'aov': 593.82,
        'templates': [
            {'label': 'Var A \u2014 No Personalisation', 'key': 'reeng_mar21_varA'},
            {'label': 'Var B \u2014 Personalised', 'key': 'reeng_mar21_varB'},
        ],
        'ab': True,
    },
]

total_revenue     = sum(c['revenue'] for c in campaigns)
total_recipients  = sum(c['recipients'] for c in campaigns)
total_conversions = sum(c['conversions'] for c in campaigns)
avg_open          = sum(c['open_rate'] for c in campaigns) / len(campaigns)

used_keys = set()
for c in campaigns:
    for t in c['templates']:
        used_keys.add(t['key'])

slim_templates = {k: templates[k]['html'] for k in used_keys if k in templates}
template_json  = json.dumps(slim_templates)

def stat_cls(v, good, mid):
    if v >= good: return 'good'
    if v >= mid:  return 'mid'
    return 'bad'

def fmt_rev(v):
    return 'R{:,.0f}'.format(v) if v else '\u2014'

def fmt_aov(v):
    return 'R{:,.0f}'.format(v) if v else '\u2014'

rows_parts = []
for c in campaigns:
    btns = ''.join(
        '<button class="pbtn" onclick="openPreview(\'{k}\',\'{l}\')">&#128065; {l}</button>'.format(
            k=t['key'], l=t['label'])
        for t in c['templates']
    )
    ab_badge = '<span class="ab">A/B</span>' if c['ab'] else ''
    oc = stat_cls(c['open_rate'], 18, 8)
    cc = stat_cls(c['click_rate'], 0.5, 0.2)
    row = (
        '<tr>'
        '<td><b>{name}</b>{ab}<br>'
        '<span class="sub">&ldquo;{subject}&rdquo;</span><br>'
        '<span class="aud">&#128101; {audience}</span></td>'
        '<td class="c">{date}</td>'
        '<td class="c"><span class="badge {sc}">{status}</span></td>'
        '<td class="r">{recipients:,}</td>'
        '<td class="r">{delivery_rate:.1f}%</td>'
        '<td class="r"><span class="{oc}">{open_rate:.1f}%</span></td>'
        '<td class="r"><span class="{cc}">{click_rate:.2f}%</span></td>'
        '<td class="r">{conversions}</td>'
        '<td class="r rev">{revenue}</td>'
        '<td class="r">{aov}</td>'
        '<td>{btns}</td>'
        '</tr>'
    ).format(
        name=c['name'], ab=ab_badge, subject=c['subject'], audience=c['audience'],
        date=c['date'], sc=c['sc'], status=c['status'],
        recipients=c['recipients'], delivery_rate=c['delivery_rate'],
        oc=oc, open_rate=c['open_rate'],
        cc=cc, click_rate=c['click_rate'],
        conversions=c['conversions'],
        revenue=fmt_rev(c['revenue']),
        aov=fmt_aov(c['aov']),
        btns=btns if btns else '<span class="dim">\u2014</span>',
    )
    rows_parts.append(row)

rows_html = '\n'.join(rows_parts)

css = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--o:#ff9501;--bg:#0d0d0d;--c1:#181818;--c2:#202020;--bd:#282828;--tx:#eee;--mu:#777;--gr:#4caf50;--rd:#e53935;--yl:#ffc107}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--tx);min-height:100vh}

.hdr{background:linear-gradient(120deg,#0d0d0d 0%,#1a0f00 60%,#0d0d0d 100%);border-bottom:2px solid var(--o);padding:24px 40px;display:flex;align-items:center;gap:20px;position:relative;overflow:hidden}
.hdr::before{content:'\\1F33F';position:absolute;font-size:180px;opacity:.03;right:0;top:-30px;pointer-events:none}
.logo{width:56px;height:56px;object-fit:contain;filter:drop-shadow(0 0 10px rgba(255,149,1,.5))}
.hdr h1{font-size:22px;font-weight:800;color:var(--o);line-height:1.2}
.hdr p{font-size:12px;color:var(--mu);margin-top:3px}
.pill{margin-left:auto;background:rgba(255,149,1,.12);border:1px solid var(--o);color:var(--o);padding:7px 14px;border-radius:20px;font-size:12px;font-weight:700;white-space:nowrap}

.cards{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;padding:28px 40px 0}
.card{background:var(--c1);border:1px solid var(--bd);border-radius:12px;padding:18px;position:relative;overflow:hidden}
.card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;background:var(--o)}
.card .lbl{font-size:10px;color:var(--mu);text-transform:uppercase;letter-spacing:1.2px;font-weight:700}
.card .val{font-size:26px;font-weight:800;color:var(--o);margin:6px 0 2px;letter-spacing:-0.5px}
.card .hint{font-size:11px;color:var(--mu)}

.sec{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:2px;color:var(--o);padding:24px 40px 12px;display:flex;align-items:center;gap:10px}
.sec::after{content:'';flex:1;height:1px;background:var(--bd)}

.tw{padding:0 40px 40px;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{background:var(--c2);color:var(--mu);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;padding:11px 14px;text-align:left;border-bottom:1px solid var(--bd);white-space:nowrap}
th.c{text-align:center}th.r{text-align:right}
tr{border-bottom:1px solid var(--bd);transition:background .12s}
tr:hover{background:rgba(255,149,1,.04)}
td{padding:13px 14px;vertical-align:middle}
td.c{text-align:center}td.r{text-align:right;font-variant-numeric:tabular-nums}
td.rev{color:var(--o);font-weight:700}
b{font-weight:700;font-size:13.5px}
.sub{font-size:11px;color:var(--mu);font-style:italic;display:block;margin-top:2px;max-width:300px}
.aud{font-size:10.5px;color:#4a4a4a;display:block;margin-top:2px}
.ab{display:inline-block;background:rgba(255,149,1,.15);color:var(--o);border:1px solid var(--o);padding:1px 5px;border-radius:3px;font-size:9px;font-weight:800;margin-left:5px;vertical-align:middle}
.badge{display:inline-block;padding:3px 8px;border-radius:20px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px}
.badge.sent{background:rgba(76,175,80,.12);color:var(--gr);border:1px solid var(--gr)}
.badge.multi{background:rgba(255,149,1,.12);color:var(--o);border:1px solid var(--o)}
.badge.cancelled{background:rgba(229,57,53,.12);color:var(--rd);border:1px solid var(--rd)}
span.good{color:var(--gr);font-weight:600}
span.mid{color:var(--yl);font-weight:600}
span.bad{color:var(--rd);font-weight:600}
.dim{color:#333}
.pbtn{display:block;background:rgba(255,149,1,.08);color:var(--o);border:1px solid rgba(255,149,1,.25);padding:5px 9px;border-radius:5px;font-size:10.5px;font-weight:600;cursor:pointer;margin-bottom:3px;width:100%;text-align:left;transition:all .12s;white-space:nowrap}
.pbtn:hover{background:rgba(255,149,1,.2);border-color:var(--o)}

.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.88);z-index:999;align-items:center;justify-content:center;backdrop-filter:blur(5px)}
.overlay.on{display:flex}
.modal{background:var(--c1);border:1px solid var(--o);border-radius:14px;width:88vw;max-width:780px;height:86vh;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 0 50px rgba(255,149,1,.18)}
.mhdr{background:linear-gradient(90deg,#180f00,#111);border-bottom:1px solid var(--o);padding:14px 18px;display:flex;align-items:center;gap:10px}
.mhdr h3{font-size:14px;font-weight:700;color:var(--o);flex:1}
.mcls{background:none;border:1px solid var(--bd);color:var(--mu);width:30px;height:30px;border-radius:7px;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;transition:all .12s}
.mcls:hover{border-color:var(--o);color:var(--o)}
.mframe{flex:1;background:#fff}
.mframe iframe{width:100%;height:100%;border:none}

footer{border-top:1px solid var(--bd);padding:20px 40px;text-align:center;color:var(--mu);font-size:11px}
footer strong{color:var(--o)}
"""

js = """
const T = TEMPLATE_DATA_PLACEHOLDER;
function openPreview(k, l) {
  var h = T[k];
  if (!h) { alert('Template not available'); return; }
  var u = URL.createObjectURL(new Blob([h], {type: 'text/html'}));
  document.getElementById('mtitle').textContent = l;
  document.getElementById('mif').src = u;
  document.getElementById('ov').classList.add('on');
}
function closeModal() {
  var ov = document.getElementById('ov');
  ov.classList.remove('on');
  var f = document.getElementById('mif');
  URL.revokeObjectURL(f.src);
  f.src = '';
}
function chkClose(e) { if (e.target === document.getElementById('ov')) closeModal(); }
document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeModal(); });
"""

js = js.replace('TEMPLATE_DATA_PLACEHOLDER', template_json)

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cannibisters \u2014 March 2026 Klaviyo Report</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
CSS_PLACEHOLDER
</style>
</head>
<body>

<div class="hdr">
  <img class="logo" src="data:image/png;base64,LOGO_PLACEHOLDER" alt="Cannibisters">
  <div>
    <h1>Klaviyo Performance Report</h1>
    <p>Cannibisters Herbal Apothecary &middot; Sea Point, Cape Town</p>
  </div>
  <div class="pill">&#128197; March 2026</div>
</div>

<div class="cards">
  <div class="card"><div class="lbl">Campaigns</div><div class="val">6</div><div class="hint">sent this month</div></div>
  <div class="card"><div class="lbl">Total Recipients</div><div class="val">TOTAL_RECIPIENTS</div><div class="hint">across all sends</div></div>
  <div class="card"><div class="lbl">Total Revenue</div><div class="val">TOTAL_REVENUE</div><div class="hint">email attributed</div></div>
  <div class="card"><div class="lbl">Avg Open Rate</div><div class="val">AVG_OPEN</div><div class="hint">across campaigns</div></div>
  <div class="card"><div class="lbl">Total Conversions</div><div class="val">TOTAL_CONVS</div><div class="hint">placed orders</div></div>
</div>

<div class="sec">&#128202; Campaign Breakdown</div>
<div class="tw">
  <table>
    <thead><tr>
      <th>Campaign</th><th class="c">Date</th><th class="c">Status</th>
      <th class="r">Recipients</th><th class="r">Delivery</th><th class="r">Open Rate</th>
      <th class="r">CTR</th><th class="r">Convs</th><th class="r">Revenue</th><th class="r">AOV</th>
      <th>Preview</th>
    </tr></thead>
    <tbody>
ROWS_PLACEHOLDER
    </tbody>
  </table>
</div>

<footer>Generated for <strong>Cannibisters Herbal Apothecary</strong> &middot; Klaviyo data &middot; March 2026</footer>

<div class="overlay" id="ov" onclick="chkClose(event)">
  <div class="modal">
    <div class="mhdr">
      <h3 id="mtitle">Email Preview</h3>
      <button class="mcls" onclick="closeModal()">&#10005;</button>
    </div>
    <div class="mframe"><iframe id="mif" sandbox="allow-same-origin"></iframe></div>
  </div>
</div>

<script>
JS_PLACEHOLDER
</script>
</body>
</html>"""

html = html.replace('CSS_PLACEHOLDER', css)
html = html.replace('LOGO_PLACEHOLDER', logo_b64)
html = html.replace('TOTAL_RECIPIENTS', '{:,}'.format(total_recipients))
html = html.replace('TOTAL_REVENUE', 'R{:,.0f}'.format(total_revenue))
html = html.replace('AVG_OPEN', '{:.1f}%'.format(avg_open))
html = html.replace('TOTAL_CONVS', str(total_conversions))
html = html.replace('ROWS_PLACEHOLDER', rows_html)
html = html.replace('JS_PLACEHOLDER', js)

out = '/home/user/workflows/March_2026_Klaviyo_Report.html'
with open(out, 'w') as f:
    f.write(html)

print('Done: {} KB'.format(int(os.path.getsize(out) / 1024)))
