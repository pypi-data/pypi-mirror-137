/*! For license information please see b6a4e485.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[44961],{18601:(e,t,n)=>{n.d(t,{qN:()=>s.q,Wg:()=>p});var o,r,a=n(87480),i=n(72367),s=n(78220);const l=null!==(r=null===(o=window.ShadyDOM)||void 0===o?void 0:o.inUse)&&void 0!==r&&r;class p extends s.H{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=e=>{this.disabled||this.setFormData(e.formData)}}findFormElement(){if(!this.shadowRoot||l)return null;const e=this.getRootNode().querySelectorAll("form");for(const t of Array.from(e))if(t.contains(this))return t;return null}connectedCallback(){var e;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(e=this.containingForm)||void 0===e||e.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var e;super.disconnectedCallback(),null===(e=this.containingForm)||void 0===e||e.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(e=>{this.dispatchEvent(new Event("change",e))}))}}p.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,a.__decorate)([(0,i.Cb)({type:Boolean})],p.prototype,"disabled",void 0)},25782:(e,t,n)=>{n(94604),n(65660),n(70019),n(97968);var o=n(9672),r=n(50856),a=n(33760);(0,o.k)({_template:r.d`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[a.U]})},33760:(e,t,n)=>{n.d(t,{U:()=>a});n(94604);var o=n(51644),r=n(26110);const a=[o.P,r.a,{hostAttributes:{role:"option",tabindex:"0"}}]},89194:(e,t,n)=>{n(94604),n(65660),n(70019);var o=n(9672),r=n(50856);(0,o.k)({_template:r.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},97968:(e,t,n)=>{n(65660),n(70019);const o=document.createElement("template");o.setAttribute("style","display: none;"),o.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(o.content)},23682:(e,t,n)=>{function o(e,t){if(t.length<e)throw new TypeError(e+" argument"+(e>1?"s":"")+" required, but only "+t.length+" present")}n.d(t,{Z:()=>o})},90394:(e,t,n)=>{function o(e){if(null===e||!0===e||!1===e)return NaN;var t=Number(e);return isNaN(t)?t:t<0?Math.ceil(t):Math.floor(t)}n.d(t,{Z:()=>o})},59699:(e,t,n)=>{n.d(t,{Z:()=>s});var o=n(90394),r=n(39244),a=n(23682),i=36e5;function s(e,t){(0,a.Z)(2,arguments);var n=(0,o.Z)(t);return(0,r.Z)(e,n*i)}},39244:(e,t,n)=>{n.d(t,{Z:()=>i});var o=n(90394),r=n(34327),a=n(23682);function i(e,t){(0,a.Z)(2,arguments);var n=(0,r.Z)(e).getTime(),i=(0,o.Z)(t);return new Date(n+i)}},34327:(e,t,n)=>{n.d(t,{Z:()=>r});var o=n(23682);function r(e){(0,o.Z)(1,arguments);var t=Object.prototype.toString.call(e);return e instanceof Date||"object"==typeof e&&"[object Date]"===t?new Date(e.getTime()):"number"==typeof e||"[object Number]"===t?new Date(e):("string"!=typeof e&&"[object String]"!==t||"undefined"==typeof console||(console.warn("Starting with v2.0.0-beta.1 date-fns doesn't accept strings as date arguments. Please use `parseISO` to parse strings. See: https://git.io/fjule"),console.warn((new Error).stack)),new Date(NaN))}},21560:(e,t,n)=>{n.d(t,{ZH:()=>d,MT:()=>a,U2:()=>l,RV:()=>r,t8:()=>p});const o=function(){if(!(!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent))||!indexedDB.databases)return Promise.resolve();let e;return new Promise((t=>{const n=()=>indexedDB.databases().finally(t);e=setInterval(n,100),n()})).finally((()=>clearInterval(e)))};function r(e){return new Promise(((t,n)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>n(e.error)}))}function a(e,t){const n=o().then((()=>{const n=indexedDB.open(e);return n.onupgradeneeded=()=>n.result.createObjectStore(t),r(n)}));return(e,o)=>n.then((n=>o(n.transaction(t,e).objectStore(t))))}let i;function s(){return i||(i=a("keyval-store","keyval")),i}function l(e,t=s()){return t("readonly",(t=>r(t.get(e))))}function p(e,t,n=s()){return n("readwrite",(n=>(n.put(t,e),r(n.transaction))))}function d(e=s()){return e("readwrite",(e=>(e.clear(),r(e.transaction))))}},57835:(e,t,n)=>{n.d(t,{Xe:()=>o.Xe,pX:()=>o.pX,XM:()=>o.XM});var o=n(38941)}}]);
//# sourceMappingURL=b6a4e485.js.map