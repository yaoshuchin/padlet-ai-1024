import { spawn } from 'child_process';
import fs from 'fs';

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const targetUrl = 'https://padlet.com/inforissuescounseling/ai-1024-s024rz6mqadq3x83gbcw';
const port = 9336;
const userDataDir = 'C:\\Users\\Administrator\\.gemini\\antigravity\\chrome_temp_profile4';

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
  console.log('Connected! Waiting 10s...');
  await sleep(10000);

  // Look for stores or scroll across the page
  // Padlet has horizontal scrolling on the board container!
  // If we scroll the board container all the way to the right or query Pinia/Vue:
  const inspectRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const keys = Object.keys(window).filter(k => !k.startsWith('webkit') && !k.startsWith('on'));
      
      // Look for pinia or vue or padlet objects
      let padletObjKeys = [];
      if (window.padlet) {
        padletObjKeys = Object.keys(window.padlet);
      }
      
      // Check Pinia stores
      let piniaStores = [];
      if (window.__PINIA__) {
        piniaStores = Object.keys(window.__PINIA__._s || {});
      }

      // Check root element __vue_app__
      const appEl = document.querySelector('#app') || document.querySelector('#root') || document.body;
      const hasVue = !!appEl.__vue_app__;

      return {
        keys: keys.slice(0, 50),
        padletObjKeys,
        piniaStores,
        hasVue
      };
    })()`,
    returnByValue: true
  });

  console.log('Inspect result:', JSON.stringify(inspectRes.result?.result?.value, null, 2));

  // Now, let's scroll the board container from left to right to force render all virtual items, or dispatch scroll!
  console.log('Scrolling horizontal container...');
  const scrollRes = await send('Runtime.evaluate', {
    expression: `(async () => {
      // Find scrollable board container
      const scrollers = Array.from(document.querySelectorAll('*')).filter(el => {
        return el.scrollWidth > el.clientWidth && el.clientWidth > 300;
      });
      console.log('Scrollers found:', scrollers.length);
      
      const scroller = scrollers[0] || document.documentElement || document.body;
      const totalWidth = scroller.scrollWidth;
      
      // Scroll in increments of 300px
      for (let x = 0; x <= totalWidth; x += 300) {
        scroller.scrollLeft = x;
        window.scrollTo(x, 0);
        await new Promise(r => setTimeout(r, 200));
      }
      
      // Collect all rendered cards and sections
      const sections = Array.from(document.querySelectorAll('[data-testid="sectionTitleText"]')).map(el => {
        return el.innerText.trim();
      });

      return {
        totalWidth,
        sectionsCount: sections.length,
        sections
      };
    })()`,
    awaitPromise: true,
    returnByValue: true
  });

  console.log('Scroll res:', JSON.stringify(scrollRes.result?.result?.value, null, 2));

  ws.close();
  chromeProc.kill();
  process.exit(0);
}

main().catch(err => {
  console.error(err);
  chromeProc.kill();
  process.exit(1);
});
