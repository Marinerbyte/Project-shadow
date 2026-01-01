from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>PROJECT SHADOW 3D</title>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        /* --- 1. THEME & RESET --- */
        :root {
            --bg-dark: #050505;
            --glass: rgba(255, 255, 255, 0.08);
            --glass-border: rgba(255, 255, 255, 0.15);
            --neon-blue: #00f3ff;
            --neon-pink: #ff0055;
            --neon-green: #00ff66;
            --text-main: #ffffff;
            --text-dim: #a0a0a0;
            --shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        * { box-sizing: border-box; outline: none; -webkit-tap-highlight-color: transparent; }

        body {
            background: linear-gradient(135deg, #09090b 0%, #110e1b 100%);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            margin: 0; padding: 0;
            height: 100vh; overflow: hidden;
            display: flex; flex-direction: column;
        }

        /* --- 2. 3D HEADER --- */
        header {
            background: rgba(10, 10, 10, 0.8);
            backdrop-filter: blur(12px);
            padding: 15px 20px;
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--glass-border);
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            z-index: 100;
        }
        .logo { 
            font-family: 'Rajdhani', sans-serif; font-size: 22px; font-weight: 700; 
            letter-spacing: 2px; 
            background: linear-gradient(90deg, var(--neon-blue), #fff);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .status-badge {
            font-size: 10px; font-weight: bold; padding: 5px 10px;
            border-radius: 20px; background: rgba(255,255,255,0.05);
            border: 1px solid var(--glass-border);
            display: flex; align-items: center; gap: 6px;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.5);
        }
        .dot { width: 8px; height: 8px; border-radius: 50%; background: #444; transition: 0.3s; }
        .dot.active { background: var(--neon-green); box-shadow: 0 0 8px var(--neon-green); }

        /* --- 3. MAIN CONTENT AREA --- */
        .container {
            flex: 1; overflow-y: auto; padding: 20px;
            position: relative;
            scroll-behavior: smooth;
        }
        
        .page { 
            display: none; animation: slideUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
        }
        .page.active { display: block; }

        @keyframes slideUp { 
            from { opacity: 0; transform: translateY(20px); } 
            to { opacity: 1; transform: translateY(0); } 
        }

        /* --- 4. GLASS CARDS & INPUTS --- */
        .glass-card {
            background: var(--glass);
            backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
            position: relative; overflow: hidden;
        }
        .glass-card::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        }

        label { 
            font-size: 11px; color: var(--neon-blue); text-transform: uppercase; 
            letter-spacing: 1px; font-weight: bold; margin-bottom: 5px; display: block;
        }

        input, textarea {
            width: 100%; background: rgba(0,0,0,0.3); border: 1px solid #333;
            color: #fff; padding: 12px; border-radius: 8px; margin-bottom: 15px;
            font-family: 'Inter', sans-serif; transition: 0.3s;
        }
        input:focus, textarea:focus {
            border-color: var(--neon-blue); box-shadow: 0 0 10px rgba(0, 243, 255, 0.2);
        }

        /* --- 5. 3D BUTTONS --- */
        .btn-3d {
            width: 100%; padding: 14px; border: none; border-radius: 10px;
            font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
            cursor: pointer; position: relative; overflow: hidden;
            transition: transform 0.1s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #0066ff, #00ccff);
            color: white; box-shadow: 0 4px 15px rgba(0, 100, 255, 0.4);
        }
        .btn-danger {
            background: linear-gradient(135deg, #ff0055, #ff4444);
            color: white; box-shadow: 0 4px 15px rgba(255, 0, 85, 0.4);
        }
        .btn-3d:active { transform: scale(0.97); }

        /* --- 6. CHAT BUBBLES --- */
        .chat-container { padding-bottom: 80px; }
        .msg-bubble {
            background: rgba(30,30,40,0.6);
            border-left: 3px solid var(--glass-border);
            padding: 10px 15px; border-radius: 0 12px 12px 0;
            margin-bottom: 10px; position: relative;
            animation: fadeIn 0.3s;
        }
        .msg-alert {
            background: rgba(255, 0, 85, 0.1);
            border-left: 3px solid var(--neon-pink);
        }
        .msg-meta { font-size: 10px; color: var(--text-dim); display: flex; justify-content: space-between; margin-bottom: 4px; }
        .msg-user { font-weight: bold; color: var(--neon-green); font-family: 'Rajdhani', sans-serif; font-size: 13px; }
        .msg-text { font-size: 13px; line-height: 1.4; color: #eee; }
        
        /* DELETED MSG STYLING */
        .del-stripe { text-decoration: line-through; opacity: 0.6; }
        .del-badge { font-size: 9px; background: var(--neon-pink); color: white; padding: 2px 4px; border-radius: 4px; margin-left: 5px; }

        /* --- 7. VAULT GRID --- */
        .media-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .m-card { 
            border-radius: 12px; overflow: hidden; position: relative; 
            border: 1px solid var(--glass-border); aspect-ratio: 1;
        }
        .m-card img { width: 100%; height: 100%; object-fit: cover; }
        .m-overlay {
            position: absolute; bottom: 0; left: 0; width: 100%;
            background: linear-gradient(to top, #000, transparent);
            padding: 10px 5px; font-size: 10px; text-align: center; color: #fff;
        }

        /* --- 8. RADAR USER LIST --- */
        .user-card {
            display: flex; align-items: center; justify-content: space-between;
            background: rgba(255,255,255,0.03); padding: 10px;
            border-radius: 10px; margin-bottom: 8px; border: 1px solid transparent;
        }
        .user-card:hover { border-color: var(--neon-blue); background: rgba(0, 243, 255, 0.05); }
        .u-pic { 
            width: 36px; height: 36px; border-radius: 50%; 
            border: 2px solid var(--glass-border); margin-right: 12px; 
        }
        .tag-btn {
            background: transparent; border: 1px solid var(--text-dim);
            color: var(--text-dim); font-size: 10px; padding: 5px 10px;
            border-radius: 20px; cursor: pointer;
        }
        .tag-btn.locked { 
            border-color: var(--neon-pink); color: var(--neon-pink); 
            background: rgba(255, 0, 85, 0.1); 
        }

        /* --- 9. BOTTOM NAV (APP STYLE) --- */
        .bottom-nav {
            position: fixed; bottom: 20px; left: 20px; right: 20px;
            background: rgba(15, 15, 20, 0.9);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            display: flex; justify-content: space-around;
            padding: 15px;
            border: 1px solid var(--glass-border);
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
            z-index: 1000;
        }
        .nav-item {
            text-align: center; color: var(--text-dim); opacity: 0.6;
            transition: 0.3s; cursor: pointer;
            font-size: 20px;
        }
        .nav-item.active { 
            opacity: 1; color: var(--neon-blue); transform: translateY(-5px); 
            text-shadow: 0 0 10px var(--neon-blue);
        }
        .nav-label { font-size: 9px; display: block; margin-top: 4px; font-weight: bold; }

    </style>
</head>
<body>

<!-- HEADER -->
<header>
    <div class="logo">SHADOW <span style="font-weight:400; font-size:14px; color:var(--text-dim);">UI 2.0</span></div>
    <div class="status-badge">
        <div class="dot" id="statusDot"></div>
        <span id="statusTxt">DISCONNECTED</span>
    </div>
</header>

<!-- MAIN SCROLL AREA -->
<div class="container">

    <!-- 1. FEED -->
    <div id="feed" class="page active">
        <div class="glass-card" style="padding:10px; display:flex; gap:10px; align-items:center;">
            <input type="text" id="filter" placeholder="Search logs..." onkeyup="filterFeed()" style="margin:0;">
            <div style="font-size:20px; cursor:pointer;" onclick="dlLogs()">💾</div>
        </div>
        <div id="chatFeed" class="chat-container"></div>
    </div>

    <!-- 2. VAULT -->
    <div id="vault" class="page">
        <h3 style="margin-top:0; color:var(--neon-blue)">CAPTURED MEDIA <span style="font-size:12px; color:#fff" id="mediaCnt">(0)</span></h3>
        <div id="mediaGrid" class="media-grid"></div>
    </div>

    <!-- 3. RADAR -->
    <div id="radar" class="page">
        <div class="glass-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <span>ONLINE USERS</span>
                <span style="color:var(--neon-green)" id="userCnt">0</span>
            </div>
            <div id="userList"></div>
        </div>
        <div style="font-size:10px; color:var(--text-dim); text-align:center; margin-top:10px;">ACTIVITY LOG</div>
        <div id="activityLog" style="font-size:10px; color:#777; padding:10px;"></div>
    </div>

    <!-- 4. SETUP -->
    <div id="cfg" class="page">
        <div class="glass-card">
            <label>TARGET ROOM</label>
            <input type="text" id="room" value="ملتقى🥂العرب">
            
            <label>STEALTH ACCOUNTS (User#Pass)</label>
            <textarea id="accs" placeholder="Agent1#pass123@Agent2#pass456"></textarea>
            
            <label>KEYWORDS (Alerts)</label>
            <input type="text" id="keywords" placeholder="name, number, admin...">

            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; margin-top:10px;">
                <button class="btn-3d btn-primary" onclick="startShadow()">ACTIVATE</button>
                <button class="btn-3d btn-danger" onclick="stopShadow()">DETACH</button>
            </div>
        </div>
        <div style="text-align:center; font-size:10px; color:#444; margin-top:20px;">
            PROJECT SHADOW | CLIENT-SIDE ENCRYPTION
        </div>
    </div>

</div>

<!-- BOTTOM NAVIGATION -->
<div class="bottom-nav">
    <div class="nav-item active" onclick="setTab('feed', this)">
        <span>👻</span><span class="nav-label">FEED</span>
    </div>
    <div class="nav-item" onclick="setTab('vault', this)">
        <span>📸</span><span class="nav-label">VAULT</span>
    </div>
    <div class="nav-item" onclick="setTab('radar', this)">
        <span>📡</span><span class="nav-label">RADAR</span>
    </div>
    <div class="nav-item" onclick="setTab('cfg', this)">
        <span>⚙️</span><span class="nav-label">SETUP</span>
    </div>
</div>

<script>
    // --- VARIABLES ---
    let sockets = [];
    let users = new Map();
    let logs = [];
    let mediaCount = 0;
    let targets = new Set();
    const WS_URL = "wss://chatp.net:5333/server"; 

    // --- UI FUNCTIONS ---
    function setTab(id, el) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        el.classList.add('active');
    }

    function updateStatus(isOnline) {
        let dot = document.getElementById('statusDot');
        let txt = document.getElementById('statusTxt');
        if(isOnline) {
            dot.classList.add('active'); txt.innerText = "MONITORING ACTIVE"; txt.style.color = "var(--neon-green)";
        } else {
            dot.classList.remove('active'); txt.innerText = "DISCONNECTED"; txt.style.color = "#777";
        }
    }

    function genId() { return Math.random().toString(36).substr(2, 9); }
    function esc(s) { return s ? s.replace(/</g,'&lt;') : ''; }
    
    // --- CORE LOGIC ---
    function startShadow() {
        if(sockets.length > 0) return;
        let raw = document.getElementById("accs").value;
        let room = document.getElementById("room").value;
        if(!raw.includes("#")) { alert("Format: User#Pass"); return; }
        
        let accs = raw.split("@").filter(s => s.includes("#"));
        accs.forEach((acc, i) => {
            let [u, p] = acc.split("#");
            setTimeout(() => connectBot(u.trim(), p.trim(), room), i * 1500);
        });
        updateStatus(true);
    }

    function stopShadow() {
        sockets.forEach(s => s.close()); sockets = []; updateStatus(false);
    }

    function connectBot(user, pass, room) {
        let ws = new WebSocket(WS_URL);
        ws.onopen = () => {
            ws.send(JSON.stringify({ handler: "login", id: genId(), username: user, password: pass }));
        };
        ws.onmessage = (e) => {
            let d = JSON.parse(e.data);
            if(d.handler === "login_event" && d.type === "success") {
                ws.send(JSON.stringify({ handler: "room_join", id: genId(), name: room }));
            }
            if(d.handler === "room_event") handleEvent(d);
            if((d.handler === "roster" || d.handler === "room_users") && d.users) {
                d.users.forEach(u => updateUser(u)); renderUsers();
            }
        };
        sockets.push(ws);
    }

    // --- DATA HANDLING ---
    function handleEvent(d) {
        let time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

        if(d.type === "text") {
            processMsg(d.from, d.body, d.id, time);
            if(d.body.match(/\.(jpg|png|gif|webp)/i)) {
                let url = d.body.match(/http[^\s]+/);
                if(url) addMedia(url[0], d.from);
            }
        }
        if(d.type === "image") {
            addMedia(d.url || d.body, d.from);
            processMsg(d.from, "📷 [SENT PHOTO]", d.id, time);
        }
        if(d.type === "delete" || d.type === "remove") {
            markDeleted(d.messageId || d.id);
        }
        if(d.type === "join") { updateUser(d); logAct(d.username, "JOINED", "#0f0"); }
        if(d.type === "leave") { users.delete(d.username); renderUsers(); logAct(d.username, "LEFT", "#f00"); }
    }

    // --- RENDERERS ---
    function processMsg(user, txt, id, time) {
        let keys = document.getElementById("keywords").value.split(",");
        let isAlert = keys.some(k => k.trim() && txt.toLowerCase().includes(k.trim().toLowerCase()));
        
        let feed = document.getElementById("chatFeed");
        logs.push(`[${time}] ${user}: ${txt}`);

        let html = `
            <div class="msg-bubble ${isAlert ? 'msg-alert' : ''}" id="msg-${id}">
                <div class="msg-meta">
                    <span class="msg-user">${user}</span>
                    <span>${time}</span>
                </div>
                <div class="msg-text">${esc(txt)}</div>
            </div>
        `;
        feed.insertAdjacentHTML('beforeend', html);
        feed.scrollTop = feed.scrollHeight;
    }

    function addMedia(url, user) {
        if(!url.startsWith("http")) url = "https://chatp.net" + url;
        mediaCount++;
        document.getElementById("mediaCnt").innerText = `(${mediaCount})`;
        let html = `
            <div class="m-card">
                <a href="${url}" target="_blank"><img src="${url}"></a>
                <div class="m-overlay">${user}</div>
            </div>`;
        document.getElementById("mediaGrid").insertAdjacentHTML('afterbegin', html);
    }

    function markDeleted(id) {
        let el = document.getElementById("msg-" + id);
        if(el) {
            el.querySelector(".msg-text").classList.add("del-stripe");
            el.querySelector(".msg-meta").innerHTML += `<span class="del-badge">DELETED</span>`;
        }
    }

    function updateUser(u) {
        let name = u.username || u.name;
        if(!users.has(name)) {
            users.set(name, {
                name: name,
                icon: u.avatar_url || u.icon || `https://ui-avatars.com/api/?name=${name}&background=00f3ff&color=fff`
            });
            renderUsers();
        }
    }

    function renderUsers() {
        let list = document.getElementById("userList");
        list.innerHTML = "";
        document.getElementById("userCnt").innerText = users.size;

        users.forEach(u => {
            let isTgt = targets.has(u.name);
            let html = `
                <div class="user-card">
                    <div style="display:flex; align-items:center;">
                        <img src="${u.icon}" class="u-pic">
                        <span style="font-weight:bold; color:#fff;">${u.name}</span>
                    </div>
                    <button class="tag-btn ${isTgt?'locked':''}" onclick="toggleTgt('${u.name}')">
                        ${isTgt ? 'LOCKED' : 'TRACK'}
                    </button>
                </div>
            `;
            list.appendChild(document.createRange().createContextualFragment(html));
        });
    }

    function toggleTgt(name) {
        if(targets.has(name)) targets.delete(name);
        else targets.add(name);
        renderUsers();
    }

    function logAct(u, act, col) {
        let b = document.getElementById("activityLog");
        b.insertAdjacentHTML('afterbegin', `<div><span style="color:${col}">${u}</span> ${act}</div>`);
    }

    function dlLogs() {
        let blob = new Blob([logs.join("\\n")], {type: "text/plain"});
        let a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "SHADOW_LOGS.txt";
        a.click();
    }
    
    function filterFeed() {
        let q = document.getElementById("filter").value.toLowerCase();
        document.querySelectorAll(".msg-bubble").forEach(row => {
            row.style.display = row.innerText.toLowerCase().includes(q) ? "block" : "none";
        });
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