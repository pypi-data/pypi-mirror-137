/*! For license information please see 679ae7e2.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[7338],{15112:(e,t,i)=>{i.d(t,{P:()=>n});i(94604);var r=i(9672);class n{constructor(e){n[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}get value(){var e=this.type,t=this.key;if(e&&t)return n.types[e]&&n.types[e][t]}set value(e){var t=this.type,i=this.key;t&&i&&(t=n.types[t]=n.types[t]||{},null==e?delete t[i]:t[i]=e)}get list(){if(this.type){var e=n.types[this.type];return e?Object.keys(e).map((function(e){return o[this.type][e]}),this):[]}}byKey(e){return this.key=e,this.value}}n[" "]=function(){},n.types={};var o=n.types;(0,r.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,i){var r=new n({type:e,key:t});return void 0!==i&&i!==r.value?r.value=i:this.value!==r.value&&(this.value=r.value),r},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new n({type:this.type,key:e}).value}})},86977:(e,t,i)=>{i.d(t,{Q:()=>r});const r=e=>!(!e.detail.selected||"property"!==e.detail.source)&&(e.currentTarget.selected=!1,!0)},15493:(e,t,i)=>{i.d(t,{Q2:()=>r,io:()=>n,ou:()=>o,j4:()=>s,pc:()=>a});const r=()=>{const e={},t=new URLSearchParams(location.search);for(const[i,r]of t.entries())e[i]=r;return e},n=e=>new URLSearchParams(window.location.search).get(e),o=e=>{const t=new URLSearchParams;return Object.entries(e).forEach((([e,i])=>{t.append(e,i)})),t.toString()},s=e=>{const t=new URLSearchParams(window.location.search);return Object.entries(e).forEach((([e,i])=>{t.set(e,i)})),t.toString()},a=e=>{const t=new URLSearchParams(window.location.search);return t.delete(e),t.toString()}},96151:(e,t,i)=>{i.d(t,{T:()=>r,y:()=>n});const r=e=>{requestAnimationFrame((()=>setTimeout(e,0)))},n=()=>new Promise((e=>{r(e)}))},2852:(e,t,i)=>{i.d(t,{t:()=>l});var r=i(37500),n=i(85415),o=i(73728),s=i(5986),a=i(52871);const l=(e,t)=>(0,a.w)(e,t,{loadDevicesAndAreas:!0,getFlowHandlers:async e=>{const[t]=await Promise.all([(0,o.d4)(e),e.loadBackendTranslation("title",void 0,!0)]);return t.sort(((t,i)=>(0,n.f)((0,s.Lh)(e.localize,t),(0,s.Lh)(e.localize,i))))},createFlow:async(e,t)=>{const[i]=await Promise.all([(0,o.Ky)(e,t),e.loadBackendTranslation("config",t),e.loadBackendTranslation("title",t)]);return i},fetchFlow:async(e,t)=>{const i=await(0,o.D4)(e,t);return await e.loadBackendTranslation("config",i.handler),i},handleFlowStep:o.XO,deleteFlow:o.oi,renderAbortDescription(e,t){const i=e.localize(`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return i?r.dy`
            <ha-markdown allowsvg breaks .content=${i}></ha-markdown>
          `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormStepDescription(e,t){const i=e.localize(`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return i?r.dy`
            <ha-markdown allowsvg breaks .content=${i}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(e,t,i)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.data.${i.name}`),renderShowFormStepFieldError:(e,t,i)=>e.localize(`component.${t.handler}.config.error.${i}`,t.description_placeholders),renderExternalStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site"),renderExternalStepDescription(e,t){const i=e.localize(`component.${t.handler}.config.${t.step_id}.description`,t.description_placeholders);return r.dy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${i?r.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const i=e.localize(`component.${t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return r.dy`
        ${i?r.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""}
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.created_config","name",t.title)}
        </p>
      `},renderShowFormProgressHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormProgressDescription(e,t){const i=e.localize(`component.${t.handler}.config.progress.${t.progress_action}`,t.description_placeholders);return i?r.dy`
            <ha-markdown allowsvg breaks .content=${i}></ha-markdown>
          `:""},renderLoadingDescription(e,t,i,r){if(!["loading_flow","loading_step"].includes(t))return"";const n=(null==r?void 0:r.handler)||i;return e.localize(`ui.panel.config.integrations.config_flow.loading.${t}`,{integration:n?(0,s.Lh)(e.localize,n):e.localize("ui.panel.config.integrations.config_flow.loading.fallback_title")})}})},47090:(e,t,i)=>{i.r(t);i(44577);var r=i(81480),n=i(37500),o=i(72367),s=i(48399),a=i(14516),l=i(83849),c=(i(7164),i(85415)),d=i(15493),h=i(96151),f=(i(81545),i(32511),i(36125),i(10983),i(52039),i(7323)),p=i(81582),u=i(73728),m=i(57292),y=i(74186),g=i(5986);var v=i(2852),b=i(26765),w=(i(15291),i(1359),i(73826)),k=i(11654),_=i(29311),E=i(228),$=i(47181),x=(i(54444),i(11254));function z(){z=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!D(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return F(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?F(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=T(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:S(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=S(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function C(e){var t,i=T(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function A(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function D(e){return e.decorators&&e.decorators.length}function P(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function S(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function T(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function F(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=z();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(P(o.descriptor)||P(n.descriptor)){if(D(o)||D(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(D(o)){if(D(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}A(o,n)}else t.push(o)}return t}(s.d.map(C)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-integration-header")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"banner",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"localizedDomainName",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"domain",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"manifest",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"configEntry",value:void 0},{kind:"method",key:"render",value:function(){var e;let t,i;const r=this.localizedDomainName||(0,g.Lh)(this.hass.localize,this.domain,this.manifest);this.label?(t=this.label,i=t.toLowerCase()===r.toLowerCase()?void 0:r):t=r;const o=[];var s;this.manifest&&(this.manifest.is_built_in||o.push(["M2,10.96C1.5,10.68 1.35,10.07 1.63,9.59L3.13,7C3.24,6.8 3.41,6.66 3.6,6.58L11.43,2.18C11.59,2.06 11.79,2 12,2C12.21,2 12.41,2.06 12.57,2.18L20.47,6.62C20.66,6.72 20.82,6.88 20.91,7.08L22.36,9.6C22.64,10.08 22.47,10.69 22,10.96L21,11.54V16.5C21,16.88 20.79,17.21 20.47,17.38L12.57,21.82C12.41,21.94 12.21,22 12,22C11.79,22 11.59,21.94 11.43,21.82L3.53,17.38C3.21,17.21 3,16.88 3,16.5V10.96C2.7,11.13 2.32,11.14 2,10.96M12,4.15V4.15L12,10.85V10.85L17.96,7.5L12,4.15M5,15.91L11,19.29V12.58L5,9.21V15.91M19,15.91V12.69L14,15.59C13.67,15.77 13.3,15.76 13,15.6V19.29L19,15.91M13.85,13.36L20.13,9.73L19.55,8.72L13.27,12.35L13.85,13.36Z",this.hass.localize("ui.panel.config.integrations.config_entry.provided_by_custom_integration")]),this.manifest.iot_class&&this.manifest.iot_class.startsWith("cloud_")&&o.push(["M19.35,10.03C18.67,6.59 15.64,4 12,4C9.11,4 6.6,5.64 5.35,8.03C2.34,8.36 0,10.9 0,14A6,6 0 0,0 6,20H19A5,5 0 0,0 24,15C24,12.36 21.95,10.22 19.35,10.03Z",this.hass.localize("ui.panel.config.integrations.config_entry.depends_on_cloud")]),null!==(s=this.configEntry)&&void 0!==s&&s.pref_disable_polling&&o.push(["M20,4H14V10L16.24,7.76C17.32,8.85 18,10.34 18,12C18,13 17.75,13.94 17.32,14.77L18.78,16.23C19.55,15 20,13.56 20,12C20,9.79 19.09,7.8 17.64,6.36L20,4M2.86,5.41L5.22,7.77C4.45,9 4,10.44 4,12C4,14.21 4.91,16.2 6.36,17.64L4,20H10V14L7.76,16.24C6.68,15.15 6,13.66 6,12C6,11 6.25,10.06 6.68,9.23L14.76,17.31C14.5,17.44 14.26,17.56 14,17.65V19.74C14.79,19.53 15.54,19.2 16.22,18.78L18.58,21.14L19.85,19.87L4.14,4.14L2.86,5.41M10,6.35V4.26C9.2,4.47 8.45,4.8 7.77,5.22L9.23,6.68C9.5,6.56 9.73,6.44 10,6.35Z",this.hass.localize("ui.panel.config.integrations.config_entry.disabled_polling")]));return n.dy`
      ${this.banner?n.dy`<div class="banner">${this.banner}</div>`:""}
      <slot name="above-header"></slot>
      <div class="header">
        <img
          src=${(0,x.X)({domain:this.domain,type:"icon",darkOptimized:null===(e=this.hass.themes)||void 0===e?void 0:e.darkMode})}
          referrerpolicy="no-referrer"
          @error=${this._onImageError}
          @load=${this._onImageLoad}
        />
        <div class="info">
          <div class="primary" role="heading">${t}</div>
          ${i?n.dy`<div class="secondary">${i}</div>`:""}
        </div>

        ${0===o.length?"":n.dy`
              <div class="icons">
                ${o.map((([e,t])=>n.dy`
                    <span>
                      <ha-svg-icon .path=${e}></ha-svg-icon>
                      <paper-tooltip animation-delay="0"
                        >${t}</paper-tooltip
                      >
                    </span>
                  `))}
              </div>
            `}
      </div>
    `}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(e){e.target.style.visibility="hidden"}},{kind:"field",static:!0,key:"styles",value:()=>n.iv`
    .banner {
      background-color: var(--state-color);
      color: var(--text-on-state-color);
      text-align: center;
      padding: 2px;
      border-top-left-radius: var(--ha-card-border-radius, 4px);
      border-top-right-radius: var(--ha-card-border-radius, 4px);
    }
    .header {
      display: flex;
      position: relative;
      padding: 0 8px 8px 16px;
    }
    .header img {
      margin-right: 16px;
      margin-top: 16px;
      width: 40px;
      height: 40px;
    }
    .header .info {
      flex: 1;
      align-self: center;
    }
    .header .info div {
      word-wrap: break-word;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .primary {
      font-size: 16px;
      margin-top: 16px;
      margin-right: 2px;
      font-weight: 400;
      word-break: break-word;
      color: var(--primary-text-color);
    }
    .secondary {
      font-size: 14px;
      color: var(--secondary-text-color);
    }
    .icons {
      margin-right: 8px;
      margin-left: auto;
      height: 28px;
      color: var(--text-on-state-color, var(--secondary-text-color));
      background-color: var(--state-color, #e0e0e0);
      border-bottom-left-radius: 4px;
      border-bottom-right-radius: 4px;
      display: flex;
      float: right;
    }
    .icons ha-svg-icon {
      width: 20px;
      height: 20px;
      margin: 4px;
    }
    paper-tooltip {
      white-space: nowrap;
    }
  `}]}}),n.oi);function O(){O=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!M(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return H(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?H(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=V(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:R(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=R(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function I(e){var t,i=V(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function L(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function M(e){return e.decorators&&e.decorators.length}function j(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function R(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function V(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function H(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=O();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(j(o.descriptor)||j(n.descriptor)){if(M(o)||M(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(M(o)){if(M(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}L(o,n)}else t.push(o)}return t}(s.d.map(I)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-integration-action-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"banner",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"localizedDomainName",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"domain",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"manifest",value:void 0},{kind:"method",key:"render",value:function(){return n.dy`
      <ha-card outlined>
        <ha-integration-header
          .hass=${this.hass}
          .banner=${this.banner}
          .domain=${this.domain}
          .label=${this.label}
          .localizedDomainName=${this.localizedDomainName}
          .manifest=${this.manifest}
        ></ha-integration-header>
        <div class="filler"></div>
        <div class="actions"><slot></slot></div>
      </ha-card>
    `}},{kind:"field",static:!0,key:"styles",value:()=>n.iv`
    ha-card {
      display: flex;
      flex-direction: column;
      height: 100%;
      --ha-card-border-color: var(--state-color);
      --mdc-theme-primary: var(--state-color);
    }
    .filler {
      flex: 1;
    }
    .attention {
      --state-color: var(--error-color);
      --text-on-state-color: var(--text-primary-color);
    }
    .discovered {
      --state-color: var(--primary-color);
      --text-on-state-color: var(--text-primary-color);
    }
    .actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 6px 0;
      height: 48px;
    }
  `}]}}),n.oi);var B=i(27322);function U(){U=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!q(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return G(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?G(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=Y(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:W(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=W(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function Z(e){var t,i=Y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function N(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function q(e){return e.decorators&&e.decorators.length}function Q(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function W(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function Y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function G(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}const J="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z";!function(e,t,i,r){var n=U();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(Q(o.descriptor)||Q(n.descriptor)){if(q(o)||q(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(q(o)){if(q(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}N(o,n)}else t.push(o)}return t}(s.d.map(Z)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-config-flow-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"flow",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"manifest",value:void 0},{kind:"method",key:"render",value:function(){const e=u.P3.includes(this.flow.context.source);return n.dy`
      <ha-integration-action-card
        class=${(0,E.$)({discovered:!e,attention:e})}
        .hass=${this.hass}
        .manifest=${this.manifest}
        .banner=${this.hass.localize("ui.panel.config.integrations."+(e?"attention":"discovered"))}
        .domain=${this.flow.handler}
        .label=${this.flow.localized_title}
      >
        <mwc-button
          unelevated
          @click=${this._continueFlow}
          .label=${this.hass.localize("ui.panel.config.integrations."+(e?"reconfigure":"configure"))}
        ></mwc-button>
        <ha-button-menu corner="BOTTOM_START">
          <ha-icon-button
            slot="trigger"
            .label=${this.hass.localize("ui.common.menu")}
            .path=${"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z"}
          ></ha-icon-button>
          ${this.flow.context.configuration_url?n.dy`<a
                href=${this.flow.context.configuration_url.replace(/^homeassistant:\/\//,"")}
                rel="noreferrer"
                target=${this.flow.context.configuration_url.startsWith("homeassistant://")?"_self":"_blank"}
              >
                <mwc-list-item hasMeta>
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.open_configuration_url")}<ha-svg-icon
                    slot="meta"
                    .path=${J}
                  ></ha-svg-icon>
                </mwc-list-item>
              </a>`:""}
          ${this.manifest?n.dy`<a
                href=${this.manifest.is_built_in?(0,B.R)(this.hass,`/integrations/${this.manifest.domain}`):this.manifest.documentation}
                rel="noreferrer"
                target="_blank"
              >
                <mwc-list-item hasMeta>
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.documentation")}<ha-svg-icon
                    slot="meta"
                    .path=${J}
                  ></ha-svg-icon>
                </mwc-list-item>
              </a>`:""}
          ${u.pV.includes(this.flow.context.source)&&this.flow.context.unique_id?n.dy`
                <mwc-list-item @click=${this._ignoreFlow}>
                  ${this.hass.localize("ui.panel.config.integrations.ignore.ignore")}
                </mwc-list-item>
              `:""}
        </ha-button-menu>
      </ha-integration-action-card>
    `}},{kind:"method",key:"_continueFlow",value:function(){(0,v.t)(this,{continueFlowId:this.flow.flow_id,dialogClosedCallback:()=>{this._handleFlowUpdated()}})}},{kind:"method",key:"_ignoreFlow",value:async function(){await(0,b.g7)(this,{title:this.hass.localize("ui.panel.config.integrations.ignore.confirm_ignore_title","name",(0,u.WW)(this.hass.localize,this.flow)),text:this.hass.localize("ui.panel.config.integrations.ignore.confirm_ignore"),confirmText:this.hass.localize("ui.panel.config.integrations.ignore.ignore")})&&(await(0,u.zO)(this.hass,this.flow.flow_id,(0,u.WW)(this.hass.localize,this.flow)),this._handleFlowUpdated())}},{kind:"method",key:"_handleFlowUpdated",value:function(){(0,$.B)(this,"change",void 0,{bubbles:!1})}},{kind:"field",static:!0,key:"styles",value:()=>n.iv`
    .attention {
      --state-color: var(--error-color);
      --text-on-state-color: var(--text-primary-color);
    }
    .discovered {
      --state-color: var(--primary-color);
      --text-on-state-color: var(--text-primary-color);
    }
    a {
      text-decoration: none;
      color: var(--primary-color);
    }
  `}]}}),n.oi);function K(){K=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!te(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return oe(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?oe(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=ne(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:re(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=re(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function X(e){var t,i=ne(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function ee(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function te(e){return e.decorators&&e.decorators.length}function ie(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function re(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function ne(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function oe(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=K();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(ie(o.descriptor)||ie(n.descriptor)){if(te(o)||te(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(te(o)){if(te(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}ee(o,n)}else t.push(o)}return t}(s.d.map(X)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-ignored-config-entry-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"entry",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"manifest",value:void 0},{kind:"method",key:"render",value:function(){return n.dy`
      <ha-integration-action-card
        .hass=${this.hass}
        .manifest=${this.manifest}
        .banner=${this.hass.localize("ui.panel.config.integrations.ignore.ignored")}
        .domain=${this.entry.domain}
        .localizedDomainName=${this.entry.localized_domain_name}
        .label=${"Ignored"===this.entry.title?this.entry.localized_domain_name:this.entry.title}
      >
        <mwc-button
          @click=${this._removeIgnoredIntegration}
          .label=${this.hass.localize("ui.panel.config.integrations.ignore.stop_ignore")}
        ></mwc-button>
      </ha-integration-action-card>
    `}},{kind:"method",key:"_removeIgnoredIntegration",value:async function(){(0,b.g7)(this,{title:this.hass.localize("ui.panel.config.integrations.ignore.confirm_delete_ignore_title","name",this.hass.localize(`component.${this.entry.domain}.title`)),text:this.hass.localize("ui.panel.config.integrations.ignore.confirm_delete_ignore"),confirmText:this.hass.localize("ui.panel.config.integrations.ignore.stop_ignore"),confirm:async()=>{(await(0,p.iJ)(this.hass,this.entry.entry_id)).require_restart&&alert(this.hass.localize("ui.panel.config.integrations.config_entry.restart_confirm")),(0,$.B)(this,"change",void 0,{bubbles:!1})}})}},{kind:"field",static:!0,key:"styles",value:()=>n.iv`
    :host {
      --state-color: var(--divider-color, #e0e0e0);
    }

    mwc-button {
      --mdc-theme-primary: var(--primary-color);
    }
  `}]}}),n.oi);i(53918),i(57301),i(51095);var se=i(86977),ae=(i(22098),i(99282),i(22814)),le=i(42916);const ce=()=>Promise.all([i.e(29907),i.e(28083),i.e(23466)]).then(i.bind(i,23466));var de=i(17416),he=i(25936);function fe(){fe=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!me(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return be(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?be(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=ve(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:ge(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=ge(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function pe(e){var t,i=ve(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function ue(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function me(e){return e.decorators&&e.decorators.length}function ye(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function ge(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function ve(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function be(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}const we="M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z",ke="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z",_e={hassio:"/hassio/dashboard",mqtt:"/config/mqtt",zha:"/config/zha/dashboard",ozw:"/config/ozw/dashboard",zwave:"/config/zwave",zwave_js:"/config/zwave_js/dashboard"};!function(e,t,i,r){var n=fe();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(ye(o.descriptor)||ye(n.descriptor)){if(me(o)||me(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(me(o)){if(me(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}ue(o,n)}else t.push(o)}return t}(s.d.map(pe)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-integration-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"domain",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"items",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"manifest",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"entityRegistryEntries",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"deviceRegistryEntries",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"selectedConfigEntryId",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"supportsDiagnostics",value:()=>!1},{kind:"method",key:"render",value:function(){let e=this._selectededConfigEntry;1===this.items.length?e=this.items[0]:this.selectedConfigEntryId&&(e=this.items.find((e=>e.entry_id===this.selectedConfigEntryId)));const t=void 0!==e;return n.dy`
      <ha-card
        outlined
        class=${(0,E.$)({single:t,group:!t,hasMultiple:this.items.length>1,disabled:this.disabled,"state-not-loaded":t&&"not_loaded"===e.state,"state-failed-unload":t&&"failed_unload"===e.state,"state-error":t&&p.LZ.includes(e.state)})}
        .configEntry=${e}
      >
        <ha-integration-header
          .hass=${this.hass}
          .banner=${this.disabled?this.hass.localize("ui.panel.config.integrations.config_entry.disable.disabled"):void 0}
          .domain=${this.domain}
          .label=${e?e.title||e.localized_domain_name||this.domain:void 0}
          .localizedDomainName=${e?e.localized_domain_name:void 0}
          .manifest=${this.manifest}
          .configEntry=${e}
        >
          ${this.items.length>1?n.dy`
                <div class="back-btn" slot="above-header">
                  <ha-icon-button
                    .path=${"M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z"}
                    @click=${this._back}
                    .label=${this.hass.localize("ui.common.back")}
                  ></ha-icon-button>
                </div>
              `:""}
        </ha-integration-header>

        ${e?this._renderSingleEntry(e):this._renderGroupedIntegration()}
      </ha-card>
    `}},{kind:"method",key:"_renderGroupedIntegration",value:function(){return n.dy`
      <paper-listbox class="ha-scrollbar">
        ${this.items.map((e=>n.dy`<paper-item
              .entryId=${e.entry_id}
              @click=${this._selectConfigEntry}
              ><paper-item-body
                >${e.title||this.hass.localize("ui.panel.config.integrations.config_entry.unnamed_entry")}</paper-item-body
              >
              ${p.LZ.includes(e.state)?n.dy`<span>
                    <ha-svg-icon
                      class="error"
                      .path=${we}
                    ></ha-svg-icon
                    ><paper-tooltip animation-delay="0" position="left">
                      ${this.hass.localize(`ui.panel.config.integrations.config_entry.state.${e.state}`)}
                    </paper-tooltip>
                  </span>`:""}
              <ha-icon-next></ha-icon-next>
            </paper-item>`))}
      </paper-listbox>
    `}},{kind:"method",key:"_renderSingleEntry",value:function(e){const t=this._getDevices(e,this.deviceRegistryEntries),i=this._getServices(e,this.deviceRegistryEntries),r=this._getEntities(e,this.entityRegistryEntries);let o,s;e.disabled_by?(o=["ui.panel.config.integrations.config_entry.disable.disabled_cause","cause",this.hass.localize(`ui.panel.config.integrations.config_entry.disable.disabled_by.${e.disabled_by}`)||e.disabled_by],"failed_unload"===e.state&&(s=n.dy`.
        ${this.hass.localize("ui.panel.config.integrations.config_entry.disable_restart_confirm")}.`)):"not_loaded"===e.state?o=["ui.panel.config.integrations.config_entry.not_loaded"]:p.LZ.includes(e.state)&&(o=[`ui.panel.config.integrations.config_entry.state.${e.state}`],e.reason?(this.hass.loadBackendTranslation("config",e.domain),s=n.dy`:
        ${this.hass.localize(`component.${e.domain}.config.error.${e.reason}`)||e.reason}`):s=n.dy`
          <br />
          <a href="/config/logs"
            >${this.hass.localize("ui.panel.config.integrations.config_entry.check_the_logs")}</a
          >
        `);let a=[];for(const[r,o]of[[t,"devices"],[i,"services"]]){if(0===r.length)continue;const t=1===r.length?`/config/devices/device/${r[0].id}`:`/config/devices/dashboard?historyBack=1&config_entry=${e.entry_id}`;a.push(n.dy`<a href=${t}
          >${this.hass.localize(`ui.panel.config.integrations.config_entry.${o}`,"count",r.length)}</a
        >`)}return r.length&&a.push(n.dy`<a
          href=${`/config/entities?historyBack=1&config_entry=${e.entry_id}`}
          >${this.hass.localize("ui.panel.config.integrations.config_entry.entities","count",r.length)}</a
        >`),2===a.length?a=[a[0],` ${this.hass.localize("ui.common.and")} `,a[1]]:3===a.length&&(a=[a[0],", ",a[1],` ${this.hass.localize("ui.common.and")} `,a[2]]),n.dy`
      ${o?n.dy`
            <div class="message">
              <ha-svg-icon .path=${we}></ha-svg-icon>
              <div>${this.hass.localize(...o)}${s}</div>
            </div>
          `:""}
      <div class="content">${a}</div>
      <div class="actions">
        <div>
          ${"user"===e.disabled_by?n.dy`<mwc-button unelevated @click=${this._handleEnable}>
                ${this.hass.localize("ui.common.enable")}
              </mwc-button>`:e.domain in _e?n.dy`<a
                href=${`${_e[e.domain]}?config_entry=${e.entry_id}`}
                ><mwc-button>
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.configure")}
                </mwc-button></a
              >`:e.supports_options?n.dy`
                <mwc-button @click=${this._showOptions}>
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.configure")}
                </mwc-button>
              `:""}
        </div>
        <ha-button-menu corner="BOTTOM_START">
          <ha-icon-button
            slot="trigger"
            .label=${this.hass.localize("ui.common.menu")}
            .path=${"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z"}
          ></ha-icon-button>
          <mwc-list-item @request-selected=${this._handleRename}>
            ${this.hass.localize("ui.panel.config.integrations.config_entry.rename")}
          </mwc-list-item>
          <mwc-list-item @request-selected=${this._handleSystemOptions}>
            ${this.hass.localize("ui.panel.config.integrations.config_entry.system_options")}
          </mwc-list-item>
          ${this.manifest?n.dy` <a
                href=${this.manifest.is_built_in?(0,B.R)(this.hass,`/integrations/${this.manifest.domain}`):this.manifest.documentation}
                rel="noreferrer"
                target="_blank"
              >
                <mwc-list-item hasMeta>
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.documentation")}<ha-svg-icon
                    slot="meta"
                    .path=${ke}
                  ></ha-svg-icon>
                </mwc-list-item>
              </a>`:""}
          ${this.manifest&&(this.manifest.is_built_in||this.manifest.issue_tracker)?n.dy`<a
                href=${(0,g.H0)(e.domain,this.manifest)}
                rel="noreferrer"
                target="_blank"
              >
                <mwc-list-item hasMeta>
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.known_issues")}<ha-svg-icon
                    slot="meta"
                    .path=${ke}
                  ></ha-svg-icon>
                </mwc-list-item>
              </a>`:""}
          ${!e.disabled_by&&"loaded"===e.state&&e.supports_unload&&"system"!==e.source?n.dy`<mwc-list-item @request-selected=${this._handleReload}>
                ${this.hass.localize("ui.panel.config.integrations.config_entry.reload")}
              </mwc-list-item>`:""}
          ${this.supportsDiagnostics&&"loaded"===e.state?n.dy`<a
                href=${(0,le.iP)(e.entry_id)}
                target="_blank"
                @click=${this._signUrl}
              >
                <mwc-list-item>
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.download_diagnostics")}
                </mwc-list-item>
              </a>`:""}
          ${"user"===e.disabled_by?n.dy`<mwc-list-item @request-selected=${this._handleEnable}>
                ${this.hass.localize("ui.common.enable")}
              </mwc-list-item>`:"system"!==e.source?n.dy`<mwc-list-item
                class="warning"
                @request-selected=${this._handleDisable}
              >
                ${this.hass.localize("ui.common.disable")}
              </mwc-list-item>`:""}
          ${"system"!==e.source?n.dy`<mwc-list-item
                class="warning"
                @request-selected=${this._handleDelete}
              >
                ${this.hass.localize("ui.panel.config.integrations.config_entry.delete")}
              </mwc-list-item>`:""}
        </ha-button-menu>
      </div>
    `}},{kind:"get",key:"_selectededConfigEntry",value:function(){return 1===this.items.length?this.items[0]:this.selectedConfigEntryId?this.items.find((e=>e.entry_id===this.selectedConfigEntryId)):void 0}},{kind:"method",key:"_selectConfigEntry",value:function(e){this.selectedConfigEntryId=e.currentTarget.entryId}},{kind:"method",key:"_back",value:function(){this.selectedConfigEntryId=void 0,this.classList.remove("highlight")}},{kind:"field",key:"_getEntities",value:()=>(0,a.Z)(((e,t)=>t?t.filter((t=>t.config_entry_id===e.entry_id)):[]))},{kind:"field",key:"_getDevices",value:()=>(0,a.Z)(((e,t)=>t?t.filter((t=>t.config_entries.includes(e.entry_id)&&"service"!==t.entry_type)):[]))},{kind:"field",key:"_getServices",value:()=>(0,a.Z)(((e,t)=>t?t.filter((t=>t.config_entries.includes(e.entry_id)&&"service"===t.entry_type)):[]))},{kind:"method",key:"_showOptions",value:function(e){(0,de.c)(this,e.target.closest("ha-card").configEntry)}},{kind:"method",key:"_handleRename",value:function(e){(0,se.Q)(e)&&this._editEntryName(e.target.closest("ha-card").configEntry)}},{kind:"method",key:"_handleReload",value:function(e){(0,se.Q)(e)&&this._reloadIntegration(e.target.closest("ha-card").configEntry)}},{kind:"method",key:"_handleDelete",value:function(e){(0,se.Q)(e)&&this._removeIntegration(e.target.closest("ha-card").configEntry)}},{kind:"method",key:"_handleDisable",value:function(e){(0,se.Q)(e)&&this._disableIntegration(e.target.closest("ha-card").configEntry)}},{kind:"method",key:"_handleEnable",value:function(e){e.detail.source&&!(0,se.Q)(e)||this._enableIntegration(e.target.closest("ha-card").configEntry)}},{kind:"method",key:"_handleSystemOptions",value:function(e){(0,se.Q)(e)&&this._showSystemOptions(e.target.closest("ha-card").configEntry)}},{kind:"method",key:"_showSystemOptions",value:function(e){var t,i;t=this,i={entry:e,manifest:this.manifest,entryUpdated:e=>(0,$.B)(this,"entry-updated",{entry:e})},(0,$.B)(t,"show-dialog",{dialogTag:"dialog-config-entry-system-options",dialogImport:ce,dialogParams:i})}},{kind:"method",key:"_disableIntegration",value:async function(e){const t=e.entry_id;if(!await(0,b.g7)(this,{text:this.hass.localize("ui.panel.config.integrations.config_entry.disable.disable_confirm")}))return;let i;try{i=await(0,p.Ny)(this.hass,t)}catch(e){return void(0,b.Ys)(this,{title:this.hass.localize("ui.panel.config.integrations.config_entry.disable_error"),text:e.message})}i.require_restart&&(0,b.Ys)(this,{text:this.hass.localize("ui.panel.config.integrations.config_entry.disable_restart_confirm")}),(0,$.B)(this,"entry-updated",{entry:{...e,disabled_by:"user"}})}},{kind:"method",key:"_enableIntegration",value:async function(e){const t=e.entry_id;let i;try{i=await(0,p.T0)(this.hass,t)}catch(e){return void(0,b.Ys)(this,{title:this.hass.localize("ui.panel.config.integrations.config_entry.disable_error"),text:e.message})}i.require_restart&&(0,b.Ys)(this,{text:this.hass.localize("ui.panel.config.integrations.config_entry.enable_restart_confirm")}),(0,$.B)(this,"entry-updated",{entry:{...e,disabled_by:null}})}},{kind:"method",key:"_removeIntegration",value:async function(e){const t=e.entry_id;if(!await(0,b.g7)(this,{text:this.hass.localize("ui.panel.config.integrations.config_entry.delete_confirm",{title:e.title})}))return;const i=await(0,p.iJ)(this.hass,t);(0,$.B)(this,"entry-removed",{entryId:t}),i.require_restart&&(0,b.Ys)(this,{text:this.hass.localize("ui.panel.config.integrations.config_entry.restart_confirm")})}},{kind:"method",key:"_reloadIntegration",value:async function(e){const t=e.entry_id,i=(await(0,p.Nn)(this.hass,t)).require_restart?"reload_restart_confirm":"reload_confirm";(0,b.Ys)(this,{text:this.hass.localize(`ui.panel.config.integrations.config_entry.${i}`)})}},{kind:"method",key:"_editEntryName",value:async function(e){const t=await(0,b.D9)(this,{title:this.hass.localize("ui.panel.config.integrations.rename_dialog"),defaultValue:e.title,inputLabel:this.hass.localize("ui.panel.config.integrations.rename_input_label")});if(null===t)return;const i=await(0,p.SO)(this.hass,e.entry_id,{title:t});(0,$.B)(this,"entry-updated",{entry:i.config_entry})}},{kind:"method",key:"_signUrl",value:async function(e){const t=e.target.closest("a");e.preventDefault();const i=await(0,ae.iI)(this.hass,t.getAttribute("href"));(0,he.N)(i.path)}},{kind:"get",static:!0,key:"styles",value:function(){return[k.Qx,k.$c,n.iv`
        ha-card {
          display: flex;
          flex-direction: column;
          height: 100%;
          --state-color: var(--divider-color, #e0e0e0);
          --ha-card-border-color: var(--state-color);
          --state-message-color: var(--state-color);
        }
        .state-error {
          --state-color: var(--error-color);
          --text-on-state-color: var(--text-primary-color);
        }
        .state-failed-unload {
          --state-color: var(--warning-color);
          --text-on-state-color: var(--primary-text-color);
        }
        .state-not-loaded {
          --state-message-color: var(--primary-text-color);
        }
        :host(.highlight) ha-card {
          --state-color: var(--primary-color);
          --text-on-state-color: var(--text-primary-color);
        }

        .back-btn {
          background-color: var(--state-color);
          color: var(--text-on-state-color);
          --mdc-icon-button-size: 32px;
          transition: height 0.1s;
          overflow: hidden;
        }
        .hasMultiple.single .back-btn {
          height: 24px;
          display: flex;
          align-items: center;
        }
        .hasMultiple.group .back-btn {
          height: 0px;
        }

        .message {
          font-weight: bold;
          padding-bottom: 16px;
          display: flex;
          margin-left: 40px;
        }
        .message ha-svg-icon {
          color: var(--state-message-color);
        }
        .message div {
          flex: 1;
          margin-left: 8px;
          padding-top: 2px;
          padding-right: 2px;
          overflow-wrap: break-word;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 7;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .content {
          flex: 1;
          padding: 0px 16px 0 72px;
        }

        .actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 8px 0 0 8px;
          height: 48px;
        }
        .actions a {
          text-decoration: none;
        }
        a {
          color: var(--primary-color);
        }
        ha-button-menu {
          color: var(--secondary-text-color);
          --mdc-menu-min-width: 200px;
        }
        @media (min-width: 563px) {
          ha-card.group {
            position: relative;
            min-height: 164px;
          }
          paper-listbox {
            position: absolute;
            top: 64px;
            left: 0;
            right: 0;
            bottom: 0;
            overflow: auto;
          }
          .disabled paper-listbox {
            top: 88px;
          }
        }
        paper-item {
          cursor: pointer;
          min-height: 35px;
        }
        paper-item-body {
          word-wrap: break-word;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 2;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        mwc-list-item ha-svg-icon {
          color: var(--secondary-text-color);
        }
      `]}}]}}),n.oi);function Ee(){Ee=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!ze(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return Pe(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?Pe(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=De(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:Ae(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=Ae(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function $e(e){var t,i=De(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function xe(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function ze(e){return e.decorators&&e.decorators.length}function Ce(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function Ae(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function De(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function Pe(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function Se(e,t,i){return Se="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=Te(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}},Se(e,t,i||e)}function Te(e){return Te=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},Te(e)}const Fe=e=>{const t=new Map;return e.forEach((e=>{t.has(e.domain)?t.get(e.domain).push(e):t.set(e.domain,[e])})),t};!function(e,t,i,r){var n=Ee();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(Ce(o.descriptor)||Ce(n.descriptor)){if(ze(o)||ze(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(ze(o)){if(ze(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}xe(o,n)}else t.push(o)}return t}(s.d.map($e)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-config-integrations")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"isWide",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"showAdvanced",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_configEntries",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"_configEntriesInProgress",value:()=>[]},{kind:"field",decorators:[(0,o.SB)()],key:"_entityRegistryEntries",value:()=>[]},{kind:"field",decorators:[(0,o.SB)()],key:"_deviceRegistryEntries",value:()=>[]},{kind:"field",decorators:[(0,o.SB)()],key:"_manifests",value:()=>({})},{kind:"field",key:"_extraFetchedManifests",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_showIgnored",value:()=>!1},{kind:"field",decorators:[(0,o.SB)()],key:"_showDisabled",value:()=>!1},{kind:"field",decorators:[(0,o.SB)()],key:"_searchParms",value:()=>new URLSearchParams(window.location.hash.substring(1))},{kind:"field",decorators:[(0,o.SB)()],key:"_filter",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_diagnosticHandlers",value:void 0},{kind:"method",key:"hassSubscribe",value:function(){return[(0,y.LM)(this.hass.connection,(e=>{this._entityRegistryEntries=e})),(0,m.q4)(this.hass.connection,(e=>{this._deviceRegistryEntries=e})),(0,u.V3)(this.hass,(async e=>{const t=[];e.forEach((e=>{e.context.title_placeholders&&t.push(this.hass.loadBackendTranslation("config",e.handler)),this._fetchManifest(e.handler)})),await Promise.all(t),await(0,h.y)(),this._configEntriesInProgress=e.map((e=>({...e,localized_title:(0,u.WW)(this.hass.localize,e)})))}))]}},{kind:"field",key:"_filterConfigEntries",value:()=>(0,a.Z)(((e,t)=>{if(!t)return[...e];return new r.Z(e,{keys:["domain","localized_domain_name","title"],isCaseSensitive:!1,minMatchCharLength:2,threshold:.2}).search(t).map((e=>e.item))}))},{kind:"field",key:"_filterGroupConfigEntries",value(){return(0,a.Z)(((e,t)=>{const i=this._filterConfigEntries(e,t),r=[],n=[];for(let e=i.length-1;e>=0;e--)"ignore"===i[e].source?r.push(i.splice(e,1)[0]):null!==i[e].disabled_by&&n.push(i.splice(e,1)[0]);return[Fe(i),r,Fe(n),n.length]}))}},{kind:"field",key:"_filterConfigEntriesInProgress",value:()=>(0,a.Z)(((e,t)=>{if(!t)return e;return new r.Z(e,{keys:["handler","localized_title"],isCaseSensitive:!1,minMatchCharLength:2,threshold:.2}).search(t).map((e=>e.item))}))},{kind:"method",key:"firstUpdated",value:function(e){Se(Te(i.prototype),"firstUpdated",this).call(this,e),this._loadConfigEntries();const t=this.hass.loadBackendTranslation("title",void 0,!0);this._fetchManifests(),"/add"===this.route.path&&this._handleAdd(t),this._scanUSBDevices(),(0,f.p)(this.hass,"diagnostics")&&(0,le.pD)(this.hass).then((e=>{const t={};for(const i of e)t[i.domain]=i.handlers.config_entry;this._diagnosticHandlers=t}))}},{kind:"method",key:"updated",value:function(e){Se(Te(i.prototype),"updated",this).call(this,e),this._searchParms.has("config_entry")&&e.has("_configEntries")&&!e.get("_configEntries")&&this._configEntries&&this._highlightEntry()}},{kind:"method",key:"render",value:function(){if(!this._configEntries)return n.dy`<hass-loading-screen
        .hass=${this.hass}
        .narrow=${this.narrow}
      ></hass-loading-screen>`;const[e,t,i,r]=this._filterGroupConfigEntries(this._configEntries,this._filter),o=this._filterConfigEntriesInProgress(this._configEntriesInProgress,this._filter),a=n.dy`<ha-button-menu
      corner="BOTTOM_START"
      multi
      slot=${(0,s.o)(this.narrow?"toolbar-icon":void 0)}
      @action=${this._handleMenuAction}
    >
      <ha-icon-button
        slot="trigger"
        .label=${this.hass.localize("ui.common.menu")}
        .path=${"M6,13H18V11H6M3,6V8H21V6M10,18H14V16H10V18Z"}
      >
      </ha-icon-button>
      <mwc-list-item graphic="control" .selected=${this._showIgnored}>
        <ha-checkbox slot="graphic" .checked=${this._showIgnored}></ha-checkbox>
        ${this.hass.localize("ui.panel.config.integrations.ignore.show_ignored")}
      </mwc-list-item>
      <mwc-list-item graphic="control" .selected=${this._showDisabled}>
        <ha-checkbox
          slot="graphic"
          .checked=${this._showDisabled}
        ></ha-checkbox>
        ${this.hass.localize("ui.panel.config.integrations.disable.show_disabled")}
      </mwc-list-item>
    </ha-button-menu>`;return n.dy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        back-path="/config"
        .route=${this.route}
        .tabs=${_.configSections.devices}
      >
        ${this.narrow?n.dy`
              <div slot="header">
                <search-input
                  .hass=${this.hass}
                  .filter=${this._filter}
                  class="header"
                  no-label-float
                  no-underline
                  @value-changed=${this._handleSearchChange}
                  .label=${this.hass.localize("ui.panel.config.integrations.search")}
                ></search-input>
              </div>
              ${a}
            `:n.dy`
              <div class="search">
                <search-input
                  .hass=${this.hass}
                  no-label-float
                  no-underline
                  .filter=${this._filter}
                  @value-changed=${this._handleSearchChange}
                  .label=${this.hass.localize("ui.panel.config.integrations.search")}
                ></search-input>
                ${!this._showDisabled&&r?n.dy`<div class="active-filters">
                      ${this.hass.localize("ui.panel.config.integrations.disable.disabled_integrations",{number:r})}
                      <mwc-button
                        @click=${this._toggleShowDisabled}
                        .label=${this.hass.localize("ui.panel.config.integrations.disable.show")}
                      ></mwc-button>
                    </div>`:""}
                ${a}
              </div>
            `}

        <div
          class="container"
          @entry-removed=${this._handleEntryRemoved}
          @entry-updated=${this._handleEntryUpdated}
        >
          ${this._showIgnored?t.map((e=>n.dy`
                  <ha-ignored-config-entry-card
                    .hass=${this.hass}
                    .manifest=${this._manifests[e.domain]}
                    .entry=${e}
                    @change=${this._handleFlowUpdated}
                  ></ha-ignored-config-entry-card>
                `)):""}
          ${o.length?o.map((e=>n.dy`
                  <ha-config-flow-card
                    .hass=${this.hass}
                    .manifest=${this._manifests[e.handler]}
                    .flow=${e}
                    @change=${this._handleFlowUpdated}
                  ></ha-config-flow-card>
                `)):""}
          ${this._showDisabled?Array.from(i.entries()).map((([e,t])=>n.dy`<ha-integration-card
                    data-domain=${e}
                    disabled
                    .hass=${this.hass}
                    .domain=${e}
                    .items=${t}
                    .manifest=${this._manifests[e]}
                    .entityRegistryEntries=${this._entityRegistryEntries}
                    .deviceRegistryEntries=${this._deviceRegistryEntries}
                  ></ha-integration-card> `)):""}
          ${e.size?Array.from(e.entries()).map((([e,t])=>n.dy`<ha-integration-card
                    data-domain=${e}
                    .hass=${this.hass}
                    .domain=${e}
                    .items=${t}
                    .manifest=${this._manifests[e]}
                    .entityRegistryEntries=${this._entityRegistryEntries}
                    .deviceRegistryEntries=${this._deviceRegistryEntries}
                    .supportsDiagnostics=${!!this._diagnosticHandlers&&this._diagnosticHandlers[e]}
                  ></ha-integration-card>`)):this._filter&&!o.length&&!e.size&&this._configEntries.length?n.dy`
                <div class="empty-message">
                  <h1>
                    ${this.hass.localize("ui.panel.config.integrations.none_found")}
                  </h1>
                  <p>
                    ${this.hass.localize("ui.panel.config.integrations.none_found_detail")}
                  </p>
                  <mwc-button
                    @click=${this._createFlow}
                    unelevated
                    .label=${this.hass.localize("ui.panel.config.integrations.add_integration")}
                  ></mwc-button>
                </div>
              `:this._filter||this._showIgnored&&0!==t.length||this._showDisabled&&0!==i.size||0!==e.size?"":n.dy`
                <div class="empty-message">
                  <h1>
                    ${this.hass.localize("ui.panel.config.integrations.none")}
                  </h1>
                  <p>
                    ${this.hass.localize("ui.panel.config.integrations.no_integrations")}
                  </p>
                  <mwc-button
                    @click=${this._createFlow}
                    unelevated
                    .label=${this.hass.localize("ui.panel.config.integrations.add_integration")}
                  ></mwc-button>
                </div>
              `}
        </div>
        <ha-fab
          slot="fab"
          .label=${this.hass.localize("ui.panel.config.integrations.add_integration")}
          extended
          @click=${this._createFlow}
        >
          <ha-svg-icon slot="icon" .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
        </ha-fab>
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_loadConfigEntries",value:function(){(0,p.pB)(this.hass).then((e=>{this._configEntries=e.map((e=>({...e,localized_domain_name:(0,g.Lh)(this.hass.localize,e.domain)}))).sort(((e,t)=>(0,c.f)(e.localized_domain_name+e.title,t.localized_domain_name+t.title)))}))}},{kind:"method",key:"_scanUSBDevices",value:async function(){var e;(0,f.p)(this.hass,"usb")&&await(e=this.hass,e.callWS({type:"usb/scan"}))}},{kind:"method",key:"_fetchManifests",value:async function(){const e=await(0,g.F3)(this.hass),t={...this._manifests};for(const i of e)t[i.domain]=i;this._manifests=t}},{kind:"method",key:"_fetchManifest",value:async function(e){if(e in this._manifests)return;if(this._extraFetchedManifests){if(this._extraFetchedManifests.has(e))return}else this._extraFetchedManifests=new Set;this._extraFetchedManifests.add(e);const t=await(0,g.t4)(this.hass,e);this._manifests={...this._manifests,[e]:t}}},{kind:"method",key:"_handleEntryRemoved",value:function(e){this._configEntries=this._configEntries.filter((t=>t.entry_id!==e.detail.entryId))}},{kind:"method",key:"_handleEntryUpdated",value:function(e){const t=e.detail.entry;this._configEntries=this._configEntries.map((e=>e.entry_id===t.entry_id?{...t,localized_domain_name:e.localized_domain_name}:e))}},{kind:"method",key:"_handleFlowUpdated",value:function(){this._loadConfigEntries(),(0,u.ZJ)(this.hass.connection).refresh(),this._fetchManifests()}},{kind:"method",key:"_createFlow",value:function(){(0,v.t)(this,{searchQuery:this._filter,dialogClosedCallback:()=>{this._handleFlowUpdated()},showAdvanced:this.showAdvanced}),this.hass.loadBackendTranslation("title",void 0,!0)}},{kind:"method",key:"_handleMenuAction",value:function(e){switch(e.detail.index){case 0:this._showIgnored=!this._showIgnored;break;case 1:this._toggleShowDisabled()}}},{kind:"method",key:"_toggleShowDisabled",value:function(){this._showDisabled=!this._showDisabled}},{kind:"method",key:"_handleSearchChange",value:function(e){this._filter=e.detail.value}},{kind:"method",key:"_highlightEntry",value:async function(){await(0,h.y)();const e=this._searchParms.get("config_entry"),t=this._configEntries.find((t=>t.entry_id===e));if(!t)return;const i=this.shadowRoot.querySelector(`[data-domain=${null==t?void 0:t.domain}]`);i&&(i.scrollIntoView({block:"center"}),i.classList.add("highlight"),i.selectedConfigEntryId=e)}},{kind:"method",key:"_handleAdd",value:async function(e){var t;const i=(0,d.io)("domain");if((0,l.c)("/config/integrations",{replace:!0}),!i)return;const r=await e;await(0,b.g7)(this,{title:r("ui.panel.config.integrations.confirm_new",{integration:(0,g.Lh)(r,i)})})&&(0,v.t)(this,{dialogClosedCallback:()=>{this._handleFlowUpdated()},startFlowHandler:i,showAdvanced:null===(t=this.hass.userData)||void 0===t?void 0:t.showAdvanced})}},{kind:"get",static:!0,key:"styles",value:function(){return[k.Qx,n.iv`
        ha-button-menu {
          margin: 0 -8px 0 8px;
        }
        .container {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          grid-gap: 16px 16px;
          padding: 8px 16px 16px;
          margin-bottom: 64px;
        }
        .container > * {
          max-width: 500px;
        }

        .empty-message {
          margin: auto;
          text-align: center;
        }
        .empty-message h1 {
          margin-bottom: 0;
        }

        search-input.header {
          display: block;
          position: relative;
          left: -8px;
          color: var(--secondary-text-color);
          margin-left: 16px;
        }
        .search {
          display: flex;
          align-items: center;
          padding: 0 16px;
          background: var(--sidebar-background-color);
          border-bottom: 1px solid var(--divider-color);
        }
        .search search-input {
          flex: 1;
          position: relative;
          top: 2px;
        }

        .active-filters {
          color: var(--primary-text-color);
          position: relative;
          display: flex;
          align-items: center;
          padding: 2px 2px 2px 8px;
          margin-left: 4px;
          font-size: 14px;
        }
        .active-filters mwc-button {
          margin-left: 8px;
        }
        .active-filters::before {
          background-color: var(--primary-color);
          opacity: 0.12;
          border-radius: 4px;
          position: absolute;
          top: 0;
          right: 0;
          bottom: 0;
          left: 0;
          content: "";
        }
      `]}}]}}),(0,w.f)(n.oi))}}]);
//# sourceMappingURL=679ae7e2.js.map