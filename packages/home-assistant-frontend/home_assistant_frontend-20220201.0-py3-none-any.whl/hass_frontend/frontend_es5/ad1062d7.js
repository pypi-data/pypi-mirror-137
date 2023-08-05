/*! For license information please see ad1062d7.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[44360,66261,82176],{14166:function(t,n,e){e.d(n,{W:function(){return r}});var o=function(){return o=Object.assign||function(t){for(var n,e=1,o=arguments.length;e<o;e++)for(var r in n=arguments[e])Object.prototype.hasOwnProperty.call(n,r)&&(t[r]=n[r]);return t},o.apply(this,arguments)};function r(t,n,e){void 0===n&&(n=Date.now()),void 0===e&&(e={});var r=o(o({},i),e||{}),a=(+t-+n)/1e3;if(Math.abs(a)<r.second)return{value:Math.round(a),unit:"second"};var l=a/60;if(Math.abs(l)<r.minute)return{value:Math.round(l),unit:"minute"};var u=a/3600;if(Math.abs(u)<r.hour)return{value:Math.round(u),unit:"hour"};var s=a/86400;if(Math.abs(s)<r.day)return{value:Math.round(s),unit:"day"};var c=new Date(t),f=new Date(n),p=c.getFullYear()-f.getFullYear();if(Math.round(Math.abs(p))>0)return{value:Math.round(p),unit:"year"};var h=12*p+c.getMonth()-f.getMonth();if(Math.round(Math.abs(h))>0)return{value:Math.round(h),unit:"month"};var d=a/604800;return{value:Math.round(d),unit:"week"}}var i={second:45,minute:45,hour:22,day:5}},18601:function(t,n,e){e.d(n,{qN:function(){return l.q},Wg:function(){return b}});var o,r,i=e(87480),a=e(72367),l=e(78220);function u(t){return u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},u(t)}function s(t,n){if(!(t instanceof n))throw new TypeError("Cannot call a class as a function")}function c(t,n){for(var e=0;e<n.length;e++){var o=n[e];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(t,o.key,o)}}function f(t,n,e){return f="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(t,n,e){var o=function(t,n){for(;!Object.prototype.hasOwnProperty.call(t,n)&&null!==(t=v(t)););return t}(t,n);if(o){var r=Object.getOwnPropertyDescriptor(o,n);return r.get?r.get.call(e):r.value}},f(t,n,e||t)}function p(t,n){return p=Object.setPrototypeOf||function(t,n){return t.__proto__=n,t},p(t,n)}function h(t){var n=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}();return function(){var e,o=v(t);if(n){var r=v(this).constructor;e=Reflect.construct(o,arguments,r)}else e=o.apply(this,arguments);return d(this,e)}}function d(t,n){if(n&&("object"===u(n)||"function"==typeof n))return n;if(void 0!==n)throw new TypeError("Derived constructors may only return object or undefined");return function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t)}function v(t){return v=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)},v(t)}var y=null!==(r=null===(o=window.ShadyDOM)||void 0===o?void 0:o.inUse)&&void 0!==r&&r,b=function(t){!function(t,n){if("function"!=typeof n&&null!==n)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(n&&n.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),n&&p(t,n)}(i,t);var n,e,o,r=h(i);function i(){var t;return s(this,i),(t=r.apply(this,arguments)).disabled=!1,t.containingForm=null,t.formDataListener=function(n){t.disabled||t.setFormData(n.formData)},t}return n=i,e=[{key:"findFormElement",value:function(){if(!this.shadowRoot||y)return null;for(var t=this.getRootNode().querySelectorAll("form"),n=0,e=Array.from(t);n<e.length;n++){var o=e[n];if(o.contains(this))return o}return null}},{key:"connectedCallback",value:function(){var t;f(v(i.prototype),"connectedCallback",this).call(this),this.containingForm=this.findFormElement(),null===(t=this.containingForm)||void 0===t||t.addEventListener("formdata",this.formDataListener)}},{key:"disconnectedCallback",value:function(){var t;f(v(i.prototype),"disconnectedCallback",this).call(this),null===(t=this.containingForm)||void 0===t||t.removeEventListener("formdata",this.formDataListener),this.containingForm=null}},{key:"click",value:function(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}},{key:"firstUpdated",value:function(){var t=this;f(v(i.prototype),"firstUpdated",this).call(this),this.shadowRoot&&this.mdcRoot.addEventListener("change",(function(n){t.dispatchEvent(new Event("change",n))}))}}],e&&c(n.prototype,e),o&&c(n,o),i}(l.H);b.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,i.__decorate)([(0,a.Cb)({type:Boolean})],b.prototype,"disabled",void 0)},39841:function(t,n,e){e(94604),e(65660);var o,r,i,a=e(9672),l=e(87156),u=e(50856),s=e(44181);(0,a.k)({_template:(0,u.d)(o||(r=['\n    <style>\n      :host {\n        display: block;\n        /**\n         * Force app-header-layout to have its own stacking context so that its parent can\n         * control the stacking of it relative to other elements (e.g. app-drawer-layout).\n         * This could be done using `isolation: isolate`, but that\'s not well supported\n         * across browsers.\n         */\n        position: relative;\n        z-index: 0;\n      }\n\n      #wrapper ::slotted([slot=header]) {\n        @apply --layout-fixed-top;\n        z-index: 1;\n      }\n\n      #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) {\n        height: 100%;\n      }\n\n      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {\n        position: absolute;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) #wrapper #contentContainer {\n        @apply --layout-fit;\n        overflow-y: auto;\n        -webkit-overflow-scrolling: touch;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {\n        position: relative;\n      }\n\n      :host([fullbleed]) {\n        @apply --layout-vertical;\n        @apply --layout-fit;\n      }\n\n      :host([fullbleed]) #wrapper,\n      :host([fullbleed]) #wrapper #contentContainer {\n        @apply --layout-vertical;\n        @apply --layout-flex;\n      }\n\n      #contentContainer {\n        /* Create a stacking context here so that all children appear below the header. */\n        position: relative;\n        z-index: 0;\n      }\n\n      @media print {\n        :host([has-scrolling-region]) #wrapper #contentContainer {\n          overflow-y: visible;\n        }\n      }\n\n    </style>\n\n    <div id="wrapper" class="initializing">\n      <slot id="headerSlot" name="header"></slot>\n\n      <div id="contentContainer">\n        <slot></slot>\n      </div>\n    </div>\n'],i=['\n    <style>\n      :host {\n        display: block;\n        /**\n         * Force app-header-layout to have its own stacking context so that its parent can\n         * control the stacking of it relative to other elements (e.g. app-drawer-layout).\n         * This could be done using \\`isolation: isolate\\`, but that\'s not well supported\n         * across browsers.\n         */\n        position: relative;\n        z-index: 0;\n      }\n\n      #wrapper ::slotted([slot=header]) {\n        @apply --layout-fixed-top;\n        z-index: 1;\n      }\n\n      #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) {\n        height: 100%;\n      }\n\n      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {\n        position: absolute;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {\n        position: relative;\n      }\n\n      :host([has-scrolling-region]) #wrapper #contentContainer {\n        @apply --layout-fit;\n        overflow-y: auto;\n        -webkit-overflow-scrolling: touch;\n      }\n\n      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {\n        position: relative;\n      }\n\n      :host([fullbleed]) {\n        @apply --layout-vertical;\n        @apply --layout-fit;\n      }\n\n      :host([fullbleed]) #wrapper,\n      :host([fullbleed]) #wrapper #contentContainer {\n        @apply --layout-vertical;\n        @apply --layout-flex;\n      }\n\n      #contentContainer {\n        /* Create a stacking context here so that all children appear below the header. */\n        position: relative;\n        z-index: 0;\n      }\n\n      @media print {\n        :host([has-scrolling-region]) #wrapper #contentContainer {\n          overflow-y: visible;\n        }\n      }\n\n    </style>\n\n    <div id="wrapper" class="initializing">\n      <slot id="headerSlot" name="header"></slot>\n\n      <div id="contentContainer">\n        <slot></slot>\n      </div>\n    </div>\n'],i||(i=r.slice(0)),o=Object.freeze(Object.defineProperties(r,{raw:{value:Object.freeze(i)}})))),is:"app-header-layout",behaviors:[s.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,l.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var t=this.header;if(this.isAttached&&t){this.$.wrapper.classList.remove("initializing"),t.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var n=t.offsetHeight;this.hasScrollingRegion?(t.style.left="",t.style.right=""):requestAnimationFrame(function(){var n=this.getBoundingClientRect(),e=document.documentElement.clientWidth-n.right;t.style.left=n.left+"px",t.style.right=e+"px"}.bind(this));var e=this.$.contentContainer.style;t.fixed&&!t.condenses&&this.hasScrollingRegion?(e.marginTop=n+"px",e.paddingTop=""):(e.paddingTop=n+"px",e.marginTop="")}}})},49075:function(t,n,e){e.d(n,{S:function(){return a},B:function(){return l}});e(94604);var o=e(51644),r=e(26110),i=e(84938),a={observers:["_focusedChanged(receivedFocusFromKeyboard)"],_focusedChanged:function(t){t&&this.ensureRipple(),this.hasRipple()&&(this._ripple.holdDown=t)},_createRipple:function(){var t=i.o._createRipple();return t.id="ink",t.setAttribute("center",""),t.classList.add("circle"),t}},l=[o.P,r.a,i.o,a]},84938:function(t,n,e){e.d(n,{o:function(){return i}});e(94604),e(60748);var o=e(51644),r=e(87156),i={properties:{noink:{type:Boolean,observer:"_noinkChanged"},_rippleContainer:{type:Object}},_buttonStateChanged:function(){this.focused&&this.ensureRipple()},_downHandler:function(t){o.$._downHandler.call(this,t),this.pressed&&this.ensureRipple(t)},ensureRipple:function(t){if(!this.hasRipple()){this._ripple=this._createRipple(),this._ripple.noink=this.noink;var n=this._rippleContainer||this.root;if(n&&(0,r.vz)(n).appendChild(this._ripple),t){var e=(0,r.vz)(this._rippleContainer||this),o=(0,r.vz)(t).rootTarget;e.deepContains(o)&&this._ripple.uiDownAction(t)}}},getRipple:function(){return this.ensureRipple(),this._ripple},hasRipple:function(){return Boolean(this._ripple)},_createRipple:function(){return document.createElement("paper-ripple")},_noinkChanged:function(t){this.hasRipple()&&(this._ripple.noink=t)}}},19596:function(t,n,e){e.d(n,{s:function(){return A}});var o=e(81563),r=e(38941);function i(t){return i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},i(t)}function a(t){return function(t){if(Array.isArray(t))return v(t)}(t)||function(t){if("undefined"!=typeof Symbol&&null!=t[Symbol.iterator]||null!=t["@@iterator"])return Array.from(t)}(t)||d(t)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function l(t,n){if(!(t instanceof n))throw new TypeError("Cannot call a class as a function")}function u(t,n){for(var e=0;e<n.length;e++){var o=n[e];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(t,o.key,o)}}function s(t,n,e){return s="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(t,n,e){var o=function(t,n){for(;!Object.prototype.hasOwnProperty.call(t,n)&&null!==(t=h(t)););return t}(t,n);if(o){var r=Object.getOwnPropertyDescriptor(o,n);return r.get?r.get.call(e):r.value}},s(t,n,e||t)}function c(t,n){return c=Object.setPrototypeOf||function(t,n){return t.__proto__=n,t},c(t,n)}function f(t){var n=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(y){return!1}}();return function(){var e,o=h(t);if(n){var r=h(this).constructor;e=Reflect.construct(o,arguments,r)}else e=o.apply(this,arguments);return p(this,e)}}function p(t,n){if(n&&("object"===i(n)||"function"==typeof n))return n;if(void 0!==n)throw new TypeError("Derived constructors may only return object or undefined");return function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t)}function h(t){return h=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)},h(t)}function d(t,n){if(t){if("string"==typeof t)return v(t,n);var e=Object.prototype.toString.call(t).slice(8,-1);return"Object"===e&&t.constructor&&(e=t.constructor.name),"Map"===e||"Set"===e?Array.from(t):"Arguments"===e||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(e)?v(t,n):void 0}}function v(t,n){(null==n||n>t.length)&&(n=t.length);for(var e=0,o=new Array(n);e<n;e++)o[e]=t[e];return o}var y=function t(n,e){var o,r,i=n._$AN;if(void 0===i)return!1;var a,l=function(t,n){var e="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(!e){if(Array.isArray(t)||(e=d(t))||n&&t&&"number"==typeof t.length){e&&(t=e);var o=0,r=function(){};return{s:r,n:function(){return o>=t.length?{done:!0}:{done:!1,value:t[o++]}},e:function(t){throw t},f:r}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var i,a=!0,l=!1;return{s:function(){e=e.call(t)},n:function(){var t=e.next();return a=t.done,t},e:function(t){l=!0,i=t},f:function(){try{a||null==e.return||e.return()}finally{if(l)throw i}}}}(i);try{for(l.s();!(a=l.n()).done;){var u=a.value;null===(r=(o=u)._$AO)||void 0===r||r.call(o,e,!1),t(u,e)}}catch(s){l.e(s)}finally{l.f()}return!0},b=function(t){var n,e;do{if(void 0===(n=t._$AM))break;(e=n._$AN).delete(t),t=n}while(0===(null==e?void 0:e.size))},g=function(t){for(var n;n=t._$AM;t=n){var e=n._$AN;if(void 0===e)n._$AN=e=new Set;else if(e.has(t))break;e.add(t),w(n)}};function m(t){void 0!==this._$AN?(b(this),this._$AM=t,g(this)):this._$AM=t}function _(t){var n=arguments.length>1&&void 0!==arguments[1]&&arguments[1],e=arguments.length>2&&void 0!==arguments[2]?arguments[2]:0,o=this._$AH,r=this._$AN;if(void 0!==r&&0!==r.size)if(n)if(Array.isArray(o))for(var i=e;i<o.length;i++)y(o[i],!1),b(o[i]);else null!=o&&(y(o,!1),b(o));else y(this,t)}var w=function(t){var n,e,o,i;t.type==r.pX.CHILD&&(null!==(n=(o=t)._$AP)&&void 0!==n||(o._$AP=_),null!==(e=(i=t)._$AQ)&&void 0!==e||(i._$AQ=m))},A=function(t){!function(t,n){if("function"!=typeof n&&null!==n)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(n&&n.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),n&&c(t,n)}(p,t);var n,e,r,i=f(p);function p(){var t;return l(this,p),(t=i.apply(this,arguments))._$AN=void 0,t}return n=p,e=[{key:"_$AT",value:function(t,n,e){s(h(p.prototype),"_$AT",this).call(this,t,n,e),g(this),this.isConnected=t._$AU}},{key:"_$AO",value:function(t){var n,e,o=!(arguments.length>1&&void 0!==arguments[1])||arguments[1];t!==this.isConnected&&(this.isConnected=t,t?null===(n=this.reconnected)||void 0===n||n.call(this):null===(e=this.disconnected)||void 0===e||e.call(this)),o&&(y(this,t),b(this))}},{key:"setValue",value:function(t){if((0,o.OR)(this._$Ct))this._$Ct._$AI(t,this);else{var n=a(this._$Ct._$AH);n[this._$Ci]=t,this._$Ct._$AI(n,this,0)}}},{key:"disconnected",value:function(){}},{key:"reconnected",value:function(){}}],e&&u(n.prototype,e),r&&u(n,r),p}(r.Xe)},81563:function(t,n,e){function o(t){return o="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},o(t)}e.d(n,{E_:function(){return v},i9:function(){return h},_Y:function(){return s},pt:function(){return i},OR:function(){return l},hN:function(){return a},ws:function(){return d},fk:function(){return c},hl:function(){return p}});var r=e(15304).Al.H,i=function(t){return null===t||"object"!=o(t)&&"function"!=typeof t},a=function(t,n){var e,o;return void 0===n?void 0!==(null===(e=t)||void 0===e?void 0:e._$litType$):(null===(o=t)||void 0===o?void 0:o._$litType$)===n},l=function(t){return void 0===t.strings},u=function(){return document.createComment("")},s=function(t,n,e){var o,i=t._$AA.parentNode,a=void 0===n?t._$AB:n._$AA;if(void 0===e){var l=i.insertBefore(u(),a),s=i.insertBefore(u(),a);e=new r(l,s,t,t.options)}else{var c,f=e._$AB.nextSibling,p=e._$AM,h=p!==t;if(h)null===(o=e._$AQ)||void 0===o||o.call(e,t),e._$AM=t,void 0!==e._$AP&&(c=t._$AU)!==p._$AU&&e._$AP(c);if(f!==a||h)for(var d=e._$AA;d!==f;){var v=d.nextSibling;i.insertBefore(d,a),d=v}}return e},c=function(t,n){var e=arguments.length>2&&void 0!==arguments[2]?arguments[2]:t;return t._$AI(n,e),t},f={},p=function(t){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:f;return t._$AH=n},h=function(t){return t._$AH},d=function(t){var n;null===(n=t._$AP)||void 0===n||n.call(t,!1,!0);for(var e=t._$AA,o=t._$AB.nextSibling;e!==o;){var r=e.nextSibling;e.remove(),e=r}},v=function(t){t._$AR()}}}]);