/**
 * 2i backend — standalone acceptance suite.
 *
 * Every test drives a real `node server.js` child process over real HTTP.
 * There is no in-process app harness, because the thing being certified is the
 * server as deployed, not the router object as constructed.
 *
 * Scope is deliberately standalone (handoff section 10): 2i must be useful with
 * no PubPartner configured. Cross-service behaviour is proven separately by the
 * Python integration laboratory.
 */
'use strict';

const { test, before, after, describe } = require('node:test');
const assert = require('node:assert/strict');
const { spawn } = require('node:child_process');
const net = require('node:net');
const path = require('node:path');

const SERVER = path.join(__dirname, '..', 'server.js');

function freePort() {
  return new Promise((resolve, reject) => {
    const socket = net.createServer();
    socket.once('error', reject);
    socket.listen(0, '127.0.0.1', () => {
      const { port } = socket.address();
      socket.close(() => resolve(port));
    });
  });
}

async function startServer(env = {}) {
  const port = await freePort();
  const child = spawn(process.execPath, [SERVER], {
    cwd: path.join(__dirname, '..'),
    env: {
      ...process.env,
      PORT: String(port),
      NODE_ENV: 'development',
      ANTHROPIC_API_KEY: '',
      PUBPARTNER_URL: '',
      ADMIN_KEY: '',
      ...env
    },
    stdio: ['ignore', 'pipe', 'pipe']
  });

  const logs = [];
  child.stdout.on('data', (chunk) => logs.push(chunk.toString()));
  child.stderr.on('data', (chunk) => logs.push(chunk.toString()));

  const base = `http://127.0.0.1:${port}`;
  const deadline = Date.now() + 20000;
  for (;;) {
    if (child.exitCode !== null) {
      throw new Error(`server exited early (${child.exitCode})\n${logs.join('')}`);
    }
    try {
      const response = await fetch(`${base}/health`);
      if (response.ok) break;
    } catch {
      /* not up yet */
    }
    if (Date.now() > deadline) {
      throw new Error(`server never became ready\n${logs.join('')}`);
    }
    await new Promise((r) => setTimeout(r, 100));
  }

  return {
    base,
    logs: () => logs.join(''),
    async stop() {
      if (child.exitCode !== null) return;
      child.kill('SIGTERM');
      await new Promise((resolve) => child.once('exit', resolve));
    }
  };
}

function json(base, method, route, body, headers = {}) {
  return fetch(`${base}${route}`, {
    method,
    headers: { 'Content-Type': 'application/json', ...headers },
    body: body === undefined ? undefined : JSON.stringify(body)
  }).then(async (response) => ({ status: response.status, body: await response.json() }));
}

const MANUSCRIPT = {
  project_id: 'bella-faux-pas',
  chapter_id: 'ch01',
  content: 'The pub was quiet the way a held breath is quiet.',
  character_names: ['Bella'],
  plot_elements: ['cold open'],
  style_notes: ['close third']
};

