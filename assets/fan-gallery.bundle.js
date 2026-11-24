"use strict";(()=>{function Yt(e,i){let t=i?.top??0,s=i?.bottom??innerHeight;for(let a=e.parentElement;a;a=a.parentElement){if(!/^(auto|scroll|hidden|clip)$/.test(getComputedStyle(a).overflowY))continue;let c=a.getBoundingClientRect(),f=a.offsetHeight?c.height/a.offsetHeight:1,r=c.top+a.clientTop*f;t=Math.max(t,r),s=Math.min(s,r+a.clientHeight*f)}return{top:t,bottom:s}}function Ft(e,{viewportStart:i=85,viewportStartUp:t,once:s=!0,played:a=!1,play:c,reset:f,finish:r,isPlaying:u=()=>!1,entryElement:o=e,entrySide:n=null}){let d=matchMedia("(prefers-reduced-motion: reduce)"),p=a,m=!a,w=!1,b=n,k=0,v=0,x=[],E=()=>{v++,cancelAnimationFrame(k),x.forEach(A=>A.disconnect()),x=[]},D=()=>{p=!0,m=!1},W=()=>{if(E(),w||d.matches||s&&p)return;if(typeof IntersectionObserver>"u"){D(),c();return}let A=Number.isFinite(i)?Math.min(100,Math.max(1,i)):85,U=typeof t=="number"&&Number.isFinite(t)?Math.min(100,Math.max(0,t)):100-A,C=v,V={},$=()=>{if(!(w||d.matches||C!==v))if(V.visible===!1){if(!s){let q=!m||p||u();p=!1,m=!0,q&&f()}}else V.visible&&m&&b&&V[b]&&!u()&&(D(),c(),s&&E())},Y=(q,M)=>{let G=new IntersectionObserver(J=>{if(w||C!==v)return;let R=J.at(-1);if(R){if(V[q]=R.isIntersecting,q==="visible")if(R.isIntersecting)b||(b="below");else{let{top:at,bottom:rt}=Yt(e,R.rootBounds);R.boundingClientRect.bottom<=at?b="above":R.boundingClientRect.top>=rt&&(b="below")}cancelAnimationFrame(k),k=requestAnimationFrame($)}},{rootMargin:M,threshold:0});x.push(G),G.observe(q==="visible"?e:o)};Y("visible","0px"),Y("below",`0px 0px -${innerHeight*(1-A/100)}px 0px`),Y("above",`-${innerHeight*U/100}px 0px 0px 0px`)},T=()=>{d.matches?(E(),r()):W()};return window.addEventListener("resize",W),d.addEventListener("change",T),d.matches?r():W(),{markPlayed:D,getEntrySide:()=>b,disconnect:()=>{w=!0,E(),window.removeEventListener("resize",W),d.removeEventListener("change",T)}}}var N={cardWidth:162,aspectRatio:.8,spacing:.69,curve:.14,tilt:14.5,lift:42,spread:.2,stackFrom:"left"},st=(e,i,t)=>Math.min(t,Math.max(i,e)),ct=Math.PI/180;function lt(e,i,t){let s=t.cardWidth,a=s/t.aspectRatio,c=(i-1)/2,f=e-c,r=f/Math.max(1,c);return{x:f*Math.max(0,t.spacing)*s,y:Math.max(0,t.curve)*a*r*r,rotation:t.tilt*r}}var wt=new Float64Array(4),tt=new Float64Array(4),Et=new Float64Array(4),et=new Float64Array(4),Lt=[[-1,-1],[1,-1],[1,1],[-1,1]];function kt(e,i,t,s,a){let c=Math.cos(e.rotation*ct),f=Math.sin(e.rotation*ct);for(let r=0;r<4;r++){let u=Lt[r][0]*i/2,o=Lt[r][1]*t/2;s[r]=e.x+u*c-o*f,a[r]=e.y+u*f+o*c}}function St(e,i,t,s){let a=s>0?-1/0:1/0;for(let c=0;c<4;c++){let f=c+1&3,r=i[c],u=i[f];if((r-t)*(u-t)>0||r===u)continue;let o=e[c]+(t-r)/(u-r)*(e[f]-e[c]);a=s>0?Math.max(a,o):Math.min(a,o)}return a}function At(e,i,t,s){kt(e,t,s,wt,tt),kt(i,t,s,Et,et);let a=Math.max(Math.min(...tt),Math.min(...et)),c=Math.min(Math.max(...tt),Math.max(...et));if(a>=c)return-1/0;let f=-1/0,r=u=>{if(u<a||u>c)return;let o=St(wt,tt,u,1),n=St(Et,et,u,-1);Number.isFinite(o)&&Number.isFinite(n)&&(f=Math.max(f,o-n))};r(a),r(c);for(let u=0;u<4;u++)r(tt[u]),r(et[u]);return f}var Pt=new WeakMap;function qt(e,i){let t=Pt.get(i);if(t&&t.count===e)return t;let s=i.cardWidth,a=s/i.aspectRatio,c=Math.max(0,i.spread)*s,f=new Float64Array(e),r=new Float64Array(e);for(let o=0;o<e;o++){let n={...lt(o,e,i),rotation:0};n.y-=i.lift;let d=0,p=0;for(let m=0;m<e;m++){if(m===o)continue;let w=lt(m,e,i);m>o?p=Math.max(p,At(n,w,s,a)):d=Math.max(d,At(w,n,s,a))}f[o]=d+c,r[o]=p+c}let u={count:e,left:f,right:r};return Pt.set(i,u),u}function _(e,i,t,s=-1){let a=lt(e,i,t);if(s<0||s>=i)return a;if(e===s)return{x:a.x,y:a.y-t.lift,rotation:0};let c=qt(i,t);return a.x+=e>s?c.right[s]:-c.left[s],a}function Ht(e,i){return st(Math.floor(st(e,0,.9999)*i),0,Math.max(0,i-1))}function It(e,i,t){return t.stackFrom==="right"?e:i-1-e}function Tt(e,i,t){let s=Math.abs(Math.cos(e*ct)),a=Math.abs(Math.sin(e*ct));return{x:(s*i+a*t)/2,y:(a*i+s*t)/2}}function pt(e,i,t){let s=Math.max(40,t.cardWidth),a=st(t.aspectRatio,.3,3),c=s/a,f=16,r=Math.max(1,e-f*2),u=(i-1)/2,o=Math.max(0,t.spacing),n=o;for(let v=0;v<i;v++){let x=Math.abs(v-u);if(!x)continue;let E=Tt(t.tilt*((v-u)/Math.max(1,u)),s,c).x;n=Math.min(n,(r/2-E)/(x*s))}n=st(n,o*.4,o);let d={...t,cardWidth:s,aspectRatio:a,spacing:n},p=1,m=0,w=1/0,b=0;for(let v=0;v<i;v++){let x=lt(v,i,d),E=Tt(x.rotation,s,c);p=Math.max(p,Math.abs(x.x)+E.x),w=Math.min(w,x.y-E.y),m=Math.min(m,x.y-E.y,x.y-d.lift-c/2),b=Math.max(b,x.y+E.y)}i||(w=0);let k=Math.min(1,r/(p*2));return{fit:k,width:s*k,height:c*k,originX:e/2,originY:-m*k+f,stageHeight:(b-m)*k+f*2,bandTop:f+(w-m)*k,bandBottom:f+(b-m)*k,spacing:n,options:d}}function $t(e,i,t){if(e<=0)return 0;let s=1-.68*Math.max(0,Math.min(1,t)),a=6.6/Math.max(.05,i);if(s>=.999)return 1-(1+a*e)*Math.exp(-a*e);let c=a*Math.sqrt(1-s*s);return 1-Math.exp(-s*a*e)*(Math.cos(c*e)+s*a/c*Math.sin(c*e))}function bt(e,i){let t=1-.68*Math.max(0,Math.min(1,i)),s=6.6/Math.max(.05,e),a=.001;if(t>=.999){let c=Math.log(1/a)/s;for(let f=0;f<8;f++)c=(Math.log(1+s*c)+Math.log(1/a))/s;return c}return Math.log(1/(a*Math.sqrt(1-t*t)))/(t*s)}var ht=Math.PI/180;function gt(e,i,t,s){let a=Math.exp(-t*s),c=e.x-i,f=(e.v+t*c)*s;e.x=i+(c+f)*a,e.v=(e.v-t*f)*a}function Rt(e,i,t,s){let{stage:a,cards:c,heading:f}=e,r=c.length,u=a.closest(".fan-gallery"),o=i,n=pt(a.clientWidth,r,o),d=-1,p=[],m=0,w=()=>{p=c.map((l,h)=>o.stackFrom==="right"?r-1-h:h),m=(r-1)*Math.max(0,o.stagger)+bt(o.speed,o.bounce)};w();let b=null,k=0,v=null,x=-1,E=c.map(()=>({x:{x:0,v:0},y:{x:0,v:0},r:{x:0,v:0},tx:0,ty:0,tr:0})),D=()=>{for(let l=0;l<r;l++){let h=_(l,r,n.options),H=_(l,r,n.options,x),y=E[l];y.tx=(H.x-h.x)*n.fit,y.ty=(H.y-h.y)*n.fit,y.tr=H.rotation-h.rotation}},W=()=>{for(let l of E)l.x.x=l.tx,l.y.x=l.ty,l.r.x=l.tr,l.x.v=l.y.v=l.r.v=0},T=0,A=0,U=c.map(()=>({transform:"",z:-1,opacity:-1})),C=-1,V=(l,h,H)=>{let y=n.fit,I=_(l,r,n.options),g=I.x*y,S=I.y*y,O=I.rotation,ot=0,Z=1,F=h;if(F<1||F>1){let B=n.height,j=B*3.2,ut=(L,P)=>({angle:Math.atan2(L,j-P)/ht,reach:Math.hypot(L,j-P)}),vt=(L,P)=>{g=Math.sin(L*ht)*P,S=j-Math.cos(L*ht)*P},it=o.stackFrom==="right"?1:-1;if(o.entrance==="stack"){let L=ut(g,S);vt(L.angle*F,L.reach),O*=F}else if(o.entrance==="deal"){let L=it*(n.originX+n.width*1.2),P=n.stageHeight-n.originY+B*.4,Q=(L+g)/2,dt=Math.min(P,S)-B*.9,X=1-F;g=X*X*L+2*X*F*Q+F*F*g,S=X*X*P+2*X*F*dt+F*F*S,O=it*-75+(O-it*-75)*F}else if(o.entrance==="circular"||o.entrance==="deck"){let L=it*100,P=ut(g,S),Q;if(o.entrance==="circular")Q=L+(P.angle-L)*F;else{let dt=o.stackFrom==="right"?r-1:0,X=_(dt,r,n.options),Mt=ut(X.x*y,X.y*y).angle,mt=Math.max(0,Math.min(1,(F-.55)/.45)),Ct=mt*mt*(3-2*mt);Q=L+(Mt-L)*H+(P.angle-Mt)*Ct}vt(Q,P.reach),O+=Q-P.angle}else if(o.entrance==="rise"){let L=n.stageHeight-n.originY+B*.9,P=l*37%11-5;S=L+(S-L)*F,O=O+P*4*(1-F)}else ot=90*(1-F),Z=Math.max(0,Math.min(1,F*3))}let z=E[l];return{x:g+z.x.x,y:S+z.y.x,rotation:O+z.r.x,rotateY:ot,opacity:Z}},$=l=>{let h=b,H=h===null?0:h===1/0?1:$t(h,o.speed,o.bounce);for(let y=0;y<r;y++){if(l&&!l[y])continue;let I=p[y]*Math.max(0,o.stagger),g=h===null?0:h===1/0?1:$t(h-I,o.speed,o.bounce),S=V(y,g,H),O=n.originX+S.x-n.width/2,ot=n.originY+S.y-n.height/2,Z=`translate(${O.toFixed(2)}px,${ot.toFixed(2)}px) rotate(${S.rotation.toFixed(3)}deg)`+(S.rotateY?` perspective(1400px) rotateY(${S.rotateY.toFixed(2)}deg)`:""),F=1+It(y,r,n.options)+(y===x?r:0),z=U[y],B=c[y].style;z.transform!==Z&&(B.transform=z.transform=Z),z.z!==F&&(B.zIndex=String(z.z=F));let j=Math.round(S.opacity*1e3)/1e3;z.opacity!==j&&(B.opacity=String(z.opacity=j))}if(f){let y=h===null?0:h===1/0?1:Math.min(1,Math.max(0,h/(o.speed*.8)));y!==C&&(f.style.opacity=String(C=y))}},Y=(l,h)=>Math.abs(l.x-h)<.02&&Math.abs(l.v)<.05,q=l=>!Y(l.x,l.tx)||!Y(l.y,l.ty)||!Y(l.r,l.tr),M=()=>b!==null&&b!==1/0,G=()=>M()||E.some(q),J=new Uint8Array(r),R=!0,at=l=>{T=0;let h=A?Math.min(.05,(l-A)/1e3):1/60;A=l;let H=6.6/Math.max(.05,o.hoverSpeed);J.fill(0);for(let I=0;I<r;I++){let g=E[I];q(g)&&(gt(g.x,g.tx,H,h),gt(g.y,g.ty,H,h),gt(g.r,g.tr,H,h),q(g)||(g.x.x=g.tx,g.y.x=g.ty,g.r.x=g.tr,g.x.v=g.y.v=g.r.v=0),J[I]=1)}if(M()){if(b=(l-k)/1e3,b>=m){b=1/0;let I=v;v=null,I?.()}R=!0}$(R?void 0:J),R=!1;let y=!G();K(!y),y?A=0:T=requestAnimationFrame(at)},rt=!1,K=l=>{l!==rt&&(rt=l,a.classList.toggle("is-moving",l),u?.classList.toggle("is-animating",l))},ft=()=>{K(!0),T||(T=requestAnimationFrame(at))},yt=l=>l===x?!1:(x>=0&&c[x]?.removeAttribute("aria-current"),x=l,x>=0&&c[x]?.setAttribute("aria-current","true"),u?.classList.toggle("is-active",x>=0),!0),xt=()=>{d=a.clientWidth,n=pt(a.clientWidth,r,o),D(),a.style.height=`${n.stageHeight}px`;let l=Math.max(0,o.radius)*n.fit;for(let h of c)h.style.width=`${n.width}px`,h.style.height=`${n.height}px`,h.style.borderRadius=`${l}px`;s?.({spacing:n.spacing,requestedSpacing:Math.max(0,o.spacing),scale:n.fit})};return{measure(){return d===a.clientWidth?!1:(xt(),W(),$(),!0)},update(l){o=l,w(),xt(),R=!0,t.matches?(W(),$()):($(),ft())},reset(){b=null,v=null,T||K(!1),$()},play(l){b=0,k=performance.now(),A=0,v=l,$(),ft()},finish(){b=1/0,v=null,T||K(!1),$()},focusCard(l){yt(l===null?-1:Math.round(l))&&(D(),R=!0,t.matches?(W(),$()):ft())},focusPoint(l,h){let H=a.getBoundingClientRect(),y=h-H.top,I=x>=0?Math.max(0,o.lift)*n.fit:0;if(y<n.bandTop-I-8||y>n.bandBottom+8){this.focusCard(null);return}let g=Math.max(.001,n.options.spacing*n.options.cardWidth*n.fit),S=n.originX+_(0,r,n.options).x*n.fit-g/2;this.focusCard(Ht((l-H.left-S)/(g*r),r))},cancel(){cancelAnimationFrame(T),T=0,A=0,v=null,K(!1)},destroy(){this.cancel(),yt(-1)}}}function Wt(e,i,t,s,a,c){let f=s,r=window.matchMedia("(prefers-reduced-motion: reduce)"),u=Rt({stage:i,cards:t,heading:e.querySelector(".fan-gallery-heading")},f,r,c),o="idle",n=!1,d=!1,p=!1,m,w=M=>{e.dataset.state=o=M},b=()=>{u.cancel(),u.finish(),w("finished")},k=()=>{if(r.matches){b();return}u.cancel(),u.reset(),w("idle")},v=()=>{if(!p){if(n=!0,m?.markPlayed(),r.matches||bt(f.speed,f.bounce)<=0){b();return}u.cancel(),w("playing"),u.play(()=>w("finished"))}},x=M=>{o!=="idle"&&u.focusCard(M<0?null:M)},E=(M,G)=>{o!=="idle"&&u.focusPoint(M,G)},D=M=>{f=M,u.update(M)},W=M=>{if(!d){a.current=M;return}a.current=null,M==="play"?v():M==="reset"?k():b()},T=()=>{u.measure()&&(e.dataset.ready="true")};T();let A,U=new ResizeObserver(()=>{A===void 0&&(A=requestAnimationFrame(()=>{A=void 0,p||T()}))});U.observe(i);let C=()=>{f.trigger==="hover"&&o!=="playing"&&v()},V=M=>{(!M.relatedTarget||!e.contains(M.relatedTarget))&&C()},$=M=>{M.pointerType!=="mouse"&&C()},Y=()=>{r.matches&&b()};return e.addEventListener("pointerenter",C),e.addEventListener("focusin",V),e.addEventListener("pointerdown",$),r.addEventListener("change",Y),Promise.resolve().then(()=>{p||(d=!0,a.current?W(a.current):r.matches?b():f.trigger==="auto"?v():k(),f.trigger==="scroll"&&(m=Ft(e,{viewportStart:f.viewportStart,viewportStartUp:f.viewportStartUp,once:f.once,played:n,play:v,reset:k,finish:b,isPlaying:()=>o==="playing"})))}),{dispatch:W,activate:x,point:E,update:D,destroy:()=>{p=!0,m?.disconnect(),U.disconnect(),A!==void 0&&cancelAnimationFrame(A),r.removeEventListener("change",Y),e.removeEventListener("pointerenter",C),e.removeEventListener("focusin",V),e.removeEventListener("pointerdown",$),u.destroy(),delete e.dataset.state,delete e.dataset.ready}}}var nt={entrance:"stack",radius:18,speed:.7,stagger:.09,bounce:.35,hoverSpeed:.28};function zt(e,i,t={}){let s={cardWidth:t.cardWidth??N.cardWidth,aspectRatio:t.aspectRatio??N.aspectRatio,spacing:t.spacing??N.spacing,curve:t.curve??N.curve,tilt:t.tilt??N.tilt,lift:t.lift??N.lift,spread:t.spread??N.spread,stackFrom:t.stackFrom??N.stackFrom,radius:t.radius??nt.radius,speed:t.speed??nt.speed,stagger:t.stagger??nt.stagger,bounce:t.bounce??nt.bounce,hoverSpeed:t.hoverSpeed??nt.hoverSpeed,trigger:t.trigger??"scroll",viewportStart:t.viewportStart??75,viewportStartUp:t.viewportStartUp,once:t.once??!0};e.className="fan-gallery"+(e.className?" "+e.className:""),e.setAttribute("aria-label",t.ariaLabel||"Fan gallery");let a="";t.showTitle&&(t.title||t.subtitle)&&(a=`<header class="fan-gallery-heading">
      ${t.title?`<h2>${t.title}</h2>`:""}
      ${t.subtitle?`<p>${t.subtitle}</p>`:""}
    </header>`);let c=i.map((n,d)=>{let p=`<img src="${n.src}" alt="${n.alt||`Image ${d+1}`}" draggable="false" loading="lazy" decoding="async" />`;return n.href?`<a class="fan-gallery-card" href="${n.href}" aria-label="${n.alt||`Image ${d+1}`}">${p}</a>`:`<button class="fan-gallery-card" type="button" aria-label="${n.alt||`Image ${d+1}`}">${p}</button>`}).join("");e.innerHTML=`${a}<div class="fan-gallery-stage">${c}</div>`;let f=e.querySelector(".fan-gallery-stage"),r=Array.from(e.querySelectorAll(".fan-gallery-card")),o=Wt(e,f,r,s,{current:null},t.onLayout);return f.addEventListener("pointermove",n=>{n.pointerType!=="touch"&&o.point(n.clientX,n.clientY)}),f.addEventListener("pointerleave",()=>{let n=r.findIndex(d=>d===document.activeElement);o.activate(n)}),f.addEventListener("blur",n=>{let d=n.relatedTarget;f.contains(d)||o.activate(-1)},!0),r.forEach((n,d)=>{n.addEventListener("focus",()=>o.activate(d)),n.addEventListener("click",()=>o.activate(d)),n.addEventListener("keydown",p=>{let m=-1;p.key==="ArrowRight"?m=(d+1)%i.length:p.key==="ArrowLeft"?m=(d-1+i.length)%i.length:p.key==="Home"?m=0:p.key==="End"&&(m=i.length-1),m>=0&&(p.preventDefault(),r[m]?.focus({preventScroll:!0})),p.key==="Escape"&&(o.activate(-1),n.blur())})}),o}typeof window<"u"&&(window.initFanGallery=zt);})();
