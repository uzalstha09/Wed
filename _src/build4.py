#!/usr/bin/env python3
"""Builds the six lace invitations (EN/NE x reception / wedding / wedding+reception).
Run from the repo root:  python3 _src/build.py   (add --preview DIR to write local previews with local fonts)
"""
import base64, json, os, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_src')
SITE = 'https://uzalstha09.github.io/Wed'
WA = '9779813013735'

PHOTO = base64.b64encode(open(os.path.join(SRC, 'couple_arch.jpg'), 'rb').read()).decode()
HAS_MUSIC = os.path.exists(os.path.join(ROOT, 'music.mp3'))

EV = {
  'j': dict(date='2026-11-25', bs={'en': 'Mangsir 9, 2083', 'ne': 'मंसिर ९, २०८३'},
            label={'en': 'Wedding', 'ne': 'विवाह'}, time={'en': '', 'ne': ''},
            venue={'en': '', 'ne': ''},
            map='https://maps.app.goo.gl/B4FtiDtbxvyte3Ln6'),
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
   guests='Number of guests', send='Send RSVP on WhatsApp', sending='Opening WhatsApp…', send2='Send RSVP', sending2='Sending…', ok2='Thank you! Your RSVP has been received.', yesw='Yes', now='No', gw='Guests', rsvpw='RSVP',
   ok='Thank you! Please tap Send in WhatsApp to finish.', err='Sorry, it could not be sent. Please try again or message us on WhatsApp.',
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
   guests='जम्मा व्यक्ति', send='WhatsApp मा पठाउनुहोस्', sending='WhatsApp खोल्दै…', send2='पठाउनुहोस्', sending2='पठाउँदै…', ok2='धन्यवाद! तपाईंको जानकारी प्राप्त भयो।', yesw='आउँछु', now='आउन सक्दिनँ', gw='जम्मा व्यक्ति', rsvpw='उपस्थिति',
   ok='धन्यवाद! पूरा गर्न WhatsApp मा Send थिच्नुहोस्।', err='माफ गर्नुहोस्, पठाउन सकिएन। फेरि प्रयास गर्नुहोस् वा WhatsApp मा सन्देश पठाउनुहोस्।',
   wa='WhatsApp मा सन्देश पठाउनुहोस्', wamsg='नमस्ते उज्ज्वल र ब्लेसी, म {n}।',
   thanks='स्नेहसहित', thankmsg='तपाईंको उपस्थिति र आशीर्वादले हाम्रो उत्सवलाई पूर्णता दिनेछ।',
   photo='दुई मन, एउटै यात्रा', months=['जनवरी', 'फेब्रुअरी', 'मार्च', 'अप्रिल', 'मे', 'जुन', 'जुलाई', 'अगस्ट', 'सेप्टेम्बर', 'अक्टोबर', 'नोभेम्बर', 'डिसेम्बर'],
   wd=['आइतबार', 'सोमबार', 'मंगलबार', 'बुधबार', 'बिहीबार', 'शुक्रबार', 'शनिबार'], namesep=' र ',
   mute='संगीत', need='कृपया हरेक कार्यक्रमका लागि छान्नुहोस्।'),
}

FONTS = {
 'en': "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Great+Vibes&family=Pinyon+Script&display=swap",
 'ne': "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Great+Vibes&family=Pinyon+Script&family=Noto+Serif+Devanagari:wght@400;500;600&family=Tiro+Devanagari+Hindi&display=swap",
}
HERO = {
 'reception': {'en': ('Welcome to the', 'Wedding Reception', 'of'), 'ne': ('हार्दिक स्वागत', 'विवाह रिसेप्सन', '')},
 'wedding': {'en': ('Welcome to the', 'Wedding Ceremony', 'of'), 'ne': ('हार्दिक स्वागत', 'शुभविवाह', '')},
 'janti': {'en': ('Welcome to the', 'Wedding Celebration', 'of'), 'ne': ('हार्दिक स्वागत', 'विवाह तथा रिसेप्सन', '')},
}
def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

