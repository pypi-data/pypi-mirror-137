"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[52524],{76270:function(e,t,r){r.d(t,{Q:function(){return i}});var i=["relative","total","date","time","datetime"]},52524:function(e,t,r){r.r(t),r.d(t,{HuiHistoryGraphCardEditor:function(){return D}});r(30879);var i,n,o=r(37500),a=r(72367),s=r(69505),c=r(47181),l=(r(1528),r(14748)),u=r(30232),f=r(45890),d=r(98346);function p(e){return p="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},p(e)}function h(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function y(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function m(e,t){return m=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},m(e,t)}function v(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,i=b(e);if(t){var n=b(this).constructor;r=Reflect.construct(i,arguments,n)}else r=i.apply(this,arguments);return g(this,r)}}function g(e,t){if(t&&("object"===p(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return _(e)}function _(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function b(e){return b=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},b(e)}function w(){w=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!j(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return S(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?S(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=O(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:P(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=P(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function k(e){var t,r=O(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function E(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function j(e){return e.decorators&&e.decorators.length}function C(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function P(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function O(e){var t=function(e,t){if("object"!==p(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!==p(i))return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===p(t)?t:String(t)}function S(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}var A=(0,s.f0)(d.I,(0,s.Ry)({entities:(0,s.IX)(u.K),title:(0,s.jt)((0,s.Z_)()),hours_to_show:(0,s.jt)((0,s.Rx)()),refresh_interval:(0,s.jt)((0,s.Rx)())})),D=function(e,t,r,i){var n=w();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(C(o.descriptor)||C(n.descriptor)){if(j(o)||j(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(j(o)){if(j(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}E(o,n)}else t.push(o)}return t}(a.d.map(k)),e);return n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,a.Mo)("hui-history-graph-card-editor")],(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&m(e,t)}(i,t);var r=v(i);function i(){var t;y(this,i);for(var n=arguments.length,o=new Array(n),a=0;a<n;a++)o[a]=arguments[a];return t=r.call.apply(r,[this].concat(o)),e(_(t)),t}return i}(t);return{F:r,d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_configEntities",value:void 0},{kind:"method",key:"setConfig",value:function(e){(0,s.hu)(e,A),this._config=e,this._configEntities=(0,l.Q)(e.entities)}},{kind:"get",key:"_title",value:function(){return this._config.title||""}},{kind:"get",key:"_hours_to_show",value:function(){return this._config.hours_to_show||24}},{kind:"get",key:"_refresh_interval",value:function(){return this._config.refresh_interval||0}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?(0,o.dy)(n||(n=h(['\n      <div class="card-config">\n        <paper-input\n          .label="'," (",')"\n          .value=',"\n          .configValue=","\n          @value-changed=",'\n        ></paper-input>\n        <div class="side-by-side">\n          <paper-input\n            type="number"\n            .label="'," (",')"\n            .value=','\n            min="1"\n            .configValue=',"\n            @value-changed=",'\n          ></paper-input>\n          <paper-input\n            type="number"\n            .label="'," (",')"\n            .value=',"\n            .configValue=","\n            @value-changed=","\n          ></paper-input>\n        </div>\n        <hui-entity-editor\n          .hass=","\n          .entities=","\n          @entities-changed=","\n        ></hui-entity-editor>\n      </div>\n    "])),this.hass.localize("ui.panel.lovelace.editor.card.generic.title"),this.hass.localize("ui.panel.lovelace.editor.card.config.optional"),this._title,"title",this._valueChanged,this.hass.localize("ui.panel.lovelace.editor.card.generic.hours_to_show"),this.hass.localize("ui.panel.lovelace.editor.card.config.optional"),this._hours_to_show,"hours_to_show",this._valueChanged,this.hass.localize("ui.panel.lovelace.editor.card.generic.refresh_interval"),this.hass.localize("ui.panel.lovelace.editor.card.config.optional"),this._refresh_interval,"refresh_interval",this._valueChanged,this.hass,this._configEntities,this._valueChanged):(0,o.dy)(i||(i=h([""])))}},{kind:"method",key:"_valueChanged",value:function(e){if(this._config&&this.hass){var t=e.target;if(e.detail||this["_".concat(t.configValue)]!==t.value){if(e.detail&&e.detail.entities)this._config=Object.assign({},this._config,{entities:e.detail.entities}),this._configEntities=(0,l.Q)(this._config.entities);else if(t.configValue)if(""===t.value)this._config=Object.assign({},this._config),delete this._config[t.configValue];else{var r=t.value;"number"===t.type&&(r=Number(r)),this._config=Object.assign({},this._config,function(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}({},t.configValue,r))}(0,c.B)(this,"config-changed",{config:this._config})}}}},{kind:"get",static:!0,key:"styles",value:function(){return f.A}}]}}),o.oi)},14748:function(e,t,r){function i(e){return e.map((function(e){return"string"==typeof e?{entity:e}:e}))}r.d(t,{Q:function(){return i}})},85677:function(e,t,r){r.d(t,{C:function(){return f}});var i=r(69505),n=(0,i.Ry)({user:(0,i.Z_)()}),o=(0,i.G0)([(0,i.O7)(),(0,i.Ry)({text:(0,i.jt)((0,i.Z_)()),excemptions:(0,i.jt)((0,i.IX)(n))})]),a=(0,i.Ry)({action:(0,i.i0)("url"),url_path:(0,i.Z_)(),confirmation:(0,i.jt)(o)}),s=(0,i.Ry)({action:(0,i.i0)("call-service"),service:(0,i.Z_)(),service_data:(0,i.jt)((0,i.Ry)()),target:(0,i.jt)((0,i.Ry)({entity_id:(0,i.jt)((0,i.G0)([(0,i.Z_)(),(0,i.IX)((0,i.Z_)())])),device_id:(0,i.jt)((0,i.G0)([(0,i.Z_)(),(0,i.IX)((0,i.Z_)())])),area_id:(0,i.jt)((0,i.G0)([(0,i.Z_)(),(0,i.IX)((0,i.Z_)())]))})),confirmation:(0,i.jt)(o)}),c=(0,i.Ry)({action:(0,i.i0)("navigate"),navigation_path:(0,i.Z_)(),confirmation:(0,i.jt)(o)}),l=(0,i.dt)({action:(0,i.i0)("fire-dom-event")}),u=(0,i.Ry)({action:(0,i.kE)(["none","toggle","more-info","call-service","url","navigate"]),confirmation:(0,i.jt)(o)}),f=(0,i.G0)([u,a,c,s,l])},98346:function(e,t,r){r.d(t,{I:function(){return n}});var i=r(69505),n=(0,i.Ry)({type:(0,i.Z_)(),view_layout:(0,i.Yj)()})},30232:function(e,t,r){r.d(t,{K:function(){return a}});var i=r(69505),n=r(76270),o=r(85677),a=(0,i.G0)([(0,i.Ry)({entity:(0,i.Z_)(),name:(0,i.jt)((0,i.Z_)()),icon:(0,i.jt)((0,i.Z_)()),image:(0,i.jt)((0,i.Z_)()),secondary_info:(0,i.jt)((0,i.Z_)()),format:(0,i.jt)((0,i.kE)(n.Q)),state_color:(0,i.jt)((0,i.O7)()),tap_action:(0,i.jt)(o.C),hold_action:(0,i.jt)(o.C),double_tap_action:(0,i.jt)(o.C)}),(0,i.Z_)()])}}]);