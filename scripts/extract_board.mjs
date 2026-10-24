import { spawn } from 'child_process';
import fs from 'fs';

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const targetUrl = 'https://padlet.com/inforissuescounseling/ai-1024-s024rz6mqadq3x83gbcw';
const port = 9335;
const userDataDir = 'C:\\Users\\Administrator\\.gemini\\antigravity\\chrome_temp_profile3';

const chromeProc = spawn(chromePath, [
  `--remote-debugging-port=${port}`,
  `--user-data-dir=${userDataDir}`,
  '--headless=new',
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
        console.log('Found padlet target:', padletTarget.url);
        break;
      }
    } catch (e) {}
    await sleep(1000);
  }

  if (!wsUrl) {
    chromeProc.kill();
    process.exit(1);
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
  console.log('Waiting 10s for page hydration...');
  await sleep(10000);

  // Extract DOM structure: columns and posts
  const evalRes = await send('Runtime.evaluate', {
    expression: `(() => {
      // Find all sections/columns
      const columns = [];
      const sectionEls = document.querySelectorAll('[data-testid="section"], [class*="section"], [class*="shelf-column"]');
      
      // Let's also check if there's a React/Vue state or store
      const root = document.querySelector('#app') || document.body;
      
      // Let's gather all column headers and their cards
      const colHeaders = Array.from(document.querySelectorAll('h2, h3, [class*="section-header"], [class*="column-header"], [data-testid*="header"]'));
      
      // Padlet usually has .surface-section or [data-testid="section"]
      // Let's iterate all sections or columns
      const allSections = Array.from(document.querySelectorAll('[data-testid*="section"], [class*="section"], [data-section-id]'));
      
      const debugInfo = {
        title: document.title,
        colHeaderTexts: colHeaders.map(h => h.innerText?.trim()).filter(Boolean),
        cardsCount: document.querySelectorAll('[data-testid*="post"], [class*="wish"], [class*="post"]').length
      };

      // Let's find columns by looking for headers and cards under them
      const sectionsData = [];
      // If Padlet uses shelves:
      const shelves = document.querySelectorAll('[data-testid="shelf"], [class*="shelf"], [class*="column"]');
      shelves.forEach(shelf => {
        const header = shelf.querySelector('h1, h2, h3, h4, [class*="header"], [class*="title"]');
        const cards = shelf.querySelectorAll('[class*="wish"], [class*="post"], [data-testid*="post"]');
        if (header || cards.length > 0) {
          sectionsData.push({
            header: header ? header.innerText.trim() : 'Unnamed',
            cardsCount: cards.length,
            cardTitles: Array.from(cards).map(c => {
              const t = c.querySelector('h1, h2, h3, h4, [class*="title"], [data-testid*="title"]');
              return t ? t.innerText.trim() : c.innerText.slice(0, 30);
            })
          });
        }
      });

      return {
        debugInfo,
        sectionsData,
        fullOuterHTML: document.documentElement.outerHTML
      };
    })()`,
    returnByValue: true
  });

  const value = evalRes.result?.result?.value;
  console.log('debugInfo:', JSON.stringify(value?.debugInfo, null, 2));
  console.log('sectionsData:', JSON.stringify(value?.sectionsData, null, 2));

  if (value?.fullOuterHTML) {
    fs.writeFileSync('padlet_rendered.html', value.fullOuterHTML, 'utf-8');
    console.log('Saved padlet_rendered.html successfully, length:', value.fullOuterHTML.length);
  }

  ws.close();
  chromeProc.kill();
  process.exit(0);
}

main().catch(err => {
  console.error(err);
  chromeProc.kill();
  process.exit(1);
});
