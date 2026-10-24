import { spawn } from 'child_process';

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const targetUrl = 'https://padlet.com/inforissuescounseling/ai-1024-s024rz6mqadq3x83gbcw/wish/wKmOZ52YJVweWzMA';
const port = 9339;
const userDataDir = 'C:\\Users\\Administrator\\.gemini\\antigravity\\chrome_temp_profile_wish';

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

  const evalRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const links = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);
      const buttons = Array.from(document.querySelectorAll('button, [role="button"]')).map(b => b.innerText);
      return {
        title: document.title,
        links,
        html: document.body.innerHTML.substring(0, 3000)
      };
    })()`,
    returnByValue: true
  });

  console.log('Result:', JSON.stringify(evalRes.result?.result?.value, null, 2));

  ws.close();
  chromeProc.kill();
  process.exit(0);
}

main().catch(err => {
  console.error(err);
  chromeProc.kill();
  process.exit(1);
});
