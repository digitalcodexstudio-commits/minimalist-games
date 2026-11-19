// Classic generator: remove clues while the solution stays unique (no technique budget),
// then rate each puzzle with the full human toolbox. Output: clues level steps.
const S=require("../../../src/games/sudoku/sudoku-core.js"); const N=+process.argv[2]; const rnd=S.makeRng(+process.argv[3]);
for(let k=0;k<N;k++){const sol=S.solvedGrid(rnd);const p=sol.slice();const order=[...Array(81).keys()];
 for(let i=80;i>0;i--){const j=Math.floor(rnd()*(i+1));[order[i],order[j]]=[order[j],order[i]];}
 for(const i of order){const keep=p[i];p[i]=0;if(S.countSolutions(p,2)!==1)p[i]=keep;}
 const r=S.rate(p,6); console.log(JSON.stringify({c:p.filter(Boolean).length,l:r.level,st:r.steps,p:p.join('')}));}
