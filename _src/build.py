#!/usr/bin/env python3
"""Builds the six lace invitations (EN/NE x reception / wedding / wedding+reception).
Run from the repo root:  python3 _src/build.py   (add --preview DIR to write local previews with local fonts)
"""
import base64, json, os, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_src')
SITE = 'https://invitationrecption.netlify.app'
WA = '9779813013735'

PHOTO = base64.b64encode(open(os.path.join(SRC, 'couple_arch.jpg'), 'rb').read()).decode()
HAS_MUSIC = os.path.exists(os.path.join(ROOT, 'music.mp3'))

EV = {
  'j': dict(date='2026-11-25', bs={'en': 'Mangsir 9, 2083', 'ne': 'मंसिर ९, २०८३'},
            label={'en': 'Wedding', 'ne': 'विवाह'}, time={'en': '', 'ne': ''},
            venue={'en': '', 'ne': ''},
            map='https://www.google.com/maps/place/MFC7+VQW+Rose+Party+Palace,+H10,+Butwal,+Lumbini+Province+32907/@0,0,22z/data=!4m2!3m1!1s0x3996842b4da06a89:0xe2a5776e09e72b59'),
  'r': dict(date='2026-11-28', bs={'en': 'Mangsir 12, 2083', 'ne': 'मंसिर १२, २०८३'},
            label={'en': 'Reception', 'ne': 'रिसेप्सन'}, time={'en': '5:00 PM onwards', 'ne': 'साँझ ५:०० बजेदेखि'},
            venue={'en': '', 'ne': ''},
            map='https://www.google.com/maps/place/MFG6%2BV5X+Diyalo+Foodland+Kalikanagar,+Butwal,+Lumbini+Province+32907/@27.6771345,83.4606209,16z/data=!4m6!3m5!1s0x399687000e38b619:0xd6fbbf73869bbccb!8m2!3d27.6771345!4d83.4606209!16s%2Fg%2F11vqbf059t'),
}

PAGES = {
  'reception': dict(ev=['r'], form='rsvp-reception',
     title={'en': 'Wedding Reception', 'ne': 'विवाह रिसेप्सन'},
     invite={'en': 'request the pleasure of your company at their wedding reception',
             'ne': 'आफ्नो विवाह रिसेप्सनमा तपाईंको गरिमामय उपस्थितिको हार्दिक अनुरोध गर्दछन्'},
     desc={'en': 'You are warmly invited to the wedding reception of Ujjwal & Blesy on 28 November 2026 (Mangsir 12), 5:00 PM onwards. Tap to open your invitation.',
           'ne': 'उज्ज्वल र ब्लेसीको २०८३ मंसिर १२ (२८ नोभेम्बर २०२६) साँझ ५:०० बजेदेखि हुने विवाह रिसेप्सनमा हार्दिक निमन्त्रणा। निमन्त्रणा खोल्न ट्याप गर्नुहोस्।'}),
  'wedding': dict(ev=['j'], form='rsvp-wedding',
     title={'en': 'Wedding', 'ne': 'विवाह'},
     invite={'en': 'invite you to celebrate their wedding',
             'ne': 'आफ्नो शुभविवाहमा तपाईंलाई हार्दिक निमन्त्रणा गर्दछन्'},
     desc={'en': 'You are warmly invited to the wedding of Ujjwal & Blesy on 25 November 2026 (Mangsir 9). Tap to open your invitation.',
           'ne': 'उज्ज्वल र ब्लेसीको २०८३ मंसिर ९ (२५ नोभेम्बर २०२६) मा हुने शुभविवाहमा हार्दिक निमन्त्रणा। निमन्त्रणा खोल्न ट्याप गर्नुहोस्।'}),
  'janti': dict(ev=['j', 'r'], form='rsvp-wedding-reception',
     title={'en': 'Wedding & Reception', 'ne': 'विवाह र रिसेप्सन'},
     invite={'en': 'invite you to celebrate their wedding and reception',
             'ne': 'आफ्नो शुभविवाह तथा रिसेप्सनमा तपाईंलाई हार्दिक निमन्त्रणा गर्दछन्'},
     desc={'en': 'You are warmly invited to the wedding (25 Nov, Mangsir 9) and reception (28 Nov 2026, Mangsir 12) of Ujjwal & Blesy. Tap to open your invitation.',
           'ne': 'उज्ज्वल र ब्लेसीको मंसिर ९ (२५ नोभेम्बर) को शुभविवाह र मंसिर १२ (२८ नोभेम्बर २०२६) को रिसेप्सनमा हार्दिक निमन्त्रणा। निमन्त्रणा खोल्न ट्याप गर्नुहोस्।'}),
}

