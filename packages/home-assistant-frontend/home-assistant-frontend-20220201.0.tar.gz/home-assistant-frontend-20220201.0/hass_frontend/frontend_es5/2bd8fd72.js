/*! For license information please see 2bd8fd72.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[89585],{14114:function(e,t,n){n.d(t,{P:function(){return o}});var o=function(e){return function(t,n){if(t.constructor._observers){if(!t.constructor.hasOwnProperty("_observers")){var o=t.constructor._observers;t.constructor._observers=new Map,o.forEach((function(e,n){return t.constructor._observers.set(n,e)}))}}else{t.constructor._observers=new Map;var r=t.updated;t.updated=function(e){var t=this;r.call(this,e),e.forEach((function(e,n){var o=t.constructor._observers.get(n);void 0!==o&&o.call(t,t[n],e)}))}}t.constructor._observers.set(n,e)}}},67810:function(e,t,n){n.d(t,{o:function(){return l}});n(94604);var o=n(87156);function r(e){return r="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},r(e)}var l={properties:{scrollTarget:{type:HTMLElement,value:function(){return this._defaultScrollTarget}}},observers:["_scrollTargetChanged(scrollTarget, isAttached)"],_shouldHaveListener:!0,_scrollTargetChanged:function(e,t){if(this._oldScrollTarget&&(this._toggleScrollListener(!1,this._oldScrollTarget),this._oldScrollTarget=null),t)if("document"===e)this.scrollTarget=this._doc;else if("string"==typeof e){var n=this.domHost;this.scrollTarget=n&&n.$?n.$[e]:(0,o.vz)(this.ownerDocument).querySelector("#"+e)}else this._isValidScrollTarget()&&(this._oldScrollTarget=e,this._toggleScrollListener(this._shouldHaveListener,e))},_scrollHandler:function(){},get _defaultScrollTarget(){return this._doc},get _doc(){return this.ownerDocument.documentElement},get _scrollTop(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageYOffset:this.scrollTarget.scrollTop:0},get _scrollLeft(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageXOffset:this.scrollTarget.scrollLeft:0},set _scrollTop(e){this.scrollTarget===this._doc?window.scrollTo(window.pageXOffset,e):this._isValidScrollTarget()&&(this.scrollTarget.scrollTop=e)},set _scrollLeft(e){this.scrollTarget===this._doc?window.scrollTo(e,window.pageYOffset):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=e)},scroll:function(e,t){var n;"object"===r(e)?(n=e.left,t=e.top):n=e,n=n||0,t=t||0,this.scrollTarget===this._doc?window.scrollTo(n,t):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=n,this.scrollTarget.scrollTop=t)},get _scrollTargetWidth(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerWidth:this.scrollTarget.offsetWidth:0},get _scrollTargetHeight(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerHeight:this.scrollTarget.offsetHeight:0},_isValidScrollTarget:function(){return this.scrollTarget instanceof HTMLElement},_toggleScrollListener:function(e,t){var n=t===this._doc?window:t;e?this._boundScrollHandler||(this._boundScrollHandler=this._scrollHandler.bind(this),n.addEventListener("scroll",this._boundScrollHandler)):this._boundScrollHandler&&(n.removeEventListener("scroll",this._boundScrollHandler),this._boundScrollHandler=null)},toggleScrollListener:function(e){this._shouldHaveListener=e,this._toggleScrollListener(e,this.scrollTarget)}}},8878:function(e,t,n){n(94604),n(8621),n(63207),n(30879),n(78814),n(60748),n(57548),n(73962);var o,r=n(51644),l=n(26110),i=n(21006),s=n(98235),a=n(18890),c=n(9672),u=n(87156),d=n(81668),p=n(50856),f=n(62276);var h,g,v=(0,a.x)(HTMLElement);(0,c.k)({_template:(0,p.d)(o||(h=['\n    <style include="paper-dropdown-menu-shared-styles"></style>\n\n    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" dynamic-align="[[dynamicAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate allow-outside-scroll="[[allowOutsideScroll]]" restore-focus-on-close="[[restoreFocusOnClose]]" expand-sizing-target-for-scrollbars="[[expandSizingTargetForScrollbars]]">\n      \x3c!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> --\x3e\n      <div class="dropdown-trigger" slot="dropdown-trigger">\n        <paper-ripple></paper-ripple>\n        \x3c!-- paper-input has type="text" for a11y, do not remove --\x3e\n        <paper-input id="input" type="text" invalid="[[invalid]]" readonly disabled="[[disabled]]" value="[[value]]" placeholder="[[placeholder]]" error-message="[[errorMessage]]" always-float-label="[[alwaysFloatLabel]]" no-label-float="[[noLabelFloat]]" label="[[label]]" input-role="button" input-aria-haspopup="listbox" autocomplete="off">\n          \x3c!-- support hybrid mode: user might be using paper-input 1.x which distributes via <content> --\x3e\n          <iron-icon icon="paper-dropdown-menu:arrow-drop-down" suffix slot="suffix"></iron-icon>\n        </paper-input>\n      </div>\n      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>\n    </paper-menu-button>\n'],g||(g=h.slice(0)),o=Object.freeze(Object.defineProperties(h,{raw:{value:Object.freeze(g)}})))),is:"paper-dropdown-menu",behaviors:[r.P,l.a,i.V,s.x],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0},expandSizingTargetForScrollbars:{type:Boolean,value:!1}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},observers:["_selectedItemChanged(selectedItem)"],_attachDom:function(e){var t=(0,f.r)(this);return t.attachShadow({mode:"open",delegatesFocus:!0,shadyUpgradeFragment:e}),t.shadowRoot.appendChild(e),v.prototype._attachDom.call(this,e)},focus:function(){this.$.input._focusableElement.focus()},attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=(0,u.vz)(this.$.content).getDistributedNodes(),t=0,n=e.length;t<n;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){d.nJ(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},25782:function(e,t,n){n(94604),n(65660),n(70019),n(97968);var o,r,l,i=n(9672),s=n(50856),a=n(33760);(0,i.k)({_template:(0,s.d)(o||(r=['\n    <style include="paper-item-shared-styles"></style>\n    <style>\n      :host {\n        @apply --layout-horizontal;\n        @apply --layout-center;\n        @apply --paper-font-subhead;\n\n        @apply --paper-item;\n        @apply --paper-icon-item;\n      }\n\n      .content-icon {\n        @apply --layout-horizontal;\n        @apply --layout-center;\n\n        width: var(--paper-item-icon-width, 56px);\n        @apply --paper-item-icon;\n      }\n    </style>\n\n    <div id="contentIcon" class="content-icon">\n      <slot name="item-icon"></slot>\n    </div>\n    <slot></slot>\n'],l||(l=r.slice(0)),o=Object.freeze(Object.defineProperties(r,{raw:{value:Object.freeze(l)}})))),is:"paper-icon-item",behaviors:[a.U]})},89194:function(e,t,n){n(94604),n(65660),n(70019);var o,r,l,i=n(9672),s=n(50856);(0,i.k)({_template:(0,s.d)(o||(r=["\n    <style>\n      :host {\n        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */\n        @apply --layout-vertical;\n        @apply --layout-center-justified;\n        @apply --layout-flex;\n      }\n\n      :host([two-line]) {\n        min-height: var(--paper-item-body-two-line-min-height, 72px);\n      }\n\n      :host([three-line]) {\n        min-height: var(--paper-item-body-three-line-min-height, 88px);\n      }\n\n      :host > ::slotted(*) {\n        overflow: hidden;\n        text-overflow: ellipsis;\n        white-space: nowrap;\n      }\n\n      :host > ::slotted([secondary]) {\n        @apply --paper-font-body1;\n\n        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));\n\n        @apply --paper-item-body-secondary;\n      }\n    </style>\n\n    <slot></slot>\n"],l||(l=r.slice(0)),o=Object.freeze(Object.defineProperties(r,{raw:{value:Object.freeze(l)}})))),is:"paper-item-body"})},21560:function(e,t,n){n.d(t,{ZH:function(){return u},MT:function(){return i},U2:function(){return a},RV:function(){return l},t8:function(){return c}});var o,r=function(){var e;return!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent)&&indexedDB.databases?new Promise((function(t){var n=function(){return indexedDB.databases().finally(t)};e=setInterval(n,100),n()})).finally((function(){return clearInterval(e)})):Promise.resolve()};function l(e){return new Promise((function(t,n){e.oncomplete=e.onsuccess=function(){return t(e.result)},e.onabort=e.onerror=function(){return n(e.error)}}))}function i(e,t){var n=r().then((function(){var n=indexedDB.open(e);return n.onupgradeneeded=function(){return n.result.createObjectStore(t)},l(n)}));return function(e,o){return n.then((function(n){return o(n.transaction(t,e).objectStore(t))}))}}function s(){return o||(o=i("keyval-store","keyval")),o}function a(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:s();return t("readonly",(function(t){return l(t.get(e))}))}function c(e,t){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:s();return n("readwrite",(function(n){return n.put(t,e),l(n.transaction)}))}function u(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:s();return e("readwrite",(function(e){return e.clear(),l(e.transaction)}))}},81563:function(e,t,n){function o(e){return o="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},o(e)}n.d(t,{E_:function(){return g},i9:function(){return f},_Y:function(){return c},pt:function(){return l},OR:function(){return s},hN:function(){return i},ws:function(){return h},fk:function(){return u},hl:function(){return p}});var r=n(15304).Al.H,l=function(e){return null===e||"object"!=o(e)&&"function"!=typeof e},i=function(e,t){var n,o;return void 0===t?void 0!==(null===(n=e)||void 0===n?void 0:n._$litType$):(null===(o=e)||void 0===o?void 0:o._$litType$)===t},s=function(e){return void 0===e.strings},a=function(){return document.createComment("")},c=function(e,t,n){var o,l=e._$AA.parentNode,i=void 0===t?e._$AB:t._$AA;if(void 0===n){var s=l.insertBefore(a(),i),c=l.insertBefore(a(),i);n=new r(s,c,e,e.options)}else{var u,d=n._$AB.nextSibling,p=n._$AM,f=p!==e;if(f)null===(o=n._$AQ)||void 0===o||o.call(n,e),n._$AM=e,void 0!==n._$AP&&(u=e._$AU)!==p._$AU&&n._$AP(u);if(d!==i||f)for(var h=n._$AA;h!==d;){var g=h.nextSibling;l.insertBefore(h,i),h=g}}return n},u=function(e,t){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:e;return e._$AI(t,n),e},d={},p=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:d;return e._$AH=t},f=function(e){return e._$AH},h=function(e){var t;null===(t=e._$AP)||void 0===t||t.call(e,!1,!0);for(var n=e._$AA,o=e._$AB.nextSibling;n!==o;){var r=n.nextSibling;n.remove(),n=r}},g=function(e){e._$AR()}},57835:function(e,t,n){n.d(t,{Xe:function(){return o.Xe},pX:function(){return o.pX},XM:function(){return o.XM}});var o=n(38941)}}]);