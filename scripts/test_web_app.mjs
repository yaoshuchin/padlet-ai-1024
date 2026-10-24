import { spawn } from 'child_process';
import http from 'http';
import fs from 'fs';
import path from 'path';

// Start a lightweight http static server
const server = http.createServer((req, res) => {
  let reqPath = req.url.split('?')[0];
  if (reqPath === '/') reqPath = '/index.html';
  const filePath = path.join(process.cwd(), reqPath);
  if (fs.existsSync(filePath)) {
    const ext = path.extname(filePath);
    const contentType = ext === '.html' ? 'text/html' :
                        ext === '.js' ? 'application/javascript' :
                        ext === '.json' ? 'application/json' : 'text/plain';
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(fs.readFileSync(filePath));
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

const PORT = 8089;
server.listen(PORT, async () => {
  console.log(`Server listening at http://localhost:${PORT}`);

  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const cdpPort = 9338;
  const chromeProc = spawn(chromePath, [
    `--remote-debugging-port=${cdpPort}`,
    '--headless=new',
    '--no-first-run',
    `http://localhost:${PORT}/index.html`
  ]);

  await new Promise(r => setTimeout(r, 2000));
  const res = await fetch(`http://127.0.0.1:${cdpPort}/json`);
  const list = await res.json();
  const page = list.find(t => t.url && t.url.includes(`localhost:${PORT}`));

  if (!page) {
    console.error('Page target not found');
    chromeProc.kill();
    server.close();
    process.exit(1);
  }

  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let msgId = 1;
  const pending = new Map();
  const logs = [];

  ws.onmessage = (e) => {
    const data = JSON.parse(e.data);
    if (data.method === 'Runtime.consoleAPICalled') {
      logs.push(data.params);
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
  await send('Runtime.enable');
  await send('Page.enable');

  await new Promise(r => setTimeout(r, 3000));

  const evalRes = await send('Runtime.evaluate', {
    expression: `(() => {
      return {
        title: document.title,
        columnsCount: document.querySelectorAll('#boardView > div').length,
        cardsCount: document.querySelectorAll('.card-theme-yellow, .card-theme-red, .card-theme-blue, .card-theme-green').length,
        hasError: false
      };
    })()`,
    returnByValue: true
  });

  console.log('Test result:', JSON.stringify(evalRes.result?.result?.value, null, 2));

  // Take screenshot
  const screenshotRes = await send('Page.captureScreenshot', { format: 'png' });
  if (screenshotRes.result?.data) {
    fs.writeFileSync('preview_screenshot.png', Buffer.from(screenshotRes.result.data, 'base64'));
    console.log('Saved preview_screenshot.png');
  }

  ws.close();
  chromeProc.kill();
  server.close();
  process.exit(0);
});