S = {
 'en': dict(groom='Ujjwal', bride='Blesy', full='Ujjwal Shrestha & Blesy Shrestha', amp='&',
   hint='Tap to open', dear='Dear', together='Together with their families',
   cd='Counting down to', units=['Days', 'Hours', 'Mins', 'Secs'], day='The Day', loc='Location',
   viewloc='View Location', rsvp='RSVP', rsvpsub='Kindly let us know if you can join us',
   yname='Your name', attend='Will you attend the {e}?', yes='Joyfully yes', no='Sadly no',
   guests='Number of guests', send='Send RSVP', sending='Sending…',
   ok='Thank you! Your RSVP has been received.', err='Sorry, it could not be sent. Please try again or message us on WhatsApp.',
   wa='Message us on WhatsApp', wamsg='Hello Ujjwal & Blesy, this is {n}.',
   thanks='With love', thankmsg='Your presence and blessings will make our celebration complete.',
   photo='Two hearts, one journey', months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
   wd=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], namesep=' & ',
   mute='Music', need='Please choose for each event.'),
 'ne': dict(groom='उज्ज्वल', bride='ब्लेसी', full='उज्ज्वल श्रेष्ठ र ब्लेसी श्रेष्ठ', amp='र',
   hint='खोल्न ट्याप गर्नुहोस्', dear='आदरणीय', together='आफ्ना परिवारसँगै',
   cd='शुभ घडीसम्म', units=['दिन', 'घण्टा', 'मिनेट', 'सेकेन्ड'], day='शुभ दिन', loc='स्थान',
   viewloc='स्थान हेर्नुहोस्', rsvp='उपस्थिति', rsvpsub='कृपया आफ्नो उपस्थिति जानकारी गराउनुहोस्',
   yname='तपाईंको नाम', attend='{e}मा आउनुहुन्छ?', yes='हो, आउँछु', no='माफ गर्नुहोस्, आउन सक्दिनँ',
   guests='जम्मा व्यक्ति', send='पठाउनुहोस्', sending='पठाउँदै…',
   ok='धन्यवाद! तपाईंको जानकारी प्राप्त भयो।', err='माफ गर्नुहोस्, पठाउन सकिएन। फेरि प्रयास गर्नुहोस् वा WhatsApp मा सन्देश पठाउनुहोस्।',
   wa='WhatsApp मा सन्देश पठाउनुहोस्', wamsg='नमस्ते उज्ज्वल र ब्लेसी, म {n}।',
   thanks='स्नेहसहित', thankmsg='तपाईंको उपस्थिति र आशीर्वादले हाम्रो उत्सवलाई पूर्णता दिनेछ।',
   photo='दुई मन, एउटै यात्रा', months=['जनवरी', 'फेब्रुअरी', 'मार्च', 'अप्रिल', 'मे', 'जुन', 'जुलाई', 'अगस्ट', 'सेप्टेम्बर', 'अक्टोबर', 'नोभेम्बर', 'डिसेम्बर'],
   wd=['आइतबार', 'सोमबार', 'मंगलबार', 'बुधबार', 'बिहीबार', 'शुक्रबार', 'शनिबार'], namesep=' र ',
   mute='संगीत', need='कृपया हरेक कार्यक्रमका लागि छान्नुहोस्।'),
}

FONTS = {
 'en': "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Great+Vibes&display=swap",
 'ne': "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Great+Vibes&family=Noto+Serif+Devanagari:wght@400;500;600&family=Tiro+Devanagari+Hindi&display=swap",
}

def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