CSS = r"""
:root{--ink:#5e4a3e;--deep:#5a3e2e;--soft:#8a8196;--sc:@@SCRIPT@@;--sc2:@@SCRIPT2@@;--bd:@@BODY@@}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#1c1a22}
body{color:var(--ink);font-family:var(--bd);overflow:hidden;-webkit-font-smoothing:antialiased;-webkit-tap-highlight-color:transparent}
body.rd{overflow-y:auto}
#app{position:relative;max-width:460px;margin:0 auto;background:#f3ece6}
/* ---------- envelope ---------- */
#env{position:fixed;inset:0;margin:0 auto;width:100%;max-width:460px;z-index:10;cursor:pointer;overflow:hidden;perspective:2400px;perspective-origin:50% 40%;background:#e8e5ee}
#env{background:#efecee}
#env .stage{position:absolute;left:50%;top:50%;width:max(100%,calc(100vh*941/1672));aspect-ratio:941/1672;transform:translate(-50%,-50%);transform-style:preserve-3d}
@property --r{syntax:'<length>';inherits:false;initial-value:0px}
#waves{position:absolute;inset:0;pointer-events:none}
.wv{position:absolute;inset:0;opacity:0;--r:0px;background:url(@@A@@env-shine.webp) 0 0/100% 100% no-repeat;filter:drop-shadow(0 0 6px #fffdf6);will-change:opacity;
 -webkit-mask-image:radial-gradient(circle at var(--x) var(--y),transparent calc(var(--r) - 26vh),#000 calc(var(--r) - 16vh),#000 calc(var(--r) - 2vh),transparent calc(var(--r) + 7vh));mask-image:radial-gradient(circle at var(--x) var(--y),transparent calc(var(--r) - 26vh),#000 calc(var(--r) - 16vh),#000 calc(var(--r) - 2vh),transparent calc(var(--r) + 7vh))}
#flap3{position:absolute;inset:0;transform-origin:50% 0;will-change:transform,opacity;clip-path:polygon(0 0,100% 0,100% 21.5%,50% 53.2%,0 21.5%);filter:drop-shadow(0 6px 10px #6a5d5333)}
#seal3{transform-origin:50.2% 50.3%;will-change:transform,opacity;filter:drop-shadow(0 4px 6px #5a463322)}
#fsh{position:absolute;inset:0;opacity:0;background:linear-gradient(#0000 10%,#4a3a2a30 55%)}
.lay{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;pointer-events:none;user-select:none;-webkit-user-drag:none}
.glow{opacity:0;will-change:opacity;mix-blend-mode:screen}
#rays{position:absolute;left:50%;top:44.3%;width:260%;aspect-ratio:1;transform:translate(-50%,-50%) scale(.6);opacity:0;pointer-events:none;will-change:transform,opacity;mix-blend-mode:screen;
 background:radial-gradient(circle,#fffdf6 0,#ffe9c6c8 3%,#ffd9a860 8%,transparent 16%),repeating-conic-gradient(from 2deg,#ffe8c400 0deg,#ffd9a6ee 1.4deg,#ffe8c400 3.4deg,#ffe8c400 7deg,#ffd59cb8 8.2deg,#ffe8c400 10deg,#ffe8c400 13deg);
 -webkit-mask:radial-gradient(circle,#000 4%,#000c 14%,#0005 27%,transparent 46%);mask:radial-gradient(circle,#000 4%,#000c 14%,#0005 27%,transparent 46%)}

#flash{position:fixed;inset:0;margin:0 auto;max-width:460px;background:#fffdf9;opacity:0;pointer-events:none;z-index:15;will-change:opacity}
.spk{position:absolute;width:14px;height:14px;margin:-7px 0 0 -7px;opacity:0;pointer-events:none;will-change:transform,opacity;background:radial-gradient(circle,#fff 0,#fff 18%,transparent 60%)}
.spk:before,.spk:after{content:'';position:absolute;left:50%;top:50%;background:linear-gradient(90deg,transparent,#fff,transparent);transform:translate(-50%,-50%)}
.spk:before{width:14px;height:1.6px}.spk:after{width:1.6px;height:14px;background:linear-gradient(transparent,#fff,transparent)}
.hint{position:absolute;left:0;right:0;bottom:3%;text-align:center;font:500 10.5px var(--bd);letter-spacing:.36em;text-transform:uppercase;color:#8d869a;z-index:6;animation:breathe 2.6s ease-in-out infinite}
@keyframes breathe{50%{opacity:.4}}
#env.go .hint{opacity:0;animation:none;transition:opacity .3s}
.forn{position:absolute;left:0;right:0;top:3.2%;text-align:center;font:400 22px var(--sc);color:#7d7590;display:none;z-index:6}
.named .forn{display:block}
#env.go .forn{opacity:0;transition:opacity .6s}
/* ---------- hero (arch card) ---------- */
.sec{position:relative;min-height:100vh;min-height:100svh;overflow:hidden}
.hero .sky{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 50%}
.hero .couple{position:absolute;left:13%;right:13%;bottom:0;height:56%;background:url(@@A@@couple.jpg) 50% 100%/cover no-repeat;-webkit-mask:linear-gradient(transparent,#000 42%);mask:linear-gradient(transparent,#000 42%);filter:saturate(.55) brightness(1.1) contrast(.9) sepia(.12)}
.hero .arch{z-index:2}
.hero .txt{position:absolute;left:22%;right:22%;top:17%;z-index:3;text-align:center;color:var(--deep)}
.k1{font:400 15px var(--bd);font-style:italic;letter-spacing:.04em;color:#7a6152}
.k2{font:400 31px/1.15 var(--sc2);color:#6b5040;margin-top:2px}
.k3{font:italic 400 16px var(--bd);color:#6d6478;margin:6px 0 2px}
.k3:before,.k3:after{content:'';display:inline-block;width:42px;height:1px;background:#b9a97a;vertical-align:middle;margin:0 10px}
.nm{font:400 56px/1 var(--sc2);color:#5a3e2e;margin-top:6px}
.nm span{display:block}.nm .a2{margin-left:30%;margin-top:-4px}
.nm .amp{font-size:.6em;margin-right:6px}
.dear0{display:none;font:400 21px/1.3 var(--sc);color:#8a6a55;margin-bottom:8px}.named .dear0{display:block}
.hd{margin-top:18px;font:500 12px/1.7 var(--bd);letter-spacing:.2em;text-transform:uppercase;color:#6d5a4c}.hd span{display:block;font:italic 400 14px var(--bd);letter-spacing:.02em;text-transform:none;color:#8a7262}
.cue{position:absolute;left:0;right:0;bottom:7%;z-index:4;text-align:center;font:400 26px var(--sc2);color:#7a5c48;text-shadow:0 1px 8px #fff8}
.cue:after{content:'';display:block;width:12px;height:12px;margin:2px auto 0;border-right:1.4px solid #7a5c48;border-bottom:1.4px solid #7a5c48;transform:rotate(45deg);animation:bob 1.8s ease-in-out infinite}
@keyframes bob{50%{transform:translateY(5px) rotate(45deg)}}
.rv{opacity:0;transform:translate3d(0,12px,0);transition:opacity 1.2s cubic-bezier(.2,.6,.2,1),transform 1.4s cubic-bezier(.16,.7,.2,1);transition-delay:var(--d,0s)}
.in .rv{opacity:1;transform:none}
/* ---------- details page ---------- */
.det{display:flex;align-items:center;justify-content:center;background:url(@@A@@details.webp) center/cover}
.det .win{background:#fffaf6b8;border-radius:18px;padding:26px 18px;box-shadow:0 10px 40px #8a6a5522;-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px)}
.det .win{width:74%;display:flex;flex-direction:column;align-items:center;text-align:center;transform-origin:50% 50%}
.dear{display:none;font:400 27px/1.2 var(--sc);color:#8a6a55;margin-bottom:10px;overflow-wrap:anywhere}
.named .dear{display:block}
.cap{font:500 11px var(--bd);letter-spacing:.32em;text-transform:uppercase;color:#9a8270}
.names1{font:400 46px/1.15 var(--sc2);color:var(--deep);white-space:nowrap;margin:6px 0 2px}
.names1 i{font:italic 400 22px var(--bd);color:#8a8196}
.inv{font:italic 400 16px/1.45 var(--bd);max-width:26ch;margin:2px auto 0}
.rule{width:120px;height:14px;margin:12px auto;color:#a99772}
.evg{display:grid;gap:14px;width:100%}
.evg.n2{grid-template-columns:1fr 1fr}
.ec{display:flex;flex-direction:column;align-items:center}
.evg.n2 .ec+.ec{border-left:1px solid #c4bccf}
.ec .cap{font-size:10.5px;margin-bottom:5px;color:#a2916a}
.ec .d1{font:500 15px/1.3 var(--bd);color:var(--deep)}
.ec .bs{font:italic 400 13.5px var(--bd);color:#8a8196;margin-top:1px}
.ec .tm{font:500 14.5px var(--bd);color:var(--deep);margin-top:5px}
.ec .vn{font:600 13px/1.3 var(--bd);color:#675d74;margin-top:2px;max-width:16ch}
.ec .lk{display:inline-flex;align-items:center;gap:5px;margin-top:8px;padding:6px 11px;white-space:nowrap;border:1px solid #a99c79aa;border-radius:30px;font:500 9.5px var(--bd);letter-spacing:.14em;text-transform:uppercase;color:var(--deep);text-decoration:none;background:#ffffff70}
.cds{display:flex;justify-content:center;margin-top:16px}
.cds div{padding:0 11px;border-left:1px solid #c4bccf}.cds div:first-child{border-left:0}
.cds b{display:block;font:400 22px/1 var(--bd);color:var(--deep)}
.cds span{display:block;margin-top:3px;font:500 8.5px var(--bd);letter-spacing:.2em;text-transform:uppercase;color:#8a8196}
.acts{display:flex;flex-direction:column;align-items:center;gap:10px;margin-top:16px}
.rbtn{padding:12px 34px;border:0;border-radius:40px;background:#6b4c3a;color:#fbf6f1;font:600 11px var(--bd);letter-spacing:.32em;text-transform:uppercase;cursor:pointer;box-shadow:0 6px 16px #4a3f5744}
.wa{display:inline-flex;align-items:center;gap:8px;font:500 10px var(--bd);letter-spacing:.22em;text-transform:uppercase;color:#6e6580;text-decoration:none;border-bottom:1px solid #a89fb566;padding-bottom:3px}
.bless{font:italic 400 14px/1.4 var(--bd);color:#6e6580;margin-top:14px;max-width:28ch}
/* rsvp modal */
#rmodal{position:fixed;inset:0;z-index:40;display:flex;align-items:center;justify-content:center;background:#2a243388;-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);opacity:0;visibility:hidden;transition:opacity .35s,visibility 0s .35s}
#rmodal.on{opacity:1;visibility:visible;transition:opacity .35s}
#rmodal .panel{position:relative;width:min(92%,410px);max-height:92vh;overflow:auto;padding:30px 24px 24px;border-radius:18px;background:#5e4234;color:#efeaf4;text-align:center;box-shadow:0 20px 50px #0008;transform:translateY(20px) scale(.98);transition:transform .45s cubic-bezier(.2,.7,.2,1)}
#rmodal.on .panel{transform:none}
#rmodal .x{position:absolute;top:10px;right:12px;width:34px;height:34px;border:0;background:none;color:#efeaf4;font-size:26px;line-height:1;cursor:pointer}
#rmodal .scr{font:400 42px var(--sc2);color:#f4f0f8}
#rmodal .txt{font:italic 400 16px var(--bd);margin-top:4px}
form{width:100%;margin-top:18px;text-align:left}
.f{margin-bottom:20px}
.f .l{display:block;font:500 10.5px var(--bd);letter-spacing:.28em;text-transform:uppercase;color:#cfc6db;margin-bottom:10px}
.f input[type=text],.f select{width:100%;padding:10px 2px;border:0;border-bottom:1px solid #cfc6db88;background:transparent;color:#f7f4fa;font:400 20px var(--bd);outline:none;border-radius:0;-webkit-appearance:none;appearance:none}
.f select option{color:#2a2433}
.pills{display:flex;gap:10px}.pills label{flex:1;position:relative}
.pills input{position:absolute;opacity:0;pointer-events:none}
.pills span{display:block;text-align:center;padding:12px 6px;border:1px solid #cfc6db77;border-radius:40px;font:italic 400 17px var(--bd);color:#efeaf4;cursor:pointer;transition:all .35s}
.pills input:checked+span{background:#fbf3ec;color:#5e4234;border-color:#f4f0f8}
.send{display:block;width:100%;margin-top:6px;padding:16px;border:0;border-radius:40px;background:#fbf3ec;color:#5e4234;font:600 11.5px var(--bd);letter-spacing:.3em;text-transform:uppercase;cursor:pointer}
.send:disabled{opacity:.55}
.msg{margin-top:14px;text-align:center;font:italic 400 17px var(--bd);color:#e7e0ee;min-height:1.4em}
#mute{position:fixed;top:14px;z-index:30;right:max(14px,calc(50% - 216px));width:38px;height:38px;border-radius:50%;border:1px solid #b9b0c6;background:#f6f4f9cc;color:var(--deep);font-size:15px;display:none;align-items:center;justify-content:center;cursor:pointer}
body.rd #mute.on{display:flex}
@media (prefers-reduced-motion:reduce){.rv{transition:none!important;transform:none!important;opacity:1!important}}
@@NECSS@@

body.rd{overflow:hidden}
.hero{height:100vh;height:100svh}
.hero .txt{position:absolute;left:24%;right:24%;top:13%;z-index:3;text-align:center;transform-origin:50% 0}
.k1{font-size:14px}.k2{font-size:27px}.k3{font-size:14px;margin:3px 0 0}.nm{font-size:44px;margin-top:4px}
.info{position:absolute;left:11%;right:11%;top:47%;z-index:3;display:flex;flex-direction:column;align-items:center;text-align:center;transform-origin:50% 0;
 background:radial-gradient(ellipse at 50% 45%,#fff9f2d9 0,#fff9f2b0 55%,#fff9f200 78%);padding:12px 4px 18px}
.info .ec .cap{color:#9a7a5e}.info .evg.n2 .ec+.ec{border-left-color:#c9b3a2}
.info .ec .lk{background:#fffaf5cc;border-color:#b79a7c}
.info .cds{margin-top:12px}.info .cds div{border-left-color:#c9b3a2}
.info .acts{margin-top:12px}
"""
NECSS = "*{letter-spacing:0!important;text-transform:none!important}.nm{font-size:46px;line-height:1.3}.k2{font-size:26px}.names1{font-size:40px;line-height:1.35}.dear{line-height:1.4}"

