const S=require("../../../src/games/sudoku/sudoku-core.js");const fs=require('fs');const out={};
for(const d of ['easy','medium','hard','expert']){out[d]=[];for(let k=0;k<300;k++){const r=S.generate(d,{seed:50000+k*13+d.length*7});out[d].push({c:r.clues,l:r.level,a:r.attempts,st:r.steps});}}
for(const d of ['master','extreme']){out[d]=require("./bank-"+d+".json").map(e=>({c:e.c,l:S.LEVELS[d],st:S.rate([...e.p].map(Number)).steps}));}
fs.writeFileSync('levels.json',JSON.stringify(out));
for(const d in out){const cs=out[d].map(x=>x.c);const lv=new Set(out[d].map(x=>x.l));console.log(d,'n',cs.length,'levels',[...lv],'clues',Math.min(...cs),'-',Math.max(...cs),'mean',(cs.reduce((a,b)=>a+b)/cs.length).toFixed(1),'attempts', out[d][0].a!==undefined?(out[d].reduce((a,x)=>a+x.a,0)/cs.length).toFixed(1):'');}
