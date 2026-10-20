const assert = require("node:assert/strict");
const { readFileSync } = require("node:fs");
const { join } = require("node:path");
const { test } = require("node:test");
const { runInNewContext } = require("node:vm");

const template = readFileSync(
  join(__dirname, "../djangocms_video/templates/djangocms_video/default/hls_stream_source.html"),
  "utf8",
);
const script = template.match(/<script>([\s\S]*?)<\/script>/)[1]
  .replace("{{ source_id }}", "42");

function renderStream({ supported = true, native = false, autoplay = false } = {}) {
  const handlers = {};
  const calls = [];
  const video = {
    autoplay,
    canPlayType(type) {
      assert.equal(type, "application/vnd.apple.mpegurl");
      return native ? "probably" : "";
    },
    play() {
      calls.push("play");
      // Autoplay policy rejection must not cause an unhandled promise rejection.
      return Promise.reject(new Error("Autoplay blocked"));
    },
  };
  const source = {
    parentElement: video,
    src: "https://example.com/live.m3u8?token=example",
  };
  class Hls {
    static isSupported() { return supported; }
    static Events = { MANIFEST_PARSED: "manifest", ERROR: "error" };
    static ErrorTypes = { MEDIA_ERROR: "media", NETWORK_ERROR: "network" };
    loadSource(url) { calls.push(["load", url]); }
    attachMedia(element) { assert.equal(element, video); }
    on(event, handler) { handlers[event] = handler; }
    recoverMediaError() { calls.push("recover"); }
    destroy() { calls.push("destroy"); }
  }
  runInNewContext(script, {
    Hls,
    document: {
      getElementById(id) {
        assert.equal(id, "42");
        return source;
      },
    },
    console: { error() { calls.push("error"); } },
  });
  return { calls, handlers, source, video };
}

test("hls.js loads the source URL including query parameters without forcing playback", () => {
  const { calls, handlers, source } = renderStream();
  assert.deepEqual(calls, [["load", source.src]]);
  handlers.manifest();
  assert.equal(calls.includes("play"), false);
});

test("hls.js honors autoplay and handles browser policy rejection", async () => {
  const { calls, handlers } = renderStream({ autoplay: true });
  handlers.manifest();
  await new Promise(setImmediate);
  assert.equal(calls.includes("play"), true);
});

test("native HLS sets the video URL and leaves autoplay to the browser", () => {
  for (const autoplay of [false, true]) {
    const { calls, source, video } = renderStream({ supported: false, native: true, autoplay });
    assert.equal(video.src, source.src);
    assert.deepEqual(calls, []);
  }
});

test("unsupported browsers report the error without accessing undefined variables", () => {
  const { calls } = renderStream({ supported: false });
  assert.deepEqual(calls, ["error"]);
});

test("fatal media errors recover and other fatal errors destroy the player", () => {
  const { calls, handlers } = renderStream();
  handlers.error(null, { fatal: false, type: "media" });
  assert.equal(calls.includes("recover"), false);
  handlers.error(null, { fatal: true, type: "media" });
  assert.equal(calls.includes("recover"), true);
  handlers.error(null, { fatal: true, type: "unknown" });
  assert.equal(calls.includes("destroy"), true);
});
