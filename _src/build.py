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
 'en': "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Great+Vibes&display=swap",
 'ne': "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Great+Vibes&family=Noto+Serif+Devanagari:wght@400;500;600&family=Tiro+Devanagari+Hindi&display=swap",
}

def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

LACE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='46' height='46' viewBox='0 0 46 46'%3E%3Cg fill='none' stroke='%23b88a3a' stroke-width='.9' opacity='.5'%3E%3Ccircle cx='23' cy='23' r='10'/%3E%3Cpath d='M23 7c4 5 4 11 0 16c-4-5-4-11 0-16zM23 39c4-5 4-11 0-16c-4 5-4 11 0 16zM7 23c5-4 11-4 16 0c-5 4-11 4-16 0zM39 23c-5 4-11 4-16 0c5-4 11-4 16 0z'/%3E%3Ccircle cx='0' cy='0' r='6'/%3E%3Ccircle cx='46' cy='0' r='6'/%3E%3Ccircle cx='0' cy='46' r='6'/%3E%3Ccircle cx='46' cy='46' r='6'/%3E%3C/g%3E%3Cg fill='%23b88a3a' opacity='.45'%3E%3Ccircle cx='23' cy='23' r='1.6'/%3E%3Ccircle cx='0' cy='0' r='1.2'/%3E%3Ccircle cx='46' cy='46' r='1.2'/%3E%3C/g%3E%3C/svg%3E\")")

def edge(fill):
    f = fill.replace('#', '%23')
    return ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E"
            "%3Cpath fill='" + f + "' fill-rule='evenodd' d='M0 0H40V18A20 20 0 0 1 0 18Z M20 9a4 4 0 1 0 .01 0Z M8 22a2.2 2.2 0 1 0 .01 0Z M32 22a2.2 2.2 0 1 0 .01 0Z M20 27a2.4 2.4 0 1 0 .01 0Z'/%3E"
            "%3Cpath fill='none' stroke='%23c99b4a' stroke-width='1' d='M0 18A20 20 0 0 0 40 18'/%3E"
            "%3Cpath fill='none' stroke='%23c99b4a' stroke-width='.8' stroke-dasharray='2 2.4' opacity='.8' d='M4 18A16 16 0 0 0 36 18'/%3E%3C/svg%3E\")")

IV, MA = '#f3ead6', '#5e0f1f'

