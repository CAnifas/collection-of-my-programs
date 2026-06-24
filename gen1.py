f = open("desktop.html", "w", encoding="utf-8")

css = """
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
body{font-family:"Inter",sans-serif;background:#0a0a1a;width:100vw;height:100vh;overflow:hidden;user-select:none;cursor:default;}
.desktop{width:100%;height:calc(100% - 44px);position:relative;background:radial-gradient(ellipse at 20% 30%,#0d1b3e,#050c1a 70%);}
.taskbar{position:fixed;bottom:0;left:0;right:0;height:44px;background:rgba(10,10,25,0.97);border-top:1px solid rgba(255,255,255,0.07);display:flex;align-items:center;padding:0 12px;gap:6px;z-index:9999;}
.tb-btn{display:flex;align-items:center;gap:6px;padding:5px 12px;border-radius:8px;cursor:pointer;font-size:12px;font-weight:500;color:rgba(255,255,255,0.45);border:1px solid transparent;transition:all 0.2s;}
.tb-btn:hover{background:rgba(255,255,255,0.07);color:rgba(255,255,255,0.85);}
.tb-open{background:rgba(255,255,255,0.08);color:#fff;border-color:rgba(255,255,255,0.1);}
.tb-active{border-color:rgba(99,210,150,0.4)!important;color:#63d296!important;}
.tb-sep{width:1px;height:24px;background:rgba(255,255,255,0.07);}
.tb-time{margin-left:auto;font-size:12px;color:rgba(255,255,255,0.35);padding:0 10px;}
.aw{position:absolute;display:flex;flex-direction:column;background:linear-gradient(160deg,#1a1a2e,#16213e);border-radius:12px;border:1px solid rgba(255,255,255,0.08);box-shadow:0 20px 60px rgba(0,0,0,0.7),0 0 0 1px rgba(100,120,255,0.07);overflow:hidden;}
.aw.focused{box-shadow:0 25px 70px rgba(0,0,0,0.8),0 0 0 1px rgba(99,210,150,0.12);}
.aw.minimized{display:none;}
.wbar{display:flex;align-items:center;gap:10px;padding:11px 14px;background:rgba(255,255,255,0.03);border-bottom:1px solid rgba(255,255,255,0.06);cursor:grab;flex-shrink:0;}
.wbar:active{cursor:grabbing;}
.wdots{display:flex;gap:7px;}
.wd{width:12px;height:12px;border-radius:50%;border:none;cursor:pointer;transition:filter 0.2s;}
.wd:hover{filter:brightness(1.3);}
.wr{background:#ff5f57;}.wy{background:#febc2e;}.wg{background:#28c840;}
.wtitle{font-size:12px;font-weight:600;color:rgba(255,255,255,0.7);display:flex;align-items:center;gap:6px;}
.wicon{font-size:15px;}
.wbody{flex:1;overflow:hidden;display:flex;}
.panel{background:rgba(255,255,255,0.04);border-radius:8px;border:1px solid rgba(255,255,255,0.07);padding:12px;}
.plbl{font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:8px;}
.sled{width:8px;height:8px;border-radius:50%;flex-shrink:0;animation:lp 2s ease-in-out infinite;}
.sled.on{background:#00e676;box-shadow:0 0 6px rgba(0,230,118,0.7);}
.sled.wait{background:#ffab00;box-shadow:0 0 6px rgba(255,171,0,0.7);}
.sled.off{background:#ff5252;box-shadow:0 0 6px rgba(255,82,82,0.7);animation:none;}
@keyframes lp{0%,100%{opacity:1;}50%{opacity:0.3;}}
.strow{display:flex;align-items:center;gap:8px;}
.stm{font-size:12px;font-weight:600;color:#e8e8ff;}
.sts{font-size:10px;color:rgba(255,255,255,0.35);margin-top:2px;}
.plrow{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05);border-radius:5px;transition:all 0.2s;}
.plrow:last-child{border-bottom:none;padding-bottom:0;}
.plat{background:rgba(99,210,150,0.08);padding-left:5px;}
.plat .plnm{color:#63d296;}
.av{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0;}
.avw{background:linear-gradient(135deg,#f0e8d0,#d4c4a0);}
.avb{background:linear-gradient(135deg,#2a2a4a,#1a1a2e);border:1.5px solid rgba(255,255,255,0.12);}
.plnm{font-size:11px;font-weight:600;color:#e2e8ff;}
.plcl{font-size:9px;color:rgba(255,255,255,0.3);}
.dg{display:flex;gap:5px;}
.dbtn{flex:1;padding:5px 3px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:6px;color:rgba(255,255,255,0.4);font-size:9px;font-weight:600;cursor:pointer;transition:all 0.2s;font-family:inherit;}
.dbtn:hover{color:rgba(255,255,255,0.7);border-color:rgba(255,255,255,0.2);}
.da{background:linear-gradient(135deg,#5b3cf5,#9b59f7);border-color:transparent!important;color:#fff!important;}
.capln{font-size:15px;letter-spacing:-1px;min-height:20px;}
.hists{max-height:90px;overflow-y:auto;scrollbar-width:thin;scrollbar-color:rgba(255,255,255,0.1) transparent;}
.hrow{display:flex;gap:3px;margin-bottom:2px;}
.hnum{font-size:9px;color:rgba(255,255,255,0.2);width:18px;flex-shrink:0;}
.hcl{flex:1;font-size:10px;color:rgba(255,255,255,0.5);padding:1px 4px;border-radius:3px;font-family:monospace;}
.hl{color:#63d296;background:rgba(99,210,150,0.08);}
.ngbtn{width:100%;padding:9px;background:linear-gradient(135deg,#5b3cf5,#9b59f7);border:none;border-radius:7px;color:#fff;font-size:11px;font-weight:700;cursor:pointer;font-family:inherit;transition:all 0.2s;}
.ngbtn:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(91,60,245,0.5);}
.clay{display:flex;gap:12px;padding:14px;align-items:flex-start;}
.bwrap{display:flex;align-items:center;gap:4px;}
.rlbls{display:flex;flex-direction:column;}
.rlbl{width:16px;height:60px;display:flex;align-items:center;justify-content:flex-end;padding-right:4px;font-size:10px;color:rgba(255,255,255,0.3);font-weight:600;}
.bcol{display:flex;flex-direction:column;}
.cbd{display:grid;grid-template-columns:repeat(8,60px);grid-template-rows:repeat(8,60px);border-radius:4px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.6),0 0 0 2px rgba(100,120,255,0.12);position:relative;}
.flbls{display:flex;margin-top:3px;}
.flbl{width:60px;text-align:center;font-size:10px;color:rgba(255,255,255,0.3);font-weight:600;}
.csq{width:60px;height:60px;display:flex;align-items:center;justify-content:center;position:relative;cursor:pointer;}
.csq.clt{background:#e8d5b7;}.csq.cdk{background:#b58863;}
.csq.csl{background:#f6f669!important;}
.csq.clm.clt{background:#cdd16f;}.csq.clm.cdk{background:#aaa23a;}
.csq.cch{background:linear-gradient(135deg,#ff4e4e,#cc2222)!important;}
.csq.cht::after{content:"";position:absolute;width:20px;height:20px;border-radius:50%;background:rgba(0,0,0,0.22);pointer-events:none;}
.csq.chc::before{content:"";position:absolute;inset:3px;border-radius:3px;border:4px solid rgba(0,0,0,0.22);pointer-events:none;}
.csq:hover{filter:brightness(1.07);}.csq.csl{filter:none;}
.cpi{font-size:36px;line-height:1;z-index:2;pointer-events:none;transition:transform 0.1s;}
.csq:hover .cpi{transform:scale(1.08);}.csq.csl .cpi{transform:scale(1.12);}
.cwp{filter:drop-shadow(0 1px 2px rgba(0,0,0,0.5));}
.cbp{filter:drop-shadow(0 1px 2px rgba(0,0,0,0.55));}
.cside{display:flex;flex-direction:column;gap:9px;width:175px;}
.klay{display:flex;gap:12px;padding:14px;align-items:flex-start;}
.kbd{display:grid;grid-template-columns:repeat(8,54px);grid-template-rows:repeat(8,54px);border-radius:4px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.6),0 0 0 2px rgba(100,120,255,0.12);position:relative;}
.ksq{width:54px;height:54px;display:flex;align-items:center;justify-content:center;}
.klt{background:#f0d9b5;}.kdk{background:#7a4a1e;cursor:pointer;}
.kdk:hover{filter:brightness(1.1);}
.ksl{background:#d4a017!important;}.khnt{background:#4a7a2a!important;}.klm{background:#5a6a1a!important;}
.kpc{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.5);transition:transform 0.1s;pointer-events:none;border:2px solid transparent;}
.ksq:hover .kpc{transform:scale(1.08);}.ksq.ksl .kpc{transform:scale(1.12);}
.kwm{background:radial-gradient(circle at 38% 35%,#fff,#ccc);border-color:rgba(0,0,0,0.25);}
.kbm{background:radial-gradient(circle at 38% 35%,#666,#222);border-color:rgba(255,255,255,0.15);}
.kwk{background:radial-gradient(circle at 38% 35%,#fff,#ccc);border-color:#ffd700;border-width:3px;}
.kbk{background:radial-gradient(circle at 38% 35%,#666,#222);border-color:#ffd700;border-width:3px;}
.kside{display:flex;flex-direction:column;gap:9px;width:175px;}
.ksco{display:flex;justify-content:space-around;}
.scb{text-align:center;}.scn{font-size:22px;font-weight:700;color:#e8e8ff;}
.scl{font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.5px;}
.chatlay{display:flex;flex-direction:column;width:100%;height:100%;}
.chattop{display:flex;align-items:center;gap:10px;padding:10px 12px;background:rgba(255,255,255,0.03);border-bottom:1px solid rgba(255,255,255,0.06);flex-shrink:0;}
.gav{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#5b3cf5,#9b59f7);display:flex;align-items:center;justify-content:center;font-size:17px;box-shadow:0 0 12px rgba(91,60,245,0.4);}
.gname{font-size:13px;font-weight:700;color:#e8e8ff;}
.gdesc{font-size:10px;color:rgba(255,255,255,0.35);}
.gmood{font-size:10px;padding:3px 8px;background:rgba(255,255,255,0.05);border-radius:20px;border:1px solid rgba(255,255,255,0.08);color:rgba(255,255,255,0.5);margin-left:auto;}
.chatmsgs{flex:1;overflow-y:auto;padding:10px;display:flex;flex-direction:column;gap:7px;scrollbar-width:thin;scrollbar-color:rgba(255,255,255,0.1) transparent;}
.msg{display:flex;gap:7px;max-width:90%;animation:mi 0.3s ease;}
@keyframes mi{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:none;}}
.msg.user{align-self:flex-end;flex-direction:row-reverse;}
.msg.event{align-self:center;}
.mav{width:26px;height:26px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:13px;}
.mav.gp{background:linear-gradient(135deg,#5b3cf5,#9b59f7);}
.mav.us{background:rgba(255,255,255,0.08);}
.mbub{padding:7px 11px;border-radius:10px;font-size:11px;line-height:1.5;}
.msg.gaspar .mbub{background:rgba(91,60,245,0.15);border:1px solid rgba(91,60,245,0.2);color:#e2e8ff;border-radius:3px 10px 10px 10px;}
.msg.user .mbub{background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.1);color:#e2e8ff;border-radius:10px 3px 10px 10px;}
.msg.event .mbub{background:rgba(255,171,0,0.07);border:1px solid rgba(255,171,0,0.15);color:rgba(255,200,80,0.85);font-size:10px;border-radius:8px;font-style:italic;}
.chatinp{padding:8px 10px;border-top:1px solid rgba(255,255,255,0.06);display:flex;gap:7px;flex-shrink:0;}
.ci{flex:1;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:7px;padding:7px 10px;color:#e2e8ff;font-size:11px;font-family:inherit;outline:none;transition:border-color 0.2s;}
.ci:focus{border-color:rgba(91,60,245,0.5);}
.ci::placeholder{color:rgba(255,255,255,0.2);}
.csbtn{padding:7px 12px;background:linear-gradient(135deg,#5b3cf5,#9b59f7);border:none;border-radius:7px;color:#fff;font-size:11px;font-weight:600;cursor:pointer;font-family:inherit;transition:all 0.2s;}
.csbtn:hover{transform:translateY(-1px);}
.goov{position:absolute;inset:0;background:rgba(5,12,26,0.82);backdrop-filter:blur(6px);display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity 0.4s;z-index:20;}
.goov.show{opacity:1;pointer-events:all;}
.got{font-size:26px;font-weight:800;color:#fff;text-shadow:0 0 25px rgba(99,210,150,0.6);}
.gos{font-size:12px;color:rgba(255,255,255,0.5);margin-top:5px;}
.proov{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.8);z-index:9998;align-items:center;justify-content:center;}
.proov.show{display:flex;}
.probox{background:linear-gradient(160deg,#1a1a2e,#16213e);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:22px;}
.prot{font-size:13px;font-weight:700;color:#e8e8ff;text-align:center;margin-bottom:14px;}
.props{display:flex;gap:10px;}
.prop{width:54px;height:54px;background:rgba(255,255,255,0.05);border:2px solid rgba(255,255,255,0.1);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:32px;cursor:pointer;transition:all 0.18s;}
.prop:hover{border-color:#9b59f7;transform:scale(1.1);}
@keyframes d1{0%,60%,100%{opacity:.2;}30%{opacity:1;}}
@keyframes d2{0%,60%,100%{opacity:.2;}40%{opacity:1;}}
@keyframes d3{0%,60%,100%{opacity:.2;}50%{opacity:1;}}
.tdots{display:inline-flex;gap:3px;margin-left:4px;}
.tdots span{width:3px;height:3px;background:#ffab00;border-radius:50%;}
.tdots span:nth-child(1){animation:d1 1.2s infinite;}
.tdots span:nth-child(2){animation:d2 1.2s infinite;}
.tdots span:nth-child(3){animation:d3 1.2s infinite;}
"""

