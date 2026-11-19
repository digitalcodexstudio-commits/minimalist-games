// Minesweeper "perfect logic + best-probability guess" solver.
// Rules match minimalist-games.com: mines placed after first click, 3x3 around it safe.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#define MAXC 480
static int R,C,M,N;
static int mine[MAXC],num[MAXC],rev[MAXC],flag[MAXC];
static int nb[MAXC][8],nbn[MAXC];
static uint64_t rs=88172645463325252ULL;
static inline uint64_t xr(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
static int revealedCount; static long interiorGuess=0;
static long nodeLimitHits=0;
static void setup(){for(int i=0;i<N;i++){nbn[i]=0;int r=i/C,c=i%C;for(int dr=-1;dr<=1;dr++)for(int dc=-1;dc<=1;dc++){if(!dr&&!dc)continue;int a=r+dr,b=c+dc;if(a<0||b<0||a>=R||b>=C)continue;nb[i][nbn[i]++]=a*C+b;}}}
static void place(int s){int pos[MAXC],np=0;int sr=s/C,sc=s%C;for(int i=0;i<N;i++){int r=i/C,c=i%C;if(abs(r-sr)<=1&&abs(c-sc)<=1)continue;pos[np++]=i;}
 for(int i=np-1;i>0;i--){int j=xr()%(i+1);int t=pos[i];pos[i]=pos[j];pos[j]=t;}
 memset(mine,0,sizeof(int)*N);for(int i=0;i<M&&i<np;i++)mine[pos[i]]=1;
 for(int i=0;i<N;i++){num[i]=0;for(int k=0;k<nbn[i];k++)num[i]+=mine[nb[i][k]];}}
static int stack_[MAXC*9];
static int reveal(int s){ // returns 0 if mine
 if(mine[s])return 0; int sp=0;stack_[sp++]=s;
 while(sp){int x=stack_[--sp];if(rev[x])continue;rev[x]=1;revealedCount++;if(num[x]==0)for(int k=0;k<nbn[x];k++){int y=nb[x][k];if(!rev[y])stack_[sp++]=y;}}
 return 1;}
// ---- enumeration
static int fr[MAXC],nfr,frIdx[MAXC];
static int cons[MAXC],ncons; // constraint cells (revealed numbers bordering unknown)
static int comp[MAXC];
static int assign_[MAXC];
static double cnt[MAXC+1]; static double ccnt[MAXC][MAXC+1]; // per component local
static int cm[MAXC],ncm; // cells in current component (ordered)
static int conList[MAXC],nconList;
static int cellCons[MAXC][8],cellConsN[MAXC];
static int need[MAXC],unk[MAXC]; // per constraint cell: remaining mines needed, unassigned unknown count
static long nodes; static long NODELIM=4000000;
static int aborted;
static void rec(int k,int m){
 if(aborted)return; if(++nodes>NODELIM){aborted=1;return;}
 if(k==ncm){cnt[m]+=1;for(int i=0;i<ncm;i++)if(assign_[cm[i]])ccnt[i][m]+=1;return;}
 int x=cm[k];
 for(int v=0;v<=1;v++){
  int okk=1;
  for(int j=0;j<cellConsN[x];j++){int q=cellCons[x][j];int nn=need[q]-v,uu=unk[q]-1;if(nn<0||nn>uu){okk=0;break;}}
  if(!okk)continue;
  for(int j=0;j<cellConsN[x];j++){int q=cellCons[x][j];need[q]-=v;unk[q]--;}
  assign_[x]=v; rec(k+1,m+v);
  for(int j=0;j<cellConsN[x];j++){int q=cellCons[x][j];need[q]+=v;unk[q]++;}
 }}
static double lchoose(int n,int k){if(k<0||k>n)return -INFINITY;return lgamma(n+1.0)-lgamma(k+1.0)-lgamma(n-k+1.0);}
// result arrays
static double prob[MAXC];
typedef struct {int n; int cells[MAXC]; double *dist; double *cell; } Comp; // cell[i*(n+1)+m]
static Comp comps[MAXC]; static int ncomps;
// returns -1 if aborted
static int analyse(){
 // simple rules first handled outside. Build frontier.
 nfr=0;ncons=0;for(int i=0;i<N;i++)frIdx[i]=-1;
 int interior=0, minesLeft=M;
 for(int i=0;i<N;i++)if(flag[i])minesLeft--;
 for(int i=0;i<N;i++){ if(rev[i]||flag[i])continue; int isf=0;for(int k=0;k<nbn[i];k++)if(rev[nb[i][k]]){isf=1;break;}
   if(isf){frIdx[i]=nfr;fr[nfr++]=i;} else interior++; }
 for(int i=0;i<N;i++){ if(!rev[i])continue; int u=0,f=0;for(int k=0;k<nbn[i];k++){int y=nb[i][k];if(flag[y])f++;else if(!rev[y])u++;}
   need[i]=num[i]-f;unk[i]=u; }
 for(int i=0;i<nfr;i++){int x=fr[i];cellConsN[x]=0;for(int k=0;k<nbn[x];k++){int y=nb[x][k];if(rev[y])cellCons[x][cellConsN[x]++]=y;}}
 // components via BFS through shared constraints
 for(int i=0;i<nfr;i++)comp[i]=-1; ncomps=0;
 for(int i=0;i<nfr;i++){ if(comp[i]>=0)continue; Comp*C_=&comps[ncomps]; C_->n=0; int q[MAXC],qh=0,qt=0;q[qt++]=i;comp[i]=ncomps;
  while(qh<qt){int a=q[qh++];int x=fr[a];C_->cells[C_->n++]=x;
   for(int j=0;j<cellConsN[x];j++){int cc=cellCons[x][j];for(int k=0;k<nbn[cc];k++){int y=nb[cc][k];int b=frIdx[y];if(b>=0&&comp[b]<0){comp[b]=ncomps;q[qt++]=b;}}}}
  ncomps++; }
 for(int c=0;c<ncomps;c++){Comp*C_=&comps[c];ncm=C_->n;memcpy(cm,C_->cells,sizeof(int)*ncm);
  for(int m=0;m<=ncm;m++)cnt[m]=0; for(int i=0;i<ncm;i++)for(int m=0;m<=ncm;m++)ccnt[i][m]=0;
  nodes=0;aborted=0;rec(0,0); if(aborted){nodeLimitHits++;return -1;}
  C_->dist=realloc(NULL,sizeof(double)*(ncm+1)); memcpy(C_->dist,cnt,sizeof(double)*(ncm+1));
  C_->cell=malloc(sizeof(double)*ncm*(ncm+1)); for(int i=0;i<ncm;i++)memcpy(C_->cell+i*(ncm+1),ccnt[i],sizeof(double)*(ncm+1)); }
 // total convolution
 int tot=0;for(int c=0;c<ncomps;c++)tot+=comps[c].n;
 double *all=calloc(tot+1,sizeof(double)); all[0]=1; int cur=0;
 for(int c=0;c<ncomps;c++){double*nw=calloc(tot+1,sizeof(double));for(int a=0;a<=cur;a++)if(all[a])for(int b=0;b<=comps[c].n;b++)nw[a+b]+=all[a]*comps[c].dist[b];cur+=comps[c].n;free(all);all=nw;}
 // weights w(k)=C(interior, minesLeft-k), normalised in log space
 double lw[MAXC+1],mx=-INFINITY; for(int k=0;k<=tot;k++){lw[k]=lchoose(interior,minesLeft-k);if(all[k]>0&&lw[k]>mx)mx=lw[k];}
 double Z=0,intE=0; for(int k=0;k<=tot;k++){if(all[k]<=0||lw[k]==-INFINITY)continue;double w=all[k]*exp(lw[k]-mx);Z+=w; if(interior>0)intE+=w*(double)(minesLeft-k)/interior;}
 for(int i=0;i<N;i++)prob[i]=-1;
 for(int i=0;i<N;i++)if(!rev[i]&&!flag[i]&&frIdx[i]<0)prob[i]=intE/Z;
 for(int c=0;c<ncomps;c++){ // leave-one-out conv
  double*o=calloc(tot+1,sizeof(double));o[0]=1;int oc=0;
  for(int d=0;d<ncomps;d++){if(d==c)continue;double*nw=calloc(tot+1,sizeof(double));for(int a=0;a<=oc;a++)if(o[a])for(int b=0;b<=comps[d].n;b++)nw[a+b]+=o[a]*comps[d].dist[b];oc+=comps[d].n;free(o);o=nw;}
  int n=comps[c].n;
  for(int i=0;i<n;i++){double s=0;for(int m=0;m<=n;m++){double cv=comps[c].cell[i*(n+1)+m];if(!cv)continue;for(int a=0;a<=oc;a++){if(!o[a])continue;double l=lw[a+m];if(l==-INFINITY)continue;s+=cv*o[a]*exp(l-mx);}}
   prob[comps[c].cells[i]]=s/Z;}
  free(o);}
 free(all);
 for(int c=0;c<ncomps;c++){free(comps[c].dist);free(comps[c].cell);}
 return 0;
}
static int simple(){ int ch=0;
 for(int i=0;i<N;i++){ if(!rev[i]||num[i]==0)continue; int u=0,f=0;for(int k=0;k<nbn[i];k++){int y=nb[i][k];if(flag[y])f++;else if(!rev[y])u++;}
  if(!u)continue;
  if(f==num[i]){for(int k=0;k<nbn[i];k++){int y=nb[i][k];if(!flag[y]&&!rev[y]){reveal(y);ch=1;}}}
  else if(num[i]-f==u){for(int k=0;k<nbn[i];k++){int y=nb[i][k];if(!flag[y]&&!rev[y]){flag[y]=1;ch=1;}}}}
 return ch;}
// play one game. returns 1 win, 0 loss; *guesses out; *firstOpen = cells revealed by first click
static int play(int first,int*guesses,int*firstOpen,int*guessProbBins){
 memset(rev,0,sizeof(int)*N);memset(flag,0,sizeof(int)*N);revealedCount=0;*guesses=0;
 place(first); reveal(first); *firstOpen=revealedCount;
 while(revealedCount<N-M){
  if(simple())continue;
  if(analyse()<0){ // fallback: random unknown guess on frontier (rare)
    int c=-1;for(int i=0;i<N;i++)if(!rev[i]&&!flag[i]){c=i;break;}
    (*guesses)++; if(!reveal(c))return 0; continue;}
  int ch=0; double best=2;int bi=-1;
  for(int i=0;i<N;i++){ if(prob[i]<0)continue;
   if(prob[i]<1e-12){reveal(i);ch=1;}
   else if(prob[i]>1-1e-12){flag[i]=1;ch=1;}
   else if(prob[i]<best-1e-12){best=prob[i];bi=i;} }
  if(ch)continue;
  if(bi<0)break;
  (*guesses)++; if(frIdx[bi]<0)interiorGuess++; int bin=(int)(best*20); if(bin>19)bin=19; guessProbBins[bin]++;
  if(!reveal(bi))return 0;
 }
 return 1;}
int main(int argc,char**argv){
 R=atoi(argv[1]);C=atoi(argv[2]);M=atoi(argv[3]);int games=atoi(argv[4]);char*where=argv[5]; rs^=(uint64_t)atoi(argv[6])*2654435761ULL; N=R*C; setup();
 int first; if(!strcmp(where,"corner"))first=0; else if(!strcmp(where,"edge"))first=(R/2)*C; else first=(R/2)*C+C/2;
 long wins=0,noGuess=0,winsNoGuess=0; long ghist[40]={0}; long openSum=0; int gpb[20]={0};
 long gWinBy[40]={0};
 for(int g=0;g<games;g++){int gs,fo;int w=play(first,&gs,&fo,gpb);wins+=w;openSum+=fo;if(gs==0){noGuess++;} if(gs>39)gs=39;ghist[gs]++; if(w)gWinBy[gs]++;}
 printf("{\"R\":%d,\"C\":%d,\"M\":%d,\"where\":\"%s\",\"games\":%d,\"wins\":%ld,\"noGuess\":%ld,\"avgFirstOpen\":%.2f,\"nodeLimitHits\":%ld,\"ghist\":[",R,C,M,where,games,wins,noGuess,(double)openSum/games,nodeLimitHits);
 for(int i=0;i<40;i++)printf("%ld%s",ghist[i],i<39?",":"");printf("],\"gwin\":[");for(int i=0;i<40;i++)printf("%ld%s",gWinBy[i],i<39?",":"");printf("],\"guessProb\":[");for(int i=0;i<20;i++)printf("%d%s",gpb[i],i<19?",":"");printf("],\"interiorGuess\":%ld}\n",interiorGuess);
}
