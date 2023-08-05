/*! For license information please see 1608b185.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[75009],{71780:(t,e,i)=>{i.d(e,{L:()=>n});i(94604);var o=i(87156);let s;const n={properties:{sizingTarget:{type:Object,value:function(){return this}},fitInto:{type:Object,value:window},noOverlap:{type:Boolean},positionTarget:{type:Element},horizontalAlign:{type:String},verticalAlign:{type:String},dynamicAlign:{type:Boolean},horizontalOffset:{type:Number,value:0,notify:!0},verticalOffset:{type:Number,value:0,notify:!0},autoFitOnAttach:{type:Boolean,value:!1},expandSizingTargetForScrollbars:{type:Boolean,value:!1},_fitInfo:{type:Object}},get _fitWidth(){return this.fitInto===window?this.fitInto.innerWidth:this.fitInto.getBoundingClientRect().width},get _fitHeight(){return this.fitInto===window?this.fitInto.innerHeight:this.fitInto.getBoundingClientRect().height},get _fitLeft(){return this.fitInto===window?0:this.fitInto.getBoundingClientRect().left},get _fitTop(){return this.fitInto===window?0:this.fitInto.getBoundingClientRect().top},get _defaultPositionTarget(){var t=(0,o.vz)(this).parentNode;return t&&t.nodeType===Node.DOCUMENT_FRAGMENT_NODE&&(t=t.host),t},get _localeHorizontalAlign(){if(this._isRTL){if("right"===this.horizontalAlign)return"left";if("left"===this.horizontalAlign)return"right"}return this.horizontalAlign},get __shouldPosition(){return(this.horizontalAlign||this.verticalAlign)&&this.positionTarget},get _isRTL(){return void 0===this._memoizedIsRTL&&(this._memoizedIsRTL="rtl"==window.getComputedStyle(this).direction),this._memoizedIsRTL},attached:function(){this.positionTarget=this.positionTarget||this._defaultPositionTarget,this.autoFitOnAttach&&("none"===window.getComputedStyle(this).display?setTimeout(function(){this.fit()}.bind(this)):(window.ShadyDOM&&ShadyDOM.flush(),this.fit()))},detached:function(){this.__deferredFit&&(clearTimeout(this.__deferredFit),this.__deferredFit=null)},fit:function(){this.position(),this.constrain(),this.center()},_discoverInfo:function(){if(!this._fitInfo){var t=window.getComputedStyle(this),e=window.getComputedStyle(this.sizingTarget);this._fitInfo={inlineStyle:{top:this.style.top||"",left:this.style.left||"",position:this.style.position||""},sizerInlineStyle:{maxWidth:this.sizingTarget.style.maxWidth||"",maxHeight:this.sizingTarget.style.maxHeight||"",boxSizing:this.sizingTarget.style.boxSizing||""},positionedBy:{vertically:"auto"!==t.top?"top":"auto"!==t.bottom?"bottom":null,horizontally:"auto"!==t.left?"left":"auto"!==t.right?"right":null},sizedBy:{height:"none"!==e.maxHeight,width:"none"!==e.maxWidth,minWidth:parseInt(e.minWidth,10)||0,minHeight:parseInt(e.minHeight,10)||0},margin:{top:parseInt(t.marginTop,10)||0,right:parseInt(t.marginRight,10)||0,bottom:parseInt(t.marginBottom,10)||0,left:parseInt(t.marginLeft,10)||0}}}},resetFit:function(){var t=this._fitInfo||{};for(var e in t.sizerInlineStyle)this.sizingTarget.style[e]=t.sizerInlineStyle[e];for(var e in t.inlineStyle)this.style[e]=t.inlineStyle[e];this._fitInfo=null},refit:function(){var t=this.sizingTarget.scrollLeft,e=this.sizingTarget.scrollTop;this.resetFit(),this.fit(),this.sizingTarget.scrollLeft=t,this.sizingTarget.scrollTop=e},position:function(){if(!this.__shouldPosition)return;this._discoverInfo(),window.ShadyDOM&&window.ShadyDOM.flush(),this.style.position="fixed",this.sizingTarget.style.boxSizing="border-box",this.style.left="0px",this.style.top="0px";var t=this.getBoundingClientRect(),e=this.__getNormalizedRect(this.positionTarget),i=this.__getNormalizedRect(this.fitInto);let o,n,r,l;this.expandSizingTargetForScrollbars&&(o=this.sizingTarget.offsetWidth,n=this.sizingTarget.offsetHeight,r=this.sizingTarget.clientWidth,l=this.sizingTarget.clientHeight);var a=this._fitInfo.margin,h={width:t.width+a.left+a.right,height:t.height+a.top+a.bottom},d=this.__getPosition(this._localeHorizontalAlign,this.verticalAlign,h,t,e,i),c=d.left+a.left,f=d.top+a.top,p=Math.min(i.right-a.right,c+t.width),u=Math.min(i.bottom-a.bottom,f+t.height);c=Math.max(i.left+a.left,Math.min(c,p-this._fitInfo.sizedBy.minWidth)),f=Math.max(i.top+a.top,Math.min(f,u-this._fitInfo.sizedBy.minHeight));const _=Math.max(p-c,this._fitInfo.sizedBy.minWidth),g=Math.max(u-f,this._fitInfo.sizedBy.minHeight);this.sizingTarget.style.maxWidth=_+"px",this.sizingTarget.style.maxHeight=g+"px";const v=c-t.left,m=f-t.top;if(this.style.left=`${v}px`,this.style.top=`${m}px`,this.expandSizingTargetForScrollbars){const t=this.sizingTarget.offsetHeight,e=t-this.sizingTarget.clientHeight-(n-l);if(e>0){const o=i.height-a.top-a.bottom,s=Math.min(o,g+e);this.sizingTarget.style.maxHeight=`${s}px`;const n=this.sizingTarget.offsetHeight,r=n-t;let l;"top"===d.verticalAlign?l=m:"middle"===d.verticalAlign?l=m-r/2:"bottom"===d.verticalAlign&&(l=m-r),l=Math.max(i.top+a.top,Math.min(l,i.bottom-a.bottom-n)),this.style.top=`${l}px`}const h=this.sizingTarget.offsetWidth,c=h-this.sizingTarget.clientWidth-(o-r);if(c>0){const t=(()=>{if(void 0!==s)return s;const t=document.createElement("div");Object.assign(t.style,{overflow:"auto",position:"fixed",left:"0px",top:"0px",maxWidth:"100px",maxHeight:"100px"});const e=document.createElement("div");return e.style.width="200px",e.style.height="200px",t.appendChild(e),document.body.appendChild(t),s=Math.abs(t.offsetWidth-100)>1?t.offsetWidth-t.clientWidth:0,document.body.removeChild(t),s})(),e=i.width-a.left-a.right,o=Math.min(e,_+c-t);this.sizingTarget.style.maxWidth=`${o}px`;const n=this.sizingTarget.offsetWidth+t,r=n-h;let l;"left"===d.horizontalAlign?l=v:"center"===d.horizontalAlign?l=v-r/2:"right"===d.horizontalAlign&&(l=v-r),l=Math.max(i.left+a.left,Math.min(l,i.right-a.right-n)),this.style.left=`${l}px`}}},constrain:function(){if(!this.__shouldPosition){this._discoverInfo();var t=this._fitInfo;t.positionedBy.vertically||(this.style.position="fixed",this.style.top="0px"),t.positionedBy.horizontally||(this.style.position="fixed",this.style.left="0px"),this.sizingTarget.style.boxSizing="border-box";var e=this.getBoundingClientRect();t.sizedBy.height||this.__sizeDimension(e,t.positionedBy.vertically,"top","bottom","Height"),t.sizedBy.width||this.__sizeDimension(e,t.positionedBy.horizontally,"left","right","Width")}},_sizeDimension:function(t,e,i,o,s){this.__sizeDimension(t,e,i,o,s)},__sizeDimension:function(t,e,i,o,s){var n=this._fitInfo,r=this.__getNormalizedRect(this.fitInto),l="Width"===s?r.width:r.height,a=e===o,h=a?l-t[o]:t[i],d=n.margin[a?i:o],c="offset"+s,f=this[c]-this.sizingTarget[c];this.sizingTarget.style["max"+s]=l-d-h-f+"px"},center:function(){if(!this.__shouldPosition){this._discoverInfo();var t=this._fitInfo.positionedBy;if(!t.vertically||!t.horizontally){this.style.position="fixed",t.vertically||(this.style.top="0px"),t.horizontally||(this.style.left="0px");var e=this.getBoundingClientRect(),i=this.__getNormalizedRect(this.fitInto);if(!t.vertically){var o=i.top-e.top+(i.height-e.height)/2;this.style.top=o+"px"}if(!t.horizontally){var s=i.left-e.left+(i.width-e.width)/2;this.style.left=s+"px"}}}},__getNormalizedRect:function(t){return t===document.documentElement||t===window?{top:0,left:0,width:window.innerWidth,height:window.innerHeight,right:window.innerWidth,bottom:window.innerHeight}:t.getBoundingClientRect()},__getOffscreenArea:function(t,e,i){var o=Math.min(0,t.top)+Math.min(0,i.bottom-(t.top+e.height)),s=Math.min(0,t.left)+Math.min(0,i.right-(t.left+e.width));return Math.abs(o)*e.width+Math.abs(s)*e.height},__getPosition:function(t,e,i,o,s,n){var r,l=[{verticalAlign:"top",horizontalAlign:"left",top:s.top+this.verticalOffset,left:s.left+this.horizontalOffset},{verticalAlign:"top",horizontalAlign:"right",top:s.top+this.verticalOffset,left:s.right-i.width-this.horizontalOffset},{verticalAlign:"bottom",horizontalAlign:"left",top:s.bottom-i.height-this.verticalOffset,left:s.left+this.horizontalOffset},{verticalAlign:"bottom",horizontalAlign:"right",top:s.bottom-i.height-this.verticalOffset,left:s.right-i.width-this.horizontalOffset}];if(this.noOverlap){for(var a=0,h=l.length;a<h;a++){var d={};for(var c in l[a])d[c]=l[a][c];l.push(d)}l[0].top=l[1].top+=s.height,l[2].top=l[3].top-=s.height,l[4].left=l[6].left+=s.width,l[5].left=l[7].left-=s.width}e="auto"===e?null:e,(t="auto"===t?null:t)&&"center"!==t||(l.push({verticalAlign:"top",horizontalAlign:"center",top:s.top+this.verticalOffset+(this.noOverlap?s.height:0),left:s.left-o.width/2+s.width/2+this.horizontalOffset}),l.push({verticalAlign:"bottom",horizontalAlign:"center",top:s.bottom-i.height-this.verticalOffset-(this.noOverlap?s.height:0),left:s.left-o.width/2+s.width/2+this.horizontalOffset})),e&&"middle"!==e||(l.push({verticalAlign:"middle",horizontalAlign:"left",top:s.top-o.height/2+s.height/2+this.verticalOffset,left:s.left+this.horizontalOffset+(this.noOverlap?s.width:0)}),l.push({verticalAlign:"middle",horizontalAlign:"right",top:s.top-o.height/2+s.height/2+this.verticalOffset,left:s.right-i.width-this.horizontalOffset-(this.noOverlap?s.width:0)})),"middle"===e&&"center"===t&&l.push({verticalAlign:"middle",horizontalAlign:"center",top:s.top-o.height/2+s.height/2+this.verticalOffset,left:s.left-o.width/2+s.width/2+this.horizontalOffset});for(a=0;a<l.length;a++){var f=l[a],p=f.verticalAlign===e,u=f.horizontalAlign===t;if(!this.dynamicAlign&&!this.noOverlap&&p&&u){r=f;break}var _=(!e||p)&&(!t||u);if(this.dynamicAlign||_){if(f.offscreenArea=this.__getOffscreenArea(f,i,n),0===f.offscreenArea&&_){r=f;break}r=r||f;var g=f.offscreenArea-r.offscreenArea;(g<0||0===g&&(p||u))&&(r=f)}}return r}}},93592:(t,e,i)=>{i.d(e,{H:()=>r});i(94604);var o=i(87156),s=Element.prototype,n=s.matches||s.matchesSelector||s.mozMatchesSelector||s.msMatchesSelector||s.oMatchesSelector||s.webkitMatchesSelector;const r=new class{getTabbableNodes(t){var e=[];return this._collectTabbableNodes(t,e)?this._sortByTabIndex(e):e}isFocusable(t){return n.call(t,"input, select, textarea, button, object")?n.call(t,":not([disabled])"):n.call(t,"a[href], area[href], iframe, [tabindex], [contentEditable]")}isTabbable(t){return this.isFocusable(t)&&n.call(t,':not([tabindex="-1"])')&&this._isVisible(t)}_normalizedTabIndex(t){if(this.isFocusable(t)){var e=t.getAttribute("tabindex")||0;return Number(e)}return-1}_collectTabbableNodes(t,e){if(t.nodeType!==Node.ELEMENT_NODE)return!1;var i=t;if(!this._isVisible(i))return!1;var s,n=this._normalizedTabIndex(i),r=n>0;n>=0&&e.push(i),s="content"===i.localName||"slot"===i.localName?(0,o.vz)(i).getDistributedNodes():(0,o.vz)(i.root||i).children;for(var l=0;l<s.length;l++)r=this._collectTabbableNodes(s[l],e)||r;return r}_isVisible(t){var e=t.style;return"hidden"!==e.visibility&&"none"!==e.display&&("hidden"!==(e=window.getComputedStyle(t)).visibility&&"none"!==e.display)}_sortByTabIndex(t){var e=t.length;if(e<2)return t;var i=Math.ceil(e/2),o=this._sortByTabIndex(t.slice(0,i)),s=this._sortByTabIndex(t.slice(i));return this._mergeSortByTabIndex(o,s)}_mergeSortByTabIndex(t,e){for(var i=[];t.length>0&&e.length>0;)this._hasLowerTabOrder(t[0],e[0])?i.push(e.shift()):i.push(t.shift());return i.concat(t,e)}_hasLowerTabOrder(t,e){var i=Math.max(t.tabIndex,0),o=Math.max(e.tabIndex,0);return 0===i||0===o?o>i:i>o}}},24101:(t,e,i)=>{i(94604);var o=i(9672),s=i(87156),n=i(50856);(0,o.k)({_template:n.d`
    <style>
      :host {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: var(--iron-overlay-backdrop-background-color, #000);
        opacity: 0;
        transition: opacity 0.2s;
        pointer-events: none;
        @apply --iron-overlay-backdrop;
      }

      :host(.opened) {
        opacity: var(--iron-overlay-backdrop-opacity, 0.6);
        pointer-events: auto;
        @apply --iron-overlay-backdrop-opened;
      }
    </style>

    <slot></slot>
`,is:"iron-overlay-backdrop",properties:{opened:{reflectToAttribute:!0,type:Boolean,value:!1,observer:"_openedChanged"}},listeners:{transitionend:"_onTransitionend"},created:function(){this.__openedRaf=null},attached:function(){this.opened&&this._openedChanged(this.opened)},prepare:function(){this.opened&&!this.parentNode&&(0,s.vz)(document.body).appendChild(this)},open:function(){this.opened=!0},close:function(){this.opened=!1},complete:function(){this.opened||this.parentNode!==document.body||(0,s.vz)(this.parentNode).removeChild(this)},_onTransitionend:function(t){t&&t.target===this&&this.complete()},_openedChanged:function(t){if(t)this.prepare();else{var e=window.getComputedStyle(this);"0s"!==e.transitionDuration&&0!=e.opacity||this.complete()}this.isAttached&&(this.__openedRaf&&(window.cancelAnimationFrame(this.__openedRaf),this.__openedRaf=null),this.scrollTop=this.scrollTop,this.__openedRaf=window.requestAnimationFrame(function(){this.__openedRaf=null,this.toggleClass("opened",this.opened)}.bind(this)))}})},75009:(t,e,i)=>{i.d(e,{Q:()=>d,$:()=>f});i(94604);var o=i(71780),s=i(72986),n=i(87156),r=i(74460),l=i(93592),a=i(105),h=i(63550);const d={properties:{opened:{observer:"_openedChanged",type:Boolean,value:!1,notify:!0},canceled:{observer:"_canceledChanged",readOnly:!0,type:Boolean,value:!1},withBackdrop:{observer:"_withBackdropChanged",type:Boolean},noAutoFocus:{type:Boolean,value:!1},noCancelOnEscKey:{type:Boolean,value:!1},noCancelOnOutsideClick:{type:Boolean,value:!1},closingReason:{type:Object},restoreFocusOnClose:{type:Boolean,value:!1},allowClickThrough:{type:Boolean},alwaysOnTop:{type:Boolean},scrollAction:{type:String},_manager:{type:Object,value:a.E},_focusedChild:{type:Object}},listeners:{"iron-resize":"_onIronResize"},observers:["__updateScrollObservers(isAttached, opened, scrollAction)"],get backdropElement(){return this._manager.backdropElement},get _focusNode(){return this._focusedChild||(0,n.vz)(this).querySelector("[autofocus]")||this},get _focusableNodes(){return l.H.getTabbableNodes(this)},ready:function(){this.__isAnimating=!1,this.__shouldRemoveTabIndex=!1,this.__firstFocusableNode=this.__lastFocusableNode=null,this.__rafs={},this.__restoreFocusNode=null,this.__scrollTop=this.__scrollLeft=null,this.__onCaptureScroll=this.__onCaptureScroll.bind(this),this.__rootNodes=null,this._ensureSetup()},attached:function(){this.opened&&this._openedChanged(this.opened),this._observer=(0,n.vz)(this).observeNodes(this._onNodesChange)},detached:function(){for(var t in this._observer&&(0,n.vz)(this).unobserveNodes(this._observer),this._observer=null,this.__rafs)null!==this.__rafs[t]&&cancelAnimationFrame(this.__rafs[t]);this.__rafs={},this._manager.removeOverlay(this),this.__isAnimating&&(this.opened?this._finishRenderOpened():(this._applyFocus(),this._finishRenderClosed()))},toggle:function(){this._setCanceled(!1),this.opened=!this.opened},open:function(){this._setCanceled(!1),this.opened=!0},close:function(){this._setCanceled(!1),this.opened=!1},cancel:function(t){this.fire("iron-overlay-canceled",t,{cancelable:!0}).defaultPrevented||(this._setCanceled(!0),this.opened=!1)},invalidateTabbables:function(){this.__firstFocusableNode=this.__lastFocusableNode=null},_ensureSetup:function(){this._overlaySetup||(this._overlaySetup=!0,this.style.outline="none",this.style.display="none")},_openedChanged:function(t){t?this.removeAttribute("aria-hidden"):this.setAttribute("aria-hidden","true"),this.isAttached&&(this.__isAnimating=!0,this.__deraf("__openedChanged",this.__openedChanged))},_canceledChanged:function(){this.closingReason=this.closingReason||{},this.closingReason.canceled=this.canceled},_withBackdropChanged:function(){this.withBackdrop&&!this.hasAttribute("tabindex")?(this.setAttribute("tabindex","-1"),this.__shouldRemoveTabIndex=!0):this.__shouldRemoveTabIndex&&(this.removeAttribute("tabindex"),this.__shouldRemoveTabIndex=!1),this.opened&&this.isAttached&&this._manager.trackBackdrop()},_prepareRenderOpened:function(){this.__restoreFocusNode=this._manager.deepActiveElement,this._preparePositioning(),this.refit(),this._finishPositioning(),this.noAutoFocus&&document.activeElement===this._focusNode&&(this._focusNode.blur(),this.__restoreFocusNode.focus())},_renderOpened:function(){this._finishRenderOpened()},_renderClosed:function(){this._finishRenderClosed()},_finishRenderOpened:function(){this.notifyResize(),this.__isAnimating=!1,this.fire("iron-overlay-opened")},_finishRenderClosed:function(){this.style.display="none",this.style.zIndex="",this.notifyResize(),this.__isAnimating=!1,this.fire("iron-overlay-closed",this.closingReason)},_preparePositioning:function(){this.style.transition=this.style.webkitTransition="none",this.style.transform=this.style.webkitTransform="none",this.style.display=""},_finishPositioning:function(){this.style.display="none",this.scrollTop=this.scrollTop,this.style.transition=this.style.webkitTransition="",this.style.transform=this.style.webkitTransform="",this.style.display="",this.scrollTop=this.scrollTop},_applyFocus:function(){if(this.opened)this.noAutoFocus||this._focusNode.focus();else{if(this.restoreFocusOnClose&&this.__restoreFocusNode){var t=this._manager.deepActiveElement;(t===document.body||c(this,t))&&this.__restoreFocusNode.focus()}this.__restoreFocusNode=null,this._focusNode.blur(),this._focusedChild=null}},_onCaptureClick:function(t){this.noCancelOnOutsideClick||this.cancel(t)},_onCaptureFocus:function(t){if(this.withBackdrop){var e=(0,n.vz)(t).path;-1===e.indexOf(this)?(t.stopPropagation(),this._applyFocus()):this._focusedChild=e[0]}},_onCaptureEsc:function(t){this.noCancelOnEscKey||this.cancel(t)},_onCaptureTab:function(t){if(this.withBackdrop){this.__ensureFirstLastFocusables();var e=t.shiftKey,i=e?this.__firstFocusableNode:this.__lastFocusableNode,o=e?this.__lastFocusableNode:this.__firstFocusableNode,s=!1;if(i===o)s=!0;else{var n=this._manager.deepActiveElement;s=n===i||n===this}s&&(t.preventDefault(),this._focusedChild=o,this._applyFocus())}},_onIronResize:function(){this.opened&&!this.__isAnimating&&this.__deraf("refit",this.refit)},_onNodesChange:function(){this.opened&&!this.__isAnimating&&(this.invalidateTabbables(),this.notifyResize())},__ensureFirstLastFocusables:function(){var t=this._focusableNodes;this.__firstFocusableNode=t[0],this.__lastFocusableNode=t[t.length-1]},__openedChanged:function(){this.opened?(this._prepareRenderOpened(),this._manager.addOverlay(this),this._applyFocus(),this._renderOpened()):(this._manager.removeOverlay(this),this._applyFocus(),this._renderClosed())},__deraf:function(t,e){var i=this.__rafs;null!==i[t]&&cancelAnimationFrame(i[t]),i[t]=requestAnimationFrame(function(){i[t]=null,e.call(this)}.bind(this))},__updateScrollObservers:function(t,e,i){t&&e&&this.__isValidScrollAction(i)?("lock"===i&&(this.__saveScrollPosition(),(0,h.$A)(this)),this.__addScrollListeners()):((0,h.fm)(this),this.__removeScrollListeners())},__addScrollListeners:function(){if(!this.__rootNodes){if(this.__rootNodes=[],r.my)for(var t=this;t;)t.nodeType===Node.DOCUMENT_FRAGMENT_NODE&&t.host&&this.__rootNodes.push(t),t=t.host||t.assignedSlot||t.parentNode;this.__rootNodes.push(document)}this.__rootNodes.forEach((function(t){t.addEventListener("scroll",this.__onCaptureScroll,{capture:!0,passive:!0})}),this)},__removeScrollListeners:function(){this.__rootNodes&&this.__rootNodes.forEach((function(t){t.removeEventListener("scroll",this.__onCaptureScroll,{capture:!0,passive:!0})}),this),this.isAttached||(this.__rootNodes=null)},__isValidScrollAction:function(t){return"lock"===t||"refit"===t||"cancel"===t},__onCaptureScroll:function(t){if(!(this.__isAnimating||(0,n.vz)(t).path.indexOf(this)>=0))switch(this.scrollAction){case"lock":this.__restoreScrollPosition();break;case"refit":this.__deraf("refit",this.refit);break;case"cancel":this.cancel(t)}},__saveScrollPosition:function(){document.scrollingElement?(this.__scrollTop=document.scrollingElement.scrollTop,this.__scrollLeft=document.scrollingElement.scrollLeft):(this.__scrollTop=Math.max(document.documentElement.scrollTop,document.body.scrollTop),this.__scrollLeft=Math.max(document.documentElement.scrollLeft,document.body.scrollLeft))},__restoreScrollPosition:function(){document.scrollingElement?(document.scrollingElement.scrollTop=this.__scrollTop,document.scrollingElement.scrollLeft=this.__scrollLeft):(document.documentElement.scrollTop=document.body.scrollTop=this.__scrollTop,document.documentElement.scrollLeft=document.body.scrollLeft=this.__scrollLeft)}},c=(t,e)=>{for(let o=e;o;o=(i=o).assignedSlot||i.parentNode||i.host)if(o===t)return!0;var i;return!1},f=[o.L,s.z,d]},105:(t,e,i)=>{i.d(e,{E:()=>r});i(94604),i(24101);var o=i(8621),s=i(87156),n=i(81668);const r=new class{constructor(){this._overlays=[],this._minimumZ=101,this._backdropElement=null,n.NH(document.documentElement,"tap",(function(){})),document.addEventListener("tap",this._onCaptureClick.bind(this),!0),document.addEventListener("focus",this._onCaptureFocus.bind(this),!0),document.addEventListener("keydown",this._onCaptureKeyDown.bind(this),!0)}get backdropElement(){return this._backdropElement||(this._backdropElement=document.createElement("iron-overlay-backdrop")),this._backdropElement}get deepActiveElement(){var t=document.activeElement;for(t&&t instanceof Element!=!1||(t=document.body);t.root&&(0,s.vz)(t.root).activeElement;)t=(0,s.vz)(t.root).activeElement;return t}_bringOverlayAtIndexToFront(t){var e=this._overlays[t];if(e){var i=this._overlays.length-1,o=this._overlays[i];if(o&&this._shouldBeBehindOverlay(e,o)&&i--,!(t>=i)){var s=Math.max(this.currentOverlayZ(),this._minimumZ);for(this._getZ(e)<=s&&this._applyOverlayZ(e,s);t<i;)this._overlays[t]=this._overlays[t+1],t++;this._overlays[i]=e}}}addOrRemoveOverlay(t){t.opened?this.addOverlay(t):this.removeOverlay(t)}addOverlay(t){var e=this._overlays.indexOf(t);if(e>=0)return this._bringOverlayAtIndexToFront(e),void this.trackBackdrop();var i=this._overlays.length,o=this._overlays[i-1],s=Math.max(this._getZ(o),this._minimumZ),n=this._getZ(t);if(o&&this._shouldBeBehindOverlay(t,o)){this._applyOverlayZ(o,s),i--;var r=this._overlays[i-1];s=Math.max(this._getZ(r),this._minimumZ)}n<=s&&this._applyOverlayZ(t,s),this._overlays.splice(i,0,t),this.trackBackdrop()}removeOverlay(t){var e=this._overlays.indexOf(t);-1!==e&&(this._overlays.splice(e,1),this.trackBackdrop())}currentOverlay(){var t=this._overlays.length-1;return this._overlays[t]}currentOverlayZ(){return this._getZ(this.currentOverlay())}ensureMinimumZ(t){this._minimumZ=Math.max(this._minimumZ,t)}focusOverlay(){var t=this.currentOverlay();t&&t._applyFocus()}trackBackdrop(){var t=this._overlayWithBackdrop();(t||this._backdropElement)&&(this.backdropElement.style.zIndex=this._getZ(t)-1,this.backdropElement.opened=!!t,this.backdropElement.prepare())}getBackdrops(){for(var t=[],e=0;e<this._overlays.length;e++)this._overlays[e].withBackdrop&&t.push(this._overlays[e]);return t}backdropZ(){return this._getZ(this._overlayWithBackdrop())-1}_overlayWithBackdrop(){for(var t=this._overlays.length-1;t>=0;t--)if(this._overlays[t].withBackdrop)return this._overlays[t]}_getZ(t){var e=this._minimumZ;if(t){var i=Number(t.style.zIndex||window.getComputedStyle(t).zIndex);i==i&&(e=i)}return e}_setZ(t,e){t.style.zIndex=e}_applyOverlayZ(t,e){this._setZ(t,e+2)}_overlayInPath(t){t=t||[];for(var e=0;e<t.length;e++)if(t[e]._manager===this)return t[e]}_onCaptureClick(t){var e=this._overlays.length-1;if(-1!==e)for(var i,o=(0,s.vz)(t).path;(i=this._overlays[e])&&this._overlayInPath(o)!==i&&(i._onCaptureClick(t),i.allowClickThrough);)e--}_onCaptureFocus(t){var e=this.currentOverlay();e&&e._onCaptureFocus(t)}_onCaptureKeyDown(t){var e=this.currentOverlay();e&&(o.G.keyboardEventMatchesKeys(t,"esc")?e._onCaptureEsc(t):o.G.keyboardEventMatchesKeys(t,"tab")&&e._onCaptureTab(t))}_shouldBeBehindOverlay(t,e){return!t.alwaysOnTop&&e.alwaysOnTop}}},63550:(t,e,i)=>{i.d(e,{$A:()=>d,fm:()=>c});i(94604);var o,s,n=i(87156),r={pageX:0,pageY:0},l=null,a=[],h=["wheel","mousewheel","DOMMouseScroll","touchstart","touchmove"];function d(t){f.indexOf(t)>=0||(0===f.length&&function(){o=o||_.bind(void 0);for(var t=0,e=h.length;t<e;t++)document.addEventListener(h[t],o,{capture:!0,passive:!1})}(),f.push(t),s=f[f.length-1],p=[],u=[])}function c(t){var e=f.indexOf(t);-1!==e&&(f.splice(e,1),s=f[f.length-1],p=[],u=[],0===f.length&&function(){for(var t=0,e=h.length;t<e;t++)document.removeEventListener(h[t],o,{capture:!0,passive:!1})}())}const f=[];let p=null,u=null;function _(t){if(t.cancelable&&function(t){var e=(0,n.vz)(t).rootTarget;"touchmove"!==t.type&&l!==e&&(l=e,a=function(t){for(var e=[],i=t.indexOf(s),o=0;o<=i;o++)if(t[o].nodeType===Node.ELEMENT_NODE){var n=t[o],r=n.style;"scroll"!==r.overflow&&"auto"!==r.overflow&&(r=window.getComputedStyle(n)),"scroll"!==r.overflow&&"auto"!==r.overflow||e.push(n)}return e}((0,n.vz)(t).path));if(!a.length)return!0;if("touchstart"===t.type)return!1;var i=function(t){var e={deltaX:t.deltaX,deltaY:t.deltaY};if("deltaX"in t);else if("wheelDeltaX"in t&&"wheelDeltaY"in t)e.deltaX=-t.wheelDeltaX,e.deltaY=-t.wheelDeltaY;else if("wheelDelta"in t)e.deltaX=0,e.deltaY=-t.wheelDelta;else if("axis"in t)e.deltaX=1===t.axis?t.detail:0,e.deltaY=2===t.axis?t.detail:0;else if(t.targetTouches){var i=t.targetTouches[0];e.deltaX=r.pageX-i.pageX,e.deltaY=r.pageY-i.pageY}return e}(t);return!function(t,e,i){if(!e&&!i)return;for(var o=Math.abs(i)>=Math.abs(e),s=0;s<t.length;s++){var n=t[s];if(o?i<0?n.scrollTop>0:n.scrollTop<n.scrollHeight-n.clientHeight:e<0?n.scrollLeft>0:n.scrollLeft<n.scrollWidth-n.clientWidth)return n}}(a,i.deltaX,i.deltaY)}(t)&&t.preventDefault(),t.targetTouches){var e=t.targetTouches[0];r.pageX=e.pageX,r.pageY=e.pageY}}}}]);
//# sourceMappingURL=1608b185.js.map