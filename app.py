from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TITAN MONITOR v5.0</title>
    <link href="https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* --- 1. THEME: TITAN DARK --- */
        :root {
            --bg: #000000;
            --panel: #0f0f13;
            --border: #333;
            --neon-blue: #00f0ff;
            --neon-green: #0aff0a;
            --neon-red: #ff003c;
            --text-main: #ffffff;
            --text-dim: #888;
            --card-shadow: 0 8px 32px rgba(0,0,0,0.8);
        }

        * { box-sizing: border-box; outline: none; -webkit-tap-highlight-color: transparent; }
        
        body {
            background: var(--bg); color: var(--text-main);
            font-family: 'Roboto Mono', monospace;
            margin: 0; padding: 0;
            height: 100vh;
            height: 100dvh;
            display: flex; flex-direction: column;
            overflow: hidden;
            font-size: 14px; /* Increased Base Font */
        }

        /* --- 2. HEADER (BIG & BOLD) --- */
        header {
            background: rgba(10,10,15,0.95);
            border-bottom: 2px solid var(--border);
            padding: 15px 20px;
            display: flex; justify-content: space-between; align-items: center;
            z-index: 100; box-shadow: 0 5px 20px #000;
        }
        .logo {
            font-family: 'Teko', sans-serif; font-size: 28px; line-height: 1;
            color: var(--neon-blue); text-transform: uppercase; letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
        }
        .sys-status {
            font-size: 12px; font-weight: bold; color: var(--text-dim);
            display: flex; align-items: center; gap: 8px;
        }
        .pulse-dot {
            width: 10px; height: 10px; background: #333; border-radius: 50%;
            transition: 0.3s;
        }
        .pulse-dot.active { background: var(--neon-green); box-shadow: 0 0 10px var(--neon-green); animation: pulse 1s infinite; }
        @keyframes pulse { 0% {opacity:1;} 50% {opacity:0.5;} 100% {opacity:1;} }

        /* --- 3. LAYOUT --- */
        .viewport {
            flex: 1; overflow-y: auto; padding: 15px; padding-bottom: 110px;
            background: radial-gradient(circle at center, #111 0%, #000 100%);
            -webkit-overflow-scrolling: touch;
        }
        .page { display: none; animation: fadeIn 0.3s ease-out; }
        .page.active { display: block; }
        @keyframes fadeIn { from {opacity:0; transform:translateY(10px);} to {opacity:1; transform:translateY(0);} }

        /* --- 4. COMPONENTS (BIGGER UI) --- */
        .card {
            background: var(--panel); border: 1px solid var(--border);
            border-radius: 12px; padding: 15px; margin-bottom: 20px;
            box-shadow: var(--card-shadow);
        }
        .c-title {
            color: var(--neon-blue); font-family: 'Teko', sans-serif;
            font-size: 22px; margin-bottom: 10px; border-bottom: 1px solid #222;
            padding-bottom: 5px; display: flex; justify-content: space-between;
        }

        /* INPUTS - BIGGER */
        input, textarea {
            width: 100%; background: #050505; border: 1px solid #444;
            color: #fff; padding: 15px; border-radius: 8px; font-size: 14px;
            margin-bottom: 15px; font-family: 'Roboto Mono', monospace;
            transition: 0.3s;
        }
        input:focus, textarea:focus { border-color: var(--neon-blue); box-shadow: 0 0 10px rgba(0,240,255,0.2); }

        /* BUTTONS - BIGGER */
        .btn-main {
            width: 100%; padding: 18px; font-size: 16px; font-weight: bold;
            background: linear-gradient(180deg, #1a1a1a, #000);
            border: 1px solid var(--border); color: #fff;
            border-radius: 8px; cursor: pointer; text-transform: uppercase;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        .btn-go { border-color: var(--neon-green); color: var(--neon-green); }
        .btn-go:active { background: #002200; transform: scale(0.98); }
        .btn-stop { border-color: var(--neon-red); color: var(--neon-red); }

        /* --- 5. SATISFYING AGENT CARDS (THE LOGIN UI) --- */
        .agent-list { display: flex; flex-direction: column; gap: 15px; }
        .agent-card {
            display: flex; align-items: center; background: #080808;
            border: 1px solid #333; padding: 15px; border-radius: 10px;
            transition: 0.3s; border-left: 4px solid #333;
        }
        .agent-card.online { 
            border-color: var(--neon-green); 
            border-left-color: var(--neon-green);
            background: rgba(0, 255, 10, 0.05);
            box-shadow: 0 0 15px rgba(0, 255, 10, 0.1);
        }
        .agent-avatar {
            width: 50px; height: 50px; border-radius: 50%; border: 2px solid #555;
            margin-right: 15px;
        }
        .agent-info { flex: 1; }
        .agent-name { font-size: 16px; font-weight: bold; color: #fff; }
        .agent-status { font-size: 12px; color: #666; margin-top: 4px; font-weight: bold; }
        .online .agent-status { color: var(--neon-green); }
        
        .power-btn {
            width: 40px; height: 40px; border-radius: 50%; border: 1px solid #444;
            background: #111; color: #555; display: flex; align-items: center;
            justify-content: center; font-size: 18px; cursor: pointer;
        }
        .power-btn:hover { color: var(--neon-red); border-color: var(--neon-red); }

        /* --- 6. CHAT FEED (BIGGER) --- */
        .msg-bubble {
            background: #121212; border-left: 3px solid #333;
            padding: 12px 15px; border-radius: 0 10px 10px 10px;
            margin-bottom: 12px; font-size: 14px; line-height: 1.5;
            position: relative;
        }
        .msg-bubble.alert { border-left-color: var(--neon-red); background: rgba(255,0,60,0.1); }
        .msg-top { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 5px; color: #666; }
        .msg-user { font-weight: bold; color: var(--neon-blue); font-size: 13px; }
        .deleted-tag { 
            background: var(--neon-red); color: #fff; padding: 2px 6px; 
            font-size: 10px; border-radius: 4px; margin-left: 8px; display: inline-block; 
        }

        /* --- 7. RADAR LIST (RESTORED FEATURES) --- */
        .user-row {
            display: flex; align-items: center; padding: 12px;
            background: #0a0a0a; border-bottom: 1px solid #222;
        }
        .u-pic { width: 45px; height: 45px; border-radius: 50%; margin-right: 15px; border: 2px solid #333; }
        .u-info { flex: 1; }
        .u-name { font-size: 15px; font-weight: bold; color: #eee; }
        .u-seen { font-size: 12px; color: #555; margin-top: 2px; }
        .target-btn {
            background: transparent; border: 1px solid #444; color: #666;
            padding: 8px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;
        }
        .target-btn.active { 
            border-color: var(--neon-red); color: var(--neon-red); 
            background: rgba(255,0,60,0.1); box-shadow: 0 0 10px rgba(255,0,60,0.2);
        }

        /* --- 8. VAULT (MEDIA) --- */
        .vault-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .media-card { background: #000; border: 1px solid #333; border-radius: 8px; overflow: hidden; }
        .media-card img { width: 100%; height: 120px; object-fit: cover; display: block; }
        .media-audio { padding: 15px; background: #111; display:flex; align-items:center; justify-content:center; }
        .media-meta { padding: 5px; font-size: 11px; color: #777; background: #080808; text-align: center; }

        /* --- 9. NAVIGATION (BOTTOM) --- */
        .nav-bar {
            position: fixed; bottom: 0; left: 0; right: 0;
            background: #0f0f13; border-top: 1px solid var(--border);
            display: flex; height: 80px; align-items: center; justify-content: space-around;
            z-index: 200; box-shadow: 0 -5px 20px rgba(0,0,0,0.5);
        }
        .nav-icon { 
            font-size: 24px; color: #444; padding: 10px; 
            display: flex; flex-direction: column; align-items: center; gap: 5px;
            transition: 0.3s;
        }
        .nav-icon span { font-size: 10px; font-weight: bold; font-family: 'Teko', sans-serif; letter-spacing: 1px; }
        .nav-icon.active { color: var(--neon-blue); transform: translateY(-5px); text-shadow: 0 0 10px var(--neon-blue); }

        /* Audio element fix */
        audio { width: 100%; height: 30px; filter: invert(1); }
    </style>
</head>
<body>

<header>
    <div class="logo">TITAN <span style="color:#fff">SYSTEM</span></div>
    <div class="sys-status">
        <div class="pulse-dot" id="sysDot"></div>
        <span id="sysTxt">STANDBY</span>
    </div>
</header>

<div class="viewport">
    
    <!-- 1. DEPLOYMENT (LOGIN) -->
    <div id="p-deploy" class="page active">
        <div class="card">
            <div class="c-title">MISSION CONTROL</div>
            <label style="color:#666; font-size:12px; margin-bottom:5px; display:block;">TARGET ROOM</label>
            <input type="text" id="room" value="ملتقى🥂العرب">
            
            <label style="color:#666; font-size:12px; margin-bottom:5px; display:block;">AGENTS (User#Pass)</label>
            <textarea id="accs" placeholder="Spy1#pass123@Spy2#pass456"></textarea>
            
            <button class="btn-main btn-go" onclick="deployAgents()">INITIATE SEQUENCE</button>
        </div>

        <div class="card">
            <div class="c-title">AGENT STATUS</div>
            <div id="agentList" class="agent-list">
                <div style="text-align:center; padding:20px; color:#444;">NO ACTIVE AGENTS</div>
            </div>
        </div>
    </div>

    <!-- 2. LIVE FEED -->
    <div id="p-feed" class="page">
        <div class="card">
            <div class="c-title">LIVE INTERCEPTION</div>
            <div id="feedBox" style="min-height:300px;"></div>
        </div>
    </div>

    <!-- 3. RADAR -->
    <div id="p-radar" class="page">
        <div class="card">
            <div class="c-title">
                <span>SONAR RADAR</span>
                <span id="uCount" style="color:#fff">0</span>
            </div>
            <div id="radarList"></div>
        </div>
    </div>

    <!-- 4. VAULT -->
    <div id="p-vault" class="page">
        <div class="card">
            <div class="c-title">EVIDENCE VAULT</div>
            <div id="vaultGrid" class="vault-grid"></div>
        </div>
    </div>

</div>

<!-- BOTTOM NAVIGATION -->
<div class="nav-bar">
    <div class="nav-icon active" onclick="nav('p-deploy', this)">
        <div>⚙️</div><span>DEPLOY</span>
    </div>
    <div class="nav-icon" onclick="nav('p-feed', this)">
        <div>💬</div><span>FEED</span>
    </div>
    <div class="nav-icon" onclick="nav('p-radar', this)">
        <div>🎯</div><span>RADAR</span>
    </div>
    <div class="nav-icon" onclick="nav('p-vault', this)">
        <div>📂</div><span>VAULT</span>
    </div>
</div>

<script>
    // --- VARIABLES ---
    let bots = [];
    let users = new Map();
    let targets = new Set();
    const WS_URL = "wss://chatp.net:5333/server";

    // --- AUDIO & VIBRATION ---
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const audCtx = new AudioContext();

    function triggerAlert() {
        // Vibrate
        if(navigator.vibrate) navigator.vibrate([200, 100, 200]);
        // Beep
        if(audCtx.state === 'suspended') audCtx.resume();
        let osc = audCtx.createOscillator();
        let gain = audCtx.createGain();
        osc.connect(gain);
        gain.connect(audCtx.destination);
        osc.frequency.setValueAtTime(600, audCtx.currentTime);
        osc.type = 'square';
        osc.start();
        osc.stop(audCtx.currentTime + 0.15);
    }

    // --- NAVIGATION ---
    function nav(id, el) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-icon').forEach(n => n.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        el.classList.add('active');
    }

    function setSysStatus(active) {
        let d = document.getElementById('sysDot');
        let t = document.getElementById('sysTxt');
        if(active) {
            d.classList.add('active'); t.innerText = "SYSTEM ACTIVE"; t.style.color = "var(--neon-green)";
        } else {
            d.classList.remove('active'); t.innerText = "STANDBY"; t.style.color = "#666";
        }
    }

    function genId() { return Math.random().toString(36).substr(2, 8); }

    // --- DEPLOYMENT LOGIC (The Satisfying Part) ---
    function deployAgents() {
        let raw = document.getElementById("accs").value;
        let room = document.getElementById("room").value;
        if(!raw.includes("#")) { alert("Format: User#Pass"); return; }

        let list = document.getElementById("agentList");
        list.innerHTML = "";
        bots = [];
        
        let arr = raw.split("@").filter(s => s.includes("#"));
        
        arr.forEach((creds, i) => {
            let [u, p] = creds.split("#");
            let user = u.trim();
            let domId = `bot-${i}`;

            // Create Visual Card (Waiting State)
            let html = `
                <div class="agent-card" id="${domId}">
                    <img src="https://ui-avatars.com/api/?name=${user}&background=111&color=fff" class="agent-avatar">
                    <div class="agent-info">
                        <div class="agent-name">${user}</div>
                        <div class="agent-status" id="st-${domId}">INITIALIZING...</div>
                    </div>
                    <div class="power-btn" onclick="killBot(${i})">⏻</div>
                </div>
            `;
            list.insertAdjacentHTML('beforeend', html);

            // Connect with delay
            setTimeout(() => {
                connectBot(user, p.trim(), room, domId, i);
            }, i * 1500);
        });
        setSysStatus(true);
    }

    function connectBot(user, pass, room, domId, index) {
        let ws = new WebSocket(WS_URL);
        
        const update = (msg, state) => {
            let st = document.getElementById(`st-${domId}`);
            let card = document.getElementById(domId);
            if(st) st.innerText = msg;
            if(state === 'ok') { 
                card.classList.add('online'); 
            }
            if(state === 'err') { 
                st.style.color = "var(--neon-red)"; 
            }
        };

        ws.onopen = () => {
            update("AUTHENTICATING...", "wait");
            ws.send(JSON.stringify({ handler: "login", id: genId(), username: user, password: pass }));
        };

        ws.onmessage = (e) => {
            let d = JSON.parse(e.data);

            if(d.handler === "login_event" && d.type === "success") {
                update("🟢 ONLINE - JOINING ROOM", "wait");
                ws.send(JSON.stringify({ handler: "room_join", id: genId(), name: room }));
            }
            
            if(d.handler === "room_event" && d.type === "room_joined") {
                update("🟢 SECURE CONNECTION ESTABLISHED", "ok");
            }

            // PASSIVE SNIFFER (Global Handler)
            handlePacket(d);
        };

        ws.onclose = () => { update("🔴 DISCONNECTED", "err"); };
        bots[index] = ws;
    }

    function killBot(i) {
        if(bots[i]) { bots[i].close(); bots[i] = null; }
    }

    // --- CENTRAL INTELLIGENCE ---
    function handlePacket(d) {
        let time = new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});

        // 1. RADAR UPDATE (Any activity updates user)
        if(d.username || d.from) {
            updateRadar(d.username || d.from, d.icon || d.avatar_url);
        }

        // 2. CHAT FEED
        if(d.type === "text") {
            addMsg(d.from, d.body, d.id, time);
            
            // Media Sniffer inside text
            if(d.body.match(/http.*?\.(jpg|png|gif|mp3|wav|ogg)/i)) {
                let url = d.body.match(/http.*?\.(jpg|png|gif|mp3|wav|ogg)/i)[0];
                addVault(url, d.from);
            }
        }

        // 3. IMAGE PACKET
        if(d.type === "image") {
            addMsg(d.from, "📷 [SENT MEDIA]", d.id, time);
            addVault(d.url || d.body, d.from);
        }

        // 4. DELETED MSG
        if(d.type === "delete" || d.type === "remove") {
            markDeleted(d.messageId || d.id);
        }
    }

    // --- UI RENDERERS ---

    function addMsg(user, txt, id, time) {
        let isTgt = targets.has(user);
        if(isTgt) triggerAlert(); // Vibrate & Beep

        let box = document.getElementById("feedBox");
        let html = `
            <div class="msg-bubble ${isTgt ? 'alert' : ''}" id="msg-${id}">
                <div class="msg-top">
                    <span class="msg-user" style="color:${isTgt ? 'var(--neon-red)' : 'var(--neon-blue)'}">${user}</span>
                    <span>${time}</span>
                </div>
                <div class="msg-txt">${esc(txt)}</div>
            </div>
        `;
        box.insertAdjacentHTML('beforeend', html);
        box.scrollTop = box.scrollHeight;
    }

    function markDeleted(id) {
        let el = document.getElementById(`msg-${id}`);
        if(el) {
            el.querySelector('.msg-txt').style.textDecoration = "line-through";
            el.querySelector('.msg-user').innerHTML += `<span class="deleted-tag">DELETED</span>`;
        }
    }

    function addVault(url, user) {
        if(!url.startsWith("http")) url = "https://chatp.net" + url;
        let isAudio = url.match(/\.(mp3|wav|ogg)/i);
        let box = document.getElementById("vaultGrid");
        
        let content = isAudio 
            ? `<div class="media-audio"><audio controls src="${url}"></audio></div>`
            : `<img src="${url}">`;
            
        let html = `
            <div class="media-card">
                ${content}
                <div class="media-meta">${user}</div>
            </div>
        `;
        box.insertAdjacentHTML('afterbegin', html);
    }

    function updateRadar(name, icon) {
        if(!name) return;
        let now = Date.now();
        if(!users.has(name)) {
            users.set(name, { 
                name: name, 
                icon: icon || `https://ui-avatars.com/api/?name=${name}&background=random`, 
                last: now 
            });
        } else {
            let u = users.get(name);
            u.last = now;
            if(icon) u.icon = icon;
            users.set(name, u);
        }
        renderRadar();
    }

    function renderRadar() {
        let list = document.getElementById("radarList");
        list.innerHTML = "";
        document.getElementById("uCount").innerText = users.size;

        // Sort: Targets first, then most recent
        let sorted = [...users.values()].sort((a,b) => {
            if(targets.has(a.name) && !targets.has(b.name)) return -1;
            if(!targets.has(a.name) && targets.has(b.name)) return 1;
            return b.last - a.last;
        });

        sorted.forEach(u => {
            let isTgt = targets.has(u.name);
            let diff = Math.floor((Date.now() - u.last) / 1000);
            let seen = diff < 60 ? "Active now" : `${Math.floor(diff/60)}m ago`;

            let html = `
                <div class="user-row">
                    <img src="${u.icon}" class="u-pic">
                    <div class="u-info">
                        <div class="u-name" style="color:${isTgt ? 'var(--neon-red)' : '#eee'}">${u.name}</div>
                        <div class="u-seen">${seen}</div>
                    </div>
                    <button class="target-btn ${isTgt ? 'active' : ''}" onclick="toggleTgt('${u.name}')">
                        ${isTgt ? 'LOCKED' : 'TRACK'}
                    </button>
                </div>
            `;
            list.insertAdjacentHTML('beforeend', html);
        });
    }

    function toggleTgt(n) {
        if(targets.has(n)) targets.delete(n); else targets.add(n);
        renderRadar();
    }
    
    // Auto-update Last Seen times every minute
    setInterval(renderRadar, 60000);

    function esc(s) { return s ? s.replace(/</g,'&lt;') : ''; }

</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)