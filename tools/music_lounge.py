import numpy as np, wave
SR = 44100
def music(path, dur, bpm=116):
    n = int(SR * dur); tt = np.arange(n) / SR; out = np.zeros(n)
    beat = 60 / bpm; bar = beat * 4
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    prog = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]]  # Am7 Fmaj7 Cmaj7 G7
    bass = [45, 41, 36, 43]
    # pad: ondas de sierra suaves y desafinadas, con filtro paso bajo simple
    b = 0
    while b * bar < dur:
        st = int(b * bar * SR); L = min(int(bar * SR), n - st)
        if L <= 0: break
        t0 = np.arange(L) / SR; ch = prog[b % 4]; s = np.zeros(L)
        for m in ch:
            for det in (-0.08, 0.08):
                f = hz(m + det)
                s += 2 * (t0 * f - np.floor(0.5 + t0 * f))
        k = np.ones(40) / 40; s = np.convolve(s, k, "same")
        env = np.minimum(1, t0 / 0.25) * np.minimum(1, (bar - t0) / 0.25)
        out[st:st + L] += s * env * 0.035
        # bajo pulsante
        for q in range(8):
            qs = int((b * bar + q * beat / 2) * SR)
            if qs >= n: continue
            Lq = int(0.2 * SR); tq = np.arange(Lq) / SR
            sb = np.sin(2 * np.pi * hz(bass[b % 4]) * tq) * np.exp(-tq * 9) * 0.22
            e = min(Lq, n - qs); out[qs:qs + e] += sb[:e]
        # arpegio brillante
        for q in range(16):
            qs = int((b * bar + q * beat / 4) * SR)
            if qs >= n: continue
            Lq = int(0.18 * SR); tq = np.arange(Lq) / SR
            note = ch[(q * 3) % 4] + 12
            sa = np.sin(2 * np.pi * hz(note) * tq) * np.exp(-tq * 18) * 0.05
            e = min(Lq, n - qs); out[qs:qs + e] += sa[:e]
        b += 1
    # batería suave a partir del compás 1
    k = 0
    while k * beat < dur:
        st = int(k * beat * SR)
        if k * beat >= bar * 0.5:
            L = int(0.22 * SR); t0 = np.arange(L) / SR
            kick = np.sin(2 * np.pi * (48 + 70 * np.exp(-t0 * 35)) * t0) * np.exp(-t0 * 10) * 0.55
            e = min(L, n - st); out[st:st + e] += kick[:e]
            if k % 2 == 1:
                Lc = int(0.12 * SR); rng = np.random.default_rng(k)
                clap = rng.standard_normal(Lc) * np.exp(-np.linspace(0, 9, Lc)) * 0.12
                e = min(Lc, n - st); out[st:st + e] += clap[:e]
        hs = int((k + 0.5) * beat * SR)
        if hs < n:
            Lh = int(0.05 * SR); rng = np.random.default_rng(k + 99)
            hat = np.diff(np.concatenate([[0], rng.standard_normal(Lh)])) * np.exp(-np.linspace(0, 8, Lh)) * 0.06
            e = min(Lh, n - hs); out[hs:hs + e] += hat[:e]
        k += 1
    fi, fo = int(1.2 * SR), int(2.0 * SR)
    out[:fi] *= np.linspace(0, 1, fi); out[-fo:] *= np.linspace(1, 0, fo)
    out = np.tanh(out * 1.3) * 0.85
    st = np.stack([out, np.roll(out, 220)], 1)  # leve estéreo
    pcm = (st * 32767).astype(np.int16)
    with wave.open(path, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