CSS = r"""
:root{--rose:#e7dce1;--mauve:#c3adb8;--plum:#4b2537;--plum2:#3a1b2a;--ink:#5a3f4d;--deep:#4b2537;--lite:#efe5ea;--sc:@@SCRIPT@@;--bd:@@BODY@@}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#2a1520}
body{background:#2a1520;color:var(--ink);font-family:var(--bd);overflow:hidden;-webkit-font-smoothing:antialiased;-webkit-tap-highlight-color:transparent}
body.rd{overflow-y:auto}
#app{position:relative;max-width:460px;margin:0 auto;background:var(--rose);overflow:hidden}
/* ---------- envelope ---------- */
#env{position:fixed;inset:0;margin:0 auto;width:100%;max-width:460px;z-index:10;cursor:pointer;overflow:hidden;background:#d9c8cf}
#env .stage{position:absolute;inset:0;will-change:transform}
.fl{position:absolute;inset:0;will-change:transform,opacity}
.fl img{pointer-events:none;user-select:none;-webkit-user-drag:none}.fl img.full{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.fl .shade{position:absolute;inset:0;background:#2a1220;opacity:0;pointer-events:none;-webkit-mask:var(--m) center/cover no-repeat;mask:var(--m) center/cover no-repeat}
.fl.t{transform-origin:50% 0;z-index:4}.fl.b{transform-origin:50% 100%;z-index:3}.fl.l{transform-origin:0 50%;z-index:1}.fl.r{transform-origin:100% 50%;z-index:2}
#seal{position:absolute;left:50%;top:50%;width:37.8%;height:auto;transform:translate(-50%,-50%);filter:drop-shadow(0 8px 10px #3a1b2a66);will-change:transform}
.tag{position:absolute;left:50%;bottom:7.5%;transform:translateX(-50%);min-width:58%;max-width:82%;padding:12px 18px 11px;text-align:center;background:linear-gradient(#f6eff2,#e9dde3);border-radius:2px;box-shadow:0 0 0 1px #b9a0ad,0 0 0 4px #f3ebef,0 0 0 5px #b9a0ad88,0 10px 18px #3a1b2a55;color:var(--deep);display:none}
.tag:before{content:'';position:absolute;left:50%;top:-8px;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,#d8c8d0 45%,#9d8592);box-shadow:0 1px 2px #0005}
.tag small{display:block;font:500 10.5px var(--bd);letter-spacing:.34em;text-transform:uppercase;color:#8a6f7d}
.tag b{display:block;font:400 26px/1.15 var(--sc);color:var(--deep);overflow-wrap:anywhere}
.named .tag{display:block}
.hint{position:absolute;left:0;right:0;bottom:2.4%;text-align:center;font:500 11px var(--bd);letter-spacing:.36em;text-transform:uppercase;color:#7a5f6d;z-index:6;transition:opacity .4s;animation:breathe 2.6s ease-in-out infinite;transform:translateZ(2px)}
@keyframes breathe{50%{opacity:.4}}
#env.go .hint{opacity:0;animation:none}
/* ---------- sections ---------- */
.sec{position:relative;min-height:100vh;min-height:100svh;padding:90px 11% 90px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.sec>.bg{position:absolute;inset:0;background-size:cover;background-position:center;transform:scale(1.08);transition:transform 3.2s cubic-bezier(.16,.7,.2,1);z-index:0}
.sec.in>.bg{transform:none}
.sec>*:not(.bg):not(.trim){position:relative;z-index:2}
.lt{color:var(--ink)}.lt>.bg{background-image:url(@@A@@paper.webp)}
.dk{color:#eadde3}.dk>.bg{background-image:url(@@A@@plum.webp)}
.hero{padding:0;min-height:100vh;min-height:100svh}
.hero>.bg{background-image:url(@@A@@card.webp);transform:scale(1.06)}
.hero .win{position:relative;z-index:2;width:72%;display:flex;flex-direction:column;align-items:center;padding:0 2%}
.trim{position:absolute;left:0;right:0;height:32px;background:url(@@A@@trim.webp) repeat-x 0 0/100% 100%;z-index:3;pointer-events:none;will-change:transform}
.trim.tp{top:-14px}.trim.bt{bottom:-14px;transform:scaleY(-1)}
.rv{opacity:0;transform:translateY(18px);filter:blur(5px);transition:opacity 1.4s cubic-bezier(.2,.6,.2,1),transform 1.6s cubic-bezier(.16,.7,.2,1),filter 1.4s ease;transition-delay:var(--d,0s)}
.in .rv{opacity:1;transform:none;filter:none}
.cap{font:500 11.5px var(--bd);letter-spacing:.36em;text-transform:uppercase;color:#8a6f7d}
.dk .cap{color:#c9b0bd}
.scr{font:400 54px/1.1 var(--sc);color:var(--deep)}
.dk .scr{color:#f1e7ec}
.rule{width:120px;height:14px;margin:18px auto}
.txt{font:italic 400 19px/1.55 var(--bd);max-width:28ch;margin:0 auto}
.dear{display:none;font:400 28px/1.25 var(--sc);color:#7b5f6e;margin-bottom:16px;overflow-wrap:anywhere}
.named .dear{display:block}
.names{font:400 66px/.95 var(--sc);color:var(--deep);margin:16px 0 4px}
.names i{display:block;font:italic 400 24px/1.6 var(--bd);color:#9b7f8d}
.full{font:500 10.5px var(--bd);letter-spacing:.3em;text-transform:uppercase;color:#8a6f7d;margin-top:8px}
.dates{margin-top:16px;display:flex;flex-direction:column;gap:10px}
.dates div{font:500 13px var(--bd);letter-spacing:.24em;text-transform:uppercase;color:var(--deep)}
.dates span{display:block;font:italic 400 15px var(--bd);letter-spacing:.02em;text-transform:none;color:#8a6f7d;margin-top:2px}
.cue{position:absolute;left:0;right:0;bottom:1.6%;z-index:2;font:500 10px var(--bd);letter-spacing:.34em;text-transform:uppercase;color:#8a6f7d}
.cue:after{content:'';display:block;width:1px;height:34px;margin:8px auto 0;background:linear-gradient(#8a6f7d,transparent);animation:drip 2.2s ease-in-out infinite;transform-origin:top}
@keyframes drip{0%{transform:scaleY(0);opacity:1}70%{transform:scaleY(1);opacity:1}100%{transform:scaleY(1);opacity:0}}
/* photo */
.ph{position:relative;width:78%;max-width:320px;aspect-ratio:340/380;margin:26px auto 4px}
.ph .pic{position:absolute;left:10%;top:8%;width:80%;height:84%;border-radius:50%;overflow:hidden;box-shadow:0 10px 30px #0008}
.ph .pic img{width:100%;height:100%;object-fit:cover;display:block}
.ph .lace{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
/* countdown */
.cd{display:flex;align-items:stretch;margin-top:26px}
.cd div{padding:0 15px;border-left:1px solid #b9a0ad99}.cd div:first-child{border-left:0}
.cd b{display:block;font:400 44px/1 var(--bd);color:var(--deep);font-variant-numeric:lining-nums}
.cd span{display:block;margin-top:8px;font:500 9.5px var(--bd);letter-spacing:.24em;text-transform:uppercase;color:#8a6f7d}
.cdt{margin-top:22px;font:italic 400 17px var(--bd);color:#8a6f7d}
/* the day */
.evs{width:100%;margin-top:6px}
.ev{padding:26px 0}
.ev+.ev{border-top:1px solid #c9b0bd44}
.ev .dn{font:300 76px/1 var(--bd);color:#f1e7ec;margin:6px 0 2px}
.ev .mo{font:500 13px var(--bd);letter-spacing:.3em;text-transform:uppercase}
.ev .wd{font:italic 400 17px var(--bd);margin-top:4px;color:#d9c3ce}
.ev .bs{font:500 12px var(--bd);letter-spacing:.2em;text-transform:uppercase;margin-top:8px;color:#c9b0bd}
.ev .tv{font:400 18px var(--bd);margin-top:12px}
/* location */
.loc{width:100%;margin-top:6px}
.lc{padding:22px 0}.lc+.lc{border-top:1px solid #b9a0ad55}
.lc .vn{font:500 21px var(--bd);color:var(--deep);margin-top:6px}
.lc .dt{font:italic 400 16px var(--bd);color:#8a6f7d;margin-top:4px}
.btn{display:inline-flex;align-items:center;gap:8px;margin-top:16px;padding:13px 26px;border:1px solid var(--deep);border-radius:40px;font:500 11.5px var(--bd);letter-spacing:.28em;text-transform:uppercase;color:var(--deep);text-decoration:none;background:#ffffff40;transition:background .3s,color .3s}
.btn:active{background:var(--deep);color:#fff}
/* rsvp */
form{width:100%;margin-top:24px;text-align:left}
.f{margin-bottom:22px}
.f .l{display:block;font:500 10.5px var(--bd);letter-spacing:.28em;text-transform:uppercase;color:#c9b0bd;margin-bottom:10px}
.f input[type=text],.f select{width:100%;padding:10px 2px;border:0;border-bottom:1px solid #c9b0bd88;background:transparent;color:#f6eef2;font:400 20px var(--bd);outline:none;border-radius:0;-webkit-appearance:none;appearance:none}
.f select{background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%23c9b0bd' stroke-width='1.3'/%3E%3C/svg%3E") no-repeat right 4px center}
.f select option{color:#3a1b2a}
.f input:focus,.f select:focus{border-bottom-color:#f1e7ec}
.pills{display:flex;gap:10px}
.pills label{flex:1;position:relative}
.pills input{position:absolute;opacity:0;pointer-events:none}
.pills span{display:block;text-align:center;padding:12px 6px;border:1px solid #c9b0bd77;border-radius:40px;font:italic 400 17px var(--bd);color:#eadde3;cursor:pointer;transition:all .35s}
.pills input:checked+span{background:#f1e7ec;color:var(--plum);border-color:#f1e7ec}
.send{display:block;width:100%;margin-top:8px;padding:16px;border:1px solid #f1e7ec;border-radius:40px;background:#f1e7ec;color:var(--plum);font:600 11.5px var(--bd);letter-spacing:.32em;text-transform:uppercase;cursor:pointer;transition:opacity .3s}
.send:disabled{opacity:.55}
.msg{margin-top:14px;text-align:center;font:italic 400 17px var(--bd);color:#e6d3dc;min-height:1.4em}
.wa{display:inline-flex;align-items:center;gap:9px;margin-top:20px;font:500 11px var(--bd);letter-spacing:.24em;text-transform:uppercase;color:#d9c3ce;text-decoration:none;border-bottom:1px solid #c9b0bd66;padding-bottom:4px}
.hp{display:none}
.end>.bg{background-image:url(@@A@@card.webp)}
.end .names{font-size:60px}
/* music */
#mute{position:fixed;top:14px;z-index:30;right:max(14px,calc(50% - 216px));width:38px;height:38px;border-radius:50%;border:1px solid #b9a0adaa;background:#f6eff2cc;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);color:var(--deep);font-size:15px;display:none;align-items:center;justify-content:center;cursor:pointer}
body.rd #mute.on{display:flex}
#spk{position:fixed;inset:0;margin:0 auto;width:100%;max-width:460px;height:100%;pointer-events:none;z-index:20;opacity:.8}
@media (prefers-reduced-motion:reduce){.rv,.sec>.bg{transition:none!important;transform:none!important;opacity:1!important;filter:none!important}}
@@NECSS@@
"""

