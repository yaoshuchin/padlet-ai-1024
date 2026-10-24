import { spawn } from 'child_process';

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const targetUrl = 'https://padlet.com/inforissuescounseling/ai-1024-s024rz6mqadq3x83gbcw';
const port = 9340;
const userDataDir = 'C:\\Users\\Administrator\\.gemini\\antigravity\\chrome_temp_profile_fetch';

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
  await sleep(3000);
  const res = await fetch(`http://127.0.0.1:${port}/json`);
  const list = await res.json();
  const target = list.find(t => t.url && t.url.includes('padlet.com'));
  if (!target) {
    chromeProc.kill();
    process.exit(1);
  }

  const ws = new WebSocket(target.webSocketDebuggerUrl);
  let msgId = 1;
  const pending = new Map();
  const capturedUrls = [];

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.method === 'Network.requestWillBeSent') {
      const u = data.params?.request?.url;
      if (u && (u.includes('docx') || u.includes('storage.googleapis') || u.includes('padletusercontent') || u.includes('download') || u.includes('wKmOZ52YJVweWzMA'))) {
        capturedUrls.push(u);
        console.log('Captured Network Req:', u);
      }
    }
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
  await send('Network.enable');
  await sleep(10000);

  // Click on the wish card for 範例教案
  console.log('Clicking on 範例教案 wish...');
  const clickRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const card = document.querySelector('#wish-4113216291') || document.querySelector('[data-id="4113216291"]');
      if (card) {
        card.click();
        const link = card.querySelector('a');
        if (link) link.click();
        return 'Clicked card';
      }
      return 'Card not found';
    })()`,
    returnByValue: true
  });

  console.log('Click eval:', clickRes.result?.result?.value);
  await sleep(6000);

  // Inspect any newly opened modals or links in DOM
  const modalLinksRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const allLinks = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);
      return allLinks.filter(u => u.includes('padletusercontent') || u.includes('docx') || u.includes('download'));
    })()`,
    returnByValue: true
  });

  console.log('Modal links in DOM:', modalLinksRes.result?.result?.value);
  console.log('All captured URLs:', capturedUrls);

  import('fs').then(fs => {
    fs.writeFileSync('data/captured_docx_urls.json', JSON.stringify({
      modalLinks: modalLinksRes.result?.result?.value,
      capturedUrls
    }, null, 2));
    ws.close();
    chromeProc.kill();
    process.exit(0);
  });
}

main().catch(err => {
  console.error(err);
  chromeProc.kill();
  process.exit(1);
});
