# Build /workspace/news-web/index.html
SITE_TITLE="南恩新聞報報"; DATE="2026.10.15"
import os,zipfile,datetime
D8=DATE.replace(".","")
WD="日一二三四五六"[(datetime.date(*map(int,DATE.split(".")) ).isoweekday())%7]
fx=[("美元","USD","32.34","32.135"),("澳幣","AUD","22.44","22.57"),("日圓","JPY","0.207","0.2047"),("人民幣","CNY","4.854","4.818")]
idx=[("道瓊","51,621.48","-48.62","-0.09%"),("標普500","7,718.94","-86.51","-1.11%"),("那斯達克","26,692.87","-511.51","-1.88%"),("台股加權","46,969.87","-1,655.96","-3.41%")]
heads=[("台股挫跌1655點　失守月線創單日第6大跌點","中央社","2026/10/15 13:53","https://www.cna.com.tw/news/afe/202610150126.aspx"),
("美9月通膨升至3.7%　共和黨期中選舉再添變數","中央社","2026/10/15 10:02","https://www.cna.com.tw/news/afe/202610150034.aspx"),
("政府將普發萬元　全教總籲正視退休基金永續經營","中央社","2026/10/15 11:19","https://www.cna.com.tw/news/ahel/202610150057.aspx"),
("股市大跌景氣差？今年前八月總薪資年增4.55％ 創16年新高","工商時報","2026/10/15 20:20","https://www.ctee.com.tw/news/20261015702223-430503"),
("拚2035年達「失智友善台灣888」　衛福部研議用藥納健保","中央社","2026/10/15 16:24","https://www.cna.com.tw/news/ahel/202610150214.aspx")]
posters=[("poster-v4-studio.png","每日報報 2026.10.15（新聞棚版）","20261015-每日報報-新聞棚版.png"),
("poster-v3-bluegreen.png","每日報報 2026.10.15（藍綠版）","20261015-每日報報-藍綠版.png"),
("poster-v2-101.png","每日報報 2026.10.15（101版）","20261015-每日報報-101版.png"),
("poster-v1-navy.png","每日報報 2026.10.15（深藍版）","20261015-每日報報-深藍版.png")]
clips=[("clip-ctee-salary.png","前八月總薪資 創16年同期新高","工商時報 2026/10/15","https://www.ctee.com.tw/news/20261015702223-430503","20261015-剪報-前八月總薪資.png"),
("clip-cna-cpi.png","美9月通膨3.7% 升息壓力再起","中央社 2026/10/15","https://www.cna.com.tw/news/afe/202610150034.aspx","20261015-剪報-美國9月通膨.png"),
("clip-cna-dementia.png","失智照護3.0 研議用藥納健保","中央社 2026/10/15","https://www.cna.com.tw/news/ahel/202610150214.aspx","20261015-剪報-失智照護3.0.png"),
("clip-cna-pension.png","普發萬元之際 全教總籲撥補退休基金","中央社 2026/10/15","https://www.cna.com.tw/news/ahel/202610150057.aspx","20261015-剪報-全教總退休基金.png")]
def chg(v,p):
    d=float(v)-float(p);dec=max(len(v.split('.')[1]),len(p.split('.')[1]));return ("up" if d>0 else "dn"),f"{d:+.{dec}f}",f"{d/float(p)*100:+.2f}%"
fxh="".join(f'<div class=q><div class=qn>{n} <small>{c}</small></div><div class=qv>{v}</div><div class="{chg(v,p)[0]} qd">{"▲" if chg(v,p)[0]=="up" else "▼"} {chg(v,p)[1]}（{chg(v,p)[2]}）</div></div>' for n,c,v,p in fx)
ixh="".join(f'<div class=q><div class=qn>{n}</div><div class=qv>{v}</div><div class="{"up" if d[0]=="+" else "dn"} qd">{"▲" if d[0]=="+" else "▼"} {d}（{p}）</div></div>' for n,v,d,p in idx)
hh="".join(f'<a class=hl href="{u}" target=_blank rel=noopener><span class=no>{i+1}</span><span class=ht>{h}<small>{s}｜{t}</small></span></a>' for i,(h,s,t,u) in enumerate(heads))
def fig(f,cap,dl,extra=""):
    return f'<figure><img src="img/{f}" alt="{cap}" loading=lazy><figcaption><b>{cap}</b>{extra}</figcaption><a class=btn href="img/{f}" download="{dl}">下載圖片</a></figure>'
ph="".join(fig(f,c,d) for f,c,d in posters)
ch="".join(fig(f,c,d,f'<br><a href="{u}" target=_blank rel=noopener>原文：{s} ›</a>') for f,c,s,u,d in clips)
# date-driven zip
ZIP=f"news-{D8}-all.zip"
for z in os.listdir('/workspace/news-web'):
    if z.startswith('news-') and z.endswith('-all.zip') and z!=ZIP: os.remove('/workspace/news-web/'+z)
with zipfile.ZipFile('/workspace/news-web/'+ZIP,'w') as z:
    for f,c,d in posters: z.write('/workspace/news-web/img/'+f,d)
    for f,c,s,u,d in clips: z.write('/workspace/news-web/img/'+f,d)
