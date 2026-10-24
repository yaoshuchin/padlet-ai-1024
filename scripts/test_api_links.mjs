import { spawn } from 'child_process';

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const targetUrl = 'https://padlet.com/inforissuescounseling/ai-1024-s024rz6mqadq3x83gbcw';
const port = 9341;
const userDataDir = 'C:\\Users\\Administrator\\.gemini\\antigravity\\chrome_temp_profile_api';

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

  const ws = new WebSocket(target.webSocketDebuggerUrl);
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
  await sleep(6000);

  const testApiRes = await send('Runtime.evaluate', {
    expression: `(async () => {
      const u = 'https://padlet-uploads-usc1.storage.googleapis.com/1736270122/094571458e1d9ef6a1851ec6eb3fcea2/____.docx';
      try {
        const r = await fetch('/api/6/links?url=' + encodeURIComponent(u));
        const json = await r.json();
        return { status: r.status, json };
      } catch (e) {
        return { err: e.message };
      }
    })()`,
    awaitPromise: true,
    returnByValue: true
  });

  console.log('API Res:', JSON.stringify(testApiRes.result?.result?.value, null, 2));

  // Also query wish 4113216291 details from Padlet API
  const wishApiRes = await send('Runtime.evaluate', {
    expression: `(async () => {
      try {
        // Padlet has internal API for wish
        const r = await fetch('/api/5/wishes/4113216291');
        const json = await r.json();
        return { status: r.status, json };
      } catch (e) {
        return { err: e.message };
      }
    })()`,
    awaitPromise: true,
    returnByValue: true
  });

  console.log('Wish API Res:', JSON.stringify(wishApiRes.result?.result?.value, null, 2));

  ws.close();
  chromeProc.kill();
  process.exit(0);
}

main().catch(err => {
  console.error(err);
  chromeProc.kill();
  process.exit(1);
});
