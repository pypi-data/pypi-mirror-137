(()=>{var e,t,s={31410:()=>{Array.prototype.flat||Object.defineProperty(Array.prototype,"flat",{configurable:!0,writable:!0,value:function(...e){const t=void 0===e[0]?1:Number(e[0])||0,s=[],n=s.forEach,o=(e,t)=>{n.call(e,(e=>{t>0&&Array.isArray(e)?o(e,t-1):s.push(e)}))};return o(this,t),s}})},37846:()=>{if(/^((?!chrome|android).)*version\/14\.0\s.*safari/i.test(navigator.userAgent)){const e=window.Element.prototype.attachShadow;window.Element.prototype.attachShadow=function(t){return t&&t.delegatesFocus&&delete t.delegatesFocus,e.apply(this,[t])}}},10280:(e,t,s)=>{"use strict";s.d(t,{gx:()=>c,v0:()=>d});var n=s(63094),o=s(10968);function r(e,t,s,n){s+=(s.includes("?")?"&":"?")+"auth_callback=1",document.location.href=function(e,t,s,n){let o=`${e}/auth/authorize?response_type=code&redirect_uri=${encodeURIComponent(s)}`;return null!==t&&(o+=`&client_id=${encodeURIComponent(t)}`),n&&(o+=`&state=${encodeURIComponent(n)}`),o}(e,t,s,n)}async function i(e,t,s){const n="undefined"!=typeof location&&location;if(n&&"https:"===n.protocol){const t=document.createElement("a");if(t.href=e,"http:"===t.protocol&&"localhost"!==t.hostname)throw o.rh}const r=new FormData;null!==t&&r.append("client_id",t),Object.keys(s).forEach((e=>{r.append(e,s[e])}));const i=await fetch(`${e}/auth/token`,{method:"POST",credentials:"same-origin",body:r});if(!i.ok)throw 400===i.status||403===i.status?o.DJ:new Error("Unable to fetch tokens");const a=await i.json();return a.hassUrl=e,a.clientId=t,a.expires=1e3*a.expires_in+Date.now(),a}function a(e,t,s){return i(e,t,{code:s,grant_type:"authorization_code"})}class c{constructor(e,t){this.data=e,this._saveTokens=t}get wsUrl(){return`ws${this.data.hassUrl.substr(4)}/api/websocket`}get accessToken(){return this.data.access_token}get expired(){return Date.now()>this.data.expires}async refreshAccessToken(){if(!this.data.refresh_token)throw new Error("No refresh_token");const e=await i(this.data.hassUrl,this.data.clientId,{grant_type:"refresh_token",refresh_token:this.data.refresh_token});e.refresh_token=this.data.refresh_token,this.data=e,this._saveTokens&&this._saveTokens(e)}async revoke(){if(!this.data.refresh_token)throw new Error("No refresh_token to revoke");const e=new FormData;e.append("action","revoke"),e.append("token",this.data.refresh_token),await fetch(`${this.data.hassUrl}/auth/token`,{method:"POST",credentials:"same-origin",body:e}),this._saveTokens&&this._saveTokens(null)}}async function d(e={}){let t,s=e.hassUrl;s&&"/"===s[s.length-1]&&(s=s.substr(0,s.length-1));const i=void 0!==e.clientId?e.clientId:`${location.protocol}//${location.host}/`;if(!t&&e.authCode&&s&&(t=await a(s,i,e.authCode),e.saveTokens&&e.saveTokens(t)),!t){const s=(0,n.m)(location.search.substr(1));if("auth_callback"in s){const n=(d=s.state,JSON.parse(atob(d)));t=await a(n.hassUrl,n.clientId,s.code),e.saveTokens&&e.saveTokens(t)}}var d,h;if(!t&&e.loadTokens&&(t=await e.loadTokens()),t)return new c(t,e.saveTokens);if(void 0===s)throw o.Js;return r(s,i,e.redirectUrl||function(){const{protocol:e,host:t,pathname:s,search:n}=location;return`${e}//${t}${s}${n}`}(),(h={hassUrl:s,clientId:i},btoa(JSON.stringify(h)))),new Promise((()=>{}))}},10968:(e,t,s)=>{"use strict";s.d(t,{OH:()=>n,DJ:()=>o,Wf:()=>r,Js:()=>i,rh:()=>a});const n=1,o=2,r=3,i=4,a=5},63094:(e,t,s)=>{"use strict";function n(e){const t={},s=e.split("&");for(let e=0;e<s.length;e++){const n=s[e].split("="),o=decodeURIComponent(n[0]),r=n.length>1?decodeURIComponent(n[1]):void 0;t[o]=r}return t}s.d(t,{m:()=>n,D:()=>o});const o=(e,t,s=!1)=>{let n;return function(...o){const r=this,i=s&&!n;clearTimeout(n),n=setTimeout((()=>{n=void 0,s||e.apply(r,o)}),t),i&&e.apply(r,o)}}}},n={};function o(e){var t=n[e];if(void 0!==t)return t.exports;var r=n[e]={exports:{}};return s[e](r,r.exports,o),r.exports}o.m=s,o.d=(e,t)=>{for(var s in t)o.o(t,s)&&!o.o(e,s)&&Object.defineProperty(e,s,{enumerable:!0,get:t[s]})},o.f={},o.e=e=>Promise.all(Object.keys(o.f).reduce(((t,s)=>(o.f[s](e,t),t)),[])),o.u=e=>"c93fc7eb.js",o.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),e={},t="home-assistant-frontend:",o.l=(s,n,r,i)=>{if(e[s])e[s].push(n);else{var a,c;if(void 0!==r)for(var d=document.getElementsByTagName("script"),h=0;h<d.length;h++){var l=d[h];if(l.getAttribute("src")==s||l.getAttribute("data-webpack")==t+r){a=l;break}}a||(c=!0,(a=document.createElement("script")).charset="utf-8",a.timeout=120,o.nc&&a.setAttribute("nonce",o.nc),a.setAttribute("data-webpack",t+r),a.src=s),e[s]=[n];var u=(t,n)=>{a.onerror=a.onload=null,clearTimeout(f);var o=e[s];if(delete e[s],a.parentNode&&a.parentNode.removeChild(a),o&&o.forEach((e=>e(n))),t)return t(n)},f=setTimeout(u.bind(null,void 0,{type:"timeout",target:a}),12e4);a.onerror=u.bind(null,a.onerror),a.onload=u.bind(null,a.onload),c&&document.head.appendChild(a)}},o.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},o.p="/frontend_latest/",(()=>{var e={61321:0};o.f.j=(t,s)=>{var n=o.o(e,t)?e[t]:void 0;if(0!==n)if(n)s.push(n[2]);else{var r=new Promise(((s,o)=>n=e[t]=[s,o]));s.push(n[2]=r);var i=o.p+o.u(t),a=new Error;o.l(i,(s=>{if(o.o(e,t)&&(0!==(n=e[t])&&(e[t]=void 0),n)){var r=s&&("load"===s.type?"missing":s.type),i=s&&s.target&&s.target.src;a.message="Loading chunk "+t+" failed.\n("+r+": "+i+")",a.name="ChunkLoadError",a.type=r,a.request=i,n[1](a)}}),"chunk-"+t,t)}};var t=(t,s)=>{var n,r,[i,a,c]=s,d=0;if(i.some((t=>0!==e[t]))){for(n in a)o.o(a,n)&&(o.m[n]=a[n]);if(c)c(o)}for(t&&t(s);d<i.length;d++)r=i[d],o.o(e,r)&&e[r]&&e[r][0](),e[i[d]]=0},s=self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[];s.forEach(t.bind(null,0)),s.push=t.bind(null,s.push.bind(s))})(),(()=>{"use strict";var e=o(10968);function t(e){return{type:"unsubscribe_events",subscription:e}}function s(t){if(!t.auth)throw e.Js;const s=t.auth;let n=s.expired?s.refreshAccessToken().then((()=>{n=void 0}),(()=>{n=void 0})):void 0;const o=s.wsUrl;function r(t,i,a){const c=new WebSocket(o);let d=!1;const h=()=>{if(c.removeEventListener("close",h),d)return void a(e.DJ);if(0===t)return void a(e.OH);const s=-1===t?-1:t-1;setTimeout((()=>r(s,i,a)),1e3)},l=async t=>{try{s.expired&&await(n||s.refreshAccessToken()),c.send(JSON.stringify({type:"auth",access_token:s.accessToken}))}catch(t){d=t===e.DJ,c.close()}},u=async e=>{const t=JSON.parse(e.data);switch(t.type){case"auth_invalid":d=!0,c.close();break;case"auth_ok":c.removeEventListener("open",l),c.removeEventListener("message",u),c.removeEventListener("close",h),c.removeEventListener("error",h),c.haVersion=t.ha_version,i(c)}};c.addEventListener("open",l),c.addEventListener("message",u),c.addEventListener("close",h),c.addEventListener("error",h)}return new Promise(((e,s)=>r(t.setupRetry,e,s)))}const n=!1;class r{constructor(s,o){this._handleMessage=e=>{const s=JSON.parse(e.data);const n=this.commands.get(s.id);switch(s.type){case"event":n?n.callback(s.event):(console.warn(`Received event for unknown subscription ${s.id}. Unsubscribing.`),this.sendMessagePromise(t(s.id)));break;case"result":n&&(s.success?(n.resolve(s.result),"subscribe"in n||this.commands.delete(s.id)):(n.reject(s.error),this.commands.delete(s.id)));break;case"pong":n?(n.resolve(),this.commands.delete(s.id)):console.warn(`Received unknown pong response ${s.id}`)}},this._handleClose=async()=>{const t=this.commands;if(this.commandId=1,this.oldSubscriptions=this.commands,this.commands=new Map,this.socket=void 0,t.forEach((t=>{"subscribe"in t||t.reject({type:"result",success:!1,error:{code:e.Wf,message:"Connection lost"}})})),this.closeRequested)return;this.fireEvent("disconnected");const s=Object.assign(Object.assign({},this.options),{setupRetry:0}),o=t=>{setTimeout((async()=>{if(!this.closeRequested){n;try{const e=await s.createSocket(s);this._setSocket(e)}catch(s){if(this._queuedMessages){const t=this._queuedMessages;this._queuedMessages=void 0;for(const s of t)s.reject&&s.reject(e.Wf)}s===e.DJ?this.fireEvent("reconnect-error",s):o(t+1)}}}),1e3*Math.min(t,5))};this.suspendReconnectPromise&&(await this.suspendReconnectPromise,this.suspendReconnectPromise=void 0,this._queuedMessages=[]),o(0)},this.options=o,this.commandId=1,this.commands=new Map,this.eventListeners=new Map,this.closeRequested=!1,this._setSocket(s)}get connected(){return void 0!==this.socket&&this.socket.readyState==this.socket.OPEN}_setSocket(e){this.socket=e,this.haVersion=e.haVersion,e.addEventListener("message",this._handleMessage),e.addEventListener("close",this._handleClose);const t=this.oldSubscriptions;t&&(this.oldSubscriptions=void 0,t.forEach((e=>{"subscribe"in e&&e.subscribe&&e.subscribe().then((t=>{e.unsubscribe=t,e.resolve()}))})));const s=this._queuedMessages;if(s){this._queuedMessages=void 0;for(const e of s)e.resolve()}this.fireEvent("ready")}addEventListener(e,t){let s=this.eventListeners.get(e);s||(s=[],this.eventListeners.set(e,s)),s.push(t)}removeEventListener(e,t){const s=this.eventListeners.get(e);if(!s)return;const n=s.indexOf(t);-1!==n&&s.splice(n,1)}fireEvent(e,t){(this.eventListeners.get(e)||[]).forEach((e=>e(this,t)))}suspendReconnectUntil(e){this.suspendReconnectPromise=e}suspend(){if(!this.suspendReconnectPromise)throw new Error("Suspend promise not set");this.socket&&this.socket.close()}reconnect(e=!1){this.socket&&(e?(this.socket.removeEventListener("message",this._handleMessage),this.socket.removeEventListener("close",this._handleClose),this.socket.close(),this._handleClose()):this.socket.close())}close(){this.closeRequested=!0,this.socket&&this.socket.close()}async subscribeEvents(e,t){return this.subscribeMessage(e,function(e){const t={type:"subscribe_events"};return e&&(t.event_type=e),t}(t))}ping(){return this.sendMessagePromise({type:"ping"})}sendMessage(t,s){if(!this.connected)throw e.Wf;if(this._queuedMessages){if(s)throw new Error("Cannot queue with commandId");this._queuedMessages.push({resolve:()=>this.sendMessage(t)})}else s||(s=this._genCmdId()),t.id=s,this.socket.send(JSON.stringify(t))}sendMessagePromise(e){return new Promise(((t,s)=>{if(this._queuedMessages)return void this._queuedMessages.push({reject:s,resolve:async()=>{try{t(await this.sendMessagePromise(e))}catch(e){s(e)}}});const n=this._genCmdId();this.commands.set(n,{resolve:t,reject:s}),this.sendMessage(e,n)}))}async subscribeMessage(e,s,n){let o;return this._queuedMessages&&await new Promise(((e,t)=>{this._queuedMessages.push({resolve:e,reject:t})})),await new Promise(((r,i)=>{const a=this._genCmdId();o={resolve:r,reject:i,callback:e,subscribe:!1!==(null==n?void 0:n.resubscribe)?()=>this.subscribeMessage(e,s):void 0,unsubscribe:async()=>{this.connected&&await this.sendMessagePromise(t(a)),this.commands.delete(a)}},this.commands.set(a,o);try{this.sendMessage(s,a)}catch(e){}})),()=>o.unsubscribe()}_genCmdId(){return++this.commandId}}async function i(e){const t=Object.assign({setupRetry:0,createSocket:s},e),n=await t.createSocket(t);return new r(n,t)}const a=e=>{let t=[];function s(s,n){e=n?s:Object.assign(Object.assign({},e),s);let o=t;for(let t=0;t<o.length;t++)o[t](e)}return{get state(){return e},action(t){function n(e){s(e,!1)}return function(){let s=[e];for(let e=0;e<arguments.length;e++)s.push(arguments[e]);let o=t.apply(this,s);if(null!=o)return o instanceof Promise?o.then(n):n(o)}},setState:s,subscribe:e=>(t.push(e),()=>{!function(e){let s=[];for(let n=0;n<t.length;n++)t[n]===e?e=null:s.push(t[n]);t=s}(e)})}},c=(e,t,s,n)=>{if(e[t])return e[t];let o,r=0,i=a();const c=()=>s(e).then((e=>i.setState(e,!0))),d=()=>c().catch((t=>{if(e.connected)throw t}));return e[t]={get state(){return i.state},refresh:c,subscribe(t){r++,1===r&&(n&&(o=n(e,i)),e.addEventListener("ready",d),d());const s=i.subscribe(t);return void 0!==i.state&&setTimeout((()=>t(i.state)),0),()=>{s(),r--,r||(o&&o.then((e=>{e()})),e.removeEventListener("ready",c))}}},e[t]},d=(e,t,s,n,o)=>c(n,e,t,s).subscribe(o),h=e=>e.sendMessagePromise({type:"get_states"});async function l(e){const t=await h(e),s={};for(let e=0;e<t.length;e++){const n=t[e];s[n.entity_id]=n}return s}const u=(e,t)=>e.subscribeEvents((e=>function(e,t){const s=e.state;if(void 0===s)return;const{entity_id:n,new_state:o}=t.data;if(o)e.setState({[o.entity_id]:o});else{const t=Object.assign({},s);delete t[n],e.setState(t,!0)}}(t,e)),"state_changed"),f=(e,t)=>(e=>c(e,"_ent",l,u))(e).subscribe(t);function p(e,t){return void 0===e?null:{components:e.components.concat(t.data.component)}}const v=e=>e.sendMessagePromise({type:"get_config"}),m=(e,t)=>Promise.all([e.subscribeEvents(t.action(p),"component_loaded"),e.subscribeEvents((()=>v(e).then((e=>t.setState(e,!0)))),"core_config_updated")]).then((e=>()=>e.forEach((e=>e())))),b=(e,t)=>(e=>c(e,"_cnf",v,m))(e).subscribe(t);function g(e,t){if(void 0===e)return null;const{domain:s,service:n}=t.data,o=e[s];if(!o||!(n in o))return null;const r={};return Object.keys(o).forEach((e=>{e!==n&&(r[e]=o[e])})),{[s]:r}}const w=(0,o(63094).D)(((e,t)=>k(e).then((e=>t.setState(e,!0)))),5e3),k=e=>e.sendMessagePromise({type:"get_services"}),_=(e,t)=>Promise.all([e.subscribeEvents((s=>function(e,t,s){var n;const o=t.state;if(void 0===o)return;const{domain:r,service:i}=s.data;if(!(null===(n=o.domain)||void 0===n?void 0:n.service)){const e=Object.assign(Object.assign({},o[r]),{[i]:{description:"",fields:{}}});t.setState({[r]:e})}w(e,t)}(e,t,s)),"service_registered"),e.subscribeEvents(t.action(g),"service_removed")]).then((e=>()=>e.forEach((e=>e())))),y=(e,t)=>(e=>c(e,"_srv",k,_))(e).subscribe(t);var E=o(10280);const S=window.localStorage||{};let P=window.__tokenCache;function M(e){var t;if(P.tokens=e,P.writeEnabled||"true"!==(t="storeToken",new URLSearchParams(window.location.search).get(t))||(P.writeEnabled=!0),P.writeEnabled)try{S.hassTokens=JSON.stringify(e)}catch(e){}}P||(P=window.__tokenCache={tokens:void 0,writeEnabled:void 0});const T=`${location.protocol}//${location.host}`;var O,C;const j=window.externalApp||(null===(O=window.webkit)||void 0===O||null===(C=O.messageHandlers)||void 0===C?void 0:C.getExternalAuth)||location.search.includes("external_auth=1"),L=(e,t)=>((e,t,s,n,o)=>{const r=`${s}-optimistic`;return{...c(t,s,n,(async(e,s)=>{const n=o?o(t,s):void 0;return t[r]=s,()=>{n&&n.then((e=>e())),t[r]=void 0}})),async save(s){const n=t[r];let o;n&&(o=n.state,n.setState(s,!0));try{return await e(t,s)}catch(e){throw n&&n.setState(o,!0),e}}}})(((s,n)=>(async(e,t,s)=>e.sendMessagePromise({type:"frontend/set_user_data",key:t,value:s}))(e,t,n)),e,`_frontendUserData-${t}`,(()=>(async(e,t)=>(await e.sendMessagePromise({type:"frontend/get_user_data",key:t})).value)(e,t))),$=(e,t,s)=>e.sendMessagePromise({type:"lovelace/config",url_path:t,force:s}),R=e=>e.sendMessagePromise({type:"get_panels"}),U=(e,t)=>e.subscribeEvents((()=>R(e).then((e=>t.setState(e,!0)))),"panels_updated"),I=e=>e.sendMessagePromise({type:"frontend/get_themes"}),q=(e,t)=>e.subscribeEvents((()=>I(e).then((e=>t.setState(e,!0)))),"themes_updated"),x=(e,t)=>(e=>c(e,"_usr",(()=>e.sendMessagePromise({type:"auth/current_user"})),void 0))(e).subscribe(t);o(31410),o(37846);window.name="ha-main-window",window.frontendVersion="20220201.0";const J=()=>{if(location.search.includes("auth_callback=1")){const e=new URLSearchParams(location.search);e.delete("auth_callback"),e.delete("code"),e.delete("state"),e.delete("storeToken");const t=e.toString();history.replaceState(null,"",`${location.pathname}${t?`?${t}`:""}`)}},A=j?()=>o.e(39085).then(o.bind(o,39085)).then((({createExternalAuth:e})=>e(T))):()=>(0,E.v0)({hassUrl:T,saveTokens:M,loadTokens:()=>Promise.resolve(function(){if(void 0===P.tokens)try{delete S.tokens;const e=S.hassTokens;e?(P.tokens=JSON.parse(e),P.writeEnabled=!0):P.tokens=null}catch(e){P.tokens=null}return P.tokens}())});window.hassConnection=A().then((async t=>{try{const e=await i({auth:t});return J(),{auth:t,conn:e}}catch(s){if(s!==e.DJ)throw s;j?await t.refreshAccessToken(!0):M(null),t=await A();const n=await i({auth:t});return J(),{auth:t,conn:n}}})),window.hassConnectionReady&&window.hassConnectionReady(window.hassConnection),window.hassConnection.then((({conn:e})=>{const t=()=>{};if(f(e,t),b(e,t),y(e,t),((e,t)=>{d("_pnl",R,U,e,t)})(e,t),((e,t)=>{d("_thm",I,q,e,t)})(e,t),x(e,t),((e,t,s)=>{L(e,t).subscribe(s)})(e,"core",t),"/"===location.pathname||location.pathname.startsWith("/lovelace/")){const t=window;t.llConfProm=$(e,null,!1),t.llConfProm.catch((()=>{})),t.llResProm=(e=>e.sendMessagePromise({type:"lovelace/resources"}))(e)}})),window.addEventListener("error",(e=>{if("ResizeObserver loop limit exceeded"===e.message)return e.stopImmediatePropagation(),void e.stopPropagation();const t=document.querySelector("home-assistant");t&&t.hass&&t.hass.callService&&t.hass.callService("system_log","write",{logger:`frontend.js.latest.${"20220201.0".replace(".","")}`,message:`${e.filename}:${e.lineno}:${e.colno} ${e.message}`})}))})()})();