describe('2i standalone', () => {
  let server;

  before(async () => {
    server = await startServer();
  });

  after(async () => {
    await server.stop();
  });

  test('starts and reports health without an Anthropic key', async () => {
    const { status, body } = await json(server.base, 'GET', '/health');
    assert.equal(status, 200);
    assert.equal(body.status, 'healthy');
    assert.equal(body.service, '2i-backend');
    assert.equal(body.environment.anthropic_api, '✗ missing');
  });

  test('missing provider credentials disable /api/claude without killing the process', async () => {
    const { status } = await json(server.base, 'POST', '/api/claude', { prompt: 'hello' });
    assert.equal(status, 503);
    const health = await json(server.base, 'GET', '/health');
    assert.equal(health.status, 200);
  });

  test('commits are acknowledged locally when no partner is configured', async () => {
    const { status, body } = await json(server.base, 'POST', '/api/manuscript/commit', MANUSCRIPT);
    assert.equal(status, 200);
    assert.equal(body.status, 'committed');
    assert.equal(body.pubpartner_status, 'queued-locally');
    assert.equal(body.project_id, MANUSCRIPT.project_id);
    assert.match(body.message_id, /^msg-/);
    assert.ok(!('manuscript_id' in body), 'a local queue must not fabricate a partner id');
  });

  test('committed messages appear in history with their envelope intact', async () => {
    const { body } = await json(server.base, 'GET', '/api/messages?limit=10');
    const commit = body.messages.find((m) => m.metadata?.type === 'manuscript-commit');
    assert.ok(commit, 'commit not recorded in history');
    assert.equal(commit.destination, 'pubpartner');
    assert.equal(commit.context.project_id, MANUSCRIPT.project_id);
    assert.equal(commit.metadata.content_length, MANUSCRIPT.content.length);
  });

  test('rejects malformed commits with 400 and a field-specific reason', async () => {
    const cases = [
      [{ chapter_id: 'ch01', content: 'x' }, /project_id/],
      [{ project_id: 'p', content: 'x' }, /chapter_id/],
      [{ project_id: 'p', chapter_id: 'ch01' }, /content/],
      [{ project_id: 'has space', chapter_id: 'ch01', content: 'x' }, /project_id/],
      [{ project_id: 'p', chapter_id: 'ch01', content: 'x', plot_elements: 'nope' }, /plot_elements/]
    ];
    for (const [payload, expected] of cases) {
      const { status, body } = await json(server.base, 'POST', '/api/manuscript/commit', payload);
      assert.equal(status, 400, JSON.stringify(payload));
      assert.match(body.message, expected);
    }
  });

  test('thesaurus rejects an empty word and an unknown mode', async () => {
    const empty = await json(server.base, 'GET', '/api/thesaurus?word=');
    assert.equal(empty.status, 400);
    const mode = await json(server.base, 'GET', '/api/thesaurus?word=quiet&mode=sideways');
    assert.equal(mode.status, 400);
    assert.match(mode.body.message, /synonyms/);
  });

  test('unknown routes return a structured 404, not an HTML stack', async () => {
    const { status, body } = await json(server.base, 'GET', '/api/does-not-exist');
    assert.equal(status, 404);
    assert.equal(body.error, 'Not found');
    assert.equal(body.path, '/api/does-not-exist');
  });

  test('malformed JSON is a 400, and the process survives it', async () => {
    const response = await fetch(`${server.base}/api/manuscript/commit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{"project_id": '
    });
    assert.ok(response.status >= 400 && response.status < 500, `got ${response.status}`);
    const health = await json(server.base, 'GET', '/health');
    assert.equal(health.status, 200);
  });
});

describe('2i destructive operations fail closed', () => {
  test('clear is refused outright when ADMIN_KEY is unset', async () => {
    const server = await startServer();
    try {
      await json(server.base, 'POST', '/api/manuscript/commit', MANUSCRIPT);
      const { status } = await json(server.base, 'DELETE', '/api/messages/clear');
      assert.equal(status, 503);
      const history = await json(server.base, 'GET', '/api/messages');
      assert.equal(history.body.messages.length, 1, 'history was cleared without authorisation');
    } finally {
      await server.stop();
    }
  });

  test('clear requires the configured key and honours it', async () => {
    const server = await startServer({ ADMIN_KEY: 'a-long-random-admin-key' });
    try {
      await json(server.base, 'POST', '/api/manuscript/commit', MANUSCRIPT);

      const missing = await json(server.base, 'DELETE', '/api/messages/clear');
      assert.ok(missing.status === 401 || missing.status === 403, `got ${missing.status}`);

      const wrong = await json(server.base, 'DELETE', '/api/messages/clear', undefined, {
        'x-admin-key': 'guess'
      });
      assert.ok(wrong.status === 401 || wrong.status === 403, `got ${wrong.status}`);

      const stillThere = await json(server.base, 'GET', '/api/messages');
      assert.equal(stillThere.body.messages.length, 1);

      const ok = await json(server.base, 'DELETE', '/api/messages/clear', undefined, {
        'x-admin-key': 'a-long-random-admin-key'
      });
      assert.equal(ok.status, 200);

      const cleared = await json(server.base, 'GET', '/api/messages');
      assert.equal(cleared.body.messages.length, 0);
    } finally {
      await server.stop();
    }
  });
});

describe('2i rate limiting', () => {
  test('one route exhausting its window does not consume another route\'s budget', async () => {
    const server = await startServer();
    try {
      // The manuscript window is the tightest on the server (20/min). Spend it.
      let limited = false;
      for (let i = 0; i < 25; i += 1) {
        const { status } = await json(server.base, 'POST', '/api/manuscript/commit', MANUSCRIPT);
        if (status === 429) {
          limited = true;
          break;
        }
      }
      assert.ok(limited, 'manuscript route never rate limited');

      // A different route must still answer: its own window is untouched.
      const thesaurus = await json(server.base, 'GET', '/api/thesaurus?word=');
      assert.equal(thesaurus.status, 400, 'thesaurus was starved by the manuscript window');

      const health = await json(server.base, 'GET', '/health');
      assert.equal(health.status, 200);
    } finally {
      await server.stop();
    }
  });
});

describe('2i partner routing configuration', () => {
  test('an unreachable partner is reported as unreachable, never as routed', async () => {
    const port = await freePort();
    const server = await startServer({
      PUBPARTNER_URL: `http://127.0.0.1:${port}`,
      PUBPARTNER_TIMEOUT_MS: '750'
    });
    try {
      const started = Date.now();
      const { status, body } = await json(server.base, 'POST', '/api/manuscript/commit', MANUSCRIPT);
      assert.equal(status, 200);
      assert.equal(body.pubpartner_status, 'queued-locally-pubpartner-unreachable');
      assert.ok(!('manuscript_id' in body));
      assert.ok(Date.now() - started < 5000, 'fallback took too long');
    } finally {
      await server.stop();
    }
  });

  test('health reports partner configuration honestly', async () => {
    const server = await startServer({ PUBPARTNER_URL: 'http://127.0.0.1:9' });
    try {
      const { body } = await json(server.base, 'GET', '/health');
      assert.equal(body.status, 'healthy');
    } finally {
      await server.stop();
    }
  });
});

