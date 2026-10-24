import { spawn } from 'child_process';
import fs from 'fs';

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const targetUrl = 'https://padlet.com/inforissuescounseling/ai-1024-s024rz6mqadq3x83gbcw';
const port = 9337;
const userDataDir = 'C:\\Users\\Administrator\\.gemini\\antigravity\\chrome_temp_profile5';

// Launch chrome with ultra-wide window so all 15-20 columns fit without virtualization!
const chromeProc = spawn(chromePath, [
  `--remote-debugging-port=${port}`,
  `--user-data-dir=${userDataDir}`,
  '--headless=new',
  '--window-size=12000,3000',
  '--no-first-run',
  '--no-default-browser-check',
  targetUrl
]);

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  await sleep(2000);
  let wsUrl = '';
  for (let i = 0; i < 20; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json`);
      const list = await res.json();
      const padletTarget = list.find(t => t.url && t.url.includes('padlet.com'));
      if (padletTarget) {
        wsUrl = padletTarget.webSocketDebuggerUrl;
        break;
      }
    } catch (e) {}
    await sleep(1000);
  }

  const ws = new WebSocket(wsUrl);
  let msgId = 1;
  const pending = new Map();

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.id && pending.has(data.id)) {
      const cb = pending.get(data.id);
      pending.delete(data.id);
      cb(data);
    }
  };

  function send(method, params = {}) {
    return new Promise((resolve) => {
      const id = msgId++;
      pending.set(id, resolve);
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  await new Promise(r => ws.onopen = r);
  console.log('Connected! Waiting 12 seconds for full ultra-wide hydration...');
  await sleep(12000);

  // Set viewport to 12000x3000 in CDP just to be certain
  await send('Emulation.setDeviceMetricsOverride', {
    width: 12000,
    height: 3000,
    deviceScaleFactor: 1,
    mobile: false
  });

  await sleep(3000);

  const evalRes = await send('Runtime.evaluate', {
    expression: 'document.documentElement.outerHTML',
    returnByValue: true
  });

  const fullHtml = evalRes.result?.result?.value || '';
  console.log('Ultra-wide HTML length:', fullHtml.length);
  fs.writeFileSync('padlet_ultrawide.html', fullHtml, 'utf-8');

  // Let's count cards across sections in this DOM
  const checkRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const sections = Array.from(document.querySelectorAll('[data-testid="sectionTitleText"]')).map(st => {
        const title = st.innerText.trim();
        // find group-posts
        let p = st;
        let gp = null;
        for (let i = 0; i < 10; i++) {
          if (p.parentElement) {
            p = p.parentElement;
            gp = p.querySelector('[class*="group-posts"]');
            if (gp) break;
          }
        }
        const cards = gp ? Array.from(gp.querySelectorAll('.surface-post')).map(c => ({
          id: c.getAttribute('data-id') || c.id,
          color: c.getAttribute('data-color'),
          title: c.querySelector('[id*="surface-post-subject"]')?.innerText?.trim() || '',
          body: c.querySelector('[class*="body"]')?.innerText?.trim() || ''
        })) : [];

        return {
          title,
          cardsCount: cards.length,
          cards
        };
      });

      return {
        totalSections: sections.length,
        totalCards: sections.reduce((acc, s) => acc + s.cardsCount, 0),
        sections
      };
    })()`,
    returnByValue: true
  });

  const summary = checkRes.result?.result?.value;
  console.log('Summary:', JSON.stringify({
    totalSections: summary?.totalSections,
    totalCards: summary?.totalCards,
    sectionCardCounts: summary?.sections?.map(s => ({ title: s.title, count: s.cardsCount }))
  }, null, 2));

  fs.writeFileSync('board_ultrawide.json', JSON.stringify(summary, null, 2), 'utf-8');

  ws.close();
  chromeProc.kill();
  process.exit(0);
}

main().catch(err => {
  console.error(err);
  chromeProc.kill();
  process.exit(1);
});