RULE = '<svg class="rule" viewBox="0 0 120 14"><g fill="none" stroke="currentColor" stroke-width=".8"><path d="M0 7H48M72 7H120"/><path d="M60 1.5l5.5 5.5-5.5 5.5-5.5-5.5z"/><circle cx="52" cy="7" r="1.4"/><circle cx="68" cy="7" r="1.4"/></g></svg>'

def build(page, lang, asset_prefix='../assets2/', preview_fonts=None):
    P, T = PAGES[page], S[lang]
    evs = [dict(k=k, label=EV[k]['label'][lang], date=EV[k]['date'], bs=EV[k]['bs'][lang], time=EV[k]['time'][lang], venue=EV[k]['venue'][lang], map=EV[k]['map']) for k in P['ev']]
    url = SITE + ('/ne/' if lang == 'ne' else '/') + page + '/'
    title = P['title'][lang] + ' — ' + T['groom'] + (' र ' if lang == 'ne' else ' & ') + T['bride']
    cfg = dict(lang=lang, ev=evs, T={'g0': T['groom'], 'b0': T['bride'], **{k: T[k] for k in ['months', 'wd', 'units', 'viewloc', 'sending', 'ok', 'err', 'wamsg', 'need', 'dear', 'yesw', 'now', 'gw', 'rsvpw', 'sending2', 'ok2', 'send2']}}, wa=WA)
    rows = ''
    for e in evs:
        rows += ('<div class="f"><span class="l">' + esc(T['attend'].replace('{e}', e['label'])) + '</span><div class="pills">'
                 '<label><input type="radio" name="attend-' + e['k'] + '" value="yes"><span>' + esc(T['yes']) + '</span></label>'
                 '<label><input type="radio" name="attend-' + e['k'] + '" value="no"><span>' + esc(T['no']) + '</span></label></div></div>')
    dig = str.maketrans('0123456789', '०१२३४५६७८९')
    opts = ''.join('<option value="%d">%s</option>' % (i, str(i) if lang == 'en' else str(i).translate(dig)) for i in range(1, 11))
    form = ('<form id="rf" novalidate>'
            '<div class="f"><label class="l" for="rn">' + esc(T['yname']) + '</label><input type="text" id="rn" name="name" required maxlength="80" autocomplete="name"></div>'
            + rows +
            '<div class="f"><label class="l" for="rg">' + esc(T['guests']) + '</label><select id="rg" name="guests">' + opts + '</select></div>'
            '<button class="send" type="submit">' + esc(T['send']) + '</button><div class="msg" id="rmsg"></div></form>')
    sc = "'Great Vibes','Tiro Devanagari Hindi','Noto Serif Devanagari',cursive" if lang == 'ne' else "'Great Vibes',cursive"
    sc2 = "'Pinyon Script','Great Vibes','Tiro Devanagari Hindi','Noto Serif Devanagari',cursive" if lang == 'ne' else "'Pinyon Script','Great Vibes',cursive"
    bd = "'Cormorant Garamond','Noto Serif Devanagari',serif" if lang == 'ne' else "'Cormorant Garamond',Georgia,serif"
    A = asset_prefix
    css = CSS.replace('@@A@@', A).replace('@@SCRIPT@@', sc).replace('@@SCRIPT2@@', sc2).replace('@@BODY@@', bd).replace('@@NECSS@@', NECSS if lang == 'ne' else '')
    pf = ''
    if preview_fonts:
        F = preview_fonts
        pf = "<style>" + ''.join("@font-face{font-family:'%s';font-weight:%s;font-style:%s;src:url(%s%s)}" % (fam, w, st, F, path) for fam, w, st, path in [
            ('Great Vibes', 400, 'normal', 'great-vibes/files/great-vibes-latin-400-normal.woff2'),
            ('Pinyon Script', 400, 'normal', 'pinyon-script/files/pinyon-script-latin-400-normal.woff2'),
            ('Cormorant Garamond', 400, 'normal', 'cormorant-garamond/files/cormorant-garamond-latin-400-normal.woff2'),
            ('Cormorant Garamond', 500, 'normal', 'cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2'),
            ('Cormorant Garamond', 600, 'normal', 'cormorant-garamond/files/cormorant-garamond-latin-600-normal.woff2'),
            ('Cormorant Garamond', 400, 'italic', 'cormorant-garamond/files/cormorant-garamond-latin-400-italic.woff2'),
            ('Cormorant Garamond', 500, 'italic', 'cormorant-garamond/files/cormorant-garamond-latin-500-italic.woff2')]) + "</style>"
    ogimg = SITE + ('/ne/' if lang == 'ne' else '/') + page + '/og.jpg'
    k1, k2, k3 = HERO[page][lang]
    amp = T['amp']
    html = f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title><meta name="description" content="{esc(P['desc'][lang])}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(P['desc'][lang])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{ogimg}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#efecee">
