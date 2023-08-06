/*! For license information please see 8cd7770b.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[76645,47102,31223,39452],{14114:(e,t,o)=>{o.d(t,{P:()=>n});const n=e=>(t,o)=>{if(t.constructor._observers){if(!t.constructor.hasOwnProperty("_observers")){const e=t.constructor._observers;t.constructor._observers=new Map,e.forEach(((e,o)=>t.constructor._observers.set(o,e)))}}else{t.constructor._observers=new Map;const e=t.updated;t.updated=function(t){e.call(this,t),t.forEach(((e,t)=>{const o=this.constructor._observers.get(t);void 0!==o&&o.call(this,this[t],e)}))}}t.constructor._observers.set(o,e)}},99257:(e,t,o)=>{o(94604);var n=o(15112),r=o(9672),i=o(87156);(0,r.k)({is:"iron-iconset-svg",properties:{name:{type:String,observer:"_nameChanged"},size:{type:Number,value:24},rtlMirroring:{type:Boolean,value:!1},useGlobalRtlAttribute:{type:Boolean,value:!1}},created:function(){this._meta=new n.P({type:"iconset",key:null,value:null})},attached:function(){this.style.display="none"},getIconNames:function(){return this._icons=this._createIconMap(),Object.keys(this._icons).map((function(e){return this.name+":"+e}),this)},applyIcon:function(e,t){this.removeIcon(e);var o=this._cloneIcon(t,this.rtlMirroring&&this._targetIsRTL(e));if(o){var n=(0,i.vz)(e.root||e);return n.insertBefore(o,n.childNodes[0]),e._svgIcon=o}return null},removeIcon:function(e){e._svgIcon&&((0,i.vz)(e.root||e).removeChild(e._svgIcon),e._svgIcon=null)},_targetIsRTL:function(e){if(null==this.__targetIsRTL)if(this.useGlobalRtlAttribute){var t=document.body&&document.body.hasAttribute("dir")?document.body:document.documentElement;this.__targetIsRTL="rtl"===t.getAttribute("dir")}else e&&e.nodeType!==Node.ELEMENT_NODE&&(e=e.host),this.__targetIsRTL=e&&"rtl"===window.getComputedStyle(e).direction;return this.__targetIsRTL},_nameChanged:function(){this._meta.value=null,this._meta.key=this.name,this._meta.value=this,this.async((function(){this.fire("iron-iconset-added",this,{node:window})}))},_createIconMap:function(){var e=Object.create(null);return(0,i.vz)(this).querySelectorAll("[id]").forEach((function(t){e[t.id]=t})),e},_cloneIcon:function(e,t){return this._icons=this._icons||this._createIconMap(),this._prepareSvgClone(this._icons[e],this.size,t)},_prepareSvgClone:function(e,t,o){if(e){var n=e.cloneNode(!0),r=document.createElementNS("http://www.w3.org/2000/svg","svg"),i=n.getAttribute("viewBox")||"0 0 "+t+" "+t,s="pointer-events: none; display: block; width: 100%; height: 100%;";return o&&n.hasAttribute("mirror-in-rtl")&&(s+="-webkit-transform:scale(-1,1);transform:scale(-1,1);transform-origin:center;"),r.setAttribute("viewBox",i),r.setAttribute("preserveAspectRatio","xMidYMid meet"),r.setAttribute("focusable","false"),r.style.cssText=s,r.appendChild(n).removeAttribute("id"),r}return null}})},8878:(e,t,o)=>{o(94604),o(8621),o(63207),o(30879),o(78814),o(60748),o(57548),o(73962);var n=o(51644),r=o(26110),i=o(21006),s=o(98235),a=o(18890),l=o(9672),c=o(87156),p=o(81668),u=o(50856),d=o(62276);const h=(0,a.x)(HTMLElement);(0,l.k)({_template:u.d`
    <style include="paper-dropdown-menu-shared-styles"></style>

    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" dynamic-align="[[dynamicAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate allow-outside-scroll="[[allowOutsideScroll]]" restore-focus-on-close="[[restoreFocusOnClose]]" expand-sizing-target-for-scrollbars="[[expandSizingTargetForScrollbars]]">
      <!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> -->
      <div class="dropdown-trigger" slot="dropdown-trigger">
        <paper-ripple></paper-ripple>
        <!-- paper-input has type="text" for a11y, do not remove -->
        <paper-input id="input" type="text" invalid="[[invalid]]" readonly disabled="[[disabled]]" value="[[value]]" placeholder="[[placeholder]]" error-message="[[errorMessage]]" always-float-label="[[alwaysFloatLabel]]" no-label-float="[[noLabelFloat]]" label="[[label]]" input-role="button" input-aria-haspopup="listbox" autocomplete="off">
          <!-- support hybrid mode: user might be using paper-input 1.x which distributes via <content> -->
          <iron-icon icon="paper-dropdown-menu:arrow-drop-down" suffix slot="suffix"></iron-icon>
        </paper-input>
      </div>
      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>
    </paper-menu-button>
`,is:"paper-dropdown-menu",behaviors:[n.P,r.a,i.V,s.x],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0},expandSizingTargetForScrollbars:{type:Boolean,value:!1}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},observers:["_selectedItemChanged(selectedItem)"],_attachDom(e){const t=(0,d.r)(this);return t.attachShadow({mode:"open",delegatesFocus:!0,shadyUpgradeFragment:e}),t.shadowRoot.appendChild(e),h.prototype._attachDom.call(this,e)},focus(){this.$.input._focusableElement.focus()},attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=(0,c.vz)(this.$.content).getDistributedNodes(),t=0,o=e.length;t<o;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){p.nJ(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},25782:(e,t,o)=>{o(94604),o(65660),o(70019),o(97968);var n=o(9672),r=o(50856),i=o(33760);(0,n.k)({_template:r.d`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[i.U]})},51095:(e,t,o)=>{o(94604);var n=o(78161),r=o(9672),i=o(50856);(0,r.k)({_template:i.d`
    <style>
      :host {
        display: block;
        padding: 8px 0;

        background: var(--paper-listbox-background-color, var(--primary-background-color));
        color: var(--paper-listbox-color, var(--primary-text-color));

        @apply --paper-listbox;
      }
    </style>

    <slot></slot>
`,is:"paper-listbox",behaviors:[n.i],hostAttributes:{role:"listbox"}})}}]);
//# sourceMappingURL=8cd7770b.js.map