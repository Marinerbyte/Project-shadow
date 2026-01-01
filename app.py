from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TITAN OS v6.0</title>
    <link href="https://fonts.googleapis.com/css2?family=Teko:wght@400;500;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* --- 1. CORE THEME & ANIMATIONS --- */
        :root {
            --bg-dark: #050505;
            --panel-bg: rgba(20, 20, 25, 0.7);
            --border: rgba(255, 255, 255, 0.1);
            --neon-blue: #00f3ff;
            --neon-green: #00ff41;
            --neon-red: #ff003c;
            --neon-gold: #ffd700;
            --glass: blur(10px);
            --font-head: 'Teko', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * { box-sizing: border-box; outline: none; -webkit-tap-highlight-color: transparent; user-select: none; }
        
        body {
            background-color: var(--bg-dark);
            color: #e0e0e0;
            font-family: var(--font-mono);
            margin: 0; padding: 0;
            height: 100vh; height: 100dvh;
            display: flex; flex-direction: column;
            overflow: hidden;
            font-size: 13px;
        }

        /* Cyberpunk Grid Background */
        .bg-grid {
            position: fixed; top: 0; left: 0; width: 200vw; height: 200vh;
            background: 
                linear-gradient(rgba(0, 243, 255, 0.03) 1px, transparent 1px), 
                linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px);
            background-size: 40px 40px;
            transform: perspective(500px) rotateX(60deg) translateY(-100px) translateZ(-200px);
            animation: gridMove 20s linear infinite;
            z-index: -1; pointer-events: none;
        }
        @keyframes gridMove { 0% { transform: perspective(500px) rotateX(60deg) translateY(0) translateZ(-200px); } 100% { transform: perspective(500px) rotateX(60deg) translateY(40px) translateZ(-200px); } }

        /* --- 2. HEADER --- */
        header {
            background: rgba(5, 5, 8, 0.9);
            backdrop-filter: var(--glass);
            border-bottom: 1px solid var(--neon-blue);
            padding: 12px 18px;
            display: flex; justify-content: space-between; align-items: center;
            z-index: 100; box-shadow: 0 0 15px rgba(0, 243, 255, 0.15);
        }
        .logo {
            font-family: var(--font-head); font-size: 26px; letter-spacing: 2px;
            color: #fff; text-shadow: 0 0 5px var(--neon-blue);
        }
        .logo span { color: var(--neon-blue); }
        .sys-badge {
            font-size: 10px; background: rgba(255,255,255,0.1); padding: 3px 8px;
            border: 1px solid var(--border); border-radius: 4px;
        }

        /* --- 3. LAYOUT & CARDS --- */
        .viewport {
            flex: 1; overflow-y: auto; padding: 15px; padding-bottom: 100px;
            position: relative;
        }
        .page { display: none; animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .page.active { display: block; }
        @keyframes slideUp { from {opacity:0; transform:translateY(20px);} to {opacity:1; transform:translateY(0);} }

        .card {
            background: var(--panel-bg);
            border: 1px solid var(--border);
            backdrop-filter: var(--glass);
            border-radius: 6px; padding: 15px; margin-bottom: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            position: relative; overflow: hidden;
        }
        .card::before {
            content:''; position: absolute; top:0; left:0; width: 4px; height: 100%;
            background: var(--neon-blue); opacity: 0.5;
        }
        .c-head {
            display: flex; justify-content: space-between; align-items: flex-end;
            border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 8px; margin-bottom: 12px;
        }
        .c-title {
            font-family: var(--font-head); font-size: 20px; color: var(--neon-blue);
            letter-spacing: 1px; text-transform: uppercase;
        }

        /* --- 4. INPUTS & CONTROLS --- */
        input, textarea {
            width: 100%; background: rgba(0,0,0,0.4); border: 1px solid #333;
            color: var(--neon-blue); padding: 12px; font-family: var(--font-mono); font-size: 13px;
            border-radius: 4px; margin-bottom: 10px; transition: 0.3s;
        }
        input:focus, textarea:focus { border-color: var(--neon-blue); box-shadow: 0 0 8px rgba(0,243,255,0.2); }

        .btn {
            width: 100%; padding: 14px; font-family: var(--font-head); font-size: 18px;
            background: linear-gradient(90deg, #111, #1a1a1a);
            border: 1px solid #333; color: #fff; cursor: pointer;
            text-transform: uppercase; letter-spacing: 1px;
            transition: 0.2s; position: relative; overflow: hidden;
        }
        .btn::after { content:''; position:absolute; bottom:0; left:0; width:0%; height:2px; background:var(--neon-blue); transition:0.3s; }
        .btn:hover::after { width: 100%; }
        .btn-go { color: var(--neon-green); border-color: rgba(0,255,65,0.3); }
        .btn-stop { color: var(--neon-red); border-color: rgba(255,0,60,0.3); }

        /* --- 5. AGENT UI --- */
        .agent-item {
            display: flex; align-items: center; background: rgba(0,0,0,0.3);
            border: 1px solid #222; padding: 10px; margin-bottom: 8px;
        }
        .status-led {
            width: 8px; height: 8px; background: #333; border-radius: 50%;
            margin-right: 12px; box-shadow: 0 0 5px #000;
        }
        .online .status-led { background: var(--neon-green); box-shadow: 0 0 8px var(--neon-green); }

        /* --- 6. TARGET OPS UI (NEW & ADVANCED) --- */
        .target-selector {
            display: flex; gap: 10px; overflow-x: auto; padding-bottom: 10px;
            margin-bottom: 15px;
        }
        .t-chip {
            background: #111; border: 1px solid #333; padding: 6px 12px;
            border-radius: 20px; white-space: nowrap; cursor: pointer; color: #888;
            transition: 0.3s;
        }
        .t-chip.active {
            border-color: var(--neon-red); color: var(--neon-red);
            background: rgba(255,0,60,0.1); box-shadow: 0 0 10px rgba(255,0,60,0.2);
        }

        .dossier-grid {
            display: grid; grid-template-columns: 80px 1fr; gap: 15px;
            background: rgba(0,0,0,0.3); padding: 15px; border: 1px solid #333;
            margin-bottom: 15px;
        }
        .t-avatar { width: 80px; height: 80px; border: 2px solid var(--neon-red); object-fit: cover; }
        .t-stat { display: flex; justify-content: space-between; font-size: 12px; color: #666; border-bottom: 1px solid #222; padding: 4px 0; }
        .t-stat b { color: #fff; }

        .timeline {
            position: relative; border-left: 2px solid #333; margin-left: 10px; padding-left: 20px;
        }
        .tl-item {
            position: relative; margin-bottom: 15px; padding: 10px;
            background: rgba(255,255,255,0.03); border-radius: 4px;
            border-left: 2px solid transparent;
        }
        .tl-item::before {
            content: ''; position: absolute; left: -26px; top: 15px;
            width: 10px; height: 10px; background: #111; border: 2px solid #555; border-radius: 50%;
        }
        .tl-item.msg { border-left-color: var(--neon-blue); }
        .tl-item.msg::before { border-color: var(--neon-blue); }
        .tl-item.media { border-left-color: var(--neon-gold); }
        .tl-item.media::before { border-color: var(--neon-gold); }
        .tl-item.alert { border-left-color: var(--neon-red); animation: flashRed 2s infinite; }
        .tl-item.alert::before { background: var(--neon-red); border-color: var(--neon-red); }

        .tl-time { font-size: 10px; color: #666; margin-bottom: 4px; font-family: var(--font-head); letter-spacing: 1px; }
        .tl-content { font-size: 13px; color: #ddd; word-break: break-all; }

        /* --- 7. NAVIGATION --- */
        .nav-bar {
            position: fixed; bottom: 0; left: 0; right: 0; height: 70px;
            background: rgba(5,5,8,0.95); border-top: 1px solid #333;
            backdrop-filter: blur(15px); display: flex; justify-content: space-around;
            align-items: center; z-index: 200;
        }
        .nav-btn {
            display: flex; flex-direction: column; align-items: center; gap: 4px;
            color: #444; transition: 0.3s; padding: 10px;
        }
        .nav-btn i { font-size: 20px; font-style: normal; }
        .nav-btn span { font-size: 10px; font-family: var(--font-head); letter-spacing: 1px; }
        .nav-btn.active { color: var(--neon-blue); text-shadow: 0 0 10px rgba(0,243,255,0.4); transform: translateY(-5px); }
        .nav-btn.tgt-active { color: var(--neon-red); text-shadow: 0 0 10px rgba(255,0,60,0.4); }

        /* ALARM ANIMATION */
        @keyframes flashRed { 0% {background: rgba(255,0,60,0.1);} 50% {background: rgba(255,0,60,0.0);} 100% {background: rgba(255,0,60,0.1);} }
        .screen-flash {
            position: fixed; inset: 0; pointer-events: none; z-index: 999;
            box-shadow: inset 0 0 50px var(--neon-red); opacity: 0; transition: 0.3s;
        }
        .screen-flash.active { opacity: 1; animation: flashBorder 1s infinite; }
        @keyframes flashBorder { 0%, 100% {box-shadow: inset 0 0 50px var(--neon-red);} 50% {box-shadow: inset 0 0 100px var(--neon-red);} }

    </style>
</head>
<body>

<div class="bg-grid"></div>
<div class="screen-flash" id="alertFlash"></div>

<header>
    <div class="logo">TITAN <span>OS</span></div>
    <div class="sys-badge" id="sysStatus">OFFLINE</div>
</header>

<div class="viewport">
    
    <!-- 1. DEPLOYMENT -->
    <div id="p-deploy" class="page active">
        <div class="card">
            <div class="c-head">
                <span class="c-title">NETWORK INFILTRATION</span>
                <span style="font-size:10px; color:#666">MODULE 01</span>
            </div>
            <label style="color:var(--neon-blue); font-size:10px;">TARGET ROOM</label>
            <input type="text" id="room" value="ملتقى🥂العرب">
            
            <label style="color:var(--neon-blue); font-size:10px;">BOTNET CREDENTIALS (User#Pass)</label>
            <textarea id="accs" rows="3" placeholder="Spy1#pass123@Spy2#pass456"></textarea>
            
            <button class="btn btn-go" onclick="deployAgents()">INITIATE CONNECTION</button>
        </div>

        <div class="card">
            <div class="c-head"><span class="c-title">ACTIVE AGENTS</span></div>
            <div id="agentList" style="min-height: 50px; color:#444; text-align:center; padding:10px;">
                SYSTEM STANDBY
            </div>
        </div>
    </div>

    <!-- 2. TARGET OPS (NEW UI) -->
    <div id="p-targets" class="page">
        <div class="card" style="border-color: var(--neon-red);">
            <div class="c-head">
                <span class="c-title" style="color:var(--neon-red)">TARGET SURVEILLANCE</span>
                <span style="font-size:10px; color:var(--neon-red)">PRIORITY CLASS A</span>
            </div>
            
            <!-- Selector -->
            <div class="target-selector" id="targetSelect">
                <!-- Chips added via JS -->
                <div style="color:#666; font-size:12px; padding:10px;">No targets locked in Radar.</div>
            </div>

            <!-- Target Dossier (Hidden until selected) -->
            <div id="targetView" style="display:none;">
                <div class="dossier-grid">
                    <img id="t-img" src="" class="t-avatar">
                    <div>
                        <div class="t-stat"><span>CODENAME</span> <b id="t-name">UNKNOWN</b></div>
                        <div class="t-stat"><span>STATUS</span> <b id="t-status" style="color:var(--neon-green)">ONLINE</b></div>
                        <div class="t-stat"><span>MSG COUNT</span> <b id="t-count">0</b></div>
                        <div class="t-stat"><span>LAST SEEN</span> <b id="t-seen">NOW</b></div>
                    </div>
                </div>

                <div style="font-family:var(--font-head); color:#888; font-size:16px; margin-bottom:10px;">ACTIVITY LOG</div>
                <div class="timeline" id="targetTimeline">
                    <!-- Logs go here -->
                </div>
            </div>
        </div>
    </div>

    <!-- 3. RADAR LIST -->
    <div id="p-radar" class="page">
        <div class="card">
            <div class="c-head">
                <span class="c-title">GLOBAL SONAR</span>
                <span id="uCount" style="color:#fff; font-family:var(--font-mono)">0</span>
            </div>
            <div id="radarList"></div>
        </div>
    </div>

    <!-- 4. FEED -->
    <div id="p-feed" class="page">
        <div class="card">
            <div class="c-head"><span class="c-title">RAW DATA STREAM</span></div>
            <div id="feedBox" style="font-size:12px;"></div>
        </div>
    </div>

</div>

<!-- NAV -->
<div class="nav-bar">
    <div class="nav-btn active" onclick="nav('p-deploy', this)"><i>⚙️</i><span>SYSTEM</span></div>
    <div class="nav-btn" onclick="nav('p-radar', this)"><i>📡</i><span>RADAR</span></div>
    <div class="nav-btn tgt-active" onclick="nav('p-targets', this)"><i>🎯</i><span>TARGETS</span></div>
    <div class="nav-btn" onclick="nav('p-feed', this)"><i>💬</i><span>FEED</span></div>
</div>

<script>
    // --- STATE MANAGEMENT ---
    let bots = [];
    let users = new Map(); // All users seen
    let targets = new Set(); // Names of targets
    let targetLogs = {}; // Key: Name, Value: Array of events
    let currentTargetView = null;
    const WS_URL = "wss://chatp.net:5333/server";

    // --- SOUND ENGINE ---
    const audCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    function playSound(type) {
        if(audCtx.state === 'suspended') audCtx.resume();
        let osc = audCtx.createOscillator();
        let gain = audCtx.createGain();
        osc.connect(gain);
        gain.connect(audCtx.destination);
        
        if(type === 'alert') {
            osc.frequency.setValueAtTime(800, audCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(400, audCtx.currentTime + 0.2);
            gain.gain.setValueAtTime(0.5, audCtx.currentTime);
            osc.start(); osc.stop(audCtx.currentTime + 0.3);
            if(navigator.vibrate) navigator.vibrate([200, 100, 200]);
        } else {
            // Blip
            osc.frequency.setValueAtTime(1200, audCtx.currentTime);
            gain.gain.setValueAtTime(0.05, audCtx.currentTime);
            osc.type = 'sine';
            osc.start(); osc.stop(audCtx.currentTime + 0.05);
        }
    }

    // --- SYSTEM LOGIC ---
    function nav(pid, el) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(pid).classList.add('active');
        if(el) el.classList.add('active');
        
        // Refresh views
        if(pid === 'p-targets') renderTargetSelector();
    }

    function genId() { return Math.random().toString(36).substr(2, 8); }
    function esc(s) { return s ? s.replace(/</g,'&lt;') : ''; }
    function getTime() { return new Date().toLocaleTimeString('en-US', {hour12:false}); }

    // --- DEPLOYMENT ---
    function deployAgents() {
        let raw = document.getElementById("accs").value;
        let room = document.getElementById("room").value;
        if(!raw.includes("#")) { alert("ERR: INVALID FORMAT"); return; }
        
        document.getElementById('agentList').innerHTML = "";
        bots = raw.split("@").filter(s => s.includes("#"));
        
        bots.forEach((creds, i) => {
            setTimeout(() => {
                let [u, p] = creds.split("#");
                startBot(u.trim(), p.trim(), room, i);
            }, i * 1000);
        });
        document.getElementById('sysStatus').innerText = "SYSTEM ACTIVE";
        document.getElementById('sysStatus').style.color = "var(--neon-green)";
        document.getElementById('sysStatus').style.borderColor = "var(--neon-green)";
    }

    function startBot(user, pass, room, i) {
        let div = document.createElement('div');
        div.className = 'agent-item';
        div.id = `bot-ui-${i}`;
        div.innerHTML = `<div class="status-led"></div><div><div style="color:#fff; font-weight:bold">${user}</div><div style="font-size:10px; color:#666" id="stat-${i}">CONNECTING...</div></div>`;
        document.getElementById('agentList').appendChild(div);

        let ws = new WebSocket(WS_URL);
        
        ws.onopen = () => {
            ws.send(JSON.stringify({ handler: "login", id: genId(), username: user, password: pass }));
        };

        ws.onmessage = (e) => {
            let d = JSON.parse(e.data);
            
            // Login Success
            if(d.handler === "login_event" && d.type === "success") {
                ws.send(JSON.stringify({ handler: "room_join", id: genId(), name: room }));
                document.getElementById(`stat-${i}`).innerText = "AUTHENTICATED";
            }
            
            // Room Joined
            if(d.handler === "room_event" && d.type === "room_joined") {
                document.getElementById(`bot-ui-${i}`).classList.add('online');
                document.getElementById(`stat-${i}`).innerText = `MONITORING: ${room}`;
                document.getElementById(`stat-${i}`).style.color = "var(--neon-green)";
            }

            // CORE PACKET PROCESSOR
            processPacket(d);
        };
    }

    // --- INTELLIGENCE CORE ---
    function processPacket(d) {
        let now = Date.now();
        let user = d.username || d.from;
        
        // 1. Update Global User Database
        if(user) {
            let existing = users.get(user) || { firstSeen: now, msgs: 0, icon: '' };
            existing.lastSeen = now;
            if(d.icon || d.avatar_url) existing.icon = d.icon || d.avatar_url;
            
            // Count messages
            if(d.type === 'text' || d.type === 'image') existing.msgs++;
            
            users.set(user, existing);
            updateRadarRow(user); // Live update radar
        }

        // 2. Target Logic
        if(user && targets.has(user)) {
            handleTargetEvent(user, d);
        }

        // 3. Raw Feed
        if(d.type === "text") renderFeed(user, d.body, false);
    }

    // --- TARGET OPS LOGIC ---
    function toggleTarget(name) {
        if(targets.has(name)) {
            targets.delete(name);
        } else {
            targets.add(name);
            if(!targetLogs[name]) targetLogs[name] = [];
            // Log the tracking start
            targetLogs[name].push({ type: 'sys', body: 'TRACKING INITIATED', time: getTime() });
        }
        renderRadar();
        renderTargetSelector();
    }

    function handleTargetEvent(name, d) {
        // Trigger Alarm
        let flash = document.getElementById('alertFlash');
        flash.classList.add('active');
        playSound('alert');
        setTimeout(() => flash.classList.remove('active'), 2000);

        // Log Data
        let event = { time: getTime(), type: 'unknown', body: '' };

        if(d.type === 'text') {
            event.type = 'msg';
            event.body = d.body;
        } else if (d.type === 'image') {
            event.type = 'media';
            event.body = `<img src="https://chatp.net${d.url}" style="max-height:100px; border-radius:4px; border:1px solid #444">`;
        } else if (d.handler === 'room_event' && d.type === 'room_joined') {
            event.type = 'alert';
            event.body = "TARGET ENTERED ROOM";
        }

        targetLogs[name].push(event);

        // Update UI if viewing this target
        if(currentTargetView === name) {
            renderTargetDossier(name);
        }
    }

    // --- UI RENDERERS ---

    function renderRadar() {
        let list = document.getElementById("radarList");
        list.innerHTML = "";
        document.getElementById("uCount").innerText = users.size;

        // Sort: Targets first, then recent
        let sorted = [...users.keys()].sort((a,b) => {
            if(targets.has(a) && !targets.has(b)) return -1;
            if(!targets.has(a) && targets.has(b)) return 1;
            return users.get(b).lastSeen - users.get(a).lastSeen;
        });

        sorted.forEach(name => {
            let u = users.get(name);
            let isTgt = targets.has(name);
            let html = `
                <div class="agent-item" style="border-left: 3px solid ${isTgt ? 'var(--neon-red)' : 'transparent'}">
                    <img src="${u.icon || 'https://ui-avatars.com/api/?name='+name}" style="width:30px; height:30px; border-radius:50%; margin-right:10px;">
                    <div style="flex:1">
                        <div style="color:${isTgt ? 'var(--neon-red)' : '#fff'}; font-weight:bold">${name}</div>
                        <div style="font-size:10px; color:#666">${Math.floor((Date.now()-u.lastSeen)/1000)}s ago</div>
                    </div>
                    <button class="btn" style="width:auto; padding:5px 10px; font-size:12px; border-color:${isTgt?'var(--neon-red)':'#444'}" onclick="toggleTarget('${name}')">
                        ${isTgt ? 'LOCK' : 'TRACK'}
                    </button>
                </div>
            `;
            list.insertAdjacentHTML('beforeend', html);
        });
    }

    // Optimization: Just update time/sort roughly every few seconds
    setInterval(renderRadar, 5000);
    function updateRadarRow(name) { /* Helper for smoother live updates, simplified here */ }

    // --- NEW TARGET UI RENDERER ---
    function renderTargetSelector() {
        let box = document.getElementById("targetSelect");
        if(targets.size === 0) {
            box.innerHTML = `<div style="padding:10px; color:#666; font-size:12px;">NO TARGETS LOCKED. GO TO RADAR.</div>`;
            document.getElementById("targetView").style.display = 'none';
            return;
        }
        
        box.innerHTML = "";
        targets.forEach(t => {
            let chip = document.createElement("div");
            chip.className = `t-chip ${currentTargetView === t ? 'active' : ''}`;
            chip.innerText = t;
            chip.onclick = () => { currentTargetView = t; renderTargetSelector(); renderTargetDossier(t); };
            box.appendChild(chip);
        });

        if(currentTargetView && targets.has(currentTargetView)) {
            renderTargetDossier(currentTargetView);
        }
    }

    function renderTargetDossier(name) {
        document.getElementById("targetView").style.display = 'block';
        let u = users.get(name);
        let logs = targetLogs[name] || [];

        // Header Stats
        document.getElementById("t-name").innerText = name;
        document.getElementById("t-img").src = u.icon || `https://ui-avatars.com/api/?name=${name}`;
        document.getElementById("t-count").innerText = u.msgs;
        document.getElementById("t-seen").innerText = new Date(u.lastSeen).toLocaleTimeString();

        // Timeline
        let tl = document.getElementById("targetTimeline");
        tl.innerHTML = "";
        
        // Reverse logs to show newest first
        [...logs].reverse().forEach(log => {
            let html = `
                <div class="tl-item ${log.type}">
                    <div class="tl-time">${log.time}</div>
                    <div class="tl-content">${log.body}</div>
                </div>
            `;
            tl.insertAdjacentHTML('beforeend', html);
        });
    }

    function renderFeed(u, txt, isImg) {
        let box = document.getElementById("feedBox");
        let html = `
            <div style="margin-bottom:8px; border-bottom:1px solid #222; padding-bottom:4px;">
                <span style="color:var(--neon-blue); font-weight:bold">${u}: </span>
                <span style="color:#bbb">${esc(txt)}</span>
            </div>
        `;
        box.insertAdjacentHTML('afterbegin', html); // Newest top
        if(box.childElementCount > 50) box.lastElementChild.remove();
    }

</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)