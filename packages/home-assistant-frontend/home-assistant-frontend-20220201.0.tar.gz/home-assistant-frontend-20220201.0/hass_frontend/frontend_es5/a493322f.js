"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[31523],{96151:function(e,t,r){r.d(t,{T:function(){return n},y:function(){return i}});var n=function(e){requestAnimationFrame((function(){return setTimeout(e,0)}))},i=function(){return new Promise((function(e){n(e)}))}},31523:function(e,t,r){var n,i,o,a,s,l,c,u=r(37500),f=r(72367),d=r(47501),p=r(18457),h=r(96151);function m(e){return m="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},m(e)}function v(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function y(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function b(e,t){return b=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},b(e,t)}function k(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=D(e);if(t){var i=D(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return g(this,r)}}function g(e,t){if(t&&("object"===m(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return w(e)}function w(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function E(){E=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!C(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,i[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&n.push(l.finisher);var c=l.extras;if(c){for(var u=0;u<c.length;u++)this.addElementPlacement(c[u],t);r.push.apply(r,c)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=S(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:O(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=O(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function P(e){var t,r=S(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function x(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function C(e){return e.decorators&&e.decorators.length}function A(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function O(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function S(e){var t=function(e,t){if("object"!==m(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==m(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===m(t)?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function T(e,t,r){return T="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=D(e)););return e}(e,t);if(n){var i=Object.getOwnPropertyDescriptor(n,t);return i.get?i.get.call(r):i.value}},T(e,t,r||e)}function D(e){return D=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},D(e)}var j=function(e,t,r){var n=function(e,t,r){return 100*(e-t)/(r-t)}(function(e,t,r){return isNaN(e)||isNaN(t)||isNaN(r)?0:e>r?r:e<t?t:e}(e,t,r),t,r);return 180*n/100};!function(e,t,r,n){var i=E();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(A(o.descriptor)||A(i.descriptor)){if(C(o)||C(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(C(o)){if(C(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}x(o,i)}else t.push(o)}return t}(a.d.map(P)),e);i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,f.Mo)("ha-gauge")],(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&b(e,t)}(n,t);var r=k(n);function n(){var t;y(this,n);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=r.call.apply(r,[this].concat(o)),e(w(t)),t}return n}(t);return{F:r,d:[{kind:"field",decorators:[(0,f.Cb)({type:Number})],key:"min",value:function(){return 0}},{kind:"field",decorators:[(0,f.Cb)({type:Number})],key:"max",value:function(){return 100}},{kind:"field",decorators:[(0,f.Cb)({type:Number})],key:"value",value:function(){return 0}},{kind:"field",decorators:[(0,f.Cb)({type:String})],key:"valueText",value:void 0},{kind:"field",decorators:[(0,f.Cb)()],key:"locale",value:void 0},{kind:"field",decorators:[(0,f.Cb)({type:Boolean})],key:"needle",value:void 0},{kind:"field",decorators:[(0,f.Cb)()],key:"levels",value:void 0},{kind:"field",decorators:[(0,f.Cb)()],key:"label",value:function(){return""}},{kind:"field",decorators:[(0,f.SB)()],key:"_angle",value:function(){return 0}},{kind:"field",decorators:[(0,f.SB)()],key:"_updated",value:function(){return!1}},{kind:"method",key:"firstUpdated",value:function(e){var t=this;T(D(r.prototype),"firstUpdated",this).call(this,e),(0,h.T)((function(){t._updated=!0,t._angle=j(t.value,t.min,t.max),t._rescale_svg()}))}},{kind:"method",key:"updated",value:function(e){T(D(r.prototype),"updated",this).call(this,e),this._updated&&e.has("value")&&(this._angle=j(this.value,this.min,this.max),this._rescale_svg())}},{kind:"method",key:"render",value:function(){var e=this;return(0,u.YP)(n||(n=v(['\n      <svg viewBox="-50 -50 100 50" class="gauge">\n        ',"\n\n        ","\n        ",'\n        </path>\n      </svg>\n      <svg class="text">\n        <text class="value-text">\n          '," ","\n        </text>\n      </svg>"])),this.needle&&this.levels?"":(0,u.YP)(i||(i=v(['<path\n          class="dial"\n          d="M -40 0 A 40 40 0 0 1 40 0"\n        ></path>']))),this.levels?this.levels.sort((function(e,t){return e.level-t.level})).map((function(t,r){var n;if(0===r&&t.level!==e.min){var i=j(e.min,e.min,e.max);n=(0,u.YP)(o||(o=v(['<path\n                        stroke="var(--info-color)"\n                        class="level"\n                        d="M\n                          ',"\n                          ",'\n                         A 40 40 0 0 1 40 0\n                        "\n                      ></path>'])),0-40*Math.cos(i*Math.PI/180),0-40*Math.sin(i*Math.PI/180))}var s=j(t.level,e.min,e.max);return(0,u.YP)(a||(a=v(["",'<path\n                      stroke="','"\n                      class="level"\n                      d="M\n                        ',"\n                        ",'\n                       A 40 40 0 0 1 40 0\n                      "\n                    ></path>'])),n,t.stroke,0-40*Math.cos(s*Math.PI/180),0-40*Math.sin(s*Math.PI/180))})):"",this.needle?(0,u.YP)(s||(s=v(['<path\n                class="needle"\n                d="M -25 -2.5 L -47.5 0 L -25 2.5 z"\n                style=',"\n              >\n              "])),(0,d.V)({transform:"rotate(".concat(this._angle,"deg)")})):(0,u.YP)(l||(l=v(['<path\n                class="value"\n                d="M -40 0 A 40 40 0 1 0 40 0"\n                style=',"\n              >"])),(0,d.V)({transform:"rotate(".concat(this._angle,"deg)")})),this.valueText||(0,p.uf)(this.value,this.locale),this.label)}},{kind:"method",key:"_rescale_svg",value:function(){var e=this.shadowRoot.querySelector(".text"),t=e.querySelector("text").getBBox();e.setAttribute("viewBox","".concat(t.x," ").concat(t.y," ").concat(t.width," ").concat(t.height))}},{kind:"get",static:!0,key:"styles",value:function(){return(0,u.iv)(c||(c=v(["\n      :host {\n        position: relative;\n      }\n      .dial {\n        fill: none;\n        stroke: var(--primary-background-color);\n        stroke-width: 15;\n      }\n      .value {\n        fill: none;\n        stroke-width: 15;\n        stroke: var(--gauge-color);\n        transition: all 1s ease 0s;\n      }\n      .needle {\n        fill: var(--primary-text-color);\n        transition: all 1s ease 0s;\n      }\n      .level {\n        fill: none;\n        stroke-width: 15;\n      }\n      .gauge {\n        display: block;\n      }\n      .text {\n        position: absolute;\n        max-height: 40%;\n        max-width: 55%;\n        left: 50%;\n        bottom: -6%;\n        transform: translate(-50%, 0%);\n      }\n      .value-text {\n        font-size: 50px;\n        fill: var(--primary-text-color);\n        text-anchor: middle;\n      }\n    "])))}}]}}),u.oi)}}]);