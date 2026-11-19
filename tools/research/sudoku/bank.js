const S=require("../../../src/games/sudoku/sudoku-core.js"); const fs=require('fs');
const level=process.argv[2], want=+process.argv[3], seed=+process.argv[4];
const out=[]; let s=seed;
while(out.length<want){const r=S.generate(level,{seed:s++,maxAttempts:1000}); if(r.level===S.LEVELS[level]&&S.countSolutions(r.puzzle)===1) out.push({p:r.puzzle.join(''),s:r.solution.join(''),c:r.clues,steps:r.steps});
 if(out.length%10===0)fs.writeFileSync(`bank-${level}.json`,JSON.stringify(out));}
fs.writeFileSync(`bank-${level}.json`,JSON.stringify(out)); console.log('done',level,out.length);
