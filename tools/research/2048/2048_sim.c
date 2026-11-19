// 2048 strategy simulation. Rules as on minimalist-games.com: two starting tiles, 90% 2 / 10% 4 spawns.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
typedef uint64_t B;
static uint16_t rowL[65536],rowR[65536]; static uint32_t scL[65536]; static float heur[65536];
static uint64_t rs=0x9E3779B97F4A7C15ULL; static inline uint64_t xr(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
static inline B transpose(B x){B a1=x&0xF0F00F0FF0F00F0FULL;B a2=x&0x0000F0F00000F0F0ULL;B a3=x&0x0F0F00000F0F0000ULL;B a=a1|(a2<<12)|(a3>>12);B b1=a&0xFF00FF0000FF00FFULL;B b2=a&0x00FF00FF00000000ULL;B b3=a&0x00000000FF00FF00ULL;return b1|(b2>>24)|(b3<<24);}
static inline int cell(B b,int i){return (b>>(4*i))&0xF;}
static void init(){
 for(int r=0;r<65536;r++){int l[4]={r&15,(r>>4)&15,(r>>8)&15,(r>>12)&15};
  // heuristic (nneonneo-style)
  float sum=0;int empty=0,merges=0,prev=0,counter=0;
  for(int i=0;i<4;i++){int v=l[i];sum+=pow(v,3.5);if(!v)empty++;else{if(prev==v)counter++;else if(counter>0){merges+=1+counter;counter=0;}prev=v;}}
  if(counter>0)merges+=1+counter;
  float ml=0,mr=0;for(int i=1;i<4;i++){if(l[i-1]>l[i])ml+=pow(l[i-1],4)-pow(l[i],4);else mr+=pow(l[i],4)-pow(l[i-1],4);}
  heur[r]=200000.0f+270.0f*empty+700.0f*merges-47.0f*(ml<mr?ml:mr)-11.0f*sum;
  // move left (toward index 0)
  int a[4]={l[0],l[1],l[2],l[3]},o[4]={0},n=0,score=0;
  for(int i=0;i<4;i++)if(a[i])o[n++]=a[i];
  int res[4]={0},k=0;for(int i=0;i<n;i++){if(i+1<n&&o[i]==o[i+1]&&o[i]<15){res[k++]=o[i]+1;score+=1<<(o[i]+1);i++;}else res[k++]=o[i];}
  rowL[r]=res[0]|(res[1]<<4)|(res[2]<<8)|(res[3]<<12); scL[r]=score;
  int rr=l[3]|(l[2]<<4)|(l[1]<<8)|(l[0]<<12); (void)rr;
 }
 for(int r=0;r<65536;r++){int rev=((r&15)<<12)|(((r>>4)&15)<<8)|(((r>>8)&15)<<4)|((r>>12)&15);int m=rowL[rev];rowR[r]=((m&15)<<12)|(((m>>4)&15)<<8)|(((m>>8)&15)<<4)|((m>>12)&15);}
}
// dirs: 0 up 1 down 2 left 3 right. Board: row i = bits 16i..16i+15, cell index within row = column. Row 0 = top.
static inline B mv(B b,int d,int*sc){B r=0;int s=0;
 if(d==2||d==3){for(int i=0;i<4;i++){int row=(b>>(16*i))&0xFFFF;int rv;if(d==2){rv=rowL[row];s+=scL[row];}else{rv=rowR[row];int rev=((row&15)<<12)|(((row>>4)&15)<<8)|(((row>>8)&15)<<4)|((row>>12)&15);s+=scL[rev];}r|=(B)rv<<(16*i);}}
 else{B t=transpose(b);for(int i=0;i<4;i++){int row=(t>>(16*i))&0xFFFF;int rv;if(d==0){rv=rowL[row];s+=scL[row];}else{rv=rowR[row];int rev=((row&15)<<12)|(((row>>4)&15)<<8)|(((row>>8)&15)<<4)|((row>>12)&15);s+=scL[rev];}r|=(B)rv<<(16*i);}r=transpose(r);}
 if(sc)*sc=s;return r;}
static inline int empties(B b){int e=0;for(int i=0;i<16;i++)if(!cell(b,i))e++;return e;}
static B spawn(B b){int e=empties(b);if(!e)return b;int k=xr()%e;for(int i=0;i<16;i++)if(!cell(b,i)){if(!k--){int v=(xr()%10==0)?2:1;return b|((B)v<<(4*i));}}return b;}
static inline int maxt(B b){int m=0;for(int i=0;i<16;i++)if(cell(b,i)>m)m=cell(b,i);return m;}
static float evalB(B b){B t=transpose(b);float s=0;for(int i=0;i<4;i++){s+=heur[(b>>(16*i))&0xFFFF]+heur[(t>>(16*i))&0xFFFF];}return s;}
static float expmax(B b,int depth,float p);
static float chance(B b,int depth,float p){
 if(depth<=0||p<0.0001f)return evalB(b);
 int e=empties(b); if(!e)return evalB(b); float s=0; float pe=p/e;
 for(int i=0;i<16;i++)if(!cell(b,i)){s+=0.9f*expmax(b|((B)1<<(4*i)),depth-1,pe*0.9f)+0.1f*expmax(b|((B)2<<(4*i)),depth-1,pe*0.1f);}
 return s/e;}
static float expmax(B b,int depth,float p){float best=0;for(int d=0;d<4;d++){B n=mv(b,d,0);if(n==b)continue;float v=chance(n,depth,p);if(v>best)best=v;}return best;}
static int searchDepth=2;
static int pick(B b,int strat,int*tick){
 int legal[4],nl=0;for(int d=0;d<4;d++)if(mv(b,d,0)!=b)legal[nl++]=d; if(!nl)return -1;
 if(strat==0)return legal[xr()%nl];
 if(strat==1){int order[4]={1,3,2,0};for(int k=0;k<4;k++)if(mv(b,order[k],0)!=b)return order[k];}
 if(strat==2){ // alternate down/right; else left; else up
   int a=(*tick)++&1?3:1,bb=a==1?3:1; if(mv(b,a,0)!=b)return a; if(mv(b,bb,0)!=b)return bb; if(mv(b,2,0)!=b)return 2; return 0;}
 if(strat==3){ // greedy: max immediate score, tiebreak empties, then order
   int bd=-1;double bv=-1;for(int k=0;k<nl;k++){int s;B n=mv(b,legal[k],&s);double v=s*100+empties(n);if(v>bv){bv=v;bd=legal[k];}}return bd;}
 if(strat==5){int up=1;for(int k=0;k<nl;k++)if(legal[k]!=0)up=0; if(up)return 0; int bd=-1;float bv=-1;for(int k=0;k<nl;k++){if(legal[k]==0)continue;B n=mv(b,legal[k],0);float v=chance(n,searchDepth*2-1,1.0f);if(v>bv){bv=v;bd=legal[k];}}return bd;}
 if(strat==4){int bd=-1;float bv=-1;for(int k=0;k<nl;k++){B n=mv(b,legal[k],0);float v=chance(n,searchDepth*2-1,1.0f);if(v>bv){bv=v;bd=legal[k];}}return bd;}
 return legal[0];}
int main(int argc,char**argv){init();int strat=atoi(argv[1]);int games=atoi(argv[2]);rs^=(uint64_t)atoll(argv[3])*0x2545F4914F6CDD1DULL; if(argc>4)searchDepth=atoi(argv[4]);
 for(int g=0;g<games;g++){B b=spawn(spawn(0));int tick=0;long moves=0,score=0,dirCount[4]={0};long movesTo2048=-1,movesTo1024=-1;int cornerAtEnd=0;long upMovesWhileBig=0;long inCorner=0;int lastCorner=-1;long cornerChanges=0;long score2048=-1;
  for(;;){int d=pick(b,strat,&tick);if(d<0)break;int s;b=mv(b,d,&s);score+=s;moves++;dirCount[d]++;b=spawn(b);int m=maxt(b);if(m>=10&&movesTo1024<0)movesTo1024=moves;if(m>=11&&movesTo2048<0)movesTo2048=moves;
   {int cs[4]={0,3,12,15};int which=-1;for(int k=0;k<4;k++)if(cell(b,cs[k])==m){inCorner++;which=k;break;} if(m>=7&&which>=0){if(lastCorner>=0&&which!=lastCorner&&cell(b,cs[lastCorner])!=m)cornerChanges++;lastCorner=which;}} if(m>=11&&score2048<0)score2048=score;
   if((strat==4||strat==5)&&m>=12)break; }
  int m=maxt(b);int corners[4]={0,3,12,15};for(int k=0;k<4;k++)if(cell(b,corners[k])==m)cornerAtEnd=1;
  printf("%d %d %ld %ld %ld %ld %ld %ld %ld %ld %d %ld %ld %ld\n",strat,1<<m,score,moves,movesTo1024,movesTo2048,dirCount[0],dirCount[1],dirCount[2],dirCount[3],cornerAtEnd,inCorner,cornerChanges,score2048);fflush(stdout);}
}
