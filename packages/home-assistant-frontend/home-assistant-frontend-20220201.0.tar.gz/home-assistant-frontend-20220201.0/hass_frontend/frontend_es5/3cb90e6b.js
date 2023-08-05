/*! For license information please see 3cb90e6b.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[93883],{51356:function(e,t,n){n.d(t,{UX:function(){return r},j2:function(){return i},KT:function(){return u},yM:function(){return o}});var o,r={MENU_SELECTED_LIST_ITEM:"mdc-menu-item--selected",MENU_SELECTION_GROUP:"mdc-menu__selection-group",ROOT:"mdc-menu"},i={ARIA_CHECKED_ATTR:"aria-checked",ARIA_DISABLED_ATTR:"aria-disabled",CHECKBOX_SELECTOR:'input[type="checkbox"]',LIST_SELECTOR:".mdc-list,.mdc-deprecated-list",SELECTED_EVENT:"MDCMenu:selected",SKIP_RESTORE_FOCUS:"data-menu-item-skip-restore-focus"},u={FOCUS_ROOT_INDEX:-1};!function(e){e[e.NONE=0]="NONE",e[e.LIST_ROOT=1]="LIST_ROOT",e[e.FIRST_ITEM=2]="FIRST_ITEM",e[e.LAST_ITEM=3]="LAST_ITEM"}(o||(o={}))},65150:function(e,t,n){var o=n(87480),r=n(72774),i=n(74015),u=n(6945),c=n(51356),a=function(e){function t(n){var r=e.call(this,(0,o.__assign)((0,o.__assign)({},t.defaultAdapter),n))||this;return r.closeAnimationEndTimerId=0,r.defaultFocusState=c.yM.LIST_ROOT,r.selectedIndex=-1,r}return(0,o.__extends)(t,e),Object.defineProperty(t,"cssClasses",{get:function(){return c.UX},enumerable:!1,configurable:!0}),Object.defineProperty(t,"strings",{get:function(){return c.j2},enumerable:!1,configurable:!0}),Object.defineProperty(t,"numbers",{get:function(){return c.KT},enumerable:!1,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{addClassToElementAtIndex:function(){},removeClassFromElementAtIndex:function(){},addAttributeToElementAtIndex:function(){},removeAttributeFromElementAtIndex:function(){},getAttributeFromElementAtIndex:function(){return null},elementContainsClass:function(){return!1},closeSurface:function(){},getElementIndex:function(){return-1},notifySelected:function(){},getMenuItemCount:function(){return 0},focusItemAtIndex:function(){},focusListRoot:function(){},getSelectedSiblingOfItemAtIndex:function(){return-1},isSelectableItemAtIndex:function(){return!1}}},enumerable:!1,configurable:!0}),t.prototype.destroy=function(){this.closeAnimationEndTimerId&&clearTimeout(this.closeAnimationEndTimerId),this.adapter.closeSurface()},t.prototype.handleKeydown=function(e){var t=e.key,n=e.keyCode;("Tab"===t||9===n)&&this.adapter.closeSurface(!0)},t.prototype.handleItemAction=function(e){var t=this,n=this.adapter.getElementIndex(e);if(!(n<0)){this.adapter.notifySelected({index:n});var o="true"===this.adapter.getAttributeFromElementAtIndex(n,c.j2.SKIP_RESTORE_FOCUS);this.adapter.closeSurface(o),this.closeAnimationEndTimerId=setTimeout((function(){var n=t.adapter.getElementIndex(e);n>=0&&t.adapter.isSelectableItemAtIndex(n)&&t.setSelectedIndex(n)}),u.k.numbers.TRANSITION_CLOSE_DURATION)}},t.prototype.handleMenuSurfaceOpened=function(){switch(this.defaultFocusState){case c.yM.FIRST_ITEM:this.adapter.focusItemAtIndex(0);break;case c.yM.LAST_ITEM:this.adapter.focusItemAtIndex(this.adapter.getMenuItemCount()-1);break;case c.yM.NONE:break;default:this.adapter.focusListRoot()}},t.prototype.setDefaultFocusState=function(e){this.defaultFocusState=e},t.prototype.getSelectedIndex=function(){return this.selectedIndex},t.prototype.setSelectedIndex=function(e){if(this.validatedIndex(e),!this.adapter.isSelectableItemAtIndex(e))throw new Error("MDCMenuFoundation: No selection group at specified index.");var t=this.adapter.getSelectedSiblingOfItemAtIndex(e);t>=0&&(this.adapter.removeAttributeFromElementAtIndex(t,c.j2.ARIA_CHECKED_ATTR),this.adapter.removeClassFromElementAtIndex(t,c.UX.MENU_SELECTED_LIST_ITEM)),this.adapter.addClassToElementAtIndex(e,c.UX.MENU_SELECTED_LIST_ITEM),this.adapter.addAttributeToElementAtIndex(e,c.j2.ARIA_CHECKED_ATTR,"true"),this.selectedIndex=e},t.prototype.setEnabled=function(e,t){this.validatedIndex(e),t?(this.adapter.removeClassFromElementAtIndex(e,i.UX.LIST_ITEM_DISABLED_CLASS),this.adapter.addAttributeToElementAtIndex(e,c.j2.ARIA_DISABLED_ATTR,"false")):(this.adapter.addClassToElementAtIndex(e,i.UX.LIST_ITEM_DISABLED_CLASS),this.adapter.addAttributeToElementAtIndex(e,c.j2.ARIA_DISABLED_ATTR,"true"))},t.prototype.validatedIndex=function(e){var t=this.adapter.getMenuItemCount();if(!(e>=0&&e<t))throw new Error("MDCMenuFoundation: No list item at specified index.")},t}(r.K);t.Z=a},95135:function(e,t,n){n.d(t,{HB:function(){return I}});var o,r=n(87480),i=(n(87502),n(1536),n(51356)),u=n(65150),c=n(78220),a=n(14114),s=n(37500),l=n(72367);function d(e){return d="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},d(e)}function f(e,t,n,o,r,i,u){try{var c=e[i](u),a=c.value}catch(s){return void n(s)}c.done?t(a):Promise.resolve(a).then(o,r)}function p(e){return function(){var t=this,n=arguments;return new Promise((function(o,r){var i=e.apply(t,n);function u(e){f(i,o,r,u,c,"next",e)}function c(e){f(i,o,r,u,c,"throw",e)}u(void 0)}))}}function m(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function y(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function h(e,t,n){return h="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var o=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=E(e)););return e}(e,t);if(o){var r=Object.getOwnPropertyDescriptor(o,t);return r.get?r.get.call(n):r.value}},h(e,t,n||e)}function v(e,t){return v=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},v(e,t)}function b(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,o=E(e);if(t){var r=E(this).constructor;n=Reflect.construct(o,arguments,r)}else n=o.apply(this,arguments);return _(this,n)}}function _(e,t){if(t&&("object"===d(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function E(e){return E=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},E(e)}var I=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&v(e,t)}(l,e);var t,n,r,i,c,a=b(l);function l(){var e;return m(this,l),(e=a.apply(this,arguments)).mdcFoundationClass=u.Z,e.listElement_=null,e.anchor=null,e.open=!1,e.quick=!1,e.wrapFocus=!1,e.innerRole="menu",e.innerAriaLabel=null,e.corner="TOP_START",e.x=null,e.y=null,e.absolute=!1,e.multi=!1,e.activatable=!1,e.fixed=!1,e.forceGroupSelection=!1,e.fullwidth=!1,e.menuCorner="START",e.stayOpenOnBodyClick=!1,e.defaultFocus="LIST_ROOT",e._listUpdateComplete=null,e}return t=l,n=[{key:"listElement",get:function(){return this.listElement_||(this.listElement_=this.renderRoot.querySelector("mwc-list")),this.listElement_}},{key:"items",get:function(){var e=this.listElement;return e?e.items:[]}},{key:"index",get:function(){var e=this.listElement;return e?e.index:-1}},{key:"selected",get:function(){var e=this.listElement;return e?e.selected:null}},{key:"render",value:function(){var e,t,n="menu"===this.innerRole?"menuitem":"option";return(0,s.dy)(o||(e=["\n      <mwc-menu-surface\n          ?hidden=","\n          .anchor=","\n          .open=","\n          .quick=","\n          .corner=","\n          .x=","\n          .y=","\n          .absolute=","\n          .fixed=","\n          .fullwidth=","\n          .menuCorner=","\n          ?stayOpenOnBodyClick=",'\n          class="mdc-menu mdc-menu-surface"\n          @closed=',"\n          @opened=","\n          @keydown=",">\n        <mwc-list\n          rootTabbable\n          .innerAriaLabel=","\n          .innerRole=","\n          .multi=",'\n          class="mdc-deprecated-list"\n          .itemRoles=',"\n          .wrapFocus=","\n          .activatable=","\n          @action=",">\n        <slot></slot>\n      </mwc-list>\n    </mwc-menu-surface>"],t||(t=e.slice(0)),o=Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))),!this.open,this.anchor,this.open,this.quick,this.corner,this.x,this.y,this.absolute,this.fixed,this.fullwidth,this.menuCorner,this.stayOpenOnBodyClick,this.onClosed,this.onOpened,this.onKeydown,this.innerAriaLabel,this.innerRole,this.multi,n,this.wrapFocus,this.activatable,this.onAction)}},{key:"createAdapter",value:function(){var e=this;return{addClassToElementAtIndex:function(t,n){var o=e.listElement;if(o){var r=o.items[t];r&&("mdc-menu-item--selected"===n?e.forceGroupSelection&&!r.selected&&o.toggle(t,!0):r.classList.add(n))}},removeClassFromElementAtIndex:function(t,n){var o=e.listElement;if(o){var r=o.items[t];r&&("mdc-menu-item--selected"===n?r.selected&&o.toggle(t,!1):r.classList.remove(n))}},addAttributeToElementAtIndex:function(t,n,o){var r=e.listElement;if(r){var i=r.items[t];i&&i.setAttribute(n,o)}},removeAttributeFromElementAtIndex:function(t,n){var o=e.listElement;if(o){var r=o.items[t];r&&r.removeAttribute(n)}},getAttributeFromElementAtIndex:function(t,n){var o=e.listElement;if(!o)return null;var r=o.items[t];return r?r.getAttribute(n):null},elementContainsClass:function(e,t){return e.classList.contains(t)},closeSurface:function(){e.open=!1},getElementIndex:function(t){var n=e.listElement;return n?n.items.indexOf(t):-1},notifySelected:function(){},getMenuItemCount:function(){var t=e.listElement;return t?t.items.length:0},focusItemAtIndex:function(t){var n=e.listElement;if(n){var o=n.items[t];o&&o.focus()}},focusListRoot:function(){e.listElement&&e.listElement.focus()},getSelectedSiblingOfItemAtIndex:function(t){var n=e.listElement;if(!n)return-1;var o=n.items[t];if(!o||!o.group)return-1;for(var r=0;r<n.items.length;r++)if(r!==t){var i=n.items[r];if(i.selected&&i.group===o.group)return r}return-1},isSelectableItemAtIndex:function(t){var n=e.listElement;if(!n)return!1;var o=n.items[t];return!!o&&o.hasAttribute("group")}}}},{key:"onKeydown",value:function(e){this.mdcFoundation&&this.mdcFoundation.handleKeydown(e)}},{key:"onAction",value:function(e){var t=this.listElement;if(this.mdcFoundation&&t){var n=e.detail.index,o=t.items[n];o&&this.mdcFoundation.handleItemAction(o)}}},{key:"onOpened",value:function(){this.open=!0,this.mdcFoundation&&this.mdcFoundation.handleMenuSurfaceOpened()}},{key:"onClosed",value:function(){this.open=!1}},{key:"getUpdateComplete",value:(c=p(regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,this._listUpdateComplete;case 2:return e.next=4,h(E(l.prototype),"getUpdateComplete",this).call(this);case 4:return t=e.sent,e.abrupt("return",t);case 6:case"end":return e.stop()}}),e,this)}))),function(){return c.apply(this,arguments)})},{key:"firstUpdated",value:(i=p(regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(h(E(l.prototype),"firstUpdated",this).call(this),!(t=this.listElement)){e.next=6;break}return this._listUpdateComplete=t.updateComplete,e.next=6,this._listUpdateComplete;case 6:case"end":return e.stop()}}),e,this)}))),function(){return i.apply(this,arguments)})},{key:"select",value:function(e){var t=this.listElement;t&&t.select(e)}},{key:"close",value:function(){this.open=!1}},{key:"show",value:function(){this.open=!0}},{key:"getFocusedItemIndex",value:function(){var e=this.listElement;return e?e.getFocusedItemIndex():-1}},{key:"focusItemAtIndex",value:function(e){var t=this.listElement;t&&t.focusItemAtIndex(e)}},{key:"layout",value:function(){var e=!(arguments.length>0&&void 0!==arguments[0])||arguments[0],t=this.listElement;t&&t.layout(e)}}],n&&y(t.prototype,n),r&&y(t,r),l}(c.H);(0,r.__decorate)([(0,l.IO)(".mdc-menu")],I.prototype,"mdcRoot",void 0),(0,r.__decorate)([(0,l.IO)("slot")],I.prototype,"slotElement",void 0),(0,r.__decorate)([(0,l.Cb)({type:Object})],I.prototype,"anchor",void 0),(0,r.__decorate)([(0,l.Cb)({type:Boolean,reflect:!0})],I.prototype,"open",void 0),(0,r.__decorate)([(0,l.Cb)({type:Boolean})],I.prototype,"quick",void 0),(0,r.__decorate)([(0,l.Cb)({type:Boolean})],I.prototype,"wrapFocus",void 0),(0,r.__decorate)([(0,l.Cb)({type:String})],I.prototype,"innerRole",void 0),(0,r.__decorate)([(0,l.Cb)({type:String})],I.prototype,"innerAriaLabel",void 0),(0,r.__decorate)([(0,l.Cb)({type:String})],I.prototype,"corner",void 0),(0,r.__decorate)([(0,l.Cb)({type:Number})],I.prototype,"x",void 0),(0,r.__decorate)([(0,l.Cb)({type:Number})],I.prototype,"y",void 0),(0,r.__decorate)([(0,l.Cb)({type:Boolean})],I.prototype,"absolute",void 0),(0,r.__decorate)([(0,l.Cb)({type:Boolean})],I.prototype,"multi",void 0),(0,r.__decorate)([(0,l.Cb)({type:Boolean})],I.prototype,"activatable",void 0),(0,r.__decorate)([(0,l.Cb)({type:Boolean})],I.prototype,"fixed",void 0),(0,r.__decorate)([(0,l.Cb)({type:Boolean})],I.prototype,"forceGroupSelection",void 0),(0,r.__decorate)([(0,l.Cb)({type:Boolean})],I.prototype,"fullwidth",void 0),(0,r.__decorate)([(0,l.Cb)({type:String})],I.prototype,"menuCorner",void 0),(0,r.__decorate)([(0,l.Cb)({type:Boolean})],I.prototype,"stayOpenOnBodyClick",void 0),(0,r.__decorate)([(0,l.Cb)({type:String}),(0,a.P)((function(e){this.mdcFoundation&&this.mdcFoundation.setDefaultFocusState(i.yM[e])}))],I.prototype,"defaultFocus",void 0)},89195:function(e,t,n){var o;n.d(t,{W:function(){return u}});var r,i,u=(0,n(37500).iv)(o||(r=["mwc-list ::slotted([mwc-list-item]:not([twoline])),mwc-list ::slotted([noninteractive]:not([twoline])){height:var(--mdc-menu-item-height, 48px)}"],i||(i=r.slice(0)),o=Object.freeze(Object.defineProperties(r,{raw:{value:Object.freeze(i)}}))))},93883:function(e,t,n){var o=n(87480),r=n(72367),i=n(95135),u=n(89195);function c(e){return c="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},c(e)}function a(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function s(e,t){return s=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},s(e,t)}function l(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,o=f(e);if(t){var r=f(this).constructor;n=Reflect.construct(o,arguments,r)}else n=o.apply(this,arguments);return d(this,n)}}function d(e,t){if(t&&("object"===c(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function f(e){return f=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},f(e)}var p=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&s(e,t)}(n,e);var t=l(n);function n(){return a(this,n),t.apply(this,arguments)}return n}(i.HB);p.styles=[u.W],p=(0,o.__decorate)([(0,r.Mo)("mwc-menu")],p)}}]);