CSS = r"""
:root{--iv:#f3ead6;--mar:#5e0f1f;--gold:#b88a3a;--gold2:#e4c47a;--ink:#3b2a1e;--sc:@@SCRIPT@@;--bd:@@BODY@@}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;background:#2a0a10}
body{background:radial-gradient(ellipse at 50% 20%,#4a0d18,#1c0508 75%) fixed;color:var(--ink);font-family:var(--bd);overflow:hidden;-webkit-font-smoothing:antialiased}
body.rd{overflow-y:auto}
#app{position:relative;max-width:460px;margin:0 auto;background:var(--iv);box-shadow:0 0 60px #0008}
/* sparkles */
#spk{position:fixed;left:0;right:0;top:0;margin:0 auto;width:100%;max-width:460px;height:100%;pointer-events:none;z-index:20}
/* envelope */
#env{position:fixed;left:0;right:0;top:0;bottom:0;margin:0 auto;width:100%;max-width:460px;z-index:10;cursor:pointer;perspective:1400px;overflow:hidden;transition:opacity .9s ease 2.3s,visibility 0s 3.2s}
#env.open{opacity:0;visibility:hidden}
.pc{position:absolute;inset:0;transition:transform 1s cubic-bezier(.55,0,.25,1) 1.35s}
.pc .sh{position:absolute;inset:0;filter:drop-shadow(0 0 7px #2a0a1088)}
.fc{position:absolute;inset:0;background:@@LACE@@,linear-gradient(160deg,#f8f1e1,#e9dabb)}
.pc.l .fc{clip-path:polygon(0 0,50% 50%,0 100%);filter:brightness(.985)}
.pc.r .fc{clip-path:polygon(100% 0,100% 100%,50% 50%);filter:brightness(.965)}
.pc.b .fc{clip-path:polygon(0 100%,50% 50%,100% 100%);filter:brightness(.94)}
.st{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
#flap{position:absolute;inset:0;transform-origin:50% 0;transform-style:preserve-3d;transition:transform 1.2s cubic-bezier(.5,0,.2,1) .35s;z-index:3}
#flap .ff,#flap .fb,#flap .st{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden}
#flap .ff,#flap .fb{clip-path:polygon(0 0,100% 0,50% 50%)}
#flap .fb{transform:rotateX(180deg);background:@@LACE@@,linear-gradient(#7a1626,#4d0b17)}
.seal{position:absolute;left:50%;top:50%;width:112px;height:112px;margin:-56px 0 0 -56px;backface-visibility:hidden;-webkit-backface-visibility:hidden;transform:translateZ(2px);transition:transform .55s ease-in,opacity .5s ease .1s;filter:drop-shadow(0 5px 5px #0007)}
.seal.h1{clip-path:polygon(0 0,58% 0,44% 22%,56% 40%,42% 62%,55% 80%,46% 100%,0 100%)}
.seal.h2{clip-path:polygon(58% 0,100% 0,100% 100%,46% 100%,55% 80%,42% 62%,56% 40%,44% 22%)}
#env.open .seal.h1{transform:translateZ(2px) translate(-34px,18px) rotate(-24deg);opacity:0}
#env.open .seal.h2{transform:translateZ(2px) translate(34px,26px) rotate(22deg);opacity:0}
#env.open #flap{transform:rotateX(-178deg)}
#env.open .pc.l{transform:translateX(-102%)}
#env.open .pc.r{transform:translateX(102%)}
#env.open .pc.b{transform:translateY(102%)}
.tag{display:none;position:absolute;left:50%;bottom:9%;transform:translateX(-50%);min-width:60%;max-width:84%;padding:13px 18px 12px;text-align:center;background:linear-gradient(#fbf5e6,#efe2c4);border:1px solid #b88a3a;box-shadow:0 0 0 3px #f4ead2,0 0 0 4px #b88a3a88,0 6px 12px #0006;border-radius:3px;color:var(--ink)}
.tag:before{content:'';position:absolute;left:50%;top:-9px;width:11px;height:11px;margin-left:-5.5px;border-radius:50%;background:radial-gradient(#e4c47a,#a6762c);box-shadow:0 1px 2px #0006}
.tag small{display:block;font:500 11px var(--bd);letter-spacing:.3em;text-transform:uppercase;color:#8a6420}
.tag b{display:block;font:400 26px/1.15 var(--sc);color:#6e1523;overflow-wrap:anywhere}
.named .tag{display:block}
.hint{position:absolute;left:0;right:0;bottom:3.4%;text-align:center;font:600 12px var(--bd);letter-spacing:.3em;text-transform:uppercase;color:#7a5a24;z-index:6;transition:opacity .3s;animation:pulse 2.4s ease-in-out infinite}
.named .hint{bottom:2.2%}
#env.open .hint{opacity:0}
@keyframes pulse{50%{opacity:.45}}
/* sections */
.sec{position:relative;min-height:100vh;min-height:100dvh;padding:76px 10% 64px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;overflow:hidden}
.sec>*{position:relative;z-index:1}
.sec:before{content:'';position:absolute;inset:-5%;background:@@LACE@@;opacity:.5;transform:scale(1.1);transition:transform 3s cubic-bezier(.2,.6,.2,1);z-index:0}
.sec.in:before{transform:scale(1)}
.iv{background:var(--iv);color:var(--ink)}
.ma{background:var(--mar);color:#f2e3c4}
.ma:before{opacity:.28}
.edge{position:absolute!important;left:0;right:0;top:-1px;height:40px;background-repeat:repeat-x;background-size:40px 40px;z-index:3!important;transform:translateY(-34px);transition:transform 1.3s cubic-bezier(.2,.7,.2,1)}
.iv .edge{background-image:@@EDGE_MA@@}
.ma .edge{background-image:@@EDGE_IV@@}
.sec.in .edge{transform:none}
.rv{opacity:0;transform:translateY(26px) scale(.97);transition:opacity 1.1s ease,transform 1.6s cubic-bezier(.2,.7,.2,1);transition-delay:var(--d,0s)}
.in .rv{opacity:1;transform:none}
.cap{font:600 12.5px var(--bd);letter-spacing:.32em;text-transform:uppercase;color:#8a6420}
.ma .cap{color:var(--gold2)}
.scr{font:400 52px/1.08 var(--sc);color:#6e1523}
.ma .scr{background:linear-gradient(#f6e0a4,#d3a756 55%,#f1d58b);-webkit-background-clip:text;background-clip:text;color:transparent}
.orn{width:150px;height:18px;margin:16px auto}
.txt{font:500 18px/1.5 var(--bd);font-style:italic;max-width:30ch;margin:0 auto}
/* hero */
.frame{position:absolute!important;inset:16px;border:1px solid #b88a3a99;border-radius:4px;pointer-events:none}
.frame:after{content:'';position:absolute;inset:6px;border:2px double #b88a3a55;border-radius:2px}
.cor{position:absolute!important;width:54px;height:54px;pointer-events:none}
.cor.a{left:10px;top:10px}.cor.b{right:10px;top:10px;transform:scaleX(-1)}.cor.c{left:10px;bottom:10px;transform:scaleY(-1)}.cor.d{right:10px;bottom:10px;transform:scale(-1)}
.dear{display:none;font:400 30px/1.2 var(--sc);color:#8a5a1c;margin-bottom:14px;overflow-wrap:anywhere}
.named .dear{display:block}
.names{font:400 64px/1 var(--sc);color:#6e1523;margin:18px 0 6px}
.names i{display:block;font:500 22px var(--bd);font-style:normal;color:var(--gold);margin:6px 0}
.full{font:500 11px var(--bd);letter-spacing:.24em;text-transform:uppercase;color:#7a6650}
.dates{margin-top:22px;display:flex;flex-direction:column;gap:6px;font:600 15px var(--bd);letter-spacing:.12em;text-transform:uppercase;color:#6e1523}
.dates span{font-weight:500;letter-spacing:.04em;text-transform:none;color:#6a5440;font-style:italic}
.scrollcue{margin-top:34px;font:500 11px var(--bd);letter-spacing:.3em;text-transform:uppercase;color:#8a6420;animation:pulse 2.4s infinite}
.scrollcue:after{content:'';display:block;width:1px;height:28px;margin:8px auto 0;background:linear-gradient(#b88a3a,transparent)}
/* photo */
.arch{width:76%;max-width:300px;aspect-ratio:600/656;margin:22px auto 6px;border-radius:999px 999px 10px 10px;padding:6px;background:linear-gradient(150deg,#f6e0a4,#b88a3a 45%,#f1d58b 70%,#8d6420);box-shadow:0 14px 30px #0007;outline:1.5px dashed #e4c47a88;outline-offset:9px}
.arch img{display:block;width:100%;height:100%;object-fit:cover;border-radius:999px 999px 6px 6px;border:2px solid #f6ead0}
/* countdown */
.cd{display:flex;gap:9px;margin-top:24px}
.cd div{width:70px;padding:15px 0 11px;border:1px solid #b88a3a99;border-radius:10px;background:#fffaf080;box-shadow:inset 0 0 0 3px #f3ead6,inset 0 0 0 4px #b88a3a33}
.cd b{display:block;font:500 34px/1 var(--bd);color:#6e1523}
.cd span{display:block;margin-top:6px;font:600 10px var(--bd);letter-spacing:.18em;text-transform:uppercase;color:#8a6420}
.cdt{margin-top:14px;font:italic 500 16px var(--bd);color:#6a5440}
/* events */
.evs{display:flex;flex-direction:column;gap:16px;width:100%;margin-top:22px}
.ev{padding:22px 16px 20px;border:1px solid #e4c47a66;border-radius:14px;background:#ffffff08;box-shadow:inset 0 0 0 4px #5e0f1f,inset 0 0 0 5px #e4c47a33}
.ev .cap{margin-bottom:6px}
.ev .dn{font:500 62px/1 var(--bd);background:linear-gradient(#f6e0a4,#d3a756 55%,#f1d58b);-webkit-background-clip:text;background-clip:text;color:transparent}
.ev .mo{font:600 14px var(--bd);letter-spacing:.2em;text-transform:uppercase;margin-top:4px}
.ev .wd{font:500 15px var(--bd);letter-spacing:.1em;margin-top:2px;opacity:.85}
.ev .bs{font:italic 500 15px var(--bd);margin-top:4px;color:var(--gold2)}
.ev .tv{font:500 16px var(--bd);margin-top:10px}
/* location */
.loc{width:100%;margin-top:20px;display:flex;flex-direction:column;gap:14px}
.loc .lc{padding:18px 14px;border-top:1px solid #b88a3a55}
.loc .lc:first-child{border-top:0}
.loc .vn{font:500 19px var(--bd);margin-top:4px}
.loc .dt{font:italic 500 15px var(--bd);color:#6a5440;margin-top:2px}
.btn{display:inline-block;margin-top:12px;padding:12px 24px;border:1px solid #b88a3a;border-radius:30px;background:linear-gradient(#fffaf0,#f2e4c6);font:600 13px var(--bd);letter-spacing:.14em;text-transform:uppercase;color:#6e1523;text-decoration:none;box-shadow:0 4px 10px #b88a3a33}
/* rsvp */
form{width:100%;margin-top:20px;text-align:left}
.f{margin-bottom:16px}
.f label.l{display:block;font:600 12px var(--bd);letter-spacing:.18em;text-transform:uppercase;color:var(--gold2);margin-bottom:7px}
.f input[type=text],.f select{width:100%;padding:13px 14px;border:1px solid #e4c47a77;border-radius:10px;background:#ffffff12;color:#f6ead0;font:500 18px var(--bd);outline:none}
.f select option{color:#3b2a1e}
.f input::placeholder{color:#f2e3c477}
.pills{display:flex;gap:8px}
.pills label{flex:1;position:relative}
.pills input{position:absolute;opacity:0}
.pills span{display:block;text-align:center;padding:12px 6px;border:1px solid #e4c47a77;border-radius:10px;font:500 16px var(--bd);color:#f2e3c4;cursor:pointer;transition:background .2s,color .2s}
.pills input:checked+span{background:linear-gradient(#f1d58b,#c79a45);color:#4d0b17;border-color:#f1d58b}
.send{width:100%;margin-top:6px;padding:15px;border:0;border-radius:30px;background:linear-gradient(#f6e0a4,#c79a45);color:#4d0b17;font:700 14px var(--bd);letter-spacing:.2em;text-transform:uppercase;cursor:pointer;box-shadow:0 6px 16px #0006}
.send:disabled{opacity:.6}
.msg{margin-top:12px;text-align:center;font:italic 500 16px var(--bd);color:var(--gold2);min-height:1.4em}
.wa{display:inline-flex;align-items:center;gap:8px;margin-top:18px;padding:11px 20px;border:1px solid #e4c47a88;border-radius:30px;color:#f2e3c4;text-decoration:none;font:600 13px var(--bd);letter-spacing:.1em}
.hp{display:none}
/* thanks */
.end .names{font-size:58px}
/* music */
#mute{position:fixed;top:14px;z-index:30;right:max(14px,calc(50% - 216px));width:40px;height:40px;border-radius:50%;border:1px solid #b88a3a;background:#fffaf0dd;color:#6e1523;font-size:17px;display:none;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 3px 10px #0004}
body.rd #mute.on{display:flex}
@media (prefers-reduced-motion:reduce){.rv,.sec:before,.edge{transition:none!important;transform:none!important;opacity:1!important}}
@@NECSS@@
"""