<link rel="preload" as="image" href="{A}env-closed.webp"><link rel="preload" as="image" href="{A}env-open.webp"><link rel="preload" as="image" href="{A}card.webp">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="{FONTS[lang]}" rel="stylesheet">
<style>{css}</style>{pf}</head><body>
<button id="mute" type="button" aria-label="{esc(T['mute'])}">♪</button>
{'<audio id="bgm" src="' + A + '../music.mp3" loop preload="auto"></audio>' if HAS_MUSIC else ''}
<div id="env" role="button" aria-label="{esc(T['hint'])}"><div class="stage" id="stg">
 <img class="lay" id="eOpen" src="{A}env-open.webp" alt="">
 <img class="lay" id="eClosed" src="{A}env-closed-ns.webp" alt="">
 <div id="flap3"><img class="lay" src="{A}env-closed-ns.webp" alt=""><div id="fsh"></div></div>
 <img class="lay" id="seal3" src="{A}seal-cut.webp" alt="">
 <div id="waves"><div class="wv" style="--x:50%;--y:17%"></div><div class="wv" style="--x:50%;--y:80%"></div><div class="wv" style="--x:9%;--y:47%"></div><div class="wv" style="--x:91%;--y:47%"></div></div>
 <div id="spks"></div>
 <div id="rays"></div>
