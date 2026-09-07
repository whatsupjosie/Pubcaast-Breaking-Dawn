/*
 * PubCast Program Audio Runtime
 * Lightweight browser mixer for dialogue, music, SFX, UI sounds, VTR, and spatial/proximity cues.
 * It does not autoplay by itself; audio starts only after caller/user action.
 */
(function initProgramAudio(global) {
  "use strict";

  const DEFAULT_BUS = { volume: 1, muted: false };
  const BUS_NAMES = ["dialogue", "music", "sfx", "ui", "vtr", "room"];

  function clamp(value, min, max, fallback) {
    const n = Number(value);
    if (!Number.isFinite(n)) return fallback;
    return Math.max(min, Math.min(max, n));
  }

  class ProgramAudioRuntime {
    constructor(options = {}) {
      this.options = Object.assign({ maxDistance: 18, duckMusicTo: 0.35 }, options);
      this.context = null;
      this.master = null;
      this.buses = new Map();
      this.active = new Set();
      this.dialogueActive = 0;
      this.lastError = null;
    }

    ensureContext() {
      if (this.context) return this.context;
      const AudioContextCtor = global.AudioContext || global.webkitAudioContext;
      if (!AudioContextCtor) throw new Error("Web Audio API unavailable");
      this.context = new AudioContextCtor();
      this.master = this.context.createGain();
      this.master.gain.value = 1;
      this.master.connect(this.context.destination);
      for (const name of BUS_NAMES) this.createBus(name);
      return this.context;
    }

    createBus(name) {
      const ctx = this.context;
      if (!ctx) return null;
      if (this.buses.has(name)) return this.buses.get(name);
      const gain = ctx.createGain();
      gain.gain.value = DEFAULT_BUS.volume;
      gain.connect(this.master);
      const bus = Object.assign({ name, gain, sources: new Set() }, DEFAULT_BUS);
      this.buses.set(name, bus);
      return bus;
    }

    setBusVolume(name, volume) {
      this.ensureContext();
      const bus = this.createBus(name);
      bus.volume = clamp(volume, 0, 1, 1);
      bus.gain.gain.value = bus.muted ? 0 : this.effectiveVolume(name);
      return bus.gain.gain.value;
    }

    setMuted(name, muted) {
      this.ensureContext();
      const bus = this.createBus(name);
      bus.muted = !!muted;
      bus.gain.gain.value = bus.muted ? 0 : this.effectiveVolume(name);
      return bus.muted;
    }

    effectiveVolume(name) {
      const bus = this.buses.get(name);
      if (!bus) return 1;
      if (name === "music" && this.dialogueActive > 0) return bus.volume * this.options.duckMusicTo;
      return bus.volume;
    }

    updateDucking() {
      const music = this.buses.get("music");
      if (music) music.gain.gain.value = music.muted ? 0 : this.effectiveVolume("music");
    }

    spatialGain(listener, source, baseVolume = 1) {
      const lx = Number(listener?.x ?? 0), ly = Number(listener?.y ?? 0), lz = Number(listener?.z ?? 0);
      const sx = Number(source?.x ?? 0), sy = Number(source?.y ?? 0), sz = Number(source?.z ?? 0);
      const distance = Math.hypot(sx - lx, sy - ly, sz - lz);
      const maxDistance = Math.max(1, Number(this.options.maxDistance || 18));
      const volume = clamp(baseVolume, 0, 1, 1) * Math.max(0, 1 - distance / maxDistance);
      const pan = clamp((sx - lx) / maxDistance, -1, 1, 0);
      return { distance, volume, pan };
    }

    async playUrl(url, options = {}) {
      this.ensureContext();
      const busName = options.bus || "sfx";
      const bus = this.createBus(busName);
      const audio = new Audio(url);
      audio.crossOrigin = options.crossOrigin || "anonymous";
      audio.loop = !!options.loop;
      const source = this.context.createMediaElementSource(audio);
      const gain = this.context.createGain();
      gain.gain.value = clamp(options.volume, 0, 1, 1);
      let lastNode = source;
      let panner = null;
      if (options.spatial && this.context.createStereoPanner) {
        panner = this.context.createStereoPanner();
        const sg = this.spatialGain(options.listener, options.position, gain.gain.value);
        gain.gain.value = sg.volume;
        panner.pan.value = sg.pan;
        lastNode.connect(panner);
        lastNode = panner;
      }
      lastNode.connect(gain);
      gain.connect(bus.gain);
      const handle = { audio, source, gain, panner, busName, stop: () => this.stopHandle(handle) };
      this.active.add(handle);
      bus.sources.add(handle);
      if (busName === "dialogue") {
        this.dialogueActive += 1;
        this.updateDucking();
      }
      audio.onended = () => this.stopHandle(handle);
      await audio.play();
      return handle;
    }

    playUISound(kind = "click") {
      this.ensureContext();
      const osc = this.context.createOscillator();
      const gain = this.context.createGain();
      const bus = this.createBus("ui");
      const frequency = kind === "error" ? 180 : kind === "confirm" ? 660 : 420;
      osc.frequency.value = frequency;
      gain.gain.value = 0.045;
      osc.connect(gain);
      gain.connect(bus.gain);
      osc.start();
      osc.stop(this.context.currentTime + 0.055);
      const handle = { oscillator: osc, gain, busName: "ui", stop: () => this.stopHandle(handle) };
      this.active.add(handle);
      bus.sources.add(handle);
      osc.onended = () => this.stopHandle(handle);
      return handle;
    }

    stopHandle(handle) {
      if (!handle || !this.active.has(handle)) return false;
      try { handle.audio?.pause?.(); } catch (_) {}
      try { handle.oscillator?.stop?.(); } catch (_) {}
      try { handle.source?.disconnect?.(); } catch (_) {}
      try { handle.gain?.disconnect?.(); } catch (_) {}
      try { handle.panner?.disconnect?.(); } catch (_) {}
      this.active.delete(handle);
      const bus = this.buses.get(handle.busName);
      if (bus) bus.sources.delete(handle);
      if (handle.busName === "dialogue") {
        this.dialogueActive = Math.max(0, this.dialogueActive - 1);
        this.updateDucking();
      }
      return true;
    }

    stopAll() {
      const handles = Array.from(this.active);
      for (const handle of handles) this.stopHandle(handle);
      this.dialogueActive = 0;
      this.updateDucking();
      return handles.length;
    }

    status() {
      const buses = {};
      for (const [name, bus] of this.buses.entries()) {
        buses[name] = { volume: bus.volume, muted: bus.muted, activeSources: bus.sources.size };
      }
      return {
        available: !!(global.AudioContext || global.webkitAudioContext),
        contextState: this.context?.state || "not_started",
        activeSources: this.active.size,
        dialogueActive: this.dialogueActive,
        buses,
        lastError: this.lastError,
      };
    }
  }

  const runtime = new ProgramAudioRuntime();
  global.PubcastProgramAudio = runtime;
  if (typeof module !== "undefined" && module.exports) {
    module.exports = { ProgramAudioRuntime };
  }
})(typeof window !== "undefined" ? window : globalThis);
