var _JUPYTERLAB;(()=>{"use strict";var e,r,t,a,n,o,i,d,l,u,f,s,c,p,b,h,v,m,g,y,w,j,S={8457:(e,r,t)=>{var a={"./index":()=>Promise.all([t.e(549),t.e(728),t.e(568)]).then((()=>()=>t(1568))),"./extension":()=>Promise.all([t.e(549),t.e(728),t.e(497),t.e(261)]).then((()=>()=>t(6261))),"./style":()=>t.e(549).then((()=>()=>t(7549)))},n=(e,r)=>(t.R=r,r=t.o(a,e)?a[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),o=(e,r)=>{if(t.S){var a="default",n=t.S[a];if(n&&n!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[a]=e,t.I(a,r)}};t.d(r,{get:()=>n,init:()=>o})}},k={};function P(e){var r=k[e];if(void 0!==r)return r.exports;var t=k[e]={id:e,exports:{}};return S[e].call(t.exports,t,t.exports,P),t.exports}P.m=S,P.c=k,P.n=e=>{var r=e&&e.__esModule?()=>e.default:()=>e;return P.d(r,{a:r}),r},P.d=(e,r)=>{for(var t in r)P.o(r,t)&&!P.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},P.f={},P.e=e=>Promise.all(Object.keys(P.f).reduce(((r,t)=>(P.f[t](e,r),r)),[])),P.u=e=>(863===e?"@jupyter-widgets/controls":e)+"."+{43:"977ebe1fbf293ad5c7f9",261:"eb6a382fac090947fcec",276:"c4667dd47bc8bfdfdf73",424:"505fc92112b360ef4e5b",497:"a88640af5e122a91bf01",549:"42284772e4a962464d9b",568:"f00f1ada234ad803ccec",584:"e7a2de59f1cc7ef2fd78",614:"7bd372e60e3c08002159",728:"d3d7f45cbb660912937a",766:"6c1cd9d090d29d4e0f6c",862:"bd092862dace3d95adee",863:"6457fe92acacc6820be3",944:"857639abede24d5ace51"}[e]+".js?v="+{43:"977ebe1fbf293ad5c7f9",261:"eb6a382fac090947fcec",276:"c4667dd47bc8bfdfdf73",424:"505fc92112b360ef4e5b",497:"a88640af5e122a91bf01",549:"42284772e4a962464d9b",568:"f00f1ada234ad803ccec",584:"e7a2de59f1cc7ef2fd78",614:"7bd372e60e3c08002159",728:"d3d7f45cbb660912937a",766:"6c1cd9d090d29d4e0f6c",862:"bd092862dace3d95adee",863:"6457fe92acacc6820be3",944:"857639abede24d5ace51"}[e],P.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),P.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),e={},r="cad-viewer-widget:",P.l=(t,a,n,o)=>{if(e[t])e[t].push(a);else{var i,d;if(void 0!==n)for(var l=document.getElementsByTagName("script"),u=0;u<l.length;u++){var f=l[u];if(f.getAttribute("src")==t||f.getAttribute("data-webpack")==r+n){i=f;break}}i||(d=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,P.nc&&i.setAttribute("nonce",P.nc),i.setAttribute("data-webpack",r+n),i.src=t),e[t]=[a];var s=(r,a)=>{i.onerror=i.onload=null,clearTimeout(c);var n=e[t];if(delete e[t],i.parentNode&&i.parentNode.removeChild(i),n&&n.forEach((e=>e(a))),r)return r(a)},c=setTimeout(s.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=s.bind(null,i.onerror),i.onload=s.bind(null,i.onload),d&&document.head.appendChild(i)}},P.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{P.S={};var e={},r={};P.I=(t,a)=>{a||(a=[]);var n=r[t];if(n||(n=r[t]={}),!(a.indexOf(n)>=0)){if(a.push(n),e[t])return e[t];P.o(P.S,t)||(P.S[t]={});var o=P.S[t],i="cad-viewer-widget",d=(e,r,t,a)=>{var n=o[e]=o[e]||{},d=n[r];(!d||!d.loaded&&(!a!=!d.eager?a:i>d.from))&&(n[r]={get:t,from:i,eager:!!a})},l=[];return"default"===t&&(d("@jupyter-widgets/jupyterlab-manager","3.0.1",(()=>Promise.all([P.e(944),P.e(728),P.e(862),P.e(614)]).then((()=>()=>P(4944))))),d("cad-viewer-widget","0.10.4",(()=>Promise.all([P.e(549),P.e(728),P.e(568)]).then((()=>()=>P(1568))))),d("js-base64","3.7.2",(()=>P.e(276).then((()=>()=>P(4276))))),d("pako","2.0.4",(()=>P.e(424).then((()=>()=>P(8424))))),d("three-cad-viewer","1.2.8",(()=>P.e(766).then((()=>()=>P(766)))))),e[t]=l.length?Promise.all(l).then((()=>e[t]=1)):1}}})(),(()=>{var e;P.g.importScripts&&(e=P.g.location+"");var r=P.g.document;if(!e&&r&&(r.currentScript&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");t.length&&(e=t[t.length-1].src)}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),P.p=e})(),t=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),a=t[1]?r(t[1]):[];return t[2]&&(a.length++,a.push.apply(a,r(t[2]))),t[3]&&(a.push([]),a.push.apply(a,r(t[3]))),a},a=(e,r)=>{e=t(e),r=t(r);for(var a=0;;){if(a>=e.length)return a<r.length&&"u"!=(typeof r[a])[0];var n=e[a],o=(typeof n)[0];if(a>=r.length)return"u"==o;var i=r[a],d=(typeof i)[0];if(o!=d)return"o"==o&&"n"==d||"s"==d||"u"==o;if("o"!=o&&"u"!=o&&n!=i)return n<i;a++}},n=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var a=1,o=1;o<e.length;o++)a--,t+="u"==(typeof(d=e[o]))[0]?"-":(a>0?".":"")+(a=2,d);return t}var i=[];for(o=1;o<e.length;o++){var d=e[o];i.push(0===d?"not("+l()+")":1===d?"("+l()+" || "+l()+")":2===d?i.pop()+" "+i.pop():n(d))}return l();function l(){return i.pop().replace(/^\((.+)\)$/,"$1")}},o=(e,r)=>{if(0 in e){r=t(r);var a=e[0],n=a<0;n&&(a=-a-1);for(var i=0,d=1,l=!0;;d++,i++){var u,f,s=d<e.length?(typeof e[d])[0]:"";if(i>=r.length||"o"==(f=(typeof(u=r[i]))[0]))return!l||("u"==s?d>a&&!n:""==s!=n);if("u"==f){if(!l||"u"!=s)return!1}else if(l)if(s==f)if(d<=a){if(u!=e[d])return!1}else{if(n?u>e[d]:u<e[d])return!1;u!=e[d]&&(l=!1)}else if("s"!=s&&"n"!=s){if(n||d<=a)return!1;l=!1,d--}else{if(d<=a||f<s!=n)return!1;l=!1}else"s"!=s&&"n"!=s&&(l=!1,d--)}}var c=[],p=c.pop.bind(c);for(i=1;i<e.length;i++){var b=e[i];c.push(1==b?p()|p():2==b?p()&p():b?o(b,r):!p())}return!!p()},i=(e,r)=>{var t=P.S[e];if(!t||!P.o(t,r))throw new Error("Shared module "+r+" doesn't exist in shared scope "+e);return t},d=(e,r)=>{var t=e[r];return(r=Object.keys(t).reduce(((e,r)=>!e||a(e,r)?r:e),0))&&t[r]},l=(e,r)=>{var t=e[r];return Object.keys(t).reduce(((e,r)=>!e||!t[e].loaded&&a(e,r)?r:e),0)},u=(e,r,t,a)=>"Unsatisfied version "+t+" from "+(t&&e[r][t].from)+" of shared singleton module "+r+" (required "+n(a)+")",f=(e,r,t,a)=>{var n=l(e,t);return o(a,n)||"undefined"!=typeof console&&console.warn&&console.warn(u(e,t,n,a)),b(e[t][n])},s=(e,r,t)=>{var n=e[r];return(r=Object.keys(n).reduce(((e,r)=>!o(t,r)||e&&!a(e,r)?e:r),0))&&n[r]},c=(e,r,t,a)=>{var o=e[t];return"No satisfying version ("+n(a)+") of shared module "+t+" found in shared scope "+r+".\nAvailable versions: "+Object.keys(o).map((e=>e+" from "+o[e].from)).join(", ")},p=(e,r,t,a)=>{"undefined"!=typeof console&&console.warn&&console.warn(c(e,r,t,a))},b=e=>(e.loaded=1,e.get()),v=(h=e=>function(r,t,a,n){var o=P.I(r);return o&&o.then?o.then(e.bind(e,r,P.S[r],t,a,n)):e(r,P.S[r],t,a,n)})(((e,r,t,a)=>(i(e,t),b(s(r,t,a)||p(r,e,t,a)||d(r,t))))),m=h(((e,r,t,a)=>(i(e,t),f(r,0,t,a)))),g=h(((e,r,t,a,n)=>{var o=r&&P.o(r,t)&&s(r,t,a);return o?b(o):n()})),y={},w={6728:()=>m("default","@jupyter-widgets/base",[1,4,0,0]),3242:()=>g("default","@jupyter-widgets/jupyterlab-manager",[1,3,0,0],(()=>Promise.all([P.e(944),P.e(862),P.e(584)]).then((()=>()=>P(4944))))),4704:()=>g("default","pako",[1,2,0,4],(()=>P.e(424).then((()=>()=>P(8424))))),4895:()=>g("default","three-cad-viewer",[4,1,2,8],(()=>P.e(766).then((()=>()=>P(766))))),9616:()=>g("default","js-base64",[1,3,7,2],(()=>P.e(276).then((()=>()=>P(4276))))),1464:()=>m("default","@jupyterlab/mainmenu",[1,3,2,1]),1797:()=>m("default","@lumino/coreutils",[1,1,5,3]),2310:()=>m("default","@jupyterlab/logconsole",[1,3,2,1]),2575:()=>m("default","@jupyterlab/notebook",[1,3,2,1]),3706:()=>m("default","@lumino/widgets",[1,1,19,0]),4337:()=>m("default","@jupyterlab/settingregistry",[1,3,2,1]),4881:()=>v("default","@jupyterlab/outputarea",[1,3,2,1]),5890:()=>m("default","@jupyterlab/services",[1,6,2,1]),6168:()=>m("default","@lumino/signaling",[1,1,4,3]),8562:()=>m("default","@lumino/properties",[1,1,2,3]),9129:()=>m("default","@lumino/disposable",[1,1,4,3]),9850:()=>m("default","@lumino/algorithm",[1,1,3,3]),9938:()=>m("default","@jupyterlab/rendermime",[1,3,2,1]),3211:()=>m("default","@lumino/messaging",[1,1,4,3]),608:()=>m("default","@lumino/domutils",[1,1,2,3])},j={497:[3242,4704,4895,9616],568:[3242,4704,4895,9616],728:[6728],862:[1464,1797,2310,2575,3706,4337,4881,5890,6168,8562,9129,9850,9938],863:[3211,608]},P.f.consumes=(e,r)=>{P.o(j,e)&&j[e].forEach((e=>{if(P.o(y,e))return r.push(y[e]);var t=r=>{y[e]=0,P.m[e]=t=>{delete P.c[e],t.exports=r()}},a=r=>{delete y[e],P.m[e]=t=>{throw delete P.c[e],r}};try{var n=w[e]();n.then?r.push(y[e]=n.then(t).catch(a)):t(n)}catch(e){a(e)}}))},(()=>{P.b=document.baseURI||self.location.href;var e={2:0};P.f.j=(r,t)=>{var a=P.o(e,r)?e[r]:void 0;if(0!==a)if(a)t.push(a[2]);else if(/^(86[23]|497|728)$/.test(r))e[r]=0;else{var n=new Promise(((t,n)=>a=e[r]=[t,n]));t.push(a[2]=n);var o=P.p+P.u(r),i=new Error;P.l(o,(t=>{if(P.o(e,r)&&(0!==(a=e[r])&&(e[r]=void 0),a)){var n=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src;i.message="Loading chunk "+r+" failed.\n("+n+": "+o+")",i.name="ChunkLoadError",i.type=n,i.request=o,a[1](i)}}),"chunk-"+r,r)}};var r=(r,t)=>{var a,n,[o,i,d]=t,l=0;if(o.some((r=>0!==e[r]))){for(a in i)P.o(i,a)&&(P.m[a]=i[a]);d&&d(P)}for(r&&r(t);l<o.length;l++)n=o[l],P.o(e,n)&&e[n]&&e[n][0](),e[n]=0},t=self.webpackChunkcad_viewer_widget=self.webpackChunkcad_viewer_widget||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})();var E=P(8457);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB)["cad-viewer-widget"]=E})();