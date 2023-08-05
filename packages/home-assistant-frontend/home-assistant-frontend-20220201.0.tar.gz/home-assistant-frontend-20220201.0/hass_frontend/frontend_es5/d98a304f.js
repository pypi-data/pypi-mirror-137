"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[35987],{44583:function(e,t,n){n.d(t,{o0:function(){return i},E8:function(){return c}});var r=n(14516),o=n(65810);n(29607);var i=function(e,t){return a(t).format(e)},a=(0,r.Z)((function(e){return new Intl.DateTimeFormat("en"!==e.language||(0,o.y)(e)?e.language:"en-u-hc-h23",{year:"numeric",month:"long",day:"numeric",hour:(0,o.y)(e)?"numeric":"2-digit",minute:"2-digit",hour12:(0,o.y)(e)})})),c=function(e,t){return s(t).format(e)},s=(0,r.Z)((function(e){return new Intl.DateTimeFormat("en"!==e.language||(0,o.y)(e)?e.language:"en-u-hc-h23",{year:"numeric",month:"long",day:"numeric",hour:(0,o.y)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hour12:(0,o.y)(e)})}));(0,r.Z)((function(e){return new Intl.DateTimeFormat("en"!==e.language||(0,o.y)(e)?e.language:"en-u-hc-h23",{year:"numeric",month:"numeric",day:"numeric",hour:"numeric",minute:"2-digit",hour12:(0,o.y)(e)})}))},65810:function(e,t,n){n.d(t,{y:function(){return i}});var r=n(14516),o=n(66477),i=(0,r.Z)((function(e){if(e.time_format===o.zt.language||e.time_format===o.zt.system){var t=e.time_format===o.zt.language?e.language:void 0,n=(new Date).toLocaleString(t);return n.includes("AM")||n.includes("PM")}return e.time_format===o.zt.am_pm}))},22098:function(e,t,n){var r,o,i,a,c=n(37500),s=n(72367);function l(e){return l="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},l(e)}function u(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function f(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function p(e,t){return p=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},p(e,t)}function d(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=y(e);if(t){var o=y(this).constructor;n=Reflect.construct(r,arguments,o)}else n=r.apply(this,arguments);return h(this,n)}}function h(e,t){if(t&&("object"===l(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return m(e)}function m(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function y(e){return y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},y(e)}function b(){b=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var i="static"===o?e:n;this.defineClassElement(i,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var r=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!w(e))return n.push(e);var t=this.decorateElement(e,o);n.push(t.element),n.push.apply(n,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:n,finishers:r};var i=this.decorateConstructor(n,t);return r.push.apply(r,i.finishers),i.finishers=r,i},addElementPlacement:function(e,t,n){var r=t[e.placement];if(!n&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var n=[],r=[],o=e.decorators,i=o.length-1;i>=0;i--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var c=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,o[i])(c)||c);e=s.element,this.addElementPlacement(e,t),s.finisher&&r.push(s.finisher);var l=s.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);n.push.apply(n,l)}}return{element:e,finishers:r,extras:n}},decorateConstructor:function(e,t){for(var n=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),i=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==i.finisher&&n.push(i.finisher),void 0!==i.elements){e=i.elements;for(var a=0;a<e.length-1;a++)for(var c=a+1;c<e.length;c++)if(e[a].key===e[c].key&&e[a].placement===e[c].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return O(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?O(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=E(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var i={kind:t,key:n,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),i.initializer=e.initializer),i},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:x(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=x(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var r=(0,t[n])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function v(e){var t,n=E(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function g(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function w(e){return e.decorators&&e.decorators.length}function k(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function x(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function E(e){var t=function(e,t){if("object"!==l(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==l(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===l(t)?t:String(t)}function O(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}!function(e,t,n,r){var o=b();if(r)for(var i=0;i<r.length;i++)o=r[i](o);var a=t((function(e){o.initializeInstanceElements(e,c.elements)}),n),c=o.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===i.key&&e.placement===i.placement},r=0;r<e.length;r++){var o,i=e[r];if("method"===i.kind&&(o=t.find(n)))if(k(i.descriptor)||k(o.descriptor)){if(w(i)||w(o))throw new ReferenceError("Duplicated methods ("+i.key+") can't be decorated.");o.descriptor=i.descriptor}else{if(w(i)){if(w(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+i.key+").");o.decorators=i.decorators}g(i,o)}else t.push(i)}return t}(a.d.map(v)),e);o.initializeClassElements(a.F,c.elements),o.runClassFinishers(a.F,c.finishers)}([(0,s.Mo)("ha-card")],(function(e,t){var n=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&p(e,t)}(r,t);var n=d(r);function r(){var t;f(this,r);for(var o=arguments.length,i=new Array(o),a=0;a<o;a++)i[a]=arguments[a];return t=n.call.apply(n,[this].concat(i)),e(m(t)),t}return r}(t);return{F:n,d:[{kind:"field",decorators:[(0,s.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean,reflect:!0})],key:"outlined",value:function(){return!1}},{kind:"get",static:!0,key:"styles",value:function(){return(0,c.iv)(r||(r=u(["\n      :host {\n        background: var(\n          --ha-card-background,\n          var(--card-background-color, white)\n        );\n        border-radius: var(--ha-card-border-radius, 4px);\n        box-shadow: var(\n          --ha-card-box-shadow,\n          0px 2px 1px -1px rgba(0, 0, 0, 0.2),\n          0px 1px 1px 0px rgba(0, 0, 0, 0.14),\n          0px 1px 3px 0px rgba(0, 0, 0, 0.12)\n        );\n        color: var(--primary-text-color);\n        display: block;\n        transition: all 0.3s ease-out;\n        position: relative;\n      }\n\n      :host([outlined]) {\n        box-shadow: none;\n        border-width: var(--ha-card-border-width, 1px);\n        border-style: solid;\n        border-color: var(\n          --ha-card-border-color,\n          var(--divider-color, #e0e0e0)\n        );\n      }\n\n      .card-header,\n      :host ::slotted(.card-header) {\n        color: var(--ha-card-header-color, --primary-text-color);\n        font-family: var(--ha-card-header-font-family, inherit);\n        font-size: var(--ha-card-header-font-size, 24px);\n        letter-spacing: -0.012em;\n        line-height: 48px;\n        padding: 12px 16px 16px;\n        display: block;\n        margin-block-start: 0px;\n        margin-block-end: 0px;\n        font-weight: normal;\n      }\n\n      :host ::slotted(.card-content:not(:first-child)),\n      slot:not(:first-child)::slotted(.card-content) {\n        padding-top: 0px;\n        margin-top: -8px;\n      }\n\n      :host ::slotted(.card-content) {\n        padding: 16px;\n      }\n\n      :host ::slotted(.card-actions) {\n        border-top: 1px solid var(--divider-color, #e8e8e8);\n        padding: 5px 16px;\n      }\n    "])))}},{kind:"method",key:"render",value:function(){return(0,c.dy)(o||(o=u(["\n      ","\n      <slot></slot>\n    "])),this.header?(0,c.dy)(i||(i=u(['<h1 class="card-header">',"</h1>"])),this.header):(0,c.dy)(a||(a=u([""]))))}}]}}),c.oi)},11052:function(e,t,n){n.d(t,{I:function(){return p}});var r=n(76389),o=n(47181);function i(e){return i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},i(e)}function a(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function c(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function s(e,t){return s=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},s(e,t)}function l(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=f(e);if(t){var o=f(this).constructor;n=Reflect.construct(r,arguments,o)}else n=r.apply(this,arguments);return u(this,n)}}function u(e,t){if(t&&("object"===i(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function f(e){return f=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},f(e)}var p=(0,r.o)((function(e){return function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&s(e,t)}(u,e);var t,n,r,i=l(u);function u(){return a(this,u),i.apply(this,arguments)}return t=u,(n=[{key:"fire",value:function(e,t,n){return n=n||{},(0,o.B)(n.node||this,e,t,n)}}])&&c(t.prototype,n),r&&c(t,r),u}(e)}))},1265:function(e,t,n){var r=n(76389);function o(e){return o="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},o(e)}function i(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function a(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function c(e,t){return c=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},c(e,t)}function s(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=u(e);if(t){var o=u(this).constructor;n=Reflect.construct(r,arguments,o)}else n=r.apply(this,arguments);return l(this,n)}}function l(e,t){if(t&&("object"===o(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function u(e){return u=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},u(e)}t.Z=(0,r.o)((function(e){return function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&c(e,t)}(l,e);var t,n,r,o=s(l);function l(){return i(this,l),o.apply(this,arguments)}return t=l,r=[{key:"properties",get:function(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}}],(n=[{key:"__computeLocalize",value:function(e){return e}}])&&a(t.prototype,n),r&&a(t,r),l}(e)}))},35987:function(e,t,n){n.r(t);n(53918),n(53268),n(12730),n(25856),n(53973),n(89194),n(91441);var r,o=n(50856),i=n(28426),a=n(44583),c=(n(22098),n(48932),n(46167),n(27849),n(11052)),s=n(1265);n(3426);function l(e){return l="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},l(e)}function u(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function f(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function p(e,t,n){return p="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=y(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(n):o.value}},p(e,t,n||e)}function d(e,t){return d=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},d(e,t)}function h(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=y(e);if(t){var o=y(this).constructor;n=Reflect.construct(r,arguments,o)}else n=r.apply(this,arguments);return m(this,n)}}function m(e,t){if(t&&("object"===l(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function y(e){return y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},y(e)}var b=!1,v=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&d(e,t)}(l,e);var t,i,c,s=h(l);function l(){return u(this,l),s.apply(this,arguments)}return t=l,c=[{key:"template",get:function(){return(0,o.d)(r||(e=['\n      <style include="ha-style">\n        :host {\n          -ms-user-select: initial;\n          -webkit-user-select: initial;\n          -moz-user-select: initial;\n        }\n\n        .content {\n          padding: 16px;\n          max-width: 600px;\n          margin: 0 auto;\n        }\n\n        ha-card {\n          overflow: hidden;\n        }\n\n        paper-item {\n          cursor: pointer;\n        }\n\n        ha-tabs {\n          margin-left: max(env(safe-area-inset-left), 24px);\n          margin-right: max(env(safe-area-inset-right), 24px);\n          --paper-tabs-selection-bar-color: #fff;\n          text-transform: uppercase;\n        }\n\n        .empty {\n          text-align: center;\n          color: var(--secondary-text-color);\n        }\n\n        .header {\n          @apply --paper-font-title;\n        }\n\n        .row {\n          display: flex;\n          justify-content: space-between;\n        }\n\n        @media all and (max-width: 450px) {\n          .content {\n            width: auto;\n            padding: 0;\n          }\n        }\n\n        .tip {\n          color: var(--secondary-text-color);\n          font-size: 14px;\n        }\n        .date {\n          color: var(--primary-text-color);\n        }\n      </style>\n\n      <ha-app-layout>\n        <app-header slot="header" fixed>\n          <app-toolbar>\n            <ha-menu-button\n              hass="[[hass]]"\n              narrow="[[narrow]]"\n            ></ha-menu-button>\n            <div main-title>[[localize(\'panel.mailbox\')]]</div>\n          </app-toolbar>\n          <div sticky hidden$="[[areTabsHidden(platforms)]]">\n            <ha-tabs\n              scrollable\n              selected="[[_currentPlatform]]"\n              on-iron-activate="handlePlatformSelected"\n            >\n              <template is="dom-repeat" items="[[platforms]]">\n                <paper-tab data-entity="[[item]]">\n                  [[getPlatformName(item)]]\n                </paper-tab>\n              </template>\n            </ha-tabs>\n          </div>\n        </app-header>\n        <div class="content">\n          <ha-card>\n            <template is="dom-if" if="[[!_messages.length]]">\n              <div class="card-content empty">\n                [[localize(\'ui.panel.mailbox.empty\')]]\n              </div>\n            </template>\n            <template is="dom-repeat" items="[[_messages]]">\n              <paper-item on-click="openMP3Dialog">\n                <paper-item-body style="width:100%" two-line>\n                  <div class="row">\n                    <div>[[item.caller]]</div>\n                    <div class="tip">\n                      [[localize(\'ui.duration.second\', \'count\', item.duration)]]\n                    </div>\n                  </div>\n                  <div secondary>\n                    <span class="date">[[item.timestamp]]</span> -\n                    [[item.message]]\n                  </div>\n                </paper-item-body>\n              </paper-item>\n            </template>\n          </ha-card>\n        </div>\n      </ha-app-layout>\n    '],t||(t=e.slice(0)),r=Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))));var e,t}},{key:"properties",get:function(){return{hass:Object,narrow:Boolean,platforms:{type:Array},_messages:{type:Array},_currentPlatform:{type:Number,value:0}}}}],(i=[{key:"connectedCallback",value:function(){var e=this;p(y(l.prototype),"connectedCallback",this).call(this),b||(b=!0,this.fire("register-dialog",{dialogShowEvent:"show-audio-message-dialog",dialogTag:"ha-dialog-show-audio-message",dialogImport:function(){return Promise.all([n.e(29907),n.e(34821),n.e(28007),n.e(67605)]).then(n.bind(n,22179))}})),this.hassChanged=this.hassChanged.bind(this),this.hass.connection.subscribeEvents(this.hassChanged,"mailbox_updated").then((function(t){e._unsubEvents=t})),this.computePlatforms().then((function(t){e.platforms=t,e.hassChanged()}))}},{key:"disconnectedCallback",value:function(){p(y(l.prototype),"disconnectedCallback",this).call(this),this._unsubEvents&&this._unsubEvents()}},{key:"hassChanged",value:function(){var e=this;this._messages||(this._messages=[]),this.getMessages().then((function(t){e._messages=t}))}},{key:"openMP3Dialog",value:function(e){this.fire("show-audio-message-dialog",{hass:this.hass,message:e.model.item})}},{key:"getMessages",value:function(){var e=this,t=this.platforms[this._currentPlatform];return this.hass.callApi("GET","mailbox/messages/".concat(t.name)).then((function(n){for(var r=[],o=n.length,i=0;i<o;i++){var c=(0,a.o0)(new Date(1e3*n[i].info.origtime),e.hass.locale);r.push({timestamp:c,caller:n[i].info.callerid,message:n[i].text,sha:n[i].sha,duration:n[i].info.duration,platform:t})}return r.sort((function(e,t){return new Date(t.timestamp)-new Date(e.timestamp)}))}))}},{key:"computePlatforms",value:function(){return this.hass.callApi("GET","mailbox/platforms")}},{key:"handlePlatformSelected",value:function(e){var t=e.detail.selected;t!==this._currentPlatform&&(this._currentPlatform=t,this.hassChanged())}},{key:"areTabsHidden",value:function(e){return!e||e.length<2}},{key:"getPlatformName",value:function(e){var t="mailbox.".concat(e.name);return this.hass.states[t.toLowerCase()].attributes.friendly_name}}])&&f(t.prototype,i),c&&f(t,c),l}((0,c.I)((0,s.Z)(i.H3)));customElements.define("ha-panel-mailbox",v)},3426:function(e,t,n){n(21384);var r=n(11654),o=document.createElement("template");o.setAttribute("style","display: none;"),o.innerHTML='<dom-module id="ha-style">\n  <template>\n    <style>\n    '.concat(r.Qx.cssText,"\n    </style>\n  </template>\n</dom-module>"),document.head.appendChild(o.content)}}]);