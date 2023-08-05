/*! For license information please see c9a53031.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[75009],{71780:function(t,e,i){i.d(e,{L:function(){return s}});i(94604);var n=i(87156),o=void 0,s={properties:{sizingTarget:{type:Object,value:function(){return this}},fitInto:{type:Object,value:window},noOverlap:{type:Boolean},positionTarget:{type:Element},horizontalAlign:{type:String},verticalAlign:{type:String},dynamicAlign:{type:Boolean},horizontalOffset:{type:Number,value:0,notify:!0},verticalOffset:{type:Number,value:0,notify:!0},autoFitOnAttach:{type:Boolean,value:!1},expandSizingTargetForScrollbars:{type:Boolean,value:!1},_fitInfo:{type:Object}},get _fitWidth(){return this.fitInto===window?this.fitInto.innerWidth:this.fitInto.getBoundingClientRect().width},get _fitHeight(){return this.fitInto===window?this.fitInto.innerHeight:this.fitInto.getBoundingClientRect().height},get _fitLeft(){return this.fitInto===window?0:this.fitInto.getBoundingClientRect().left},get _fitTop(){return this.fitInto===window?0:this.fitInto.getBoundingClientRect().top},get _defaultPositionTarget(){var t=(0,n.vz)(this).parentNode;return t&&t.nodeType===Node.DOCUMENT_FRAGMENT_NODE&&(t=t.host),t},get _localeHorizontalAlign(){if(this._isRTL){if("right"===this.horizontalAlign)return"left";if("left"===this.horizontalAlign)return"right"}return this.horizontalAlign},get __shouldPosition(){return(this.horizontalAlign||this.verticalAlign)&&this.positionTarget},get _isRTL(){return void 0===this._memoizedIsRTL&&(this._memoizedIsRTL="rtl"==window.getComputedStyle(this).direction),this._memoizedIsRTL},attached:function(){this.positionTarget=this.positionTarget||this._defaultPositionTarget,this.autoFitOnAttach&&("none"===window.getComputedStyle(this).display?setTimeout(function(){this.fit()}.bind(this)):(window.ShadyDOM&&ShadyDOM.flush(),this.fit()))},detached:function(){this.__deferredFit&&(clearTimeout(this.__deferredFit),this.__deferredFit=null)},fit:function(){this.position(),this.constrain(),this.center()},_discoverInfo:function(){if(!this._fitInfo){var t=window.getComputedStyle(this),e=window.getComputedStyle(this.sizingTarget);this._fitInfo={inlineStyle:{top:this.style.top||"",left:this.style.left||"",position:this.style.position||""},sizerInlineStyle:{maxWidth:this.sizingTarget.style.maxWidth||"",maxHeight:this.sizingTarget.style.maxHeight||"",boxSizing:this.sizingTarget.style.boxSizing||""},positionedBy:{vertically:"auto"!==t.top?"top":"auto"!==t.bottom?"bottom":null,horizontally:"auto"!==t.left?"left":"auto"!==t.right?"right":null},sizedBy:{height:"none"!==e.maxHeight,width:"none"!==e.maxWidth,minWidth:parseInt(e.minWidth,10)||0,minHeight:parseInt(e.minHeight,10)||0},margin:{top:parseInt(t.marginTop,10)||0,right:parseInt(t.marginRight,10)||0,bottom:parseInt(t.marginBottom,10)||0,left:parseInt(t.marginLeft,10)||0}}}},resetFit:function(){var t=this._fitInfo||{};for(var e in t.sizerInlineStyle)this.sizingTarget.style[e]=t.sizerInlineStyle[e];for(var e in t.inlineStyle)this.style[e]=t.inlineStyle[e];this._fitInfo=null},refit:function(){var t=this.sizingTarget.scrollLeft,e=this.sizingTarget.scrollTop;this.resetFit(),this.fit(),this.sizingTarget.scrollLeft=t,this.sizingTarget.scrollTop=e},position:function(){if(this.__shouldPosition){this._discoverInfo(),window.ShadyDOM&&window.ShadyDOM.flush(),this.style.position="fixed",this.sizingTarget.style.boxSizing="border-box",this.style.left="0px",this.style.top="0px";var t,e,i,n,s=this.getBoundingClientRect(),r=this.__getNormalizedRect(this.positionTarget),a=this.__getNormalizedRect(this.fitInto);this.expandSizingTargetForScrollbars&&(t=this.sizingTarget.offsetWidth,e=this.sizingTarget.offsetHeight,i=this.sizingTarget.clientWidth,n=this.sizingTarget.clientHeight);var l=this._fitInfo.margin,h={width:s.width+l.left+l.right,height:s.height+l.top+l.bottom},c=this.__getPosition(this._localeHorizontalAlign,this.verticalAlign,h,s,r,a),d=c.left+l.left,f=c.top+l.top,u=Math.min(a.right-l.right,d+s.width),p=Math.min(a.bottom-l.bottom,f+s.height);d=Math.max(a.left+l.left,Math.min(d,u-this._fitInfo.sizedBy.minWidth)),f=Math.max(a.top+l.top,Math.min(f,p-this._fitInfo.sizedBy.minHeight));var _=Math.max(u-d,this._fitInfo.sizedBy.minWidth),g=Math.max(p-f,this._fitInfo.sizedBy.minHeight);this.sizingTarget.style.maxWidth=_+"px",this.sizingTarget.style.maxHeight=g+"px";var v=d-s.left,y=f-s.top;if(this.style.left="".concat(v,"px"),this.style.top="".concat(y,"px"),this.expandSizingTargetForScrollbars){var m=this.sizingTarget.offsetHeight,b=m-this.sizingTarget.clientHeight-(e-n);if(b>0){var z=a.height-l.top-l.bottom,T=Math.min(z,g+b);this.sizingTarget.style.maxHeight="".concat(T,"px");var w,O=this.sizingTarget.offsetHeight,k=O-m;"top"===c.verticalAlign?w=y:"middle"===c.verticalAlign?w=y-k/2:"bottom"===c.verticalAlign&&(w=y-k),w=Math.max(a.top+l.top,Math.min(w,a.bottom-l.bottom-O)),this.style.top="".concat(w,"px")}var x=this.sizingTarget.offsetWidth,A=x-this.sizingTarget.clientWidth-(t-i);if(A>0){var C=function(){if(void 0!==o)return o;var t=document.createElement("div");Object.assign(t.style,{overflow:"auto",position:"fixed",left:"0px",top:"0px",maxWidth:"100px",maxHeight:"100px"});var e=document.createElement("div");return e.style.width="200px",e.style.height="200px",t.appendChild(e),document.body.appendChild(t),o=Math.abs(t.offsetWidth-100)>1?t.offsetWidth-t.clientWidth:0,document.body.removeChild(t),o}(),N=a.width-l.left-l.right,E=Math.min(N,_+A-C);this.sizingTarget.style.maxWidth="".concat(E,"px");var I,B=this.sizingTarget.offsetWidth+C,S=B-x;"left"===c.horizontalAlign?I=v:"center"===c.horizontalAlign?I=v-S/2:"right"===c.horizontalAlign&&(I=v-S),I=Math.max(a.left+l.left,Math.min(I,a.right-l.right-B)),this.style.left="".concat(I,"px")}}}},constrain:function(){if(!this.__shouldPosition){this._discoverInfo();var t=this._fitInfo;t.positionedBy.vertically||(this.style.position="fixed",this.style.top="0px"),t.positionedBy.horizontally||(this.style.position="fixed",this.style.left="0px"),this.sizingTarget.style.boxSizing="border-box";var e=this.getBoundingClientRect();t.sizedBy.height||this.__sizeDimension(e,t.positionedBy.vertically,"top","bottom","Height"),t.sizedBy.width||this.__sizeDimension(e,t.positionedBy.horizontally,"left","right","Width")}},_sizeDimension:function(t,e,i,n,o){this.__sizeDimension(t,e,i,n,o)},__sizeDimension:function(t,e,i,n,o){var s=this._fitInfo,r=this.__getNormalizedRect(this.fitInto),a="Width"===o?r.width:r.height,l=e===n,h=l?a-t[n]:t[i],c=s.margin[l?i:n],d="offset"+o,f=this[d]-this.sizingTarget[d];this.sizingTarget.style["max"+o]=a-c-h-f+"px"},center:function(){if(!this.__shouldPosition){this._discoverInfo();var t=this._fitInfo.positionedBy;if(!t.vertically||!t.horizontally){this.style.position="fixed",t.vertically||(this.style.top="0px"),t.horizontally||(this.style.left="0px");var e=this.getBoundingClientRect(),i=this.__getNormalizedRect(this.fitInto);if(!t.vertically){var n=i.top-e.top+(i.height-e.height)/2;this.style.top=n+"px"}if(!t.horizontally){var o=i.left-e.left+(i.width-e.width)/2;this.style.left=o+"px"}}}},__getNormalizedRect:function(t){return t===document.documentElement||t===window?{top:0,left:0,width:window.innerWidth,height:window.innerHeight,right:window.innerWidth,bottom:window.innerHeight}:t.getBoundingClientRect()},__getOffscreenArea:function(t,e,i){var n=Math.min(0,t.top)+Math.min(0,i.bottom-(t.top+e.height)),o=Math.min(0,t.left)+Math.min(0,i.right-(t.left+e.width));return Math.abs(n)*e.width+Math.abs(o)*e.height},__getPosition:function(t,e,i,n,o,s){var r,a=[{verticalAlign:"top",horizontalAlign:"left",top:o.top+this.verticalOffset,left:o.left+this.horizontalOffset},{verticalAlign:"top",horizontalAlign:"right",top:o.top+this.verticalOffset,left:o.right-i.width-this.horizontalOffset},{verticalAlign:"bottom",horizontalAlign:"left",top:o.bottom-i.height-this.verticalOffset,left:o.left+this.horizontalOffset},{verticalAlign:"bottom",horizontalAlign:"right",top:o.bottom-i.height-this.verticalOffset,left:o.right-i.width-this.horizontalOffset}];if(this.noOverlap){for(var l=0,h=a.length;l<h;l++){var c={};for(var d in a[l])c[d]=a[l][d];a.push(c)}a[0].top=a[1].top+=o.height,a[2].top=a[3].top-=o.height,a[4].left=a[6].left+=o.width,a[5].left=a[7].left-=o.width}e="auto"===e?null:e,(t="auto"===t?null:t)&&"center"!==t||(a.push({verticalAlign:"top",horizontalAlign:"center",top:o.top+this.verticalOffset+(this.noOverlap?o.height:0),left:o.left-n.width/2+o.width/2+this.horizontalOffset}),a.push({verticalAlign:"bottom",horizontalAlign:"center",top:o.bottom-i.height-this.verticalOffset-(this.noOverlap?o.height:0),left:o.left-n.width/2+o.width/2+this.horizontalOffset})),e&&"middle"!==e||(a.push({verticalAlign:"middle",horizontalAlign:"left",top:o.top-n.height/2+o.height/2+this.verticalOffset,left:o.left+this.horizontalOffset+(this.noOverlap?o.width:0)}),a.push({verticalAlign:"middle",horizontalAlign:"right",top:o.top-n.height/2+o.height/2+this.verticalOffset,left:o.right-i.width-this.horizontalOffset-(this.noOverlap?o.width:0)})),"middle"===e&&"center"===t&&a.push({verticalAlign:"middle",horizontalAlign:"center",top:o.top-n.height/2+o.height/2+this.verticalOffset,left:o.left-n.width/2+o.width/2+this.horizontalOffset});for(l=0;l<a.length;l++){var f=a[l],u=f.verticalAlign===e,p=f.horizontalAlign===t;if(!this.dynamicAlign&&!this.noOverlap&&u&&p){r=f;break}var _=(!e||u)&&(!t||p);if(this.dynamicAlign||_){if(f.offscreenArea=this.__getOffscreenArea(f,i,s),0===f.offscreenArea&&_){r=f;break}r=r||f;var g=f.offscreenArea-r.offscreenArea;(g<0||0===g&&(u||p))&&(r=f)}}return r}}},93592:function(t,e,i){i.d(e,{H:function(){return a}});i(94604);var n=i(87156);function o(t,e){for(var i=0;i<e.length;i++){var n=e[i];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}var s=Element.prototype,r=s.matches||s.matchesSelector||s.mozMatchesSelector||s.msMatchesSelector||s.oMatchesSelector||s.webkitMatchesSelector,a=new(function(){function t(){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t)}var e,i,s;return e=t,(i=[{key:"getTabbableNodes",value:function(t){var e=[];return this._collectTabbableNodes(t,e)?this._sortByTabIndex(e):e}},{key:"isFocusable",value:function(t){return r.call(t,"input, select, textarea, button, object")?r.call(t,":not([disabled])"):r.call(t,"a[href], area[href], iframe, [tabindex], [contentEditable]")}},{key:"isTabbable",value:function(t){return this.isFocusable(t)&&r.call(t,':not([tabindex="-1"])')&&this._isVisible(t)}},{key:"_normalizedTabIndex",value:function(t){if(this.isFocusable(t)){var e=t.getAttribute("tabindex")||0;return Number(e)}return-1}},{key:"_collectTabbableNodes",value:function(t,e){if(t.nodeType!==Node.ELEMENT_NODE)return!1;var i=t;if(!this._isVisible(i))return!1;var o,s=this._normalizedTabIndex(i),r=s>0;s>=0&&e.push(i),o="content"===i.localName||"slot"===i.localName?(0,n.vz)(i).getDistributedNodes():(0,n.vz)(i.root||i).children;for(var a=0;a<o.length;a++)r=this._collectTabbableNodes(o[a],e)||r;return r}},{key:"_isVisible",value:function(t){var e=t.style;return"hidden"!==e.visibility&&"none"!==e.display&&"hidden"!==(e=window.getComputedStyle(t)).visibility&&"none"!==e.display}},{key:"_sortByTabIndex",value:function(t){var e=t.length;if(e<2)return t;var i=Math.ceil(e/2),n=this._sortByTabIndex(t.slice(0,i)),o=this._sortByTabIndex(t.slice(i));return this._mergeSortByTabIndex(n,o)}},{key:"_mergeSortByTabIndex",value:function(t,e){for(var i=[];t.length>0&&e.length>0;)this._hasLowerTabOrder(t[0],e[0])?i.push(e.shift()):i.push(t.shift());return i.concat(t,e)}},{key:"_hasLowerTabOrder",value:function(t,e){var i=Math.max(t.tabIndex,0),n=Math.max(e.tabIndex,0);return 0===i||0===n?n>i:i>n}}])&&o(e.prototype,i),s&&o(e,s),t}())},24101:function(t,e,i){i(94604);var n,o,s,r=i(9672),a=i(87156),l=i(50856);(0,r.k)({_template:(0,l.d)(n||(o=["\n    <style>\n      :host {\n        position: fixed;\n        top: 0;\n        left: 0;\n        width: 100%;\n        height: 100%;\n        background-color: var(--iron-overlay-backdrop-background-color, #000);\n        opacity: 0;\n        transition: opacity 0.2s;\n        pointer-events: none;\n        @apply --iron-overlay-backdrop;\n      }\n\n      :host(.opened) {\n        opacity: var(--iron-overlay-backdrop-opacity, 0.6);\n        pointer-events: auto;\n        @apply --iron-overlay-backdrop-opened;\n      }\n    </style>\n\n    <slot></slot>\n"],s||(s=o.slice(0)),n=Object.freeze(Object.defineProperties(o,{raw:{value:Object.freeze(s)}})))),is:"iron-overlay-backdrop",properties:{opened:{reflectToAttribute:!0,type:Boolean,value:!1,observer:"_openedChanged"}},listeners:{transitionend:"_onTransitionend"},created:function(){this.__openedRaf=null},attached:function(){this.opened&&this._openedChanged(this.opened)},prepare:function(){this.opened&&!this.parentNode&&(0,a.vz)(document.body).appendChild(this)},open:function(){this.opened=!0},close:function(){this.opened=!1},complete:function(){this.opened||this.parentNode!==document.body||(0,a.vz)(this.parentNode).removeChild(this)},_onTransitionend:function(t){t&&t.target===this&&this.complete()},_openedChanged:function(t){if(t)this.prepare();else{var e=window.getComputedStyle(this);"0s"!==e.transitionDuration&&0!=e.opacity||this.complete()}this.isAttached&&(this.__openedRaf&&(window.cancelAnimationFrame(this.__openedRaf),this.__openedRaf=null),this.scrollTop=this.scrollTop,this.__openedRaf=window.requestAnimationFrame(function(){this.__openedRaf=null,this.toggleClass("opened",this.opened)}.bind(this)))}})},75009:function(t,e,i){i.d(e,{Q:function(){return c},$:function(){return f}});i(94604);var n=i(71780),o=i(72986),s=i(87156),r=i(74460),a=i(93592),l=i(105),h=i(63550),c={properties:{opened:{observer:"_openedChanged",type:Boolean,value:!1,notify:!0},canceled:{observer:"_canceledChanged",readOnly:!0,type:Boolean,value:!1},withBackdrop:{observer:"_withBackdropChanged",type:Boolean},noAutoFocus:{type:Boolean,value:!1},noCancelOnEscKey:{type:Boolean,value:!1},noCancelOnOutsideClick:{type:Boolean,value:!1},closingReason:{type:Object},restoreFocusOnClose:{type:Boolean,value:!1},allowClickThrough:{type:Boolean},alwaysOnTop:{type:Boolean},scrollAction:{type:String},_manager:{type:Object,value:l.E},_focusedChild:{type:Object}},listeners:{"iron-resize":"_onIronResize"},observers:["__updateScrollObservers(isAttached, opened, scrollAction)"],get backdropElement(){return this._manager.backdropElement},get _focusNode(){return this._focusedChild||(0,s.vz)(this).querySelector("[autofocus]")||this},get _focusableNodes(){return a.H.getTabbableNodes(this)},ready:function(){this.__isAnimating=!1,this.__shouldRemoveTabIndex=!1,this.__firstFocusableNode=this.__lastFocusableNode=null,this.__rafs={},this.__restoreFocusNode=null,this.__scrollTop=this.__scrollLeft=null,this.__onCaptureScroll=this.__onCaptureScroll.bind(this),this.__rootNodes=null,this._ensureSetup()},attached:function(){this.opened&&this._openedChanged(this.opened),this._observer=(0,s.vz)(this).observeNodes(this._onNodesChange)},detached:function(){for(var t in this._observer&&(0,s.vz)(this).unobserveNodes(this._observer),this._observer=null,this.__rafs)null!==this.__rafs[t]&&cancelAnimationFrame(this.__rafs[t]);this.__rafs={},this._manager.removeOverlay(this),this.__isAnimating&&(this.opened?this._finishRenderOpened():(this._applyFocus(),this._finishRenderClosed()))},toggle:function(){this._setCanceled(!1),this.opened=!this.opened},open:function(){this._setCanceled(!1),this.opened=!0},close:function(){this._setCanceled(!1),this.opened=!1},cancel:function(t){this.fire("iron-overlay-canceled",t,{cancelable:!0}).defaultPrevented||(this._setCanceled(!0),this.opened=!1)},invalidateTabbables:function(){this.__firstFocusableNode=this.__lastFocusableNode=null},_ensureSetup:function(){this._overlaySetup||(this._overlaySetup=!0,this.style.outline="none",this.style.display="none")},_openedChanged:function(t){t?this.removeAttribute("aria-hidden"):this.setAttribute("aria-hidden","true"),this.isAttached&&(this.__isAnimating=!0,this.__deraf("__openedChanged",this.__openedChanged))},_canceledChanged:function(){this.closingReason=this.closingReason||{},this.closingReason.canceled=this.canceled},_withBackdropChanged:function(){this.withBackdrop&&!this.hasAttribute("tabindex")?(this.setAttribute("tabindex","-1"),this.__shouldRemoveTabIndex=!0):this.__shouldRemoveTabIndex&&(this.removeAttribute("tabindex"),this.__shouldRemoveTabIndex=!1),this.opened&&this.isAttached&&this._manager.trackBackdrop()},_prepareRenderOpened:function(){this.__restoreFocusNode=this._manager.deepActiveElement,this._preparePositioning(),this.refit(),this._finishPositioning(),this.noAutoFocus&&document.activeElement===this._focusNode&&(this._focusNode.blur(),this.__restoreFocusNode.focus())},_renderOpened:function(){this._finishRenderOpened()},_renderClosed:function(){this._finishRenderClosed()},_finishRenderOpened:function(){this.notifyResize(),this.__isAnimating=!1,this.fire("iron-overlay-opened")},_finishRenderClosed:function(){this.style.display="none",this.style.zIndex="",this.notifyResize(),this.__isAnimating=!1,this.fire("iron-overlay-closed",this.closingReason)},_preparePositioning:function(){this.style.transition=this.style.webkitTransition="none",this.style.transform=this.style.webkitTransform="none",this.style.display=""},_finishPositioning:function(){this.style.display="none",this.scrollTop=this.scrollTop,this.style.transition=this.style.webkitTransition="",this.style.transform=this.style.webkitTransform="",this.style.display="",this.scrollTop=this.scrollTop},_applyFocus:function(){if(this.opened)this.noAutoFocus||this._focusNode.focus();else{if(this.restoreFocusOnClose&&this.__restoreFocusNode){var t=this._manager.deepActiveElement;(t===document.body||d(this,t))&&this.__restoreFocusNode.focus()}this.__restoreFocusNode=null,this._focusNode.blur(),this._focusedChild=null}},_onCaptureClick:function(t){this.noCancelOnOutsideClick||this.cancel(t)},_onCaptureFocus:function(t){if(this.withBackdrop){var e=(0,s.vz)(t).path;-1===e.indexOf(this)?(t.stopPropagation(),this._applyFocus()):this._focusedChild=e[0]}},_onCaptureEsc:function(t){this.noCancelOnEscKey||this.cancel(t)},_onCaptureTab:function(t){if(this.withBackdrop){this.__ensureFirstLastFocusables();var e=t.shiftKey,i=e?this.__firstFocusableNode:this.__lastFocusableNode,n=e?this.__lastFocusableNode:this.__firstFocusableNode,o=!1;if(i===n)o=!0;else{var s=this._manager.deepActiveElement;o=s===i||s===this}o&&(t.preventDefault(),this._focusedChild=n,this._applyFocus())}},_onIronResize:function(){this.opened&&!this.__isAnimating&&this.__deraf("refit",this.refit)},_onNodesChange:function(){this.opened&&!this.__isAnimating&&(this.invalidateTabbables(),this.notifyResize())},__ensureFirstLastFocusables:function(){var t=this._focusableNodes;this.__firstFocusableNode=t[0],this.__lastFocusableNode=t[t.length-1]},__openedChanged:function(){this.opened?(this._prepareRenderOpened(),this._manager.addOverlay(this),this._applyFocus(),this._renderOpened()):(this._manager.removeOverlay(this),this._applyFocus(),this._renderClosed())},__deraf:function(t,e){var i=this.__rafs;null!==i[t]&&cancelAnimationFrame(i[t]),i[t]=requestAnimationFrame(function(){i[t]=null,e.call(this)}.bind(this))},__updateScrollObservers:function(t,e,i){t&&e&&this.__isValidScrollAction(i)?("lock"===i&&(this.__saveScrollPosition(),(0,h.$A)(this)),this.__addScrollListeners()):((0,h.fm)(this),this.__removeScrollListeners())},__addScrollListeners:function(){if(!this.__rootNodes){if(this.__rootNodes=[],r.my)for(var t=this;t;)t.nodeType===Node.DOCUMENT_FRAGMENT_NODE&&t.host&&this.__rootNodes.push(t),t=t.host||t.assignedSlot||t.parentNode;this.__rootNodes.push(document)}this.__rootNodes.forEach((function(t){t.addEventListener("scroll",this.__onCaptureScroll,{capture:!0,passive:!0})}),this)},__removeScrollListeners:function(){this.__rootNodes&&this.__rootNodes.forEach((function(t){t.removeEventListener("scroll",this.__onCaptureScroll,{capture:!0,passive:!0})}),this),this.isAttached||(this.__rootNodes=null)},__isValidScrollAction:function(t){return"lock"===t||"refit"===t||"cancel"===t},__onCaptureScroll:function(t){if(!(this.__isAnimating||(0,s.vz)(t).path.indexOf(this)>=0))switch(this.scrollAction){case"lock":this.__restoreScrollPosition();break;case"refit":this.__deraf("refit",this.refit);break;case"cancel":this.cancel(t)}},__saveScrollPosition:function(){document.scrollingElement?(this.__scrollTop=document.scrollingElement.scrollTop,this.__scrollLeft=document.scrollingElement.scrollLeft):(this.__scrollTop=Math.max(document.documentElement.scrollTop,document.body.scrollTop),this.__scrollLeft=Math.max(document.documentElement.scrollLeft,document.body.scrollLeft))},__restoreScrollPosition:function(){document.scrollingElement?(document.scrollingElement.scrollTop=this.__scrollTop,document.scrollingElement.scrollLeft=this.__scrollLeft):(document.documentElement.scrollTop=document.body.scrollTop=this.__scrollTop,document.documentElement.scrollLeft=document.body.scrollLeft=this.__scrollLeft)}},d=function(t,e){for(var i=e;i;i=(n=i).assignedSlot||n.parentNode||n.host)if(i===t)return!0;var n;return!1},f=[n.L,o.z,c]},105:function(t,e,i){i.d(e,{E:function(){return a}});i(94604),i(24101);var n=i(8621),o=i(87156),s=i(81668);function r(t,e){for(var i=0;i<e.length;i++){var n=e[i];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}var a=new(function(){function t(){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),this._overlays=[],this._minimumZ=101,this._backdropElement=null,s.NH(document.documentElement,"tap",(function(){})),document.addEventListener("tap",this._onCaptureClick.bind(this),!0),document.addEventListener("focus",this._onCaptureFocus.bind(this),!0),document.addEventListener("keydown",this._onCaptureKeyDown.bind(this),!0)}var e,i,a;return e=t,(i=[{key:"backdropElement",get:function(){return this._backdropElement||(this._backdropElement=document.createElement("iron-overlay-backdrop")),this._backdropElement}},{key:"deepActiveElement",get:function(){var t=document.activeElement;for(t&&t instanceof Element!=0||(t=document.body);t.root&&(0,o.vz)(t.root).activeElement;)t=(0,o.vz)(t.root).activeElement;return t}},{key:"_bringOverlayAtIndexToFront",value:function(t){var e=this._overlays[t];if(e){var i=this._overlays.length-1,n=this._overlays[i];if(n&&this._shouldBeBehindOverlay(e,n)&&i--,!(t>=i)){var o=Math.max(this.currentOverlayZ(),this._minimumZ);for(this._getZ(e)<=o&&this._applyOverlayZ(e,o);t<i;)this._overlays[t]=this._overlays[t+1],t++;this._overlays[i]=e}}}},{key:"addOrRemoveOverlay",value:function(t){t.opened?this.addOverlay(t):this.removeOverlay(t)}},{key:"addOverlay",value:function(t){var e=this._overlays.indexOf(t);if(e>=0)return this._bringOverlayAtIndexToFront(e),void this.trackBackdrop();var i=this._overlays.length,n=this._overlays[i-1],o=Math.max(this._getZ(n),this._minimumZ),s=this._getZ(t);if(n&&this._shouldBeBehindOverlay(t,n)){this._applyOverlayZ(n,o),i--;var r=this._overlays[i-1];o=Math.max(this._getZ(r),this._minimumZ)}s<=o&&this._applyOverlayZ(t,o),this._overlays.splice(i,0,t),this.trackBackdrop()}},{key:"removeOverlay",value:function(t){var e=this._overlays.indexOf(t);-1!==e&&(this._overlays.splice(e,1),this.trackBackdrop())}},{key:"currentOverlay",value:function(){var t=this._overlays.length-1;return this._overlays[t]}},{key:"currentOverlayZ",value:function(){return this._getZ(this.currentOverlay())}},{key:"ensureMinimumZ",value:function(t){this._minimumZ=Math.max(this._minimumZ,t)}},{key:"focusOverlay",value:function(){var t=this.currentOverlay();t&&t._applyFocus()}},{key:"trackBackdrop",value:function(){var t=this._overlayWithBackdrop();(t||this._backdropElement)&&(this.backdropElement.style.zIndex=this._getZ(t)-1,this.backdropElement.opened=!!t,this.backdropElement.prepare())}},{key:"getBackdrops",value:function(){for(var t=[],e=0;e<this._overlays.length;e++)this._overlays[e].withBackdrop&&t.push(this._overlays[e]);return t}},{key:"backdropZ",value:function(){return this._getZ(this._overlayWithBackdrop())-1}},{key:"_overlayWithBackdrop",value:function(){for(var t=this._overlays.length-1;t>=0;t--)if(this._overlays[t].withBackdrop)return this._overlays[t]}},{key:"_getZ",value:function(t){var e=this._minimumZ;if(t){var i=Number(t.style.zIndex||window.getComputedStyle(t).zIndex);i==i&&(e=i)}return e}},{key:"_setZ",value:function(t,e){t.style.zIndex=e}},{key:"_applyOverlayZ",value:function(t,e){this._setZ(t,e+2)}},{key:"_overlayInPath",value:function(t){t=t||[];for(var e=0;e<t.length;e++)if(t[e]._manager===this)return t[e]}},{key:"_onCaptureClick",value:function(t){var e=this._overlays.length-1;if(-1!==e)for(var i,n=(0,o.vz)(t).path;(i=this._overlays[e])&&this._overlayInPath(n)!==i&&(i._onCaptureClick(t),i.allowClickThrough);)e--}},{key:"_onCaptureFocus",value:function(t){var e=this.currentOverlay();e&&e._onCaptureFocus(t)}},{key:"_onCaptureKeyDown",value:function(t){var e=this.currentOverlay();e&&(n.G.keyboardEventMatchesKeys(t,"esc")?e._onCaptureEsc(t):n.G.keyboardEventMatchesKeys(t,"tab")&&e._onCaptureTab(t))}},{key:"_shouldBeBehindOverlay",value:function(t,e){return!t.alwaysOnTop&&e.alwaysOnTop}}])&&r(e.prototype,i),a&&r(e,a),t}())},63550:function(t,e,i){i.d(e,{$A:function(){return c},fm:function(){return d}});i(94604);var n,o,s=i(87156),r={pageX:0,pageY:0},a=null,l=[],h=["wheel","mousewheel","DOMMouseScroll","touchstart","touchmove"];function c(t){f.indexOf(t)>=0||(0===f.length&&function(){n=n||u.bind(void 0);for(var t=0,e=h.length;t<e;t++)document.addEventListener(h[t],n,{capture:!0,passive:!1})}(),f.push(t),o=f[f.length-1],[],[])}function d(t){var e=f.indexOf(t);-1!==e&&(f.splice(e,1),o=f[f.length-1],[],[],0===f.length&&function(){for(var t=0,e=h.length;t<e;t++)document.removeEventListener(h[t],n,{capture:!0,passive:!1})}())}var f=[];function u(t){if(t.cancelable&&function(t){var e=(0,s.vz)(t).rootTarget;"touchmove"!==t.type&&a!==e&&(a=e,l=function(t){for(var e=[],i=t.indexOf(o),n=0;n<=i;n++)if(t[n].nodeType===Node.ELEMENT_NODE){var s=t[n],r=s.style;"scroll"!==r.overflow&&"auto"!==r.overflow&&(r=window.getComputedStyle(s)),"scroll"!==r.overflow&&"auto"!==r.overflow||e.push(s)}return e}((0,s.vz)(t).path));if(!l.length)return!0;if("touchstart"===t.type)return!1;var i=function(t){var e={deltaX:t.deltaX,deltaY:t.deltaY};if("deltaX"in t);else if("wheelDeltaX"in t&&"wheelDeltaY"in t)e.deltaX=-t.wheelDeltaX,e.deltaY=-t.wheelDeltaY;else if("wheelDelta"in t)e.deltaX=0,e.deltaY=-t.wheelDelta;else if("axis"in t)e.deltaX=1===t.axis?t.detail:0,e.deltaY=2===t.axis?t.detail:0;else if(t.targetTouches){var i=t.targetTouches[0];e.deltaX=r.pageX-i.pageX,e.deltaY=r.pageY-i.pageY}return e}(t);return!function(t,e,i){if(!e&&!i)return;for(var n=Math.abs(i)>=Math.abs(e),o=0;o<t.length;o++){var s=t[o];if(n?i<0?s.scrollTop>0:s.scrollTop<s.scrollHeight-s.clientHeight:e<0?s.scrollLeft>0:s.scrollLeft<s.scrollWidth-s.clientWidth)return s}}(l,i.deltaX,i.deltaY)}(t)&&t.preventDefault(),t.targetTouches){var e=t.targetTouches[0];r.pageX=e.pageX,r.pageY=e.pageY}}}}]);