NECSS = "*{letter-spacing:0!important;text-transform:none!important}.scr,.names,.dear,.tag b{line-height:1.35}.names{font-size:56px}.scr{font-size:44px}.cap,.dates div,.ev .mo,.ev .bs{font-size:14px}"

RULE = '<svg class="rule rv" style="--d:@@D@@s" viewBox="0 0 120 14"><g fill="none" stroke="currentColor" stroke-width=".8" opacity=".55"><path d="M0 7H48M72 7H120"/><path d="M60 1.5l5.5 5.5-5.5 5.5-5.5-5.5z"/><circle cx="52" cy="7" r="1.4"/><circle cx="68" cy="7" r="1.4"/></g></svg>'
def rule(d): return RULE.replace('@@D@@', str(d))

def build(page, lang, asset_prefix='/assets/', preview_fonts=None):
    P, T = PAGES[page], S[lang]
    evs = [dict(k=k, label=EV[k]['label'][lang], date=EV[k]['date'], bs=EV[k]['bs'][lang], time=EV[k]['time'][lang], venue=EV[k]['venue'][lang], map=EV[k]['map']) for k in P['ev']]
    url = SITE + ('/ne/' if lang == 'ne' else '/') + page + '/'
    title = P['title'][lang] + ' — ' + T['groom'] + (' र ' if lang == 'ne' else ' & ') + T['bride']
    cfg = dict(lang=lang, ev=evs, T={k: T[k] for k in ['months', 'wd', 'units', 'viewloc', 'sending', 'ok', 'err', 'wamsg', 'need', 'dear']}, wa=WA)
    rows = ''
    for e in evs:
        rows += ('<div class="f"><span class="l">' + esc(T['attend'].replace('{e}', e['label'])) + '</span><div class="pills">'
                 '<label><input type="radio" name="attend-' + e['k'] + '" value="yes"><span>' + esc(T['yes']) + '</span></label>'
                 '<label><input type="radio" name="attend-' + e['k'] + '" value="no"><span>' + esc(T['no']) + '</span></label></div></div>')
    dig = str.maketrans('0123456789', '०१२३४५६७८९')
    opts = ''.join('<option value="%d">%s</option>' % (i, str(i) if lang == 'en' else str(i).translate(dig)) for i in range(1, 11))
    form = ('<form name="' + P['form'] + '" method="POST" data-netlify="true" netlify-honeypot="bot" id="rf">'
            '<input type="hidden" name="form-name" value="' + P['form'] + '"><input type="hidden" name="lang" value="' + lang + '">'
            '<p class="hp"><label>Leave empty <input name="bot"></label></p>'
            '<div class="f"><label class="l" for="rn">' + esc(T['yname']) + '</label><input type="text" id="rn" name="name" required maxlength="80" autocomplete="name"></div>'
            + rows +
            '<div class="f"><label class="l" for="rg">' + esc(T['guests']) + '</label><select id="rg" name="guests">' + opts + '</select></div>'
            '<button class="send" type="submit">' + esc(T['send']) + '</button><div class="msg" id="rmsg"></div></form>')
    sc = "'Great Vibes','Tiro Devanagari Hindi','Noto Serif Devanagari',cursive" if lang == 'ne' else "'Great Vibes',cursive"
    bd = "'Cormorant Garamond','Noto Serif Devanagari',serif" if lang == 'ne' else "'Cormorant Garamond',Georgia,serif"
    A = asset_prefix
    css = CSS.replace('@@A@@', A).replace('@@SCRIPT@@', sc).replace('@@BODY@@', bd).replace('@@NECSS@@', NECSS if lang == 'ne' else '')
    pf = ''
    if preview_fonts:
        F = preview_fonts
        pf = "<style>" + ''.join("@font-face{font-family:'%s';font-weight:%s;font-style:%s;src:url(%s%s)}" % (fam, w, st, F, path) for fam, w, st, path in [
            ('Great Vibes', 400, 'normal', 'great-vibes/files/great-vibes-latin-400-normal.woff2'),
            ('Cormorant Garamond', 400, 'normal', 'cormorant-garamond/files/cormorant-garamond-latin-400-normal.woff2'),
            ('Cormorant Garamond', 500, 'normal', 'cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2'),
            ('Cormorant Garamond', 600, 'normal', 'cormorant-garamond/files/cormorant-garamond-latin-600-normal.woff2'),
            ('Cormorant Garamond', 300, 'normal', 'cormorant-garamond/files/cormorant-garamond-latin-300-normal.woff2'),
            ('Cormorant Garamond', 400, 'italic', 'cormorant-garamond/files/cormorant-garamond-latin-400-italic.woff2'),
            ('Cormorant Garamond', 500, 'italic', 'cormorant-garamond/files/cormorant-garamond-latin-500-italic.woff2')]) + "</style>"
    ogimg = SITE + ('/ne/' if lang == 'ne' else '/') + page + '/og.jpg'
    sep = T['namesep']
    html = f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title><meta name="description" content="{esc(P['desc'][lang])}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(P['desc'][lang])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{ogimg}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#4b2537">
