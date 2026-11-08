import { TAU, clamp, rgba, smoothstep } from "../math.mjs";

const W=1280,H=720,CX=640,CY=345;
const SERIF='"Source Serif 4", serif';
const MATH='"KaTeX Math", "Source Serif 4", serif';
const P={paper:"#fcfbf7",ink:"#15191e",grey:"#68717a",pale:"#e7e3d9",
 gold:"#aa7c2e",blue:"#3f6f94",red:"#a6434a",green:"#47775a",violet:"#65538c"};

function font(size,{math=false,weight=400,italic=false}={}){return `${italic?"italic ":""}${weight} ${size}px ${math?MATH:SERIF}`;}
function txt(ctx,s,x,y,{size=18,color=P.ink,alpha=1,align="center",math=false,weight=400,italic=false}={}){
 ctx.save();ctx.font=font(size,{math,weight,italic});ctx.textAlign=align;ctx.textBaseline="middle";ctx.fillStyle=rgba(color,alpha);ctx.fillText(String(s),x,y);ctx.restore();
}
function line(ctx,a,b,{color=P.grey,alpha=.45,width=1,dash=[]}={}){
 ctx.save();ctx.strokeStyle=rgba(color,alpha);ctx.lineWidth=width;ctx.setLineDash(dash);ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();ctx.restore();
}
function box(ctx,x,y,w,h,{color=P.grey,alpha=.3,width=1}={}){
 ctx.save();ctx.strokeStyle=rgba(color,alpha);ctx.lineWidth=width;ctx.strokeRect(x,y,w,h);ctx.restore();
}
function circle(ctx,x,y,r,{color=P.ink,alpha=.75,width=1.4,fill=null}={}){
 ctx.save();if(fill){ctx.fillStyle=rgba(fill,alpha*.2);ctx.beginPath();ctx.arc(x,y,r,0,TAU);ctx.fill();}
 ctx.strokeStyle=rgba(color,alpha);ctx.lineWidth=width;ctx.beginPath();ctx.arc(x,y,r,0,TAU);ctx.stroke();ctx.restore();
}
function cross(ctx,x,y,r,{color=P.red,alpha=.8,width=1.5}={}){
 line(ctx,{x:x-r,y:y-r},{x:x+r,y:y+r},{color,alpha,width});
 line(ctx,{x:x-r,y:y+r},{x:x+r,y:y-r},{color,alpha,width});
}
function arrow(ctx,a,b,{color=P.gold,alpha=.55,width=1.2,dash=[]}={}){
 line(ctx,a,b,{color,alpha,width,dash});
 const ang=Math.atan2(b.y-a.y,b.x-a.x),r=8;
 line(ctx,b,{x:b.x-r*Math.cos(ang-.55),y:b.y-r*Math.sin(ang-.55)},{color,alpha,width});
 line(ctx,b,{x:b.x-r*Math.cos(ang+.55),y:b.y-r*Math.sin(ang+.55)},{color,alpha,width});
}
function paper(ctx){ctx.fillStyle=P.paper;ctx.fillRect(0,0,W,H);}
function head(ctx,title){txt(ctx,title,68,52,{size:12,color:P.grey,align:"left",weight:700});line(ctx,{x:68,y:73},{x:420,y:73},{color:P.grey,alpha:.18,width:.7});}
function sym(ctx,type,x,y,r=25,a=1){type==="o"?circle(ctx,x,y,r,{color:P.blue,alpha:a,width:1.7}):cross(ctx,x,y,r*.72,{color:P.red,alpha:a,width:1.7});}
function q(t,a,b){return smoothstep(a,b,t);}
function grid(ctx,n,types,{x=360,y=135,size=410,alpha=1,labels=false}={}){
 const cols=Math.round(Math.sqrt(n)),cell=size/cols;
 box(ctx,x,y,size,size,{color:P.grey,alpha:.25*alpha});
 for(let i=1;i<cols;i++){line(ctx,{x:x+i*cell,y},{x:x+i*cell,y:y+size},{color:P.grey,alpha:.16*alpha});line(ctx,{x,y:y+i*cell},{x:x+size,y:y+i*cell},{color:P.grey,alpha:.16*alpha});}
 for(let i=0;i<n;i++){const c=i%cols,r=Math.floor(i/cols),cx=x+(c+.5)*cell,cy=y+(r+.5)*cell;sym(ctx,types[i]??"o",cx,cy,Math.min(24,cell*.16),alpha);if(labels)txt(ctx,i+1,cx,cy+cell*.29,{size:11,color:P.grey,alpha});}
}
function single(ctx,p){head(ctx,"ONE THING");sym(ctx,"o",CX,CY,54,q(p,.08,.5));txt(ctx,"o",CX,CY+110,{size:30,color:P.blue,math:true,alpha:q(p,.25,.7)});}
function distinction(ctx,p){head(ctx,"REPETITION IS NOT DISTINCTION");for(let i=0;i<5;i++)sym(ctx,"o",300+i*135,CY,30,q(p,.04+i*.05,.32+i*.05));txt(ctx,"still one symbol-type",CX,475,{size:17,color:P.grey,alpha:q(p,.4,.65)});const a=q(p,.58,.9);sym(ctx,"x",1010,CY,32,a);txt(ctx,"another thing requires another form",CX,565,{size:19,color:P.red,alpha:a,weight:700});}
function priority(ctx,p){head(ctx,"THIS / THAT");sym(ctx,"o",430,CY,48,1);sym(ctx,"x",850,CY,48,1);arrow(ctx,{x:500,y:CY},{x:780,y:CY},{color:P.gold,alpha:q(p,.2,.7),dash:[7,7]});txt(ctx,"this",430,455,{size:18,color:P.blue});txt(ctx,"that",850,455,{size:18,color:P.red});txt(ctx,"priority, not page position",CX,570,{size:18,color:P.ink,alpha:q(p,.55,.9)});}
function operation(ctx,p){head(ctx,"DIFFERENCE AS OPERATION");sym(ctx,"o",410,CY,48,1);sym(ctx,"x",870,CY,48,1);const a=q(p,.12,.8);arrow(ctx,{x:470,y:CY-18},{x:810,y:CY-18},{color:P.gold,alpha:a});arrow(ctx,{x:810,y:CY+22},{x:470,y:CY+22},{color:P.gold,alpha:a});txt(ctx,"T",CX,CY-70,{size:30,color:P.gold,math:true,weight:700,alpha:a});txt(ctx,"the relation is a higher-order thing",CX,565,{size:18,color:P.ink,alpha:q(p,.55,.9)});}
function pairing(ctx,p){head(ctx,"FIRST AND SECOND");const ys=[260,430];["o","o","o","x"].forEach((s,i)=>sym(ctx,s,i<2?500:780,ys[i%2],33,q(p,.04+i*.06,.35+i*.06)));box(ctx,445,205,110,280,{color:P.blue,alpha:.3});box(ctx,725,205,110,280,{color:P.red,alpha:.3});txt(ctx,"oo = one",500,535,{size:17,color:P.blue});txt(ctx,"ox = two",780,535,{size:17,color:P.red});}
function tetrad(ctx,p){head(ctx,"THE TETRAD");grid(ctx,4,["o","o","o","x"],{alpha:q(p,.05,.5),labels:true});txt(ctx,"four symbols · three pairings",CX,610,{size:20,color:P.ink,alpha:q(p,.45,.85),weight:700});}
function klein(ctx,p){head(ctx,"THREE INDEPENDENT INTERCHANGES");grid(ctx,4,["o","o","o","x"],{alpha:1});const a=q(p,.15,.75);arrow(ctx,{x:440,y:230},{x:690,y:230},{color:P.blue,alpha:a});arrow(ctx,{x:475,y:195},{x:475,y:445},{color:P.green,alpha:a});arrow(ctx,{x:440,y:230},{x:690,y:445},{color:P.violet,alpha:a});txt(ctx,"columns",900,240,{size:16,color:P.blue,alpha:a});txt(ctx,"rows",900,330,{size:16,color:P.green,alpha:a});txt(ctx,"both",900,420,{size:16,color:P.violet,alpha:a});}
function superposition(ctx,p){head(ctx,"ZERO + THREE OPERATIONS");const cards=[["0","none"],["C","columns"],["R","rows"],["D","both"]];cards.forEach((c,i)=>{const x=235+i*270,a=q(p,.05+i*.08,.28+i*.08);box(ctx,x-90,245,180,200,{color:[P.grey,P.blue,P.green,P.violet][i],alpha:.34*a});txt(ctx,c[0],x,310,{size:36,color:[P.grey,P.blue,P.green,P.violet][i],math:true,weight:700,alpha:a});txt(ctx,c[1],x,400,{size:15,color:P.ink,alpha:a});});}
function recursiveGrid(ctx,p,n=16){head(ctx,n===16?"TETRAD OF TETRADS":"INDEFINITE EXPANSION");const a=q(p,.05,.72);grid(ctx,16,Array.from({length:16},(_,i)=>i%5===0?"x":"o"),{x:360,y:120,size:440,alpha:a,labels:n===16});if(n!==16){txt(ctx,"4 → 16 → 64 → 256 → …",CX,610,{size:28,color:P.gold,math:true,weight:700,alpha:q(p,.55,.9)});}}
function groupAction(ctx,p){head(ctx,"WHOLE INVARIANT UNDER MEMBER TRANSFORMATION");grid(ctx,16,Array.from({length:16},(_,i)=>i%5===0?"x":"o"),{x:360,y:120,size:440,alpha:.7});const a=q(p,.1,.85);circle(ctx,CX,CY,275,{color:P.gold,alpha:.28*a,width:1.2});arrow(ctx,{x:390,y:130},{x:790,y:540},{color:P.gold,alpha:a});txt(ctx,"members permute",CX,625,{size:18,color:P.ink,alpha:a});}
function selfSimilarity(ctx,p){head(ctx,"STRUCTURE OF STRUCTURE");for(let k=0;k<4;k++){const s=390-k*75,a=q(p,.06+k*.1,.35+k*.1);box(ctx,CX-s/2,CY-s/2,s,s,{color:[P.grey,P.blue,P.green,P.gold][k],alpha:.28*a});}txt(ctx,"same form at immediacy and reflexion",CX,610,{size:18,color:P.ink,alpha:q(p,.55,.9)});}
function hierarchy(ctx,p){head(ctx,"INFINITE HIERARCHY");for(let i=0;i<11;i++){const y=110+i*48,s=22+Math.abs(i-5)*7,a=q(p,.03+i*.035,.22+i*.035);box(ctx,CX-s*2.5,y,s*5,32,{color:i<5?P.blue:(i===5?P.gold:P.violet),alpha:.25*a});}txt(ctx,"particular ← immediate → general",CX,655,{size:18,color:P.ink});}
function duration(ctx,p){head(ctx,"DURATION = INVARIANCE UNDER TRANSFORMATION");circle(ctx,390,CY,65,{color:P.gold,alpha:.3});txt(ctx,"lamp",390,CY,{size:18,color:P.gold});for(let i=0;i<8;i++){const a=q(p,.03+i*.06,.22+i*.06);line(ctx,{x:650+i*45,y:CY-20},{x:650+i*45,y:CY+20},{color:P.blue,alpha:a,width:2});}txt(ctx,"unchange",390,500,{size:17,color:P.gold});txt(ctx,"change",800,500,{size:17,color:P.blue});}
function momentCycle(ctx,p){head(ctx,"REPEATED MOMENTS");const left=p<.5?["o","o","o","x"]:["o","o","x","o"];grid(ctx,4,left,{alpha:1});txt(ctx,"same interchange, another moment",CX,610,{size:18,color:P.ink});}
function cogs(ctx,p){head(ctx,"FINITE RATES ARE NOT DURATION");const rot=p*TAU*4;for(const [x,r,n,c] of [[470,105,14,P.blue],[710,48,8,P.gold]]){ctx.save();ctx.translate(x,CY);ctx.rotate(rot*(r>60?1:-2.1));ctx.strokeStyle=rgba(c,.45);ctx.lineWidth=1.3;ctx.beginPath();for(let i=0;i<n*2;i++){const rr=i%2?r:r+12,a=i/(n*2)*TAU,px=Math.cos(a)*rr,py=Math.sin(a)*rr;i?ctx.lineTo(px,py):ctx.moveTo(px,py);}ctx.closePath();ctx.stroke();ctx.restore();}txt(ctx,"slow change + fast change ≠ absolute unchange + change",CX,590,{size:17,color:P.red,weight:700});}
function zeno(ctx,p){head(ctx,"INFINITE MOMENTS · FINITE COMPLETION");let x=150,w=480;for(let i=0;i<10;i++){const a=q(p,.03+i*.055,.25+i*.055);box(ctx,x,CY-35,w,70,{color:i%2?P.blue:P.gold,alpha:.3*a});x+=w;w*=.5;}txt(ctx,"1 + 1/2 + 1/4 + 1/8 + …",CX,500,{size:25,color:P.ink,math:true});}
function threeLevel(ctx,p){head(ctx,"THREE TEMPORAL LEVELS");const rows=[["eternal frame",P.gold],["regular moments",P.blue],["accelerating sub-moments",P.violet]];rows.forEach((r,i)=>{const y=210+i*150,a=q(p,.05+i*.1,.3+i*.1);box(ctx,240,y,800,82,{color:r[1],alpha:.3*a});txt(ctx,r[0],300,y+41,{size:17,color:r[1],align:"left",weight:700,alpha:a});for(let j=0;j<8*(i+1);j++)line(ctx,{x:560+j*(430/(8*(i+1))),y:y+18},{x:560+j*(430/(8*(i+1))),y:y+64},{color:r[1],alpha:.3*a});});}
function nestedTime(ctx,p){head(ctx,"NO ABSOLUTE OUTSIDE");for(let i=0;i<12;i++){const r=25+i*24,a=q(p,.02+i*.04,.2+i*.04);circle(ctx,CX,CY,r,{color:i%3===0?P.gold:(i%3===1?P.blue:P.violet),alpha:.18*a,width:1});}txt(ctx,"no universal present moment",CX,640,{size:18,color:P.red,weight:700});}
function replacement(ctx,p){head(ctx,"IRREVERSIBLE REPLACEMENT");const a=q(p,.1,.55),b=q(p,.55,.9);sym(ctx,"o",390,CY,48,1-a);sym(ctx,"x",640,CY,48,a*(1-b));sym(ctx,"o",890,CY,48,b);arrow(ctx,{x:450,y:CY},{x:580,y:CY},{alpha:a});arrow(ctx,{x:700,y:CY},{x:830,y:CY},{alpha:b});txt(ctx,"x becomes the new o",CX,540,{size:19,color:P.ink});}
function weights(ctx,p){head(ctx,"INTENSITY HIERARCHY");const vals=[2/3,1/3,1/6,1/12,1/24];vals.forEach((v,i)=>{const x=210+i*210,a=q(p,.04+i*.08,.28+i*.08);circle(ctx,x,CY,30+85*v,{color:i===0?P.blue:P.gold,alpha:.35*a,width:1.2,fill:i===0?P.blue:P.gold});txt(ctx,v===2/3?"2/3":`1/${3*Math.pow(2,i-1)}`,x,510,{size:15,color:P.ink,alpha:a,math:true});});txt(ctx,"sum = 1",CX,610,{size:23,color:P.green,math:true,weight:700});}
function perspective(ctx,p){head(ctx,"GENERALITY ↔ TEMPORAL DEPTH");for(let i=0;i<7;i++){const s=430-i*52,a=q(p,.03+i*.06,.24+i*.06);box(ctx,CX-s/2,CY-s/2,s,s,{color:i%2?P.blue:P.gold,alpha:.28*a});}txt(ctx,p<.5?"nested sizes":"equal squares receding in depth",CX,630,{size:18,color:P.ink});}
function temporal(ctx,p){head(ctx,"PAST · PRESENT · FUTURE IN THE PRESENT");const cards=[["past","over-determined",P.grey],["present","determined",P.gold],["future","under-determined",P.blue]];cards.forEach((c,i)=>{const x=260+i*380,a=q(p,.05+i*.1,.3+i*.1);box(ctx,x-135,245,270,210,{color:c[2],alpha:.34*a});txt(ctx,c[0],x,305,{size:25,color:c[2],weight:700,alpha:a});txt(ctx,c[1],x,390,{size:16,color:P.ink,alpha:a});});}
function weightedKlein(ctx,p){head(ctx,"ONE THIS · THREE THATS");circle(ctx,330,CY,100,{color:P.blue,alpha:.3,fill:P.blue});txt(ctx,"this\n2/3",330,CY,{size:21,color:P.blue,weight:700});const vals=[["1/6",P.gold],["1/9",P.green],["1/18",P.violet]];vals.forEach((v,i)=>{const y=230+i*120,r=25+parseFloat(v[0])*100;circle(ctx,850,y,r,{color:v[1],alpha:.35,fill:v[1]});txt(ctx,v[0],850,y,{size:15,color:v[1],math:true});});txt(ctx,"relative emphases vary; identity remains",CX,615,{size:18,color:P.ink});}
function chair(ctx,p){head(ctx,"IDENTITY BY NEGATIVE DETERMINATION");const items=[["chair",P.gold],["table",P.blue],["bed",P.green],["wardrobe",P.violet]];items.forEach((it,i)=>{const x=220+i*280,a=q(p,.03+i*.08,.28+i*.08);box(ctx,x-85,260,170,170,{color:it[1],alpha:.28*a});txt(ctx,it[0],x,345,{size:18,color:it[1],weight:700,alpha:a});});txt(ctx,"chair = not-table · not-bed · not-wardrobe",CX,555,{size:19,color:P.ink,alpha:q(p,.5,.85)});}
function squaring(ctx,p){head(ctx,"SELECTION BY REPEATED SQUARING");const rows=[["3 : 2 : 1",[3,2,1]],["9 : 4 : 1",[9,4,1]],["81 : 16 : 1",[81,16,1]]];rows.forEach((r,i)=>{const y=190+i*150,a=q(p,.04+i*.12,.32+i*.12);txt(ctx,r[0],250,y,{size:21,color:P.ink,math:true,align:"left",alpha:a});const sum=r[1].reduce((x,y)=>x+y,0);r[1].forEach((v,j)=>{ctx.save();ctx.fillStyle=rgba([P.blue,P.green,P.violet][j],.45*a);ctx.fillRect(480+300*r[1].slice(0,j).reduce((x,y)=>x+y,0)/sum,y-28,300*v/sum,56);ctx.restore();});});txt(ctx,"one interchange asymptotically dominates",CX,630,{size:18,color:P.red,weight:700});}
function frontier(ctx,p){head(ctx,"UNFINISHED");txt(ctx,"INTENTION",CX,230,{size:34,color:P.gold,weight:700,alpha:q(p,.05,.4)});txt(ctx,"ACTION",CX,350,{size:34,color:P.blue,weight:700,alpha:q(p,.25,.6)});txt(ctx,"CHOICE",CX,470,{size:34,color:P.red,weight:700,alpha:q(p,.45,.8)});txt(ctx,"dynamic structure continues",CX,610,{size:17,color:P.grey,alpha:q(p,.7,.95)});}