NECSS = "*{letter-spacing:0!important;text-transform:none!important}.scr,.names,.dear,.tag b{line-height:1.35}.names{font-size:54px}.scr{font-size:44px}"

CORNER = '<svg class="cor @@C@@" viewBox="0 0 54 54"><g fill="none" stroke="#b88a3a" stroke-width="1.1" stroke-linecap="round"><path d="M4 50V14C4 8 8 4 14 4H50"/><path d="M10 50V18c0-5 3-8 8-8H50" opacity=".55"/><path d="M14 14c6-1 10 2 9 7c-1 4-6 4-7 1c-1-2 1-4 3-3"/><circle cx="24" cy="24" r="1.6" fill="#b88a3a"/></g></svg>'
ORN = '<svg class="orn rv" style="--d:@@D@@s" viewBox="0 0 150 18"><g fill="none" stroke="#b88a3a" stroke-width="1"><path d="M0 9H58M92 9H150"/><path d="M75 2l7 7-7 7-7-7z"/><circle cx="62" cy="9" r="2"/><circle cx="88" cy="9" r="2"/></g></svg>'

def orn(d):
    return ORN.replace('@@D@@', str(d))

def build(page, lang, preview_fonts=None):
    P, T = PAGES[page], S[lang]
    evs = []
    for k in P['ev']:
        e = EV[k]
        evs.append(dict(k=k, label=e['label'][lang], date=e['date'], bs=e['bs'][lang], time=e['time'][lang], venue=e['venue'][lang], map=e['map']))
    url = SITE + ('/ne/' if lang == 'ne' else '/') + page + '/'
    title = P['title'][lang] + ' — ' + T['groom'] + (' र ' if lang == 'ne' else ' & ') + T['bride']
    cfg = dict(lang=lang, ev=evs, T={k: T[k] for k in ['months', 'wd', 'units', 'viewloc', 'sending', 'ok', 'err', 'wamsg', 'need', 'dear']}, wa=WA)
    # date line for hero
    # RSVP form (static, so Netlify can detect it)
    rows = ''
    for e in evs:
        rows += ('<div class="f"><label class="l">' + esc(T['attend'].replace('{e}', e['label'])) + '</label><div class="pills">'
                 '<label><input type="radio" name="attend-' + e['k'] + '" value="yes"><span>' + esc(T['yes']) + '</span></label>'
                 '<label><input type="radio" name="attend-' + e['k'] + '" value="no"><span>' + esc(T['no']) + '</span></label></div></div>')
    opts = ''.join('<option value="%d">%s</option>' % (i, str(i) if lang == 'en' else str(i).translate(str.maketrans('0123456789', '०१२३४५६७८९'))) for i in range(1, 11))
    form = ('<form name="' + P['form'] + '" method="POST" data-netlify="true" netlify-honeypot="bot" id="rf">'
            '<input type="hidden" name="form-name" value="' + P['form'] + '"><input type="hidden" name="lang" value="' + lang + '">'
            '<p class="hp"><label>Leave empty <input name="bot"></label></p>'
            '<div class="f"><label class="l" for="rn">' + esc(T['yname']) + '</label><input type="text" id="rn" name="name" required maxlength="80" autocomplete="name"></div>'
            + rows +
            '<div class="f"><label class="l" for="rg">' + esc(T['guests']) + '</label><select id="rg" name="guests">' + opts + '</select></div>'
            '<button class="send" type="submit">' + esc(T['send']) + '</button><div class="msg" id="rmsg"></div></form>')
    corners = ''.join(CORNER.replace('@@C@@', c) for c in 'abcd')
    sc = "'Great Vibes','Tiro Devanagari Hindi','Noto Serif Devanagari',cursive" if lang == 'ne' else "'Great Vibes',cursive"
    bd = "'Cormorant Garamond','Noto Serif Devanagari',serif" if lang == 'ne' else "'Cormorant Garamond',Georgia,serif"
    css = (CSS.replace('@@LACE@@', LACE).replace('@@EDGE_MA@@', edge(MA)).replace('@@EDGE_IV@@', edge(IV))
              .replace('@@SCRIPT@@', sc).replace('@@BODY@@', bd).replace('@@NECSS@@', NECSS if lang == 'ne' else ''))
    pf = ''
    if preview_fonts:
        F = preview_fonts
        pf = ("<style>@font-face{font-family:'Great Vibes';src:url(%sgreat-vibes/files/great-vibes-latin-400-normal.woff2)}"
              "@font-face{font-family:'Cormorant Garamond';font-weight:500;src:url(%scormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2)}"
              "@font-face{font-family:'Cormorant Garamond';font-weight:600;src:url(%scormorant-garamond/files/cormorant-garamond-latin-600-normal.woff2)}"
              "@font-face{font-family:'Cormorant Garamond';font-weight:700;src:url(%scormorant-garamond/files/cormorant-garamond-latin-700-normal.woff2)}"
              "@font-face{font-family:'Cormorant Garamond';font-weight:500;font-style:italic;src:url(%scormorant-garamond/files/cormorant-garamond-latin-500-italic.woff2)}</style>") % (F, F, F, F, F)
    ogimg = SITE + ('/ne/' if lang == 'ne' else '/') + page + '/og.jpg'
    html = f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title><meta name="description" content="{esc(P['desc'][lang])}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(P['desc'][lang])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{ogimg}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#5e0f1f">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="{FONTS[lang]}" rel="stylesheet">