<link rel="preload" as="image" href="{A}env-top.webp"><link rel="preload" as="image" href="{A}env-bottom.webp"><link rel="preload" as="image" href="{A}card.webp">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="{FONTS[lang]}" rel="stylesheet">
<style>{css}</style>{pf}</head><body>
<canvas id="spk"></canvas>
<button id="mute" type="button" aria-label="{esc(T['mute'])}">♪</button>
{'<audio id="bgm" src="/music.mp3" loop preload="auto"></audio>' if HAS_MUSIC else ''}
<div id="env" role="button" aria-label="{esc(T['hint'])}"><div class="stage">
 <div class="fl l"><img class="full" src="{A}env-left.webp" alt=""><div class="shade" style="--m:url({A}env-left.webp)"></div></div>
 <div class="fl r"><img class="full" src="{A}env-right.webp" alt=""><div class="shade" style="--m:url({A}env-right.webp)"></div></div>
 <div class="fl b"><img class="full" src="{A}env-bottom.webp" alt=""><div class="shade" style="--m:url({A}env-bottom.webp)"></div>
  <div class="tag"><small>{esc(T['dear'])}</small><b id="tagn"></b></div></div>
 <div class="fl t"><img class="full" src="{A}env-top.webp" alt=""><div class="shade" style="--m:url({A}env-top.webp)"></div><img id="seal" src="{A}seal.webp" alt=""></div>
