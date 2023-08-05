/*! For license information please see 16c41349.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[73792],{14166:(t,i,e)=>{e.d(i,{W:()=>n});var a=function(){return a=Object.assign||function(t){for(var i,e=1,a=arguments.length;e<a;e++)for(var n in i=arguments[e])Object.prototype.hasOwnProperty.call(i,n)&&(t[n]=i[n]);return t},a.apply(this,arguments)};function n(t,i,e){void 0===i&&(i=Date.now()),void 0===e&&(e={});var n=a(a({},o),e||{}),s=(+t-+i)/1e3;if(Math.abs(s)<n.second)return{value:Math.round(s),unit:"second"};var r=s/60;if(Math.abs(r)<n.minute)return{value:Math.round(r),unit:"minute"};var l=s/3600;if(Math.abs(l)<n.hour)return{value:Math.round(l),unit:"hour"};var p=s/86400;if(Math.abs(p)<n.day)return{value:Math.round(p),unit:"day"};var m=new Date(t),h=new Date(i),u=m.getFullYear()-h.getFullYear();if(Math.round(Math.abs(u))>0)return{value:Math.round(u),unit:"year"};var d=12*u+m.getMonth()-h.getMonth();if(Math.round(Math.abs(d))>0)return{value:Math.round(d),unit:"month"};var c=s/604800;return{value:Math.round(c),unit:"week"}}var o={second:45,minute:45,hour:22,day:5}},54444:(t,i,e)=>{e(94604);var a=e(9672),n=e(87156),o=e(50856);(0,a.k)({_template:o.d`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,n.vz)(this).parentNode,i=(0,n.vz)(this).getOwnerRoot();return this.for?(0,n.vz)(i).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?i.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,n.vz)(this).textContent.trim()){for(var t=!0,i=(0,n.vz)(this).getEffectiveChildNodes(),e=0;e<i.length;e++)if(""!==i[e].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var i,e,a=this.offsetParent.getBoundingClientRect(),n=this._target.getBoundingClientRect(),o=this.getBoundingClientRect(),s=(n.width-o.width)/2,r=(n.height-o.height)/2,l=n.left-a.left,p=n.top-a.top;switch(this.position){case"top":i=l+s,e=p-o.height-t;break;case"bottom":i=l+s,e=p+n.height+t;break;case"left":i=l-o.width-t,e=p+r;break;case"right":i=l+n.width+t,e=p+r}this.fitToVisibleBounds?(a.left+i+o.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,i)+"px",this.style.right="auto"),a.top+e+o.height>window.innerHeight?(this.style.bottom=a.height-p+t+"px",this.style.top="auto"):(this.style.top=Math.max(-a.top,e)+"px",this.style.bottom="auto")):(this.style.left=i+"px",this.style.top=e+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var i=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":i+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":i+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},93217:(t,i,e)=>{e.d(i,{Ud:()=>h});const a=Symbol("Comlink.proxy"),n=Symbol("Comlink.endpoint"),o=Symbol("Comlink.releaseProxy"),s=Symbol("Comlink.thrown"),r=t=>"object"==typeof t&&null!==t||"function"==typeof t,l=new Map([["proxy",{canHandle:t=>r(t)&&t[a],serialize(t){const{port1:i,port2:e}=new MessageChannel;return p(t,i),[e,[e]]},deserialize:t=>(t.start(),h(t))}],["throw",{canHandle:t=>r(t)&&s in t,serialize({value:t}){let i;return i=t instanceof Error?{isError:!0,value:{message:t.message,name:t.name,stack:t.stack}}:{isError:!1,value:t},[i,[]]},deserialize(t){if(t.isError)throw Object.assign(new Error(t.value.message),t.value);throw t.value}}]]);function p(t,i=self){i.addEventListener("message",(function e(n){if(!n||!n.data)return;const{id:o,type:r,path:l}=Object.assign({path:[]},n.data),h=(n.data.argumentList||[]).map(g);let u;try{const i=l.slice(0,-1).reduce(((t,i)=>t[i]),t),e=l.reduce(((t,i)=>t[i]),t);switch(r){case"GET":u=e;break;case"SET":i[l.slice(-1)[0]]=g(n.data.value),u=!0;break;case"APPLY":u=e.apply(i,h);break;case"CONSTRUCT":u=function(t){return Object.assign(t,{[a]:!0})}(new e(...h));break;case"ENDPOINT":{const{port1:i,port2:e}=new MessageChannel;p(t,e),u=function(t,i){return y.set(t,i),t}(i,[i])}break;case"RELEASE":u=void 0;break;default:return}}catch(t){u={value:t,[s]:0}}Promise.resolve(u).catch((t=>({value:t,[s]:0}))).then((t=>{const[a,n]=f(t);i.postMessage(Object.assign(Object.assign({},a),{id:o}),n),"RELEASE"===r&&(i.removeEventListener("message",e),m(i))}))})),i.start&&i.start()}function m(t){(function(t){return"MessagePort"===t.constructor.name})(t)&&t.close()}function h(t,i){return d(t,[],i)}function u(t){if(t)throw new Error("Proxy has been released and is not useable")}function d(t,i=[],e=function(){}){let a=!1;const s=new Proxy(e,{get(e,n){if(u(a),n===o)return()=>v(t,{type:"RELEASE",path:i.map((t=>t.toString()))}).then((()=>{m(t),a=!0}));if("then"===n){if(0===i.length)return{then:()=>s};const e=v(t,{type:"GET",path:i.map((t=>t.toString()))}).then(g);return e.then.bind(e)}return d(t,[...i,n])},set(e,n,o){u(a);const[s,r]=f(o);return v(t,{type:"SET",path:[...i,n].map((t=>t.toString())),value:s},r).then(g)},apply(e,o,s){u(a);const r=i[i.length-1];if(r===n)return v(t,{type:"ENDPOINT"}).then(g);if("bind"===r)return d(t,i.slice(0,-1));const[l,p]=c(s);return v(t,{type:"APPLY",path:i.map((t=>t.toString())),argumentList:l},p).then(g)},construct(e,n){u(a);const[o,s]=c(n);return v(t,{type:"CONSTRUCT",path:i.map((t=>t.toString())),argumentList:o},s).then(g)}});return s}function c(t){const i=t.map(f);return[i.map((t=>t[0])),(e=i.map((t=>t[1])),Array.prototype.concat.apply([],e))];var e}const y=new WeakMap;function f(t){for(const[i,e]of l)if(e.canHandle(t)){const[a,n]=e.serialize(t);return[{type:"HANDLER",name:i,value:a},n]}return[{type:"RAW",value:t},y.get(t)||[]]}function g(t){switch(t.type){case"HANDLER":return l.get(t.name).deserialize(t.value);case"RAW":return t.value}}function v(t,i,e){return new Promise((a=>{const n=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");t.addEventListener("message",(function i(e){e.data&&e.data.id&&e.data.id===n&&(t.removeEventListener("message",i),a(e.data))})),t.start&&t.start(),t.postMessage(Object.assign({id:n},i),e)}))}}}]);
//# sourceMappingURL=16c41349.js.map