<style>{css}</style>{pf}</head><body>
<canvas id="spk"></canvas>
<button id="mute" type="button" aria-label="{esc(T['mute'])}">♪</button>
{'<audio id="bgm" src="/music.mp3" loop preload="auto"></audio>' if HAS_MUSIC else ''}
<div id="env" role="button" aria-label="{esc(T['hint'])}">
 <div class="pc l"><div class="sh"><div class="fc"></div></div><svg class="st" viewBox="0 0 100 100" preserveAspectRatio="none"><polyline points="0,0 50,50 0,100" fill="none" stroke="#b88a3a" stroke-width="1.1" stroke-dasharray="5 4" vector-effect="non-scaling-stroke" opacity=".9"/></svg></div>
 <div class="pc r"><div class="sh"><div class="fc"></div></div><svg class="st" viewBox="0 0 100 100" preserveAspectRatio="none"><polyline points="100,0 50,50 100,100" fill="none" stroke="#b88a3a" stroke-width="1.1" stroke-dasharray="5 4" vector-effect="non-scaling-stroke" opacity=".9"/></svg></div>
 <div class="pc b"><div class="sh"><div class="fc"></div></div><svg class="st" viewBox="0 0 100 100" preserveAspectRatio="none"><polyline points="0,100 50,50 100,100" fill="none" stroke="#b88a3a" stroke-width="1.1" stroke-dasharray="5 4" vector-effect="non-scaling-stroke" opacity=".9"/></svg>
  <div class="tag"><small>{esc(T['dear'])}</small><b id="tagn"></b></div></div>
 <div id="flap"><div class="ff"><div class="fc"></div></div><div class="fb"></div><svg class="st" viewBox="0 0 100 100" preserveAspectRatio="none"><polyline points="0,0 50,50 100,0" fill="none" stroke="#b88a3a" stroke-width="1.1" stroke-dasharray="5 4" vector-effect="non-scaling-stroke" opacity=".9"/></svg>
  <svg class="seal h1" id="s1" viewBox="0 0 100 100"></svg><svg class="seal h2" id="s2" viewBox="0 0 100 100"></svg></div>
 <div class="hint">{esc(T['hint'])}</div>