</div><div class="hint">{esc(T['hint'])}</div></div>
<div id="app">
 <section class="sec hero" id="hero"><div class="bg"></div>
  <div class="win">
   <div class="dear rv" style="--d:.1s" id="dearn"></div>
   <div class="cap rv" style="--d:.3s">{esc(T['together'])}</div>
   <div class="names rv" style="--d:.55s">{esc(T['groom'])}<i>{esc(T['amp'])}</i>{esc(T['bride'])}</div>
   <div class="full rv" style="--d:.75s">{esc(T['full'])}</div>
   {rule(.9)}
   <p class="txt rv" style="--d:1s">{esc(P['invite'][lang])}</p>
   <div class="dates rv" style="--d:1.2s" id="hdates"></div>
  </div>
  <div class="cue rv" style="--d:1.8s">{'तल सार्नुहोस्' if lang=='ne' else 'Scroll'}</div>
 </section>
 <section class="sec dk"><div class="bg"></div><div class="trim tp"></div>
  <div class="cap rv">{esc(T['groom'])}{esc(sep)}{esc(T['bride'])}</div>
  <div class="ph rv" style="--d:.25s"><div class="pic"><img alt="" src="data:image/jpeg;base64,{PHOTO}"></div><img class="lace" src="{A}frame.webp" alt=""></div>
  <div class="scr rv" style="--d:.5s;margin-top:14px">{esc(T['photo'])}</div>
  <div class="trim bt"></div>
 </section>
 <section class="sec lt"><div class="bg"></div>
  <div class="cap rv">{esc(T['cd'])}</div>
  <div class="scr rv" style="--d:.15s;margin-top:6px" id="cdl"></div>
  <div class="cd rv" style="--d:.35s" id="cd"></div>
  <div class="cdt rv" style="--d:.5s" id="cdt"></div>
 </section>
 <section class="sec dk"><div class="bg"></div><div class="trim tp"></div>
  <div class="scr rv">{esc(T['day'])}</div>
  {rule(.15)}
  <div class="evs" id="evs"></div>
  <div class="trim bt"></div>
 </section>
 <section class="sec lt"><div class="bg"></div>
  <div class="scr rv">{esc(T['loc'])}</div>
  {rule(.15)}
  <div class="loc" id="locs"></div>
 </section>
 <section class="sec dk"><div class="bg"></div><div class="trim tp"></div>
  <div class="scr rv">{esc(T['rsvp'])}</div>
  <p class="txt rv" style="--d:.15s;margin-top:10px">{esc(T['rsvpsub'])}</p>
  <div class="rv" style="--d:.3s;width:100%">{form}</div>
  <a class="wa rv" style="--d:.45s" id="wa" href="https://wa.me/{WA}" rel="noopener"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>{esc(T['wa'])}</a>
  <div class="trim bt"></div>
 </section>
 <section class="sec lt end"><div class="bg"></div>
  <div class="win" style="width:72%;display:flex;flex-direction:column;align-items:center">
   <div class="cap rv">{esc(T['thanks'])}</div>
   <div class="names rv" style="--d:.25s">{esc(T['groom'])}<i>{esc(T['amp'])}</i>{esc(T['bride'])}</div>
   {rule(.45)}
   <p class="txt rv" style="--d:.6s">{esc(T['thankmsg'])}</p>
  </div>
 </section>