</div><div class="forn" id="forn"></div><div class="hint">{esc(T['hint'])}</div><b id="tagn" hidden></b></div>
<div id="flash"></div>
<div id="app">
 <section class="sec hero" id="hero">
  <img class="sky" src="{A}card.webp" alt="">
  <div class="txt" id="top"><div class="dear0 rv" style="--d:0s" id="dear0"></div><div class="k1 rv" style="--d:.15s">{esc(k1)}</div><div class="k2 rv" style="--d:.3s">{esc(k2)}</div>{('<div class="k3 rv" style="--d:.45s">' + esc(k3) + '</div>') if k3 else ''}
   <div class="nm rv" style="--d:.6s"><span class="gN">{esc(T['groom'])}</span><span class="a2"><span class="amp" style="display:inline">{esc(amp)}</span><span class="bN">{esc(T['bride'])}</span></span></div></div>
  <div class="info" id="win">
   <div class="evg rv" style="--d:.85s" id="evs"></div>
   <div class="cds rv" style="--d:1s" id="cd"></div>
   <div class="acts rv" style="--d:1.15s"><button type="button" class="rbtn" id="ropen">{esc(T['rsvp'])}</button></div>
   <a class="wa" id="wa" href="https://wa.me/{WA}" rel="noopener" hidden></a>
   <div id="dearn" hidden></div>
  </div>
 </section>