</div>
<div id="app">
 <section class="sec iv hero" id="hero"><div class="frame"></div>{corners}
  <div class="dear rv" style="--d:.1s" id="dearn"></div>
  <div class="cap rv" style="--d:.25s">{esc(T['together'])}</div>
  <div class="names rv" style="--d:.45s">{esc(T['groom'])}<i>{esc(T['amp'])}</i>{esc(T['bride'])}</div>
  <div class="full rv" style="--d:.6s">{esc(T['full'])}</div>
  {orn(.7)}
  <p class="txt rv" style="--d:.8s">{esc(P['invite'][lang])}</p>
  <div class="dates rv" style="--d:1s" id="hdates"></div>
  <div class="scrollcue rv" style="--d:1.4s">⌄</div>
 </section>
 <section class="sec ma"><div class="edge"></div>
  <div class="cap rv">{esc(T['groom'])}{esc(T['namesep'])}{esc(T['bride'])}</div>
  <div class="arch rv" style="--d:.2s"><img alt="{esc(T['groom'])} {esc(T['amp'])} {esc(T['bride'])}" src="data:image/jpeg;base64,{PHOTO}"></div>
  <div class="scr rv" style="--d:.45s;margin-top:22px">{esc(T['photo'])}</div>
 </section>
 <section class="sec iv"><div class="edge"></div>
  <div class="cap rv">{esc(T['cd'])}</div>
  <div class="scr rv" style="--d:.15s;margin-top:8px" id="cdl"></div>
  <div class="cd rv" style="--d:.3s" id="cd"></div>
  <div class="cdt rv" style="--d:.45s" id="cdt"></div>
 </section>
 <section class="sec ma"><div class="edge"></div>
  <div class="scr rv">{esc(T['day'])}</div>
  {orn(.15)}
  <div class="evs" id="evs"></div>
 </section>
 <section class="sec iv"><div class="edge"></div>
  <div class="scr rv">{esc(T['loc'])}</div>
  {orn(.15)}
  <div class="loc" id="locs"></div>
 </section>
 <section class="sec ma"><div class="edge"></div>
  <div class="scr rv">{esc(T['rsvp'])}</div>
  <p class="txt rv" style="--d:.15s;margin-top:10px">{esc(T['rsvpsub'])}</p>
  <div class="rv" style="--d:.3s;width:100%">{form}</div>
  <a class="wa rv" style="--d:.45s" id="wa" href="https://wa.me/{WA}" rel="noopener"><svg width="18" height="18" viewBox="0 0 24 24" fill="#e4c47a"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>{esc(T['wa'])}</a>
 </section>
 <section class="sec iv end"><div class="edge"></div><div class="frame"></div>{corners}
  <div class="cap rv">{esc(T['thanks'])}</div>
  <div class="names rv" style="--d:.2s">{esc(T['groom'])}<i>{esc(T['amp'])}</i>{esc(T['bride'])}</div>
  {orn(.35)}
  <p class="txt rv" style="--d:.45s">{esc(T['thankmsg'])}</p>
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
if(g){document.body.classList.add('named');$('tagn').textContent=g;$('dearn').textContent=T.dear+' '+g;$('rn').value=g;$('env').classList.add('named')}
function D(e){return new Date(e.date+'T00:00:00')}
/* hero dates */
$('hdates').innerHTML=C.ev.map(function(e){var d=D(e);return '<div>'+esc(e.label)+' · '+dv(d.getDate())+' '+T.months[d.getMonth()]+' '+dv(d.getFullYear())+'<br><span>'+esc(e.bs)+'</span></div>'}).join('');
/* the day */
$('evs').innerHTML=C.ev.map(function(e,i){var d=D(e),tv=[e.time,e.venue].filter(Boolean).join(' · ');return '<div class="ev rv" style="--d:'+(.25+i*.18)+'s"><div class="cap">'+esc(e.label)+'</div><div class="dn">'+dv(d.getDate())+'</div><div class="mo">'+T.months[d.getMonth()]+' '+dv(d.getFullYear())+'</div><div class="wd">'+T.wd[d.getDay()]+'</div><div class="bs">'+esc(e.bs)+'</div>'+(tv?'<div class="tv">'+esc(tv)+'</div>':'')+'</div>'}).join('');
/* location */
$('locs').innerHTML=C.ev.map(function(e,i){var d=D(e);return '<div class="lc rv" style="--d:'+(.25+i*.18)+'s"><div class="cap">'+esc(e.label)+'</div>'+(e.venue?'<div class="vn">'+esc(e.venue)+'</div>':'')+'<div class="dt">'+T.wd[d.getDay()]+', '+dv(d.getDate())+' '+T.months[d.getMonth()]+(e.time?' · '+esc(e.time):'')+'</div>'+(e.map?'<a class="btn" href="'+esc(cm(e.map))+'" rel="noopener">📍 '+esc(T.viewloc)+'</a>':'')+'</div>'}).join('');
/* countdown */
var tgt=D(C.ev[0]);$('cdl').textContent=C.ev[0].label;var dd=tgt;$('cdt').textContent=T.wd[dd.getDay()]+', '+dv(dd.getDate())+' '+T.months[dd.getMonth()]+' '+dv(dd.getFullYear());
$('cd').innerHTML=T.units.map(function(u){return '<div><b>00</b><span>'+esc(u)+'</span></div>'}).join('');
var cb=$('cd').querySelectorAll('b');
function tick(){var s=Math.max(0,Math.floor((tgt-new Date())/1000)),v=[Math.floor(s/86400),Math.floor(s%86400/3600),Math.floor(s%3600/60),s%60];for(var i=0;i<4;i++)cb[i].textContent=dv(String(v[i]).padStart(2,'0'))}
tick();setInterval(tick,1000);
/* whatsapp */
function wa(){var n=($('rn').value||g||'').trim();$('wa').href='https://wa.me/'+C.wa+(n?'?text='+encodeURIComponent(T.wamsg.replace('{n}',n)):'')}
wa();$('rn').addEventListener('input',wa);
/* rsvp submit */
$('rf').addEventListener('submit',function(ev){ev.preventDefault();var f=this,b=f.querySelector('.send'),m=$('rmsg');
 for(var i=0;i<C.ev.length;i++){if(!f.querySelector('input[name="attend-'+C.ev[i].k+'"]:checked')){m.textContent=T.need;return}}
 var fd=new FormData(f);fd.append('page',location.pathname);if(g)fd.append('link-name',g);
 b.disabled=true;var old=b.textContent;b.textContent=T.sending;m.textContent='';
 fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(fd).toString()})
 .then(function(r){if(!r.ok)throw 0;m.textContent=T.ok;f.querySelectorAll('input,select,button').forEach(function(x){x.disabled=true});b.textContent='✓'})
 .catch(function(){m.textContent=T.err;b.disabled=false;b.textContent=old})});