</div>
<script>var C={json.dumps(cfg, ensure_ascii=False)};</script>
<script>{JS}</script>
</body></html>"""
    return html

JS = r"""
(function(){
var $=function(i){return document.getElementById(i)},T=C.T,NE=C.lang==='ne';
function dv(s){s=String(s);return NE?s.replace(/[0-9]/g,function(d){return '०१२३४५६७८९'[d]}):s}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function cm(u){try{var x=new URL(u);if(/(^|\.)goo\.gl$/.test(x.hostname))x.search='';return x.toString()}catch(e){return u}}
var q=new URLSearchParams(location.search);
var g=(q.get('to')||q.get('name')||q.get('n')||'').replace(/[<>]/g,'').replace(/\s+/g,' ').trim().slice(0,40);
C.ev.forEach(function(e){var t=(q.get(e.k+'t')||'').trim().slice(0,40),v=(q.get(e.k+'v')||'').trim().slice(0,60),m=(q.get(e.k+'m')||'').trim();if(t)e.time=t;if(v)e.venue=v;if(/^https?:\/\//i.test(m))e.map=m.slice(0,600)});
if(g){document.body.classList.add('named');$('tagn').textContent=g;$('dearn').textContent=T.dear+' '+g;$('rn').value=g}
function D(e){return new Date(e.date+'T00:00:00')}
function fd(d){return dv(d.getDate())+' '+T.months[d.getMonth()]+' '+dv(d.getFullYear())}
$('hdates').innerHTML=C.ev.map(function(e){return '<div>'+esc(e.label)+' · '+fd(D(e))+'<span>'+esc(e.bs)+(e.time?' · '+esc(e.time):'')+'</span></div>'}).join('');
$('evs').innerHTML=C.ev.map(function(e,i){var d=D(e),tv=[e.time,e.venue].filter(Boolean).join(' · ');return '<div class="ev rv" style="--d:'+(.3+i*.2)+'s"><div class="cap">'+esc(e.label)+'</div><div class="dn">'+dv(d.getDate())+'</div><div class="mo">'+T.months[d.getMonth()]+' '+dv(d.getFullYear())+'</div><div class="wd">'+T.wd[d.getDay()]+'</div><div class="bs">'+esc(e.bs)+'</div>'+(tv?'<div class="tv">'+esc(tv)+'</div>':'')+'</div>'}).join('');
$('locs').innerHTML=C.ev.map(function(e,i){var d=D(e);return '<div class="lc rv" style="--d:'+(.3+i*.2)+'s"><div class="cap">'+esc(e.label)+'</div>'+(e.venue?'<div class="vn">'+esc(e.venue)+'</div>':'')+'<div class="dt">'+T.wd[d.getDay()]+', '+fd(d)+(e.time?' · '+esc(e.time):'')+'</div>'+(e.map?'<a class="btn" href="'+esc(cm(e.map))+'" rel="noopener"><svg width="12" height="15" viewBox="0 0 12 15" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M6 14s5-4.6 5-8.2A5 5 0 0 0 1 5.8C1 9.4 6 14 6 14z"/><circle cx="6" cy="6" r="1.8"/></svg>'+esc(T.viewloc)+'</a>':'')+'</div>'}).join('');
var tgt=D(C.ev[0]);$('cdl').textContent=C.ev[0].label;$('cdt').textContent=T.wd[tgt.getDay()]+', '+fd(tgt);
$('cd').innerHTML=T.units.map(function(u){return '<div><b>00</b><span>'+esc(u)+'</span></div>'}).join('');
var cb=$('cd').querySelectorAll('b');
function tick(){var s=Math.max(0,Math.floor((tgt-new Date())/1000)),v=[Math.floor(s/86400),Math.floor(s%86400/3600),Math.floor(s%3600/60),s%60];for(var i=0;i<4;i++)cb[i].textContent=dv(String(v[i]).padStart(2,'0'))}
tick();setInterval(tick,1000);
function wa(){var n=($('rn').value||g||'').trim();$('wa').href='https://wa.me/'+C.wa+(n?'?text='+encodeURIComponent(T.wamsg.replace('{n}',n)):'')}
wa();$('rn').addEventListener('input',wa);
$('rf').addEventListener('submit',function(ev){ev.preventDefault();var f=this,b=f.querySelector('.send'),m=$('rmsg');
 for(var i=0;i<C.ev.length;i++){if(!f.querySelector('input[name="attend-'+C.ev[i].k+'"]:checked')){m.textContent=T.need;return}}
 var fd2=new FormData(f);fd2.append('page',location.pathname);if(g)fd2.append('link-name',g);
 b.disabled=true;var old=b.textContent;b.textContent=T.sending;m.textContent='';
 fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(fd2).toString()})
 .then(function(r){if(!r.ok)throw 0;m.textContent=T.ok;f.querySelectorAll('input,select,button').forEach(function(x){x.disabled=true});b.textContent='✓'})
 .catch(function(){m.textContent=T.err;b.disabled=false;b.textContent=old})});
/* reveal */
var secs=document.querySelectorAll('.sec');
var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.2}):null;
/* scroll-linked lace trims (parallax) */
var trims=[].slice.call(document.querySelectorAll('.trim')),tk=false;
function par(){tk=false;var vh=innerHeight;trims.forEach(function(t){var r=t.parentNode.getBoundingClientRect(),p=(r.top+r.height/2-vh/2)/vh;var y=Math.max(-1,Math.min(1,p))*10;t.style.transform=(t.classList.contains('bt')?'scaleY(-1) ':'')+'translate3d(0,'+(t.classList.contains('bt')?-y:y).toFixed(1)+'px,0)'})}
addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(par)}},{passive:true});
/* sound */
var ac=null;function whoosh(){try{ac=ac||new (window.AudioContext||window.webkitAudioContext)();var t0=ac.currentTime;
 var n=ac.sampleRate*.08,bf=ac.createBuffer(1,n,ac.sampleRate),d=bf.getChannelData(0);for(var i=0;i<n;i++){var k=i/n;d[i]=(Math.random()*2-1)*Math.pow(1-k,4)}
 var s=ac.createBufferSource();s.buffer=bf;var hp=ac.createBiquadFilter();hp.type='highpass';hp.frequency.value=1500;var g1=ac.createGain();g1.gain.value=.55;s.connect(hp);hp.connect(g1);g1.connect(ac.destination);s.start(t0);
 var n2=ac.sampleRate*1.4,b2=ac.createBuffer(1,n2,ac.sampleRate),d2=b2.getChannelData(0);for(var i=0;i<n2;i++)d2[i]=Math.random()*2-1;
 var s2=ac.createBufferSource();s2.buffer=b2;var bp=ac.createBiquadFilter();bp.type='bandpass';bp.Q.value=.7;bp.frequency.setValueAtTime(500,t0+.15);bp.frequency.exponentialRampToValueAtTime(2200,t0+1.1);var g2=ac.createGain();g2.gain.setValueAtTime(0,t0+.15);g2.gain.linearRampToValueAtTime(.12,t0+.6);g2.gain.linearRampToValueAtTime(0,t0+1.5);s2.connect(bp);bp.connect(g2);g2.connect(ac.destination);s2.start(t0+.15)}catch(e){}}