</div>
<div id="rmodal" aria-hidden="true"><div class="panel" role="dialog" aria-label="{esc(T['rsvp'])}"><button type="button" class="x" id="rclose" aria-label="Close">×</button>
 <div class="scr">{esc(T['rsvp'])}</div><p class="txt">{esc(T['rsvpsub'])}</p>{form}</div></div>
<script>var C={json.dumps(cfg, ensure_ascii=False)};</script>
<script>{JS}</script>
</body></html>"""
    return html

JS = open(os.path.join(SRC, 'core_js.js'), encoding='utf-8').read().replace("(function(){", "(function(){", 1) + r"""
(function(){var gn=(q.get('gn')||'').trim().slice(0,30),bn=(q.get('bn')||'').trim().slice(0,30);
 if(gn)[].forEach.call(document.querySelectorAll('.gN'),function(e){e.textContent=gn});if(bn)[].forEach.call(document.querySelectorAll('.bN'),function(e){e.textContent=bn});
 if(gn||bn){var t1=document.title.split(' — ');document.title=t1[0]+' — '+(gn||C.T.g0)+(NE?' र ':' & ')+(bn||C.T.b0)}
 var dov=function(){C.ev.forEach(function(e){var d=(q.get(e.k+'d')||'').trim(),bs=(q.get(e.k+'b')||'').trim().slice(0,40);if(/^\d{4}-\d{2}-\d{2}$/.test(d))e.date=d;if(bs)e.bs=bs})};dov();var _u=urlOv;urlOv=function(){_u();dov()};BASE=JSON.parse(JSON.stringify(C.ev));if(typeof tgt!=='undefined')tgt=D(C.ev[0])})();