/* reveal on scroll */
var secs=document.querySelectorAll('.sec');
var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.18}):null;
/* seal */
var pts=[],N=120;for(var i=0;i<N;i++){var t=i/N*Math.PI*2,r=45+2.6*Math.sin(t*9+1)+1.6*Math.sin(t*17)+1.1*Math.sin(t*5+2);pts.push((50+r*Math.cos(t)).toFixed(1)+' '+(50+r*Math.sin(t)).toFixed(1))}
function seal(id){return '<defs><radialGradient id="w'+id+'" cx="38%" cy="30%" r="80%"><stop offset="0" stop-color="#c2364a"/><stop offset=".45" stop-color="#8a1c2e"/><stop offset="1" stop-color="#46091a"/></radialGradient><linearGradient id="g'+id+'" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1d58b"/><stop offset=".5" stop-color="#c79a45"/><stop offset="1" stop-color="#8d6420"/></linearGradient></defs><path d="M'+pts.join('L')+'Z" fill="url(#w'+id+')"/><circle cx="50" cy="50" r="33" fill="none" stroke="#e8b0a8" stroke-opacity=".5" stroke-width="1.2"/><circle cx="50" cy="50" r="37" fill="none" stroke="#2a0509" stroke-opacity=".5"/><circle cx="50" cy="50" r="30" fill="#7a1626" fill-opacity=".55"/><text x="50" y="60" text-anchor="middle" font-family="Great Vibes,cursive" font-size="32" fill="#2f0610" fill-opacity=".6" transform="translate(.8 1.2)">U&amp;B</text><text x="50" y="60" text-anchor="middle" font-family="Great Vibes,cursive" font-size="32" fill="url(#g'+id+')">U&amp;B</text><ellipse cx="36" cy="24" rx="16" ry="7" fill="#fff" opacity=".2" transform="rotate(-28 36 24)"/>'}
$('s1').innerHTML=seal('a');$('s2').innerHTML=seal('b');
/* sound */
var ac=null;function crack(){try{ac=ac||new (window.AudioContext||window.webkitAudioContext)();var n=ac.sampleRate*.22,bf=ac.createBuffer(1,n,ac.sampleRate),d=bf.getChannelData(0);for(var i=0;i<n;i++){var k=i/n;d[i]=(Math.random()*2-1)*Math.pow(1-k,3)*(k<.03?k/.03:1)}
 var s=ac.createBufferSource();s.buffer=bf;var bp=ac.createBiquadFilter();bp.type='bandpass';bp.frequency.value=2200;bp.Q.value=.8;var gn=ac.createGain();gn.gain.value=.9;s.connect(bp);bp.connect(gn);gn.connect(ac.destination);s.start();
 var o=ac.createOscillator(),og=ac.createGain();o.frequency.setValueAtTime(180,ac.currentTime);o.frequency.exponentialRampToValueAtTime(60,ac.currentTime+.12);og.gain.setValueAtTime(.5,ac.currentTime);og.gain.exponentialRampToValueAtTime(.001,ac.currentTime+.15);o.connect(og);og.connect(ac.destination);o.start();o.stop(ac.currentTime+.16)}catch(e){}}
