import { spawn } from 'child_process';
import fs from 'fs';

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const targetUrl = 'https://padlet.com/inforissuescounseling/ai-1024-s024rz6mqadq3x83gbcw';
const port = 9334;
const userDataDir = 'C:\\Users\\Administrator\\.gemini\\antigravity\\chrome_temp_profile2';

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
      console.log('Targets:', list.map(t => ({ title: t.title, url: t.url, type: t.type })));
      const padletTarget = list.find(t => t.url && t.url.includes('padlet.com'));
      if (padletTarget) {
        wsUrl = padletTarget.webSocketDebuggerUrl;
        console.log('Found padlet target:', padletTarget.url);
        break;
      }
    } catch (e) {
      // wait
    }
    await sleep(1000);
  }

  if (!wsUrl) {
    console.error('Target not found');
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
  console.log('Connected! Waiting 12 seconds for full hydration...');
  await sleep(12000);

  const evalRes = await send('Runtime.evaluate', {
    expression: 'document.documentElement.outerHTML',
    returnByValue: true
  });

  const html = evalRes.result?.value || '';
  console.log('Got HTML length:', html.length);
  fs.writeFileSync('padlet_rendered.html', html, 'utf-8');

  // Also query elements
  const dataRes = await send('Runtime.evaluate', {
    expression: `(() => {
      return {
        headings: Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6, [role="heading"]')).map(h => h.innerText)
      };
    })()`,
    returnByValue: true
  });

  console.log('Hydrated summary:', JSON.stringify(dataRes.result?.value, null, 2));

  ws.close();
  chromeProc.kill();
  process.exit(0);
}

main().catch(err => {
  console.error(err);
  chromeProc.kill();
  process.exit(1);
});