html=f"""<!doctype html><html lang=zh-Hant><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>A1 要聞 | {DATE} | {SITE_TITLE}</title>
<link rel=preconnect href=https://fonts.googleapis.com><link rel=preconnect href=https://fonts.gstatic.com crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=Noto+Serif+TC:wght@700;900&display=swap" rel=stylesheet>
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#f4f2ec;color:#222;font-family:'Noto Sans TC','Noto Sans CJK TC',sans-serif;-webkit-text-size-adjust:none}}
.paper{{max-width:640px;margin:0 auto;background:#fffefa;padding:14px 16px 28px;min-height:100vh}}
.top{{display:flex;justify-content:space-between;font-size:12px;color:#666;border-bottom:1px solid #222;padding-bottom:5px}}
.mast{{text-align:center;padding:12px 0 8px;border-bottom:4px double #222}}
.mast h1{{margin:0;font-family:'Noto Serif TC','Noto Serif CJK TC',serif;font-weight:900;font-size:clamp(42px,13vw,72px);letter-spacing:6px;line-height:1.1;color:#111}}
.mast .en{{font-size:11px;letter-spacing:4px;color:#555;margin-top:4px}}
.ed{{display:flex;align-items:center;gap:10px;border-bottom:1px solid #222;padding:7px 0;font-size:14px}}
.ed .pg{{background:#e60012;color:#fff;font-weight:900;padding:2px 8px}}
.ed b{{font-weight:900}} .ed .d{{margin-left:auto;color:#444}}
h2{{font-weight:900;font-size:19px;margin:22px 0 8px;padding:0 0 5px 10px;border-left:5px solid #e60012;border-bottom:1px solid #ccc;line-height:1.3}}
h2 small{{font-weight:400;font-size:12px;color:#777;margin-left:6px}}
.qs{{display:grid;grid-template-columns:repeat(2,1fr);border-top:1px solid #ddd;border-left:1px solid #ddd}}
.q{{border-right:1px solid #ddd;border-bottom:1px solid #ddd;padding:9px 10px}}
.qn{{font-weight:700;font-size:14px;color:#333}} .qn small{{color:#888;font-weight:400}}
.qv{{font-weight:900;font-size:24px;font-variant-numeric:tabular-nums;color:#111}}
.qd{{font-size:13px;font-weight:500}} .up{{color:#e60012}} .dn{{color:#008a3a}}
.note{{font-size:11.5px;color:#777;margin-top:5px;line-height:1.5}}
.hl{{display:flex;gap:10px;text-decoration:none;color:#111;border-bottom:1px solid #ddd;padding:11px 0}}
.hl:first-of-type{{padding-top:4px}}
.no{{flex:none;font-family:'Noto Serif TC',serif;font-weight:900;font-size:22px;color:#e60012;width:20px;line-height:1.2}}
.ht{{font-family:'Noto Serif TC','Noto Serif CJK TC',serif;font-weight:900;font-size:17px;line-height:1.45}}
.ht small{{display:block;font-family:'Noto Sans TC',sans-serif;font-weight:400;font-size:12px;color:#888;margin-top:3px}}
figure{{margin:0 0 18px;padding:0 0 14px;border-bottom:1px solid #ddd;text-align:center}}
figure img{{width:100%;height:auto;display:block;border:1px solid #ccc}}
figcaption{{font-size:14px;margin:8px 0;line-height:1.6;color:#333}} figcaption a{{color:#e60012;text-decoration:none}}
.btn{{display:inline-block;border:1px solid #e60012;color:#e60012;background:#fff;font-weight:700;text-decoration:none;border-radius:4px;padding:7px 22px;font-size:14px}}
.all{{display:block;background:#e60012;color:#fff;text-align:center;margin:6px 0 14px}}
.tip{{font-size:12px;color:#777;margin-bottom:6px}}
footer{{margin-top:22px;border-top:4px double #222;padding-top:10px;font-size:12px;line-height:1.7;color:#555;display:flex;gap:10px;align-items:center}}
footer img{{width:52px;height:auto;flex:none}}
</style></head><body><div class=paper>
<div class=top><span>{DATE}（{WD}）</span><span>財經・保險・理財</span></div>
<div class=mast><h1>{SITE_TITLE}</h1></div>
<div class=ed><span class=pg>A1</span><b>要聞</b><span class=d>{DATE}</span></div>
<h2>五大重點財經頭條</h2>{hh}
<h2>匯率<small>臺銀即期賣出・新台幣／1外幣</small></h2><div class=qs>{fxh}</div>
<div class=note>2026/10/15 21:02 掛牌；漲跌較 10/14 16:01 末次掛牌。紅漲綠跌。</div>
<h2>重要指數</h2><div class=qs>{ixh}</div>
<div class=note>美股為美東 10/14 收盤；台股加權為 10/15 收盤。</div>
<h2>今日海報</h2><div class=tip>點「下載圖片」儲存，或在手機上長按圖片另存。</div>
<a class="btn all" href="{ZIP}" download="{SITE_TITLE}-{D8}-全部圖片.zip">全部下載（ZIP）</a>
{ph}
<h2>新聞剪報</h2>{ch}
<footer><img src="img/logo.png" alt="大心團隊"><div>資料來源：臺灣銀行牌告匯率（rate.bot.com.tw）、臺灣證券交易所、Reuters／Investing.com、中央社、工商時報。<br>資料截至 2026/10/15 21:02（台北時間）。內容僅供參考，不構成投資建議。</div></footer>
</div></body></html>"""
open('/workspace/news-web/index.html','w').write(html)