/*!
ReactDrops Component License 1.0

Copyright (c) 2026 ReactDrops

1. Scope and definitions

This license applies to ReactDrops software and associated documentation that
expressly carry this license or are distributed under a LICENSE file containing
it (the "Software"). "Licensor" means the copyright holder granting rights in
the Software, and only to the extent that holder has authority to grant them.
"You" means the individual or entity exercising these rights.

An "End Product" is a website, application, service, or other finished project
whose primary purpose is something other than providing reusable components,
source code, templates, or development assets to others.

2. Permitted uses

Subject to this license, Licensor grants You a worldwide, non-exclusive,
royalty-free license to use, copy, modify, and incorporate the Software into
unlimited personal, internal, and commercial End Products. You may charge for
End Products, subscriptions, development services, and work for clients.

You may distribute the Software as an integrated part of an End Product,
including in browser-delivered JavaScript. You may provide End Product source
code to a client, and share the Software with employees and contractors who
need it to develop or maintain End Products. Those recipients may use the
Software for those purposes subject to this license. This permission does not
authorize them to redistribute the Software as a reusable development asset.

3. Restricted redistribution

Unless You obtain separate written permission from Licensor, You may not sell,
sublicense, publish, share, or otherwise redistribute the Software, or a
substantial portion of it, whether unchanged or modified:

(a) as a standalone component, component library, UI kit, source-code bundle,
    registry, or other collection of reusable development assets;
(b) as part of a theme, template, starter project, or similar product offered
    to multiple recipients for reuse in their own projects; or
(c) through a builder or generation service that offers the Software as
    reusable blocks or source-code exports for others' projects.

These restrictions apply to paid and free redistribution. Renaming, restyling,
repackaging, translating, or modifying the Software does not remove them.
Building separate finished websites or applications for multiple clients is
permitted; offering a reusable template or kit containing the Software is not.

Public source-code hosting by Licensor is not permission to republish the
Software under another license. This license does not override any separate
rights granted directly by Licensor or applicable code-hosting terms.

4. Notices and ownership

Retain this license and applicable copyright and third-party notices in source
copies of the Software and permitted source distributions. No visible credit
or ReactDrops logo is required in an End Product's user interface.

Licensor retains ownership of its Software. You retain rights in Your own
contributions, subject to the license for any incorporated Software. No rights
to trademarks, trade names, or logos are granted by this license.

5. Third-party materials and separate grants

Dependencies, fonts, images, videos, and other third-party materials remain
subject to their respective licenses. Separately identified third-party code
is licensed under its stated terms, and these restrictions do not limit rights
granted by its copyright holders. Retain all required third-party notices.
Demo media are not licensed by this document; obtain Your own permission or
replace them with media You are entitled to use.

This license does not revoke rights granted under other valid licenses. It does
not assert ownership of third-party work or grant rights Licensor lacks.

6. Termination

The permissions granted here continue unless terminated for a material breach.
If You fail to cure a material breach within 30 days after receiving written
notice from Licensor, Your permissions terminate. On termination, cease uses
and distributions requiring this license. Rights under independently granted
licenses and rights that applicable law does not allow to be restricted remain
unaffected. Sections 3 through 7 survive termination.

7. Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE, TITLE, AND NON-INFRINGEMENT. TO THE MAXIMUM EXTENT
PERMITTED BY APPLICABLE LAW, LICENSOR AND CONTRIBUTORS SHALL NOT BE LIABLE FOR
ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT, OR OTHERWISE,
ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR ITS USE.

This license does not limit rights or exceptions that applicable law makes
non-waivable. No other permissions are granted by implication.
*/
