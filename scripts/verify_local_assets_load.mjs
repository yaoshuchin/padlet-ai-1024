import { spawn } from 'child_process';
import http from 'http';
import fs from 'fs';
import path from 'path';

const server = http.createServer((req, res) => {
  let reqPath = req.url.split('?')[0];
  if (reqPath === '/') reqPath = '/index.html';
  reqPath = decodeURIComponent(reqPath);
  const filePath = path.join(process.cwd(), reqPath);
  if (fs.existsSync(filePath)) {
    const ext = path.extname(filePath);
    const contentType = ext === '.html' ? 'text/html' :
                        ext === '.js' ? 'application/javascript' :
                        ext === '.json' ? 'application/json' :
                        ext === '.png' ? 'image/png' :
                        ext === '.jpg' || ext === '.jpeg' ? 'image/jpeg' :
                        ext === '.webp' ? 'image/webp' :
                        ext === '.svg' ? 'image/svg+xml' :
                        ext === '.pdf' ? 'application/pdf' :
                        ext === '.zip' ? 'application/zip' : 'text/plain';
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(fs.readFileSync(filePath));
  } else {
    res.writeHead(404);
    res.end('Not found: ' + filePath);
  }
});

const PORT = 8091;
server.listen(PORT, async () => {
  console.log(`Server listening at http://localhost:${PORT}`);

  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const cdpPort = 9345;
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

  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let msgId = 1;
  const pending = new Map();
  const failedRequests = [];

  ws.onmessage = (e) => {
    const data = JSON.parse(e.data);
    if (data.method === 'Network.responseReceived') {
      const resp = data.params?.response;
      if (resp && resp.status >= 400 && resp.url.includes('assets/')) {
        failedRequests.push({ url: resp.url, status: resp.status });
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
  await send('Page.enable');
  await send('Runtime.enable');

  await new Promise(r => setTimeout(r, 4000));

  const checkImages = await send('Runtime.evaluate', {
    expression: `(() => {
      const imgs = Array.from(document.querySelectorAll('img[src^="assets/"]'));
      const naturalZeros = imgs.filter(img => img.naturalWidth === 0);
      return {
        totalLocalImagesOnPage: imgs.length,
        brokenImagesCount: naturalZeros.length,
        brokenSrcs: naturalZeros.map(img => img.src)
      };
    })()`,
    returnByValue: true
  });

  console.log('Local images check:', JSON.stringify(checkImages.result?.result?.value, null, 2));
  console.log('Failed asset network requests:', failedRequests);

  ws.close();
  chromeProc.kill();
  server.close();
  process.exit(0);
});
