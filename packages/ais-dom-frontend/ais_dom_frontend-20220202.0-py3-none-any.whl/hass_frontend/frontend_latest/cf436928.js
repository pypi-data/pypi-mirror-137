/*! For license information please see cf436928.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[15088],{14166:(t,e,i)=>{i.d(e,{W:()=>o});var s=function(){return s=Object.assign||function(t){for(var e,i=1,s=arguments.length;i<s;i++)for(var o in e=arguments[i])Object.prototype.hasOwnProperty.call(e,o)&&(t[o]=e[o]);return t},s.apply(this,arguments)};function o(t,e,i){void 0===e&&(e=Date.now()),void 0===i&&(i={});var o=s(s({},n),i||{}),r=(+t-+e)/1e3;if(Math.abs(r)<o.second)return{value:Math.round(r),unit:"second"};var a=r/60;if(Math.abs(a)<o.minute)return{value:Math.round(a),unit:"minute"};var h=r/3600;if(Math.abs(h)<o.hour)return{value:Math.round(h),unit:"hour"};var l=r/86400;if(Math.abs(l)<o.day)return{value:Math.round(l),unit:"day"};var d=new Date(t),c=new Date(e),u=d.getFullYear()-c.getFullYear();if(Math.round(Math.abs(u))>0)return{value:Math.round(u),unit:"year"};var p=12*u+d.getMonth()-c.getMonth();if(Math.round(Math.abs(p))>0)return{value:Math.round(p),unit:"month"};var _=r/604800;return{value:Math.round(_),unit:"week"}}var n={second:45,minute:45,hour:22,day:5}},18601:(t,e,i)=>{i.d(e,{qN:()=>a.q,Wg:()=>l});var s,o,n=i(87480),r=i(72367),a=i(78220);const h=null!==(o=null===(s=window.ShadyDOM)||void 0===s?void 0:s.inUse)&&void 0!==o&&o;class l extends a.H{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=t=>{this.disabled||this.setFormData(t.formData)}}findFormElement(){if(!this.shadowRoot||h)return null;const t=this.getRootNode().querySelectorAll("form");for(const e of Array.from(t))if(e.contains(this))return e;return null}connectedCallback(){var t;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(t=this.containingForm)||void 0===t||t.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this.containingForm)||void 0===t||t.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(t=>{this.dispatchEvent(new Event("change",t))}))}}l.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,n.__decorate)([(0,r.Cb)({type:Boolean})],l.prototype,"disabled",void 0)},49075:(t,e,i)=>{i.d(e,{S:()=>r,B:()=>a});i(94604);var s=i(51644),o=i(26110),n=i(84938);const r={observers:["_focusedChanged(receivedFocusFromKeyboard)"],_focusedChanged:function(t){t&&this.ensureRipple(),this.hasRipple()&&(this._ripple.holdDown=t)},_createRipple:function(){var t=n.o._createRipple();return t.id="ink",t.setAttribute("center",""),t.classList.add("circle"),t}},a=[s.P,o.a,n.o,r]},84938:(t,e,i)=>{i.d(e,{o:()=>n});i(94604),i(60748);var s=i(51644),o=i(87156);const n={properties:{noink:{type:Boolean,observer:"_noinkChanged"},_rippleContainer:{type:Object}},_buttonStateChanged:function(){this.focused&&this.ensureRipple()},_downHandler:function(t){s.$._downHandler.call(this,t),this.pressed&&this.ensureRipple(t)},ensureRipple:function(t){if(!this.hasRipple()){this._ripple=this._createRipple(),this._ripple.noink=this.noink;var e=this._rippleContainer||this.root;if(e&&(0,o.vz)(e).appendChild(this._ripple),t){var i=(0,o.vz)(this._rippleContainer||this),s=(0,o.vz)(t).rootTarget;i.deepContains(s)&&this._ripple.uiDownAction(t)}}},getRipple:function(){return this.ensureRipple(),this._ripple},hasRipple:function(){return Boolean(this._ripple)},_createRipple:function(){return document.createElement("paper-ripple")},_noinkChanged:function(t){this.hasRipple()&&(this._ripple.noink=t)}}},38034:(t,e,i)=>{var s=i(87480),o=i(37500),n=i(72367);class r extends o.oi{constructor(){super(),this.min=0,this.max=100,this.step=1,this.startAngle=135,this.arcLength=270,this.handleSize=6,this.handleZoom=1.5,this.readonly=!1,this.disabled=!1,this.dragging=!1,this.rtl=!1,this._scale=1,this.dragEnd=this.dragEnd.bind(this),this.drag=this.drag.bind(this),this._keyStep=this._keyStep.bind(this)}connectedCallback(){super.connectedCallback(),document.addEventListener("mouseup",this.dragEnd),document.addEventListener("touchend",this.dragEnd,{passive:!1}),document.addEventListener("mousemove",this.drag),document.addEventListener("touchmove",this.drag,{passive:!1}),document.addEventListener("keydown",this._keyStep)}disconnectedCallback(){super.disconnectedCallback(),document.removeEventListener("mouseup",this.dragEnd),document.removeEventListener("touchend",this.dragEnd),document.removeEventListener("mousemove",this.drag),document.removeEventListener("touchmove",this.drag),document.removeEventListener("keydown",this._keyStep)}get _start(){return this.startAngle*Math.PI/180}get _len(){return Math.min(this.arcLength*Math.PI/180,2*Math.PI-.01)}get _end(){return this._start+this._len}get _showHandle(){return!this.readonly&&(null!=this.value||null!=this.high&&null!=this.low)}_angleInside(t){let e=(this.startAngle+this.arcLength/2-t+180+360)%360-180;return e<this.arcLength/2&&e>-this.arcLength/2}_angle2xy(t){return this.rtl?{x:-Math.cos(t),y:Math.sin(t)}:{x:Math.cos(t),y:Math.sin(t)}}_xy2angle(t,e){return this.rtl&&(t=-t),(Math.atan2(e,t)-this._start+2*Math.PI)%(2*Math.PI)}_value2angle(t){const e=((t=Math.min(this.max,Math.max(this.min,t)))-this.min)/(this.max-this.min);return this._start+e*this._len}_angle2value(t){return Math.round((t/this._len*(this.max-this.min)+this.min)/this.step)*this.step}get _boundaries(){const t=this._angle2xy(this._start),e=this._angle2xy(this._end);let i=1;this._angleInside(270)||(i=Math.max(-t.y,-e.y));let s=1;this._angleInside(90)||(s=Math.max(t.y,e.y));let o=1;this._angleInside(180)||(o=Math.max(-t.x,-e.x));let n=1;return this._angleInside(0)||(n=Math.max(t.x,e.x)),{up:i,down:s,left:o,right:n,height:i+s,width:o+n}}_mouse2value(t){const e=t.type.startsWith("touch")?t.touches[0].clientX:t.clientX,i=t.type.startsWith("touch")?t.touches[0].clientY:t.clientY,s=this.shadowRoot.querySelector("svg").getBoundingClientRect(),o=this._boundaries,n=e-(s.left+o.left*s.width/o.width),r=i-(s.top+o.up*s.height/o.height),a=this._xy2angle(n,r);return this._angle2value(a)}dragStart(t){if(!this._showHandle||this.disabled)return;let e,i=t.target;if(this._rotation&&"focus"!==this._rotation.type)return;if(i.classList.contains("shadowpath"))if("touchstart"===t.type&&(e=window.setTimeout((()=>{this._rotation&&(this._rotation.cooldown=void 0)}),200)),null==this.low)i=this.shadowRoot.querySelector("#value");else{const e=this._mouse2value(t);i=Math.abs(e-this.low)<Math.abs(e-this.high)?this.shadowRoot.querySelector("#low"):this.shadowRoot.querySelector("#high")}if(i.classList.contains("overflow")&&(i=i.nextElementSibling),!i.classList.contains("handle"))return;i.setAttribute("stroke-width",String(2*this.handleSize*this.handleZoom*this._scale));const s="high"===i.id?this.low:this.min,o="low"===i.id?this.high:this.max;this._rotation={handle:i,min:s,max:o,start:this[i.id],type:t.type,cooldown:e},this.dragging=!0}_cleanupRotation(){const t=this._rotation.handle;t.setAttribute("stroke-width",String(2*this.handleSize*this._scale)),this._rotation=void 0,this.dragging=!1,t.blur()}dragEnd(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;const e=this._rotation.handle;this._cleanupRotation();let i=new CustomEvent("value-changed",{detail:{[e.id]:this[e.id]},bubbles:!0,composed:!0});this.dispatchEvent(i),this.low&&this.low>=.99*this.max?this._reverseOrder=!0:this._reverseOrder=!1}drag(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;if(this._rotation.cooldown)return window.clearTimeout(this._rotation.cooldown),void this._cleanupRotation();if("focus"===this._rotation.type)return;t.preventDefault();const e=this._mouse2value(t);this._dragpos(e)}_dragpos(t){if(t<this._rotation.min||t>this._rotation.max)return;const e=this._rotation.handle;this[e.id]=t;let i=new CustomEvent("value-changing",{detail:{[e.id]:t},bubbles:!0,composed:!0});this.dispatchEvent(i)}_keyStep(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;const e=this._rotation.handle;"ArrowLeft"!==t.key&&"ArrowDown"!==t.key||(t.preventDefault(),this.rtl?this._dragpos(this[e.id]+this.step):this._dragpos(this[e.id]-this.step)),"ArrowRight"!==t.key&&"ArrowUp"!==t.key||(t.preventDefault(),this.rtl?this._dragpos(this[e.id]-this.step):this._dragpos(this[e.id]+this.step)),"Home"===t.key&&(t.preventDefault(),this._dragpos(this.min)),"End"===t.key&&(t.preventDefault(),this._dragpos(this.max))}updated(t){if(this.shadowRoot.querySelector(".slider")){const t=window.getComputedStyle(this.shadowRoot.querySelector(".slider"));if(t&&t.strokeWidth){const e=parseFloat(t.strokeWidth);if(e>this.handleSize*this.handleZoom){const t=this._boundaries,i=`\n          ${e/2*Math.abs(t.up)}px\n          ${e/2*Math.abs(t.right)}px\n          ${e/2*Math.abs(t.down)}px\n          ${e/2*Math.abs(t.left)}px`;this.shadowRoot.querySelector("svg").style.margin=i}}}if(this.shadowRoot.querySelector("svg")&&void 0===this.shadowRoot.querySelector("svg").style.vectorEffect){t.has("_scale")&&1!=this._scale&&this.shadowRoot.querySelector("svg").querySelectorAll("path").forEach((t=>{if(t.getAttribute("stroke-width"))return;const e=parseFloat(getComputedStyle(t).getPropertyValue("stroke-width"));t.style.strokeWidth=e*this._scale+"px"}));const e=this.shadowRoot.querySelector("svg").getBoundingClientRect(),i=Math.max(e.width,e.height);this._scale=2/i}}_renderArc(t,e){const i=e-t,s=this._angle2xy(t),o=this._angle2xy(e+.001);return`\n      M ${s.x} ${s.y}\n      A 1 1,\n        0,\n        ${i>Math.PI?"1":"0"} ${this.rtl?"0":"1"},\n        ${o.x} ${o.y}\n    `}_renderHandle(t){const e=this._value2angle(this[t]),i=this._angle2xy(e),s={value:this.valueLabel,low:this.lowLabel,high:this.highLabel}[t]||"";return o.YP`
      <g class="${t} handle">
        <path
          id=${t}
          class="overflow"
          d="
          M ${i.x} ${i.y}
          L ${i.x+.001} ${i.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke="rgba(0,0,0,0)"
          stroke-width="${4*this.handleSize*this._scale}"
          />
        <path
          id=${t}
          class="handle"
          d="
          M ${i.x} ${i.y}
          L ${i.x+.001} ${i.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke-width="${2*this.handleSize*this._scale}"
          tabindex="0"
          @focus=${this.dragStart}
          @blur=${this.dragEnd}
          role="slider"
          aria-valuemin=${this.min}
          aria-valuemax=${this.max}
          aria-valuenow=${this[t]}
          aria-disabled=${this.disabled}
          aria-label=${s||""}
          />
        </g>
      `}render(){const t=this._boundaries;return o.dy`
      <svg
        @mousedown=${this.dragStart}
        @touchstart=${this.dragStart}
        xmln="http://www.w3.org/2000/svg"
        viewBox="${-t.left} ${-t.up} ${t.width} ${t.height}"
        style="margin: ${this.handleSize*this.handleZoom}px;"
        ?disabled=${this.disabled}
        focusable="false"
      >
        <g class="slider">
          <path
            class="path"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
          />
          <path
            class="bar"
            vector-effect="non-scaling-stroke"
            d=${this._renderArc(this._value2angle(null!=this.low?this.low:this.min),this._value2angle(null!=this.high?this.high:this.value))}
          />
          <path
            class="shadowpath"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
            stroke="rgba(0,0,0,0)"
            stroke-width="${3*this.handleSize*this._scale}"
            stroke-linecap="butt"
          />
        </g>

        <g class="handles">
          ${this._showHandle?null!=this.low?this._reverseOrder?o.YP`${this._renderHandle("high")} ${this._renderHandle("low")}`:o.YP`${this._renderHandle("low")} ${this._renderHandle("high")}`:o.YP`${this._renderHandle("value")}`:""}
        </g>
      </svg>
    `}static get styles(){return o.iv`
      :host {
        display: inline-block;
        width: 100%;
      }
      svg {
        overflow: visible;
        display: block;
      }
      path {
        transition: stroke 1s ease-out, stroke-width 200ms ease-out;
      }
      .slider {
        fill: none;
        stroke-width: var(--round-slider-path-width, 3);
        stroke-linecap: var(--round-slider-linecap, round);
      }
      .path {
        stroke: var(--round-slider-path-color, lightgray);
      }
      .bar {
        stroke: var(--round-slider-bar-color, deepskyblue);
      }
      svg[disabled] .bar {
        stroke: var(--round-slider-disabled-bar-color, darkgray);
      }
      g.handles {
        stroke: var(
          --round-slider-handle-color,
          var(--round-slider-bar-color, deepskyblue)
        );
        stroke-linecap: round;
        cursor: var(--round-slider-handle-cursor, pointer);
      }
      g.low.handle {
        stroke: var(--round-slider-low-handle-color);
      }
      g.high.handle {
        stroke: var(--round-slider-high-handle-color);
      }
      svg[disabled] g.handles {
        stroke: var(--round-slider-disabled-bar-color, darkgray);
      }
      .handle:focus {
        outline: unset;
      }
    `}}(0,s.__decorate)([(0,n.Cb)({type:Number})],r.prototype,"value",void 0),(0,s.__decorate)([(0,n.Cb)({type:Number})],r.prototype,"high",void 0),(0,s.__decorate)([(0,n.Cb)({type:Number})],r.prototype,"low",void 0),(0,s.__decorate)([(0,n.Cb)({type:Number})],r.prototype,"min",void 0),(0,s.__decorate)([(0,n.Cb)({type:Number})],r.prototype,"max",void 0),(0,s.__decorate)([(0,n.Cb)({type:Number})],r.prototype,"step",void 0),(0,s.__decorate)([(0,n.Cb)({type:Number})],r.prototype,"startAngle",void 0),(0,s.__decorate)([(0,n.Cb)({type:Number})],r.prototype,"arcLength",void 0),(0,s.__decorate)([(0,n.Cb)({type:Number})],r.prototype,"handleSize",void 0),(0,s.__decorate)([(0,n.Cb)({type:Number})],r.prototype,"handleZoom",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean})],r.prototype,"readonly",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean})],r.prototype,"disabled",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],r.prototype,"dragging",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean})],r.prototype,"rtl",void 0),(0,s.__decorate)([(0,n.Cb)()],r.prototype,"valueLabel",void 0),(0,s.__decorate)([(0,n.Cb)()],r.prototype,"lowLabel",void 0),(0,s.__decorate)([(0,n.Cb)()],r.prototype,"highLabel",void 0),(0,s.__decorate)([(0,n.SB)()],r.prototype,"_scale",void 0),customElements.define("round-slider",r)},19596:(t,e,i)=>{i.d(e,{s:()=>c});var s=i(81563),o=i(38941);const n=(t,e)=>{var i,s;const o=t._$AN;if(void 0===o)return!1;for(const t of o)null===(s=(i=t)._$AO)||void 0===s||s.call(i,e,!1),n(t,e);return!0},r=t=>{let e,i;do{if(void 0===(e=t._$AM))break;i=e._$AN,i.delete(t),t=e}while(0===(null==i?void 0:i.size))},a=t=>{for(let e;e=t._$AM;t=e){let i=e._$AN;if(void 0===i)e._$AN=i=new Set;else if(i.has(t))break;i.add(t),d(e)}};function h(t){void 0!==this._$AN?(r(this),this._$AM=t,a(this)):this._$AM=t}function l(t,e=!1,i=0){const s=this._$AH,o=this._$AN;if(void 0!==o&&0!==o.size)if(e)if(Array.isArray(s))for(let t=i;t<s.length;t++)n(s[t],!1),r(s[t]);else null!=s&&(n(s,!1),r(s));else n(this,t)}const d=t=>{var e,i,s,n;t.type==o.pX.CHILD&&(null!==(e=(s=t)._$AP)&&void 0!==e||(s._$AP=l),null!==(i=(n=t)._$AQ)&&void 0!==i||(n._$AQ=h))};class c extends o.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,e,i){super._$AT(t,e,i),a(this),this.isConnected=t._$AU}_$AO(t,e=!0){var i,s;t!==this.isConnected&&(this.isConnected=t,t?null===(i=this.reconnected)||void 0===i||i.call(this):null===(s=this.disconnected)||void 0===s||s.call(this)),e&&(n(this,t),r(this))}setValue(t){if((0,s.OR)(this._$Ct))this._$Ct._$AI(t,this);else{const e=[...this._$Ct._$AH];e[this._$Ci]=t,this._$Ct._$AI(e,this,0)}}disconnected(){}reconnected(){}}},81563:(t,e,i)=>{i.d(e,{E_:()=>v,i9:()=>p,_Y:()=>l,pt:()=>n,OR:()=>a,hN:()=>r,ws:()=>_,fk:()=>d,hl:()=>u});var s=i(15304);const{H:o}=s.Al,n=t=>null===t||"object"!=typeof t&&"function"!=typeof t,r=(t,e)=>{var i,s;return void 0===e?void 0!==(null===(i=t)||void 0===i?void 0:i._$litType$):(null===(s=t)||void 0===s?void 0:s._$litType$)===e},a=t=>void 0===t.strings,h=()=>document.createComment(""),l=(t,e,i)=>{var s;const n=t._$AA.parentNode,r=void 0===e?t._$AB:e._$AA;if(void 0===i){const e=n.insertBefore(h(),r),s=n.insertBefore(h(),r);i=new o(e,s,t,t.options)}else{const e=i._$AB.nextSibling,o=i._$AM,a=o!==t;if(a){let e;null===(s=i._$AQ)||void 0===s||s.call(i,t),i._$AM=t,void 0!==i._$AP&&(e=t._$AU)!==o._$AU&&i._$AP(e)}if(e!==r||a){let t=i._$AA;for(;t!==e;){const e=t.nextSibling;n.insertBefore(t,r),t=e}}}return i},d=(t,e,i=t)=>(t._$AI(e,i),t),c={},u=(t,e=c)=>t._$AH=e,p=t=>t._$AH,_=t=>{var e;null===(e=t._$AP)||void 0===e||e.call(t,!1,!0);let i=t._$AA;const s=t._$AB.nextSibling;for(;i!==s;){const t=i.nextSibling;i.remove(),i=t}},v=t=>{t._$AR()}},57835:(t,e,i)=>{i.d(e,{Xe:()=>s.Xe,pX:()=>s.pX,XM:()=>s.XM});var s=i(38941)}}]);
//# sourceMappingURL=cf436928.js.map