body = """</style>
</head>
<body>
<div class="desktop" id="desktop">
<div class="aw focused" id="winChess" style="left:30px;top:30px;">
  <div class="wbar" id="barChess">
    <div class="wdots">
      <button class="wd wr" onclick="closeW('winChess','chess')"></button>
      <button class="wd wy" onclick="minW('winChess','chess')"></button>
      <button class="wd wg" onclick="maxW('winChess')"></button>
    </div>
    <div class="wtitle"><span class="wicon">\u265f</span>\u0428\u0430\u0445\u043c\u0430\u0442\u044b</div>
  </div>
  <div class="wbody">
    <div class="clay">
      <div class="bwrap">
        <div class="rlbls" id="chRanks"></div>
        <div class="bcol">
          <div class="cbd" id="chBoard">
            <div class="goov" id="chGO"><div class="got" id="chGOt"></div><div class="gos" id="chGOs"></div></div>
          </div>
          <div class="flbls" id="chFiles"></div>
        </div>
      </div>
      <div class="cside">
        <div class="panel">
          <div class="plbl">\u0421\u0442\u0430\u0442\u0443\u0441</div>
          <div class="strow"><div class="sled on" id="chled"></div><div><div class="stm" id="chstm">\u0412\u0430\u0448 \u0445\u043e\u0434</div><div class="sts" id="chsts">\u0425\u043e\u0434\u044f\u0442 \u0431\u0435\u043b\u044b\u0435</div></div></div>
        </div>
        <div class="panel">
          <div class="plbl">\u0418\u0433\u0440\u043e\u043a\u0438</div>
          <div class="plrow" id="chBlP"><div class="av avb">\u2654</div><div><div class="plnm">\u0413\u0430\u0441\u043f\u0430\u0440 (\u0418\u0418)</div><div class="plcl">\u0427\u0451\u0440\u043d\u044b\u0435</div></div></div>
          <div class="plrow plat" id="chWhP"><div class="av avw">\u265a</div><div><div class="plnm">\u0412\u044b</div><div class="plcl">\u0411\u0435\u043b\u044b\u0435</div></div></div>
        </div>
        <div class="panel"><div class="plbl">\u0421\u043b\u043e\u0436\u043d\u043e\u0441\u0442\u044c</div><div class="dg"><button class="dbtn" id="cd1" onclick="setCDiff(1)">\u041b\u0451\u0433\u043a\u0438\u0439</button><button class="dbtn da" id="cd2" onclick="setCDiff(2)">\u0421\u0440\u0435\u0434\u043d\u0438\u0439</button><button class="dbtn" id="cd3" onclick="setCDiff(3)">\u0421\u043b\u043e\u0436\u043d\u044b\u0439</button></div></div>
        <div class="panel"><div class="plbl">\u0417\u0430\u0445\u0432\u0430\u0447\u0435\u043d\u043e</div>
          <div style="font-size:9px;color:rgba(255,255,255,0.2);margin-bottom:2px;">\u0412\u0430\u043c\u0438</div><div class="capln" id="chCapW"></div>
          <div style="font-size:9px;color:rgba(255,255,255,0.2);margin-top:5px;margin-bottom:2px;">\u0418\u0418</div><div class="capln" id="chCapB"></div>
        </div>
        <div class="panel" style="flex:1"><div class="plbl">\u0425\u043e\u0434\u044b</div><div class="hists" id="chHist"></div></div>
        <button class="ngbtn" onclick="newChess()">\u265f \u041d\u043e\u0432\u0430\u044f \u0438\u0433\u0440\u0430</button>
      </div>
    </div>
  </div>
</div>

<div class="aw" id="winCk" style="left:620px;top:30px;">
  <div class="wbar" id="barCk">
    <div class="wdots">
      <button class="wd wr" onclick="closeW('winCk','ck')"></button>
      <button class="wd wy" onclick="minW('winCk','ck')"></button>
      <button class="wd wg" onclick="maxW('winCk')"></button>
    </div>
    <div class="wtitle"><span class="wicon">\u26ab</span>\u0428\u0430\u0448\u043a\u0438</div>
  </div>
  <div class="wbody">
    <div class="klay">
      <div class="bwrap">
        <div class="rlbls" id="ckRanks"></div>
        <div class="bcol">
          <div class="kbd" id="ckBoard">
            <div class="goov" id="ckGO"><div class="got" id="ckGOt"></div><div class="gos" id="ckGOs"></div></div>
          </div>
          <div class="flbls" id="ckFiles"></div>
        </div>
      </div>
      <div class="kside">
        <div class="panel"><div class="plbl">\u0428\u0430\u0448\u043a\u0438</div><div class="ksco"><div class="scb"><div class="scn" id="ckSW">12</div><div class="scl">\u0412\u044b</div></div><div class="scb"><div class="scn" id="ckSB">12</div><div class="scl">\u0413\u0430\u0441\u043f\u0430\u0440</div></div></div></div>
        <div class="panel"><div class="plbl">\u0421\u0442\u0430\u0442\u0443\u0441</div><div class="strow"><div class="sled on" id="kled"></div><div><div class="stm" id="kstm">\u0412\u0430\u0448 \u0445\u043e\u0434</div><div class="sts" id="ksts">\u0425\u043e\u0434\u044f\u0442 \u0431\u0435\u043b\u044b\u0435</div></div></div></div>
        <div class="panel"><div class="plbl">\u0421\u043b\u043e\u0436\u043d\u043e\u0441\u0442\u044c</div><div class="dg"><button class="dbtn" id="kd1" onclick="setKDiff(1)">\u041b\u0451\u0433\u043a\u0438\u0439</button><button class="dbtn da" id="kd2" onclick="setKDiff(2)">\u0421\u0440\u0435\u0434\u043d\u0438\u0439</button><button class="dbtn" id="kd3" onclick="setKDiff(3)">\u0421\u043b\u043e\u0436\u043d\u044b\u0439</button></div></div>
        <div class="panel" style="flex:1"><div class="plbl">\u041f\u043e\u0434\u0441\u043a\u0430\u0437\u043a\u0438</div><div style="font-size:10px;color:rgba(255,255,255,0.35);line-height:1.7;">\u2022 \u041a\u043b\u0438\u043a \u043d\u0430 \u0448\u0430\u0448\u043a\u0443 \u2014 \u0432\u044b\u0431\u0440\u0430\u0442\u044c<br>\u2022 \u0417\u0435\u043b\u0451\u043d\u044b\u0435 \u043a\u043b\u0435\u0442\u043a\u0438 \u2014 \u0445\u043e\u0434\u044b<br>\u2022 \u0412\u0437\u044f\u0442\u0438\u0435 \u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e<br>\u2022 \u0414\u0430\u043c\u043a\u0438 \u2014 \u0437\u043e\u043b\u043e\u0442\u0430\u044f \u0440\u0430\u043c\u043a\u0430</div></div>
        <button class="ngbtn" onclick="newCk()">\u26ab \u041d\u043e\u0432\u0430\u044f \u0438\u0433\u0440\u0430</button>
      </div>
    </div>
  </div>
</div>

<div class="aw" id="winChat" style="left:30px;top:570px;width:340px;height:300px;">
  <div class="wbar" id="barChat">
    <div class="wdots">
      <button class="wd wr" onclick="closeW('winChat','chat')"></button>
      <button class="wd wy" onclick="minW('winChat','chat')"></button>
      <button class="wd wg" onclick="maxW('winChat')"></button>
    </div>
    <div class="wtitle"><span class="wicon">\ud83d\udcac</span>\u0427\u0430\u0442 \u0441 \u0413\u0430\u0441\u043f\u0430\u0440\u043e\u043c</div>
  </div>
  <div class="wbody" style="flex-direction:column;">
    <div class="chatlay">
      <div class="chattop">
        <div class="gav">\ud83c\udfad</div>
        <div><div class="gname">\u0413\u0430\u0441\u043f\u0430\u0440</div><div class="gdesc">\u0421\u0430\u0440\u043a\u0430\u0441\u0442\u0438\u0447\u043d\u044b\u0439 \u043c\u0430\u0441\u0442\u0435\u0440</div></div>
        <div class="gmood" id="gmood">\ud83d\ude0f \u0412 \u0444\u043e\u0440\u043c\u0435</div>
      </div>
      <div class="chatmsgs" id="chatmsgs"></div>
      <div class="chatinp">
        <input class="ci" id="ci" placeholder="\u041d\u0430\u043f\u0438\u0448\u0438 \u0413\u0430\u0441\u043f\u0430\u0440\u0443..." onkeydown="if(event.key==='Enter')sendChat()">
        <button class="csbtn" onclick="sendChat()">\u27a4</button>
      </div>
    </div>
  </div>
</div>

<div class="taskbar">
  <div class="tb-btn tb-open tb-active" id="tb-chess" onclick="togW('winChess','chess')">\u265f \u0428\u0430\u0445\u043c\u0430\u0442\u044b</div>
  <div class="tb-sep"></div>
  <div class="tb-btn" id="tb-ck" onclick="togW('winCk','ck')">\u26ab \u0428\u0430\u0448\u043a\u0438</div>
  <div class="tb-sep"></div>
  <div class="tb-btn" id="tb-chat" onclick="togW('winChat','chat')">\ud83d\udcac \u0413\u0430\u0441\u043f\u0430\u0440</div>
  <div class="tb-time" id="tbtime"></div>
</div>
</div>
<div class="proov" id="proov"><div class="probox"><div class="prot">\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0444\u0438\u0433\u0443\u0440\u0443</div><div class="props" id="props"></div></div></div>
<script>
"""

f.write("<!DOCTYPE html>\n<html lang=\"ru\">\n<head>\n<meta charset=\"UTF-8\"/>\n<title>\u0418\u0433\u0440\u043e\u0432\u043e\u0439 \u0441\u0442\u043e\u043b \u2014 \u0428\u0430\u0445\u043c\u0430\u0442\u044b, \u0428\u0430\u0448\u043a\u0438, \u0418\u0418 \u0413\u0430\u0441\u043f\u0430\u0440</title>\n")
f.write("<link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap\" rel=\"stylesheet\"/>\n")
f.write("<style>\n" + css + body)
f.close()
print("gen1 OK")
