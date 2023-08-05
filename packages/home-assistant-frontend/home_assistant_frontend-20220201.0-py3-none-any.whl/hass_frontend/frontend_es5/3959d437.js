/*! For license information please see 3959d437.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[43949,49995,66261,93098,11139,5713,22946,92887],{18601:function(e,t,n){n.d(t,{qN:function(){return l.q},Wg:function(){return b}});var o,r,i=n(87480),a=n(72367),l=n(78220);function c(e){return c="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},c(e)}function u(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function s(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function p(e,t,n){return p="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var o=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=h(e)););return e}(e,t);if(o){var r=Object.getOwnPropertyDescriptor(o,t);return r.get?r.get.call(n):r.value}},p(e,t,n||e)}function f(e,t){return f=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},f(e,t)}function d(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,o=h(e);if(t){var r=h(this).constructor;n=Reflect.construct(o,arguments,r)}else n=o.apply(this,arguments);return y(this,n)}}function y(e,t){if(t&&("object"===c(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function h(e){return h=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},h(e)}var v=null!==(r=null===(o=window.ShadyDOM)||void 0===o?void 0:o.inUse)&&void 0!==r&&r,b=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&f(e,t)}(i,e);var t,n,o,r=d(i);function i(){var e;return u(this,i),(e=r.apply(this,arguments)).disabled=!1,e.containingForm=null,e.formDataListener=function(t){e.disabled||e.setFormData(t.formData)},e}return t=i,n=[{key:"findFormElement",value:function(){if(!this.shadowRoot||v)return null;for(var e=this.getRootNode().querySelectorAll("form"),t=0,n=Array.from(e);t<n.length;t++){var o=n[t];if(o.contains(this))return o}return null}},{key:"connectedCallback",value:function(){var e;p(h(i.prototype),"connectedCallback",this).call(this),this.containingForm=this.findFormElement(),null===(e=this.containingForm)||void 0===e||e.addEventListener("formdata",this.formDataListener)}},{key:"disconnectedCallback",value:function(){var e;p(h(i.prototype),"disconnectedCallback",this).call(this),null===(e=this.containingForm)||void 0===e||e.removeEventListener("formdata",this.formDataListener),this.containingForm=null}},{key:"click",value:function(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}},{key:"firstUpdated",value:function(){var e=this;p(h(i.prototype),"firstUpdated",this).call(this),this.shadowRoot&&this.mdcRoot.addEventListener("change",(function(t){e.dispatchEvent(new Event("change",t))}))}}],n&&s(t.prototype,n),o&&s(t,o),i}(l.H);b.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,i.__decorate)([(0,a.Cb)({type:Boolean})],b.prototype,"disabled",void 0)},8878:function(e,t,n){n(94604),n(8621),n(63207),n(30879),n(78814),n(60748),n(57548),n(73962);var o,r=n(51644),i=n(26110),a=n(21006),l=n(98235),c=n(18890),u=n(9672),s=n(87156),p=n(81668),f=n(50856),d=n(62276);var y,h,v=(0,c.x)(HTMLElement);(0,u.k)({_template:(0,f.d)(o||(y=['\n    <style include="paper-dropdown-menu-shared-styles"></style>\n\n    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" dynamic-align="[[dynamicAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate allow-outside-scroll="[[allowOutsideScroll]]" restore-focus-on-close="[[restoreFocusOnClose]]" expand-sizing-target-for-scrollbars="[[expandSizingTargetForScrollbars]]">\n      \x3c!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> --\x3e\n      <div class="dropdown-trigger" slot="dropdown-trigger">\n        <paper-ripple></paper-ripple>\n        \x3c!-- paper-input has type="text" for a11y, do not remove --\x3e\n        <paper-input id="input" type="text" invalid="[[invalid]]" readonly disabled="[[disabled]]" value="[[value]]" placeholder="[[placeholder]]" error-message="[[errorMessage]]" always-float-label="[[alwaysFloatLabel]]" no-label-float="[[noLabelFloat]]" label="[[label]]" input-role="button" input-aria-haspopup="listbox" autocomplete="off">\n          \x3c!-- support hybrid mode: user might be using paper-input 1.x which distributes via <content> --\x3e\n          <iron-icon icon="paper-dropdown-menu:arrow-drop-down" suffix slot="suffix"></iron-icon>\n        </paper-input>\n      </div>\n      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>\n    </paper-menu-button>\n'],h||(h=y.slice(0)),o=Object.freeze(Object.defineProperties(y,{raw:{value:Object.freeze(h)}})))),is:"paper-dropdown-menu",behaviors:[r.P,i.a,a.V,l.x],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0},expandSizingTargetForScrollbars:{type:Boolean,value:!1}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},observers:["_selectedItemChanged(selectedItem)"],_attachDom:function(e){var t=(0,d.r)(this);return t.attachShadow({mode:"open",delegatesFocus:!0,shadyUpgradeFragment:e}),t.shadowRoot.appendChild(e),v.prototype._attachDom.call(this,e)},focus:function(){this.$.input._focusableElement.focus()},attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=(0,s.vz)(this.$.content).getDistributedNodes(),t=0,n=e.length;t<n;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){p.nJ(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},33760:function(e,t,n){n.d(t,{U:function(){return i}});n(94604);var o=n(51644),r=n(26110),i=[o.P,r.a,{hostAttributes:{role:"option",tabindex:"0"}}]},89194:function(e,t,n){n(94604),n(65660),n(70019);var o,r,i,a=n(9672),l=n(50856);(0,a.k)({_template:(0,l.d)(o||(r=["\n    <style>\n      :host {\n        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */\n        @apply --layout-vertical;\n        @apply --layout-center-justified;\n        @apply --layout-flex;\n      }\n\n      :host([two-line]) {\n        min-height: var(--paper-item-body-two-line-min-height, 72px);\n      }\n\n      :host([three-line]) {\n        min-height: var(--paper-item-body-three-line-min-height, 88px);\n      }\n\n      :host > ::slotted(*) {\n        overflow: hidden;\n        text-overflow: ellipsis;\n        white-space: nowrap;\n      }\n\n      :host > ::slotted([secondary]) {\n        @apply --paper-font-body1;\n\n        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));\n\n        @apply --paper-item-body-secondary;\n      }\n    </style>\n\n    <slot></slot>\n"],i||(i=r.slice(0)),o=Object.freeze(Object.defineProperties(r,{raw:{value:Object.freeze(i)}})))),is:"paper-item-body"})},97968:function(e,t,n){n(65660),n(70019);var o=document.createElement("template");o.setAttribute("style","display: none;"),o.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(o.content)},53973:function(e,t,n){n(94604),n(65660),n(97968);var o,r,i,a=n(9672),l=n(50856),c=n(33760);(0,a.k)({_template:(0,l.d)(o||(r=['\n    <style include="paper-item-shared-styles">\n      :host {\n        @apply --layout-horizontal;\n        @apply --layout-center;\n        @apply --paper-font-subhead;\n\n        @apply --paper-item;\n      }\n    </style>\n    <slot></slot>\n'],i||(i=r.slice(0)),o=Object.freeze(Object.defineProperties(r,{raw:{value:Object.freeze(i)}})))),is:"paper-item",behaviors:[c.U]})},51095:function(e,t,n){n(94604);var o,r,i,a=n(78161),l=n(9672),c=n(50856);(0,l.k)({_template:(0,c.d)(o||(r=["\n    <style>\n      :host {\n        display: block;\n        padding: 8px 0;\n\n        background: var(--paper-listbox-background-color, var(--primary-background-color));\n        color: var(--paper-listbox-color, var(--primary-text-color));\n\n        @apply --paper-listbox;\n      }\n    </style>\n\n    <slot></slot>\n"],i||(i=r.slice(0)),o=Object.freeze(Object.defineProperties(r,{raw:{value:Object.freeze(i)}})))),is:"paper-listbox",behaviors:[a.i],hostAttributes:{role:"listbox"}})},19596:function(e,t,n){n.d(t,{s:function(){return A}});var o=n(81563),r=n(38941);function i(e){return i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},i(e)}function a(e){return function(e){if(Array.isArray(e))return h(e)}(e)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||y(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function l(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function c(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function u(e,t,n){return u="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var o=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=d(e)););return e}(e,t);if(o){var r=Object.getOwnPropertyDescriptor(o,t);return r.get?r.get.call(n):r.value}},u(e,t,n||e)}function s(e,t){return s=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},s(e,t)}function p(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(v){return!1}}();return function(){var n,o=d(e);if(t){var r=d(this).constructor;n=Reflect.construct(o,arguments,r)}else n=o.apply(this,arguments);return f(this,n)}}function f(e,t){if(t&&("object"===i(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function d(e){return d=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},d(e)}function y(e,t){if(e){if("string"==typeof e)return h(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?h(e,t):void 0}}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,o=new Array(t);n<t;n++)o[n]=e[n];return o}var v=function e(t,n){var o,r,i=t._$AN;if(void 0===i)return!1;var a,l=function(e,t){var n="undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(!n){if(Array.isArray(e)||(n=y(e))||t&&e&&"number"==typeof e.length){n&&(e=n);var o=0,r=function(){};return{s:r,n:function(){return o>=e.length?{done:!0}:{done:!1,value:e[o++]}},e:function(e){throw e},f:r}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var i,a=!0,l=!1;return{s:function(){n=n.call(e)},n:function(){var e=n.next();return a=e.done,e},e:function(e){l=!0,i=e},f:function(){try{a||null==n.return||n.return()}finally{if(l)throw i}}}}(i);try{for(l.s();!(a=l.n()).done;){var c=a.value;null===(r=(o=c)._$AO)||void 0===r||r.call(o,n,!1),e(c,n)}}catch(u){l.e(u)}finally{l.f()}return!0},b=function(e){var t,n;do{if(void 0===(t=e._$AM))break;(n=t._$AN).delete(e),e=t}while(0===(null==n?void 0:n.size))},m=function(e){for(var t;t=e._$AM;e=t){var n=t._$AN;if(void 0===n)t._$AN=n=new Set;else if(n.has(e))break;n.add(e),w(t)}};function g(e){void 0!==this._$AN?(b(this),this._$AM=e,m(this)):this._$AM=e}function _(e){var t=arguments.length>1&&void 0!==arguments[1]&&arguments[1],n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:0,o=this._$AH,r=this._$AN;if(void 0!==r&&0!==r.size)if(t)if(Array.isArray(o))for(var i=n;i<o.length;i++)v(o[i],!1),b(o[i]);else null!=o&&(v(o,!1),b(o));else v(this,e)}var w=function(e){var t,n,o,i;e.type==r.pX.CHILD&&(null!==(t=(o=e)._$AP)&&void 0!==t||(o._$AP=_),null!==(n=(i=e)._$AQ)&&void 0!==n||(i._$AQ=g))},A=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&s(e,t)}(f,e);var t,n,r,i=p(f);function f(){var e;return l(this,f),(e=i.apply(this,arguments))._$AN=void 0,e}return t=f,n=[{key:"_$AT",value:function(e,t,n){u(d(f.prototype),"_$AT",this).call(this,e,t,n),m(this),this.isConnected=e._$AU}},{key:"_$AO",value:function(e){var t,n,o=!(arguments.length>1&&void 0!==arguments[1])||arguments[1];e!==this.isConnected&&(this.isConnected=e,e?null===(t=this.reconnected)||void 0===t||t.call(this):null===(n=this.disconnected)||void 0===n||n.call(this)),o&&(v(this,e),b(this))}},{key:"setValue",value:function(e){if((0,o.OR)(this._$Ct))this._$Ct._$AI(e,this);else{var t=a(this._$Ct._$AH);t[this._$Ci]=e,this._$Ct._$AI(t,this,0)}}},{key:"disconnected",value:function(){}},{key:"reconnected",value:function(){}}],n&&c(t.prototype,n),r&&c(t,r),f}(r.Xe)},81563:function(e,t,n){function o(e){return o="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},o(e)}n.d(t,{E_:function(){return h},i9:function(){return d},_Y:function(){return u},pt:function(){return i},OR:function(){return l},hN:function(){return a},ws:function(){return y},fk:function(){return s},hl:function(){return f}});var r=n(15304).Al.H,i=function(e){return null===e||"object"!=o(e)&&"function"!=typeof e},a=function(e,t){var n,o;return void 0===t?void 0!==(null===(n=e)||void 0===n?void 0:n._$litType$):(null===(o=e)||void 0===o?void 0:o._$litType$)===t},l=function(e){return void 0===e.strings},c=function(){return document.createComment("")},u=function(e,t,n){var o,i=e._$AA.parentNode,a=void 0===t?e._$AB:t._$AA;if(void 0===n){var l=i.insertBefore(c(),a),u=i.insertBefore(c(),a);n=new r(l,u,e,e.options)}else{var s,p=n._$AB.nextSibling,f=n._$AM,d=f!==e;if(d)null===(o=n._$AQ)||void 0===o||o.call(n,e),n._$AM=e,void 0!==n._$AP&&(s=e._$AU)!==f._$AU&&n._$AP(s);if(p!==a||d)for(var y=n._$AA;y!==p;){var h=y.nextSibling;i.insertBefore(y,a),y=h}}return n},s=function(e,t){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:e;return e._$AI(t,n),e},p={},f=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:p;return e._$AH=t},d=function(e){return e._$AH},y=function(e){var t;null===(t=e._$AP)||void 0===t||t.call(e,!1,!0);for(var n=e._$AA,o=e._$AB.nextSibling;n!==o;){var r=n.nextSibling;n.remove(),n=r}},h=function(e){e._$AR()}}}]);