/* music */
var bgm=$('bgm'),mute=$('mute'),muted=false;
if(bgm){mute.classList.add('on');mute.onclick=function(e){e.stopPropagation();muted=!muted;bgm.muted=muted;mute.textContent=muted?'×':'♪';if(!muted&&bgm.paused)bgm.play().catch(function(){})}}
function startMusic(){if(bgm&&!muted&&bgm.paused){bgm.volume=.5;bgm.play().catch(function(){})}}
['pointerdown','touchstart','keydown'].forEach(function(t){addEventListener(t,function(){startMusic()},{once:true,passive:true})});
/* open: cinematic unfolding with Web Animations */
var env=$('env'),opened=false,E='cubic-bezier(.65,0,.3,1)';
function an(el,kf,o){return el.animate?el.animate(kf,Object.assign({fill:'both'},o)):null}
function sh(el,o){var s=el.querySelector('.shade');an(s,[{opacity:0},{opacity:.12,offset:.5},{opacity:.3}],o)}
function open(user){if(opened)return;opened=true;env.classList.add('go');if(user){whoosh();startMusic()}
 var st=env.querySelector('.stage'),t=env.querySelector('.fl.t'),b=env.querySelector('.fl.b'),l=env.querySelector('.fl.l'),r=env.querySelector('.fl.r'),seal=$('seal'),hero=$('hero');
 if(!env.animate){finish();return}
 an(seal,[{transform:'translate(-50%,-50%) scale(1)',filter:'drop-shadow(0 8px 10px #3a1b2a66)'},{transform:'translate(-50%,-56%) scale(1.08)',filter:'drop-shadow(0 18px 18px #3a1b2a55)',offset:.45},{transform:'translate(-50%,-62%) scale(1.04)',filter:'drop-shadow(0 22px 22px #3a1b2a44)'}],{duration:800,easing:'cubic-bezier(.3,0,.2,1)'});
 var o1={duration:1500,delay:350,easing:E},o2={duration:1500,delay:800,easing:E},o3={duration:1400,delay:560,easing:E};
 an(t,[{transform:'scaleY(1)',opacity:1},{transform:'scaleY(.62)',opacity:1,offset:.55},{transform:'scaleY(.18)',opacity:0}],o1);sh(t,o1);
 an(b,[{transform:'scaleY(1)',opacity:1},{transform:'scaleY(.62)',opacity:1,offset:.55},{transform:'scaleY(.18)',opacity:0}],o2);sh(b,o2);
 an(l,[{transform:'scaleX(1)',opacity:1},{transform:'scaleX(.6)',opacity:1,offset:.55},{transform:'scaleX(.15)',opacity:0}],o3);sh(l,o3);
 an(r,[{transform:'scaleX(1)',opacity:1},{transform:'scaleX(.6)',opacity:1,offset:.55},{transform:'scaleX(.15)',opacity:0}],o3);sh(r,o3);
 an(hero.querySelector('.bg'),[{transform:'scale(1.12)',filter:'blur(6px)'},{transform:'scale(1.03)',filter:'blur(0px)'}],{duration:2200,delay:500,easing:'cubic-bezier(.2,.7,.2,1)'});
 an(st,[{transform:'scale(1)'},{transform:'scale(1.03)'}],{duration:2400,delay:200,easing:'cubic-bezier(.4,0,.2,1)'});
 an(env,[{backgroundColor:'#d9c8cf'},{backgroundColor:'rgba(217,200,207,0)'}],{duration:900,delay:1300});
 setTimeout(function(){document.body.classList.add('rd');hero.classList.add('in')},1500);
 setTimeout(finish,3000)}
function finish(){document.body.classList.add('rd');secs[0].classList.add('in');env.style.display='none';if(io)for(var i=1;i<secs.length;i++)io.observe(secs[i]);else secs.forEach(function(s){s.classList.add('in')});par()}
env.style.backgroundColor='transparent';
env.addEventListener('click',function(){open(true)});
setTimeout(function(){open(false)},3000);
/* sparkles: few soft specks */
var cv=$('spk'),cx=cv.getContext('2d'),Pp=[],W,H,DPR=Math.min(2,window.devicePixelRatio||1);
function rs(){W=cv.clientWidth;H=cv.clientHeight;cv.width=W*DPR;cv.height=H*DPR;cx.setTransform(DPR,0,0,DPR,0,0)}rs();addEventListener('resize',rs);
if(!matchMedia('(prefers-reduced-motion: reduce)').matches){for(var i=0;i<18;i++)Pp.push({x:Math.random()*W,y:Math.random()*H,r:.5+Math.random()*1.3,s:.12+Math.random()*.25,p:Math.random()*6.3});
 (function fr(){cx.clearRect(0,0,W,H);for(var i=0;i<Pp.length;i++){var a=Pp[i];a.y-=a.s;a.p+=.025;a.x+=Math.sin(a.p)*.2;if(a.y<-5){a.y=H+5;a.x=Math.random()*W}var al=.25+.45*Math.sin(a.p*1.7);if(al<0)al=0;cx.beginPath();cx.fillStyle='rgba(255,246,250,'+al.toFixed(2)+')';cx.arc(a.x,a.y,a.r,0,6.3);cx.fill()}requestAnimationFrame(fr)})()}
})();
"""

if __name__ == '__main__':
    args = sys.argv[1:]
    out, pf, only, A = ROOT, None, None, '/assets/'
    if '--preview' in args:
        out = args[args.index('--preview') + 1]
        pf = args[args.index('--fonts') + 1] if '--fonts' in args else None
    if '--assets' in args:
        A = args[args.index('--assets') + 1]
    if '--only' in args:
        only = args[args.index('--only') + 1].split(',')
    for page in PAGES:
        for lang in ('en', 'ne'):
            key = ('ne/' if lang == 'ne' else '') + page
            if only and key not in only:
                continue
            d = os.path.join(out, 'ne', page) if lang == 'ne' else os.path.join(out, page)
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(build(page, lang, A, pf))
            print('wrote', os.path.join(d, 'index.html'))
