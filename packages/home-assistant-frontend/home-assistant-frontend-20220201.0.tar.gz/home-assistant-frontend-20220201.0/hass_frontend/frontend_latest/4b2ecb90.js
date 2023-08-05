"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[28922],{66335:(e,t,r)=>{r.d(t,{H:()=>i});const i=5},58763:(e,t,r)=>{r.a(e,(async e=>{r.d(t,{vq:()=>c,_J:()=>d,Nu:()=>f,uR:()=>h,dL:()=>p,h_:()=>m,Cj:()=>y,hN:()=>v,Kj:()=>g,q6:()=>k,Nw:()=>w});var i=r(29171),n=r(22311),o=r(91741),s=e([i]);i=(s.then?await s:s)[0];const a=["climate","humidifier","water_heater"],l=["temperature","current_temperature","target_temp_low","target_temp_high","hvac_action","humidity","mode"],c=(e,t,r,i,n=!1,o,s=!0)=>{let a="history/period";return r&&(a+="/"+r.toISOString()),a+="?filter_entity_id="+t,i&&(a+="&end_time="+i.toISOString()),n&&(a+="&skip_initial_state"),void 0!==o&&(a+=`&significant_changes_only=${Number(o)}`),s&&(a+="&minimal_response"),e.callApi("GET",a)},d=(e,t,r,i)=>e.callApi("GET",`history/period/${t.toISOString()}?end_time=${r.toISOString()}&minimal_response${i?`&filter_entity_id=${i}`:""}`),u=(e,t)=>e.state===t.state&&(!e.attributes||!t.attributes||l.every((r=>e.attributes[r]===t.attributes[r]))),f=(e,t,r)=>{const s={},c=[];if(!t)return{line:[],timeline:[]};t.forEach((t=>{if(0===t.length)return;const a=t.find((e=>e.attributes&&("unit_of_measurement"in e.attributes||"state_class"in e.attributes)));let l;l=a?a.attributes.unit_of_measurement||" ":{climate:e.config.unit_system.temperature,counter:"#",humidifier:"%",input_number:"#",number:"#",water_heater:e.config.unit_system.temperature}[(0,n.N)(t[0])],l?l in s?s[l].push(t):s[l]=[t]:c.push(((e,t,r)=>{const n=[],s=r.length-1;for(const o of r)n.length>0&&o.state===n[n.length-1].state||(o.entity_id||(o.attributes=r[s].attributes,o.entity_id=r[s].entity_id),n.push({state_localize:(0,i.D)(e,o,t),state:o.state,last_changed:o.last_changed}));return{name:(0,o.C)(r[0]),entity_id:r[0].entity_id,data:n}})(r,e.locale,t))}));return{line:Object.keys(s).map((e=>((e,t)=>{const r=[];for(const e of t){const t=e[e.length-1],i=(0,n.N)(t),s=[];for(const t of e){let e;if(a.includes(i)){e={state:t.state,last_changed:t.last_updated,attributes:{}};for(const r of l)r in t.attributes&&(e.attributes[r]=t.attributes[r])}else e=t;s.length>1&&u(e,s[s.length-1])&&u(e,s[s.length-2])||s.push(e)}r.push({domain:i,name:(0,o.C)(t),entity_id:t.entity_id,states:s})}return{unit:e,identifier:t.map((e=>e[0].entity_id)).join(""),data:r}})(e,s[e]))),timeline:c}},h=(e,t)=>e.callWS({type:"history/list_statistic_ids",statistic_type:t}),p=(e,t,r,i,n="hour")=>e.callWS({type:"history/statistics_during_period",start_time:t.toISOString(),end_time:null==r?void 0:r.toISOString(),statistic_ids:i,period:n}),m=e=>e.callWS({type:"recorder/validate_statistics"}),y=(e,t,r)=>e.callWS({type:"recorder/update_statistics_metadata",statistic_id:t,unit_of_measurement:r}),v=(e,t)=>e.callWS({type:"recorder/clear_statistics",statistic_ids:t}),g=e=>{if(!e||e.length<2)return null;const t=e[e.length-1].sum;if(null===t)return null;const r=e[0].sum;return null===r?t:t-r},k=(e,t)=>{let r=null;for(const i of t){if(!(i in e))continue;const t=g(e[i]);null!==t&&(null===r?r=t:r+=t)}return r},w=(e,t)=>e.some((e=>null!==e[t]))}))},4309:(e,t,r)=>{r.d(t,{k:()=>s});var i=r(66335);const n=e=>e.reduce(((e,t)=>e+parseFloat(t.state)),0)/e.length,o=e=>parseFloat(e[e.length-1].state)||0,s=(e,t,r,s,a)=>{e.forEach((e=>{e.state=Number(e.state)})),e=e.filter((e=>!Number.isNaN(e.state)));const l=void 0!==(null==a?void 0:a.min)?a.min:Math.min(...e.map((e=>e.state))),c=void 0!==(null==a?void 0:a.max)?a.max:Math.max(...e.map((e=>e.state))),d=(new Date).getTime(),u=(e,r,i)=>{const n=d-new Date(r.last_changed).getTime();let o=Math.abs(n/36e5-t);return i?(o=60*(o-Math.floor(o)),o=Number((10*Math.round(o/10)).toString()[0])):o=Math.floor(o),e[o]||(e[o]=[]),e[o].push(r),e};if(e=e.reduce(((e,t)=>u(e,t,!1)),[]),s>1&&(e=e.map((e=>e.reduce(((e,t)=>u(e,t,!0)),[])))),e.length)return((e,t,r,s,a,l)=>{const c=[];let d=(l-a)/80;d=0!==d?d:80;let u=r/(t-(1===s?1:0));u=isFinite(u)?u:r;const f=e.filter(Boolean)[0];let h=[n(f),o(f)];const p=(e,t,r=0,s=1)=>{if(s>1&&e)return e.forEach(((e,r)=>p(e,t,r,s-1)));const l=u*(t+r/6);e&&(h=[n(e),o(e)]);const f=80+i.H/2-((e?h[0]:h[1])-a)/d;return c.push([l,f])};for(let t=0;t<e.length;t+=1)p(e[t],t,0,s);return 1===c.length&&(c[1]=[r,c[0][1]]),c.push([r,c[c.length-1][1]]),c})(e,t,r,s,l,c)}},47025:(e,t,r)=>{var i=r(37500),n=r(72367),o=r(66335);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=f(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:u(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=u(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function a(e){var t,r=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=s();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var u=t((function(e){n.initializeInstanceElements(e,f.elements)}),r),f=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(d(o.descriptor)||d(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}l(o,n)}else t.push(o)}return t}(u.d.map(a)),e);n.initializeClassElements(u.F,f.elements),n.runClassFinishers(u.F,f.finishers)}([(0,n.Mo)("hui-graph-base")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)()],key:"coordinates",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_path",value:void 0},{kind:"method",key:"render",value:function(){return i.dy`
      ${this._path?i.YP`<svg width="100%" height="100%" viewBox="0 0 500 100">
          <g>
            <mask id="fill">
              <path
                class='fill'
                fill='white'
                d="${this._path} L 500, 100 L 0, 100 z"
              />
            </mask>
            <rect height="100%" width="100%" id="fill-rect" fill="var(--accent-color)" mask="url(#fill)"></rect>
            <mask id="line">
              <path
                fill="none"
                stroke="var(--accent-color)"
                stroke-width="${o.H}"
                stroke-linecap="round"
                stroke-linejoin="round"
                d=${this._path}
              ></path>
            </mask>
            <rect height="100%" width="100%" id="rect" fill="var(--accent-color)" mask="url(#line)"></rect>
          </g>
        </svg>`:i.YP`<svg width="100%" height="100%" viewBox="0 0 500 100"></svg>`}
    `}},{kind:"method",key:"willUpdate",value:function(e){this.coordinates&&e.has("coordinates")&&(this._path=(e=>{if(!e.length)return"";let t,r,i="",n=e.filter(Boolean)[0];i+=`M ${n[0]},${n[1]}`;for(const c of e)t=c,o=n[0],s=n[1],a=t[0],l=t[1],r=[(o-a)/2+a,(s-l)/2+l],i+=` ${r[0]},${r[1]}`,i+=` Q${t[0]},${t[1]}`,n=t;var o,s,a,l;return i+=` ${t[0]},${t[1]}`,i})(this.coordinates))}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        display: flex;
        width: 100%;
      }
      .fill {
        opacity: 0.1;
      }
    `}}]}}),i.oi)},28922:(e,t,r)=>{r.a(e,(async e=>{r.r(t),r.d(t,{HuiGraphHeaderFooter:()=>w});var i=r(37500),n=r(72367),o=(r(31206),r(58763)),s=r(58831),a=r(15688),l=r(4309),c=r(53658),d=(r(47025),e([o]));function u(){u=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=v(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function f(e){var t,r=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}o=(d.then?await d:d)[0];const k=["counter","input_number","number","sensor"];let w=function(e,t,r,i){var n=u();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(m(o.descriptor)||m(n.descriptor)){if(p(o)||p(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(p(o)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}h(o,n)}else t.push(o)}return t}(s.d.map(f)),e);return n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("hui-graph-header-footer")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([r.e(75009),r.e(42955),r.e(88985),r.e(28055),r.e(69505),r.e(96715),r.e(74535),r.e(87071)]).then(r.bind(r,87071)),document.createElement("hui-graph-footer-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,r){return{type:"graph",entity:(0,a.j)(e,1,t,r,k,(e=>!isNaN(Number(e.state))&&!!e.attributes.unit_of_measurement))[0]||""}}},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"type",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_coordinates",value:void 0},{kind:"field",key:"_date",value:void 0},{kind:"field",key:"_stateHistory",value:void 0},{kind:"field",key:"_fetching",value:()=>!1},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){if(null==e||!e.entity||!k.includes((0,s.M)(e.entity)))throw new Error("Specify an entity from within the sensor domain");const t={detail:1,hours_to_show:24,...e};t.hours_to_show=Number(t.hours_to_show),t.detail=1===t.detail||2===t.detail?t.detail:1,this._config=t}},{kind:"method",key:"render",value:function(){return this._config&&this.hass?this._coordinates?this._coordinates.length?i.dy`
      <hui-graph-base .coordinates=${this._coordinates}></hui-graph-base>
    `:i.dy`
        <div class="container">
          <div class="info">No state history found.</div>
        </div>
      `:i.dy`
        <div class="container">
          <ha-circular-progress active size="small"></ha-circular-progress>
        </div>
      `:i.dy``}},{kind:"method",key:"shouldUpdate",value:function(e){return(0,c.G)(this,e)}},{kind:"method",key:"updated",value:function(e){if(this._config&&this.hass&&(!this._fetching||e.has("_config")))if(e.has("_config")){const t=e.get("_config");t&&t.entity===this._config.entity||(this._stateHistory=[]),this._getCoordinates()}else Date.now()-this._date.getTime()>=6e4&&this._getCoordinates()}},{kind:"method",key:"_getCoordinates",value:async function(){var e;this._fetching=!0;const t=new Date,r=this._date&&null!==(e=this._stateHistory)&&void 0!==e&&e.length?this._date:new Date((new Date).setHours(t.getHours()-this._config.hours_to_show));if(this._stateHistory.length){const e=[],r=[];this._stateHistory.forEach((i=>(t.getTime()-new Date(i.last_changed).getTime()<=36e5*this._config.hours_to_show?e:r).push(i))),r.length&&e.push(r[r.length-1]),this._stateHistory=e}const i=await(0,o.vq)(this.hass,this._config.entity,r,t,Boolean(this._stateHistory.length));i.length&&i[0].length&&this._stateHistory.push(...i[0]),this._coordinates=(0,l.k)(this._stateHistory,this._config.hours_to_show,500,this._config.detail,this._config.limits)||[],this._date=t,this._fetching=!1}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      ha-circular-progress {
        position: absolute;
        top: calc(50% - 14px);
      }
      .container {
        display: flex;
        justify-content: center;
        position: relative;
        padding-bottom: 20%;
      }
      .info {
        position: absolute;
        top: calc(50% - 16px);
        color: var(--secondary-text-color);
      }
    `}}]}}),i.oi)}))}}]);
//# sourceMappingURL=4b2ecb90.js.map