/* music */
var bgm=$('bgm'),mute=$('mute'),muted=false;
if(bgm){mute.classList.add('on');mute.onclick=function(e){e.stopPropagation();muted=!muted;bgm.muted=muted;mute.textContent=muted?'×':'♪';if(!muted&&bgm.paused)bgm.play().catch(function(){})}}
function startMusic(){if(bgm&&!muted&&bgm.paused){bgm.volume=.55;bgm.play().catch(function(){})}}
['pointerdown','touchstart','keydown'].forEach(function(t){addEventListener(t,function h(){startMusic()},{once:true,passive:true})});
/* open */
var env=$('env'),opened=false;
function open(user){if(opened)return;opened=true;if(user){crack();startMusic()}env.classList.add('open');
 setTimeout(function(){document.body.classList.add('rd');secs[0].classList.add('in');if(io)for(var i=1;i<secs.length;i++)io.observe(secs[i]);else secs.forEach(function(s){s.classList.add('in')})},1300);
 setTimeout(function(){env.style.display='none'},3300)}
env.addEventListener('click',function(){open(true)});
setTimeout(function(){open(false)},3000);
/* sparkles */
var cv=$('spk'),cx=cv.getContext('2d'),P=[],W,H,DPR=Math.min(2,window.devicePixelRatio||1);
function rs(){W=cv.clientWidth;H=cv.clientHeight;cv.width=W*DPR;cv.height=H*DPR;cx.setTransform(DPR,0,0,DPR,0,0)}rs();addEventListener('resize',rs);
if(!matchMedia('(prefers-reduced-motion: reduce)').matches){for(var i=0;i<28;i++)P.push({x:Math.random()*W,y:Math.random()*H,r:.6+Math.random()*1.8,s:.15+Math.random()*.35,p:Math.random()*6.3,w:.4+Math.random()*.8});
 (function fr(){cx.clearRect(0,0,W,H);for(var i=0;i<P.length;i++){var a=P[i];a.y-=a.s;a.p+=.03;a.x+=Math.sin(a.p)*.25;if(a.y<-5){a.y=H+5;a.x=Math.random()*W}var al=.35+.45*Math.sin(a.p*a.w*2);cx.beginPath();cx.fillStyle='rgba(232,196,110,'+al.toFixed(2)+')';cx.arc(a.x,a.y,a.r,0,6.3);cx.fill();if(a.r>1.8){cx.fillRect(a.x-a.r*2,a.y-.3,a.r*4,.6);cx.fillRect(a.x-.3,a.y-a.r*2,.6,a.r*4)}}requestAnimationFrame(fr)})()}
})();
"""

if __name__ == '__main__':
    args = sys.argv[1:]
    out = ROOT
    pf = None
    only = None
    if '--preview' in args:
        out = args[args.index('--preview') + 1]
        pf = args[args.index('--fonts') + 1] if '--fonts' in args else None
    if '--only' in args:
        only = args[args.index('--only') + 1].split(',')
    for page in PAGES:
        for lang in ('en', 'ne'):
            key = ('ne/' if lang == 'ne' else '') + page
            if only and key not in only:
                continue
            d = os.path.join(out, 'ne', page) if lang == 'ne' else os.path.join(out, page)
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(build(page, lang, pf))
            print('wrote', os.path.join(d, 'index.html'))
