/*! For license information please see 9e0f2b75.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[73486,10729,31296,58991,47402,31223,39452],{14114:function(e,t,n){n.d(t,{P:function(){return o}});var o=function(e){return function(t,n){if(t.constructor._observers){if(!t.constructor.hasOwnProperty("_observers")){var o=t.constructor._observers;t.constructor._observers=new Map,o.forEach((function(e,n){return t.constructor._observers.set(n,e)}))}}else{t.constructor._observers=new Map;var r=t.updated;t.updated=function(e){var t=this;r.call(this,e),e.forEach((function(e,n){var o=t.constructor._observers.get(n);void 0!==o&&o.call(t,t[n],e)}))}}t.constructor._observers.set(n,e)}}},39841:function(e,t,n){n(94604),n(65660);var o,r,i,a=n(9672),s=n(87156),l=n(50856),c=n(44181);(0,a.k)({_template:(0,l.d)(o||(r=['\n    <style>\n      :host {\n        display: block;\n        /**\n         * Force app-header-layout to have its own stacking context so that its parent can\n         * control the stacking of it relative to other elements (e.g. app-drawer-layout).\n         * This could be done using `isolation: isolate`, but that\'s not well supported\n         * across browsers.\n         */\n        position: relative;\n        z-index: 0;\n      }\n\n      #wrapper ::slotted([slot=header]) {\n        @apply --layout-fixed-top;\n        z-index: 1;\n      }\n\n      #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) {\n        height: 100%;\n      }\n\n      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {\n        position: absolute;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) #wrapper #contentContainer {\n        @apply --layout-fit;\n        overflow-y: auto;\n        -webkit-overflow-scrolling: touch;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {\n        position: relative;\n      }\n\n      :host([fullbleed]) {\n        @apply --layout-vertical;\n        @apply --layout-fit;\n      }\n\n      :host([fullbleed]) #wrapper,\n      :host([fullbleed]) #wrapper #contentContainer {\n        @apply --layout-vertical;\n        @apply --layout-flex;\n      }\n\n      #contentContainer {\n        /* Create a stacking context here so that all children appear below the header. */\n        position: relative;\n        z-index: 0;\n      }\n\n      @media print {\n        :host([has-scrolling-region]) #wrapper #contentContainer {\n          overflow-y: visible;\n        }\n      }\n\n    </style>\n\n    <div id="wrapper" class="initializing">\n      <slot id="headerSlot" name="header"></slot>\n\n      <div id="contentContainer">\n        <slot></slot>\n      </div>\n    </div>\n'],i=['\n    <style>\n      :host {\n        display: block;\n        /**\n         * Force app-header-layout to have its own stacking context so that its parent can\n         * control the stacking of it relative to other elements (e.g. app-drawer-layout).\n         * This could be done using \\`isolation: isolate\\`, but that\'s not well supported\n         * across browsers.\n         */\n        position: relative;\n        z-index: 0;\n      }\n\n      #wrapper ::slotted([slot=header]) {\n        @apply --layout-fixed-top;\n        z-index: 1;\n      }\n\n      #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) {\n        height: 100%;\n      }\n\n      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {\n        position: absolute;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) #wrapper #contentContainer {\n        @apply --layout-fit;\n        overflow-y: auto;\n        -webkit-overflow-scrolling: touch;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {\n        position: relative;\n      }\n\n      :host([fullbleed]) {\n        @apply --layout-vertical;\n        @apply --layout-fit;\n      }\n\n      :host([fullbleed]) #wrapper,\n      :host([fullbleed]) #wrapper #contentContainer {\n        @apply --layout-vertical;\n        @apply --layout-flex;\n      }\n\n      #contentContainer {\n        /* Create a stacking context here so that all children appear below the header. */\n        position: relative;\n        z-index: 0;\n      }\n\n      @media print {\n        :host([has-scrolling-region]) #wrapper #contentContainer {\n          overflow-y: visible;\n        }\n      }\n\n    </style>\n\n    <div id="wrapper" class="initializing">\n      <slot id="headerSlot" name="header"></slot>\n\n      <div id="contentContainer">\n        <slot></slot>\n      </div>\n    </div>\n'],i||(i=r.slice(0)),o=Object.freeze(Object.defineProperties(r,{raw:{value:Object.freeze(i)}})))),is:"app-header-layout",behaviors:[c.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,s.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var e=this.header;if(this.isAttached&&e){this.$.wrapper.classList.remove("initializing"),e.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var t=e.offsetHeight;this.hasScrollingRegion?(e.style.left="",e.style.right=""):requestAnimationFrame(function(){var t=this.getBoundingClientRect(),n=document.documentElement.clientWidth-t.right;e.style.left=t.left+"px",e.style.right=n+"px"}.bind(this));var n=this.$.contentContainer.style;e.fixed&&!e.condenses&&this.hasScrollingRegion?(n.marginTop=t+"px",n.paddingTop=""):(n.paddingTop=t+"px",n.marginTop="")}}})},99257:function(e,t,n){n(94604);var o=n(15112),r=n(9672),i=n(87156);(0,r.k)({is:"iron-iconset-svg",properties:{name:{type:String,observer:"_nameChanged"},size:{type:Number,value:24},rtlMirroring:{type:Boolean,value:!1},useGlobalRtlAttribute:{type:Boolean,value:!1}},created:function(){this._meta=new o.P({type:"iconset",key:null,value:null})},attached:function(){this.style.display="none"},getIconNames:function(){return this._icons=this._createIconMap(),Object.keys(this._icons).map((function(e){return this.name+":"+e}),this)},applyIcon:function(e,t){this.removeIcon(e);var n=this._cloneIcon(t,this.rtlMirroring&&this._targetIsRTL(e));if(n){var o=(0,i.vz)(e.root||e);return o.insertBefore(n,o.childNodes[0]),e._svgIcon=n}return null},removeIcon:function(e){e._svgIcon&&((0,i.vz)(e.root||e).removeChild(e._svgIcon),e._svgIcon=null)},_targetIsRTL:function(e){if(null==this.__targetIsRTL)if(this.useGlobalRtlAttribute){var t=document.body&&document.body.hasAttribute("dir")?document.body:document.documentElement;this.__targetIsRTL="rtl"===t.getAttribute("dir")}else e&&e.nodeType!==Node.ELEMENT_NODE&&(e=e.host),this.__targetIsRTL=e&&"rtl"===window.getComputedStyle(e).direction;return this.__targetIsRTL},_nameChanged:function(){this._meta.value=null,this._meta.key=this.name,this._meta.value=this,this.async((function(){this.fire("iron-iconset-added",this,{node:window})}))},_createIconMap:function(){var e=Object.create(null);return(0,i.vz)(this).querySelectorAll("[id]").forEach((function(t){e[t.id]=t})),e},_cloneIcon:function(e,t){return this._icons=this._icons||this._createIconMap(),this._prepareSvgClone(this._icons[e],this.size,t)},_prepareSvgClone:function(e,t,n){if(e){var o=e.cloneNode(!0),r=document.createElementNS("http://www.w3.org/2000/svg","svg"),i=o.getAttribute("viewBox")||"0 0 "+t+" "+t,a="pointer-events: none; display: block; width: 100%; height: 100%;";return n&&o.hasAttribute("mirror-in-rtl")&&(a+="-webkit-transform:scale(-1,1);transform:scale(-1,1);transform-origin:center;"),r.setAttribute("viewBox",i),r.setAttribute("preserveAspectRatio","xMidYMid meet"),r.setAttribute("focusable","false"),r.style.cssText=a,r.appendChild(o).removeAttribute("id"),r}return null}})},49075:function(e,t,n){n.d(t,{S:function(){return a},B:function(){return s}});n(94604);var o=n(51644),r=n(26110),i=n(84938),a={observers:["_focusedChanged(receivedFocusFromKeyboard)"],_focusedChanged:function(e){e&&this.ensureRipple(),this.hasRipple()&&(this._ripple.holdDown=e)},_createRipple:function(){var e=i.o._createRipple();return e.id="ink",e.setAttribute("center",""),e.classList.add("circle"),e}},s=[o.P,r.a,i.o,a]},84938:function(e,t,n){n.d(t,{o:function(){return i}});n(94604),n(60748);var o=n(51644),r=n(87156),i={properties:{noink:{type:Boolean,observer:"_noinkChanged"},_rippleContainer:{type:Object}},_buttonStateChanged:function(){this.focused&&this.ensureRipple()},_downHandler:function(e){o.$._downHandler.call(this,e),this.pressed&&this.ensureRipple(e)},ensureRipple:function(e){if(!this.hasRipple()){this._ripple=this._createRipple(),this._ripple.noink=this.noink;var t=this._rippleContainer||this.root;if(t&&(0,r.vz)(t).appendChild(this._ripple),e){var n=(0,r.vz)(this._rippleContainer||this),o=(0,r.vz)(e).rootTarget;n.deepContains(o)&&this._ripple.uiDownAction(e)}}},getRipple:function(){return this.ensureRipple(),this._ripple},hasRipple:function(){return Boolean(this._ripple)},_createRipple:function(){return document.createElement("paper-ripple")},_noinkChanged:function(e){this.hasRipple()&&(this._ripple.noink=e)}}},8878:function(e,t,n){n(94604),n(8621),n(63207),n(30879),n(78814),n(60748),n(57548),n(73962);var o,r=n(51644),i=n(26110),a=n(21006),s=n(98235),l=n(18890),c=n(9672),u=n(87156),p=n(81668),d=n(50856),h=n(62276);var f,v,g=(0,l.x)(HTMLElement);(0,c.k)({_template:(0,d.d)(o||(f=['\n    <style include="paper-dropdown-menu-shared-styles"></style>\n\n    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" dynamic-align="[[dynamicAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate allow-outside-scroll="[[allowOutsideScroll]]" restore-focus-on-close="[[restoreFocusOnClose]]" expand-sizing-target-for-scrollbars="[[expandSizingTargetForScrollbars]]">\n      \x3c!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> --\x3e\n      <div class="dropdown-trigger" slot="dropdown-trigger">\n        <paper-ripple></paper-ripple>\n        \x3c!-- paper-input has type="text" for a11y, do not remove --\x3e\n        <paper-input id="input" type="text" invalid="[[invalid]]" readonly disabled="[[disabled]]" value="[[value]]" placeholder="[[placeholder]]" error-message="[[errorMessage]]" always-float-label="[[alwaysFloatLabel]]" no-label-float="[[noLabelFloat]]" label="[[label]]" input-role="button" input-aria-haspopup="listbox" autocomplete="off">\n          \x3c!-- support hybrid mode: user might be using paper-input 1.x which distributes via <content> --\x3e\n          <iron-icon icon="paper-dropdown-menu:arrow-drop-down" suffix slot="suffix"></iron-icon>\n        </paper-input>\n      </div>\n      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>\n    </paper-menu-button>\n'],v||(v=f.slice(0)),o=Object.freeze(Object.defineProperties(f,{raw:{value:Object.freeze(v)}})))),is:"paper-dropdown-menu",behaviors:[r.P,i.a,a.V,s.x],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0},expandSizingTargetForScrollbars:{type:Boolean,value:!1}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},observers:["_selectedItemChanged(selectedItem)"],_attachDom:function(e){var t=(0,h.r)(this);return t.attachShadow({mode:"open",delegatesFocus:!0,shadyUpgradeFragment:e}),t.shadowRoot.appendChild(e),g.prototype._attachDom.call(this,e)},focus:function(){this.$.input._focusableElement.focus()},attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=(0,u.vz)(this.$.content).getDistributedNodes(),t=0,n=e.length;t<n;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){p.nJ(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},51095:function(e,t,n){n(94604);var o,r,i,a=n(78161),s=n(9672),l=n(50856);(0,s.k)({_template:(0,l.d)(o||(r=["\n    <style>\n      :host {\n        display: block;\n        padding: 8px 0;\n\n        background: var(--paper-listbox-background-color, var(--primary-background-color));\n        color: var(--paper-listbox-color, var(--primary-text-color));\n\n        @apply --paper-listbox;\n      }\n    </style>\n\n    <slot></slot>\n"],i||(i=r.slice(0)),o=Object.freeze(Object.defineProperties(r,{raw:{value:Object.freeze(i)}})))),is:"paper-listbox",behaviors:[a.i],hostAttributes:{role:"listbox"}})},21560:function(e,t,n){n.d(t,{ZH:function(){return u},MT:function(){return a},U2:function(){return l},RV:function(){return i},t8:function(){return c}});var o,r=function(){var e;return!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent)&&indexedDB.databases?new Promise((function(t){var n=function(){return indexedDB.databases().finally(t)};e=setInterval(n,100),n()})).finally((function(){return clearInterval(e)})):Promise.resolve()};function i(e){return new Promise((function(t,n){e.oncomplete=e.onsuccess=function(){return t(e.result)},e.onabort=e.onerror=function(){return n(e.error)}}))}function a(e,t){var n=r().then((function(){var n=indexedDB.open(e);return n.onupgradeneeded=function(){return n.result.createObjectStore(t)},i(n)}));return function(e,o){return n.then((function(n){return o(n.transaction(t,e).objectStore(t))}))}}function s(){return o||(o=a("keyval-store","keyval")),o}function l(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:s();return t("readonly",(function(t){return i(t.get(e))}))}function c(e,t){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:s();return n("readwrite",(function(n){return n.put(t,e),i(n.transaction)}))}function u(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:s();return e("readwrite",(function(e){return e.clear(),i(e.transaction)}))}},22142:function(e,t,n){n.d(t,{C:function(){return x}});var o=n(15304),r=n(38941),i=n(81563),a=n(19596);function s(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function l(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function c(e,t,n){return t&&l(e.prototype,t),n&&l(e,n),e}var u=function(){function e(t){s(this,e),this.U=t}return c(e,[{key:"disconnect",value:function(){this.U=void 0}},{key:"reconnect",value:function(e){this.U=e}},{key:"deref",value:function(){return this.U}}]),e}(),p=function(){function e(){s(this,e),this.Y=void 0,this.q=void 0}return c(e,[{key:"get",value:function(){return this.Y}},{key:"pause",value:function(){var e,t=this;null!==(e=this.Y)&&void 0!==e||(this.Y=new Promise((function(e){return t.q=e})))}},{key:"resume",value:function(){var e;null===(e=this.q)||void 0===e||e.call(this),this.Y=this.q=void 0}}]),e}();function d(e,t,n,o,r,i,a){try{var s=e[i](a),l=s.value}catch(c){return void n(c)}s.done?t(l):Promise.resolve(l).then(o,r)}function h(e){return h="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},h(e)}function f(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function v(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function g(e,t){return g=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},g(e,t)}function y(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,o=_(e);if(t){var r=_(this).constructor;n=Reflect.construct(o,arguments,r)}else n=o.apply(this,arguments);return b(this,n)}}function b(e,t){if(t&&("object"===h(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return m(e)}function m(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function _(e){return _=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},_(e)}var w=function(e){return!(0,i.pt)(e)&&"function"==typeof e.then},C=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&g(e,t)}(a,e);var t,n,r,i=y(a);function a(){var e;return f(this,a),(e=i.apply(this,arguments))._$Cft=1073741823,e._$Cwt=[],e._$CG=new u(m(e)),e._$CK=new p,e}return t=a,n=[{key:"render",value:function(){for(var e,t=arguments.length,n=new Array(t),r=0;r<t;r++)n[r]=arguments[r];return null!==(e=n.find((function(e){return!w(e)})))&&void 0!==e?e:o.Jb}},{key:"update",value:function(e,t){var n=this,r=this._$Cwt,i=r.length;this._$Cwt=t;var a=this._$CG,s=this._$CK;this.isConnected||this.disconnected();for(var l=function(e){var o=t[e];if(!w(o))return{v:(n._$Cft=e,o)};e<i&&o===r[e]||(n._$Cft=1073741823,i=0,Promise.resolve(o).then(function(){var e=function(e){return function(){var t=this,n=arguments;return new Promise((function(o,r){var i=e.apply(t,n);function a(e){d(i,o,r,a,s,"next",e)}function s(e){d(i,o,r,a,s,"throw",e)}a(void 0)}))}}(regeneratorRuntime.mark((function e(t){var n,r;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!s.get()){e.next=5;break}return e.next=3,s.get();case 3:e.next=0;break;case 5:void 0!==(n=a.deref())&&(r=n._$Cwt.indexOf(o))>-1&&r<n._$Cft&&(n._$Cft=r,n.setValue(t));case 7:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}()))},c=0;c<t.length&&!(c>this._$Cft);c++){var u=l(c);if("object"===h(u))return u.v}return o.Jb}},{key:"disconnected",value:function(){this._$CG.disconnect(),this._$CK.pause()}},{key:"reconnected",value:function(){this._$CG.reconnect(this),this._$CK.resume()}}],n&&v(t.prototype,n),r&&v(t,r),a}(a.s),x=(0,r.XM)(C)}}]);