const DRAW={
 "symbol":single,"distinction":distinction,"priority":priority,"operation":operation,"pairing":pairing,
 "tetrad":tetrad,"klein-four":klein,"superposition":superposition,"recursive-grid":(c,p)=>recursiveGrid(c,p,16),
 "recursive-growth":(c,p)=>recursiveGrid(c,p,64),"group-action":groupAction,"self-similarity":selfSimilarity,
 "hierarchy":hierarchy,"duration":duration,"moment-cycle":momentCycle,"cogwheel-rejection":cogs,
 "zeno-series":zeno,"three-level":threeLevel,"nested-time":nestedTime,"replacement":replacement,
 "weights":weights,"perspective-switch":perspective,"temporal-tetrad":temporal,"weighted-klein":weightedKlein,
 "negative-definition":chair,"winner-selection":squaring,"frontier":frontier
};

export function renderFundamentalStructure(ctx,t,scene,env){
 paper(ctx);const op=scene.params?.operation;const fn=DRAW[op];if(fn)fn(ctx,clamp(t));
 txt(ctx,scene.params?.section??"",1210,55,{size:12,color:P.grey,align:"right",weight:700});
}
export const assetImplementations=Object.freeze({});
export const mechanismImplementations=Object.freeze({"fundamental-structure":renderFundamentalStructure});