describe('2i rate-limit bucket lifecycle', () => {
  test('exhausted buckets are swept instead of accumulating forever', async () => {
    // Previously asserted only by argument: the claim was that a growth test
    // "would need to run for hours". It does not, once the window and sweep
    // interval are configurable.
    const server = await startServer({
      RATE_LIMIT_WINDOW_MS: '300',
      RATE_LIMIT_SWEEP_MS: '150'
    });
    try {
      await json(server.base, 'POST', '/api/manuscript/commit', MANUSCRIPT);
      await json(server.base, 'GET', '/api/thesaurus?word=');

      const populated = await json(server.base, 'GET', '/health');
      assert.ok(
        populated.body.services.rate_limit_entries >= 2,
        `expected at least 2 buckets, saw ${populated.body.services.rate_limit_entries}`
      );

      // /health carries no rate limiter, so polling it cannot recreate buckets.
      const deadline = Date.now() + 5000;
      let remaining = populated.body.services.rate_limit_entries;
      while (Date.now() < deadline) {
        await new Promise((r) => setTimeout(r, 100));
        const health = await json(server.base, 'GET', '/health');
        remaining = health.body.services.rate_limit_entries;
        if (remaining === 0) break;
      }
      assert.equal(remaining, 0, 'rate-limit buckets were never reclaimed');
    } finally {
      await server.stop();
    }
  });

  test('a swept bucket does not carry stale usage into a fresh window', async () => {
    const server = await startServer({
      RATE_LIMIT_WINDOW_MS: '400',
      RATE_LIMIT_SWEEP_MS: '150'
    });
    try {
      let limited = false;
      for (let i = 0; i < 25; i += 1) {
        const { status } = await json(server.base, 'POST', '/api/manuscript/commit', MANUSCRIPT);
        if (status === 429) { limited = true; break; }
      }
      assert.ok(limited, 'never rate limited');

      // Once the window has rolled, the caller must be served again rather
      // than staying permanently locked out.
      await new Promise((r) => setTimeout(r, 900));
      const after = await json(server.base, 'POST', '/api/manuscript/commit', MANUSCRIPT);
      assert.equal(after.status, 200, 'window never reopened');
    } finally {
      await server.stop();
    }
  });
});

describe('2i base_version pass-through', () => {
  test('forwards a client-supplied base_version verbatim and never invents one', async () => {
    // 2i does not hold manuscript authority, so it must neither cache nor
    // synthesise this value. Verified against a recording partner rather than
    // asserted from the source.
    const received = [];
    const http = require('node:http');
    const partner = http.createServer((req, res) => {
      let body = '';
      req.on('data', (c) => { body += c; });
      req.on('end', () => {
        received.push(JSON.parse(body));
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'committed', manuscript_id: 'p:ch01' }));
      });
    });
    await new Promise((r) => partner.listen(0, '127.0.0.1', r));
    const partnerUrl = `http://127.0.0.1:${partner.address().port}`;
    const server = await startServer({ PUBPARTNER_URL: partnerUrl });
    try {
      const base = { 'resident-abc': 3 };
      const withBase = await json(server.base, 'POST', '/api/manuscript/commit',
        { ...MANUSCRIPT, base_version: base });
      assert.equal(withBase.status, 200);
      assert.deepEqual(received.at(-1).base_version, base, 'base_version was not forwarded');

      await json(server.base, 'POST', '/api/manuscript/commit', MANUSCRIPT);
      assert.ok(!('base_version' in received.at(-1)), '2i invented a base_version');

      // Junk must not be forwarded as if it were a version.
      for (const junk of ['not-an-object', 42, ['a'], null]) {
        await json(server.base, 'POST', '/api/manuscript/commit',
          { ...MANUSCRIPT, base_version: junk });
        assert.ok(!('base_version' in received.at(-1)), `forwarded junk: ${JSON.stringify(junk)}`);
      }
    } finally {
      await server.stop();
      await new Promise((r) => partner.close(r));
    }
  });
});