if(g){var fo=$('forn');if(fo)fo.textContent=(NE?g+' का लागि':'For '+g);var d0=$('dear0');if(d0)d0.textContent=T.dear+' '+g}
function heroDates(){var h=$('hd');if(!h)return;h.innerHTML=C.ev.map(function(e){var d=D(e);return '<div>'+esc(e.label)+' · '+dv(d.getDate())+' '+T.months[d.getMonth()]+'<span>'+esc(e.bs)+(e.time?' · '+esc(e.time):'')+'</span></div>'}).join('')}heroDates();var _r=render;render=function(){_r();heroDates()};render();tick();
/* reveal on scroll */
var secs=document.querySelectorAll('.sec');
window.fitWin=function(){var w=$('win'),t=$('top');if(!w)return;var vw=Math.min(innerWidth,460),vh=innerHeight;w.style.transform='none';t.style.transform='none';var kt=Math.min(1,vh*.31/t.offsetHeight,vw*.52/t.offsetWidth);t.style.transform='scale('+kt.toFixed(3)+')';var top=vh*.13+t.offsetHeight*kt+vh*.02;w.style.top=top+'px';var k=Math.min(1,(vh*.95-top)/w.offsetHeight,vw*.78/w.offsetWidth);w.style.transform='scale('+k.toFixed(3)+')'};fitWin();addEventListener('resize',fitWin);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fitWin);
var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');if(e.target.id==='det'&&window.fitWin)fitWin();io.unobserve(e.target)}})},{threshold:.25}):null;
/* sparkles over the florals */
var spks=$('spks'),SP=[];var zones=[[.1,.3,.7,.08],[.9,.3,.7,.08],[.5,.68,.95,.6],[.5,.08,.4,.6]];
for(var i=0;i<34;i++){var z=zones[i%4],x=z[0]+(Math.random()-.5)*z[3],y=z[1]+Math.random()*(z[2]-z[1]);var d=document.createElement('i');d.className='spk';d.style.left=(x*100).toFixed(1)+'%';d.style.top=(y*100).toFixed(1)+'%';spks.appendChild(d);SP.push(d)}
/* opening */
var env=$('env'),opened=false,ready=false,want=null;
function an(el,kf,o){return el&&el.animate?el.animate(kf,Object.assign({fill:'both'},o)):null}
function open(user){if(opened)return;if(!ready){want=user;return}opened=true;env.classList.add('go');if(user){whoosh();startMusic()}
 var cl=$('eClosed'),sh=$('eShine'),fl=$('flap3'),se=$('seal3'),rays=$('rays'),flash=$('flash'),hero=$('hero'),stg=$('stg');
 if(!env.animate){finish();return}
 // 1. seal press
 an(se,[{transform:'scale(1)'},{transform:'scale(.97)',offset:.35},{transform:'scale(1)'}],{duration:500,easing:'ease-out',fill:'none'});
 // 2. seal glows, then light blooms from the centre of each floral cluster and travels outward through the embroidery
 an(se,[{filter:'drop-shadow(0 4px 6px #5a463322) brightness(1)'},{filter:'drop-shadow(0 0 16px #fffaf0) brightness(1.12)',offset:.45},{filter:'drop-shadow(0 4px 6px #5a463322) brightness(1)'}],{duration:1400,delay:150,easing:'ease-in-out',fill:'none'});
 var reg=window.CSS&&CSS.registerProperty!==undefined||(window.CSS&&CSS.supports&&CSS.supports('background:paint(x)'));
 [].forEach.call(document.querySelectorAll('.wv'),function(w,i){var side=i>1,d0=side?950:700,dur=side?2300:2700,R=side?'48vh':'72vh';
  an(w,[{'--r':'0vh'},{'--r':R}],{duration:dur,delay:d0,easing:'cubic-bezier(.35,.1,.3,1)'});
  an(w,[{opacity:0},{opacity:1,offset:.12},{opacity:1,offset:.78},{opacity:0}],{duration:dur,delay:d0,easing:'linear'})});
 SP.forEach(function(s){an(s,[{opacity:0,transform:'scale(.2) rotate(0deg)'},{opacity:1,transform:'scale(1) rotate(45deg)',offset:.4},{opacity:0,transform:'scale(.3) rotate(90deg)'}],{duration:700+Math.random()*500,delay:900+Math.random()*2300,easing:'ease-in-out'})});
 // 3. flap + seal lift on the hinge; envelope reveals its glowing inside
 var T0=3600,E='cubic-bezier(.45,0,.25,1)';
 var DUR=1900,FE='cubic-bezier(.5,0,.3,1)';
 // flap folds up from its top hinge; the seal is locked to the flap tip (same easing, linear relation)
 an(fl,[{transform:'scaleY(1)'},{transform:'scaleY(.364)'}],{duration:DUR,delay:T0,easing:FE});
 an(fl,[{opacity:1},{opacity:1,offset:.75},{opacity:0}],{duration:DUR,delay:T0,easing:'linear'});
 an($('fsh'),[{opacity:0},{opacity:1}],{duration:DUR,delay:T0,easing:FE});
 an(se,[{transform:'translateY(0) scale(1)'},{transform:'translateY(-32%) scale(.96)'}],{duration:DUR,delay:T0,easing:FE,fill:'forwards'});
 an(se,[{opacity:1},{opacity:0}],{duration:450,delay:T0+DUR+150,easing:'ease-in-out'});
 an(cl,[{opacity:1},{opacity:0,offset:.45},{opacity:0}],{duration:DUR,delay:T0,easing:'linear'});
 an(stg,[{transform:'translate(-50%,-50%) scale(1)'},{transform:'translate(-50%,-50%) scale(1.06)'}],{duration:3600,delay:T0,easing:'cubic-bezier(.3,0,.2,1)'});
 // 4. light rays bloom from the opening
 an(rays,[{opacity:0,transform:'translate(-50%,-50%) scale(.5) rotate(0deg)'},{opacity:.85,transform:'translate(-50%,-50%) scale(1) rotate(6deg)',offset:.55},{opacity:1,transform:'translate(-50%,-50%) scale(1.3) rotate(12deg)'}],{duration:2400,delay:T0+1300,easing:'cubic-bezier(.3,0,.2,1)'});
 // 5. white flash -> card
 an(flash,[{opacity:0},{opacity:1}],{duration:650,delay:T0+3100,easing:'ease-in'});
 setTimeout(function(){env.style.display='none';hero.classList.add('in');document.body.classList.add('rd');
   an(hero,[{transform:'scale(1.06)'},{transform:'scale(1)'}],{duration:2600,easing:'cubic-bezier(.2,.7,.2,1)'});
   an(flash,[{opacity:1},{opacity:0}],{duration:1200,easing:'ease-out'});setTimeout(finish,1300)},T0+3800)}
function finish(){document.body.classList.add('rd');env.style.display='none';secs[0].classList.add('in');if(io)for(var i=1;i<secs.length;i++)io.observe(secs[i]);else secs.forEach(function(s){s.classList.add('in')});if(window.fitWin)fitWin()}
env.addEventListener('click',function(){open(true)});
Promise.all([].slice.call(document.querySelectorAll('#env img,#hero img')).map(function(i){return i.decode?i.decode().catch(function(){}):Promise.resolve()})).then(function(){ready=true;if(want!==null)open(want)});
setTimeout(function(){if(!ready){ready=true;if(want!==null)open(want)}},4500);
setTimeout(function(){open(false)},3000);
})();
"""

if __name__ == '__main__':
    args = sys.argv[1:]
    out, pf, only, A = ROOT, None, None, 'REL'
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
            A2 = ('../assets3/' if lang == 'en' else '../../assets3/') if A == 'REL' else A
            open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(build(page, lang, A2, pf))
            print('wrote', os.path.join(d, 'index.html'))
