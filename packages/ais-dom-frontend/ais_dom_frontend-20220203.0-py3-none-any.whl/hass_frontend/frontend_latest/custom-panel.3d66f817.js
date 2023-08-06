/*! For license information please see custom-panel.3d66f817.js.LICENSE.txt */
(()=>{var e,t,r={47181:(e,t,r)=>{"use strict";r.d(t,{B:()=>o});const o=(e,t,r,o)=>{o=o||{},r=null==r?{}:r;const i=new Event(t,{bubbles:void 0===o.bubbles||o.bubbles,cancelable:Boolean(o.cancelable),composed:void 0===o.composed||o.composed});return i.detail=r,e.dispatchEvent(i),i}},37846:()=>{if(/^((?!chrome|android).)*version\/14\.0\s.*safari/i.test(navigator.userAgent)){const e=window.Element.prototype.attachShadow;window.Element.prototype.attachShadow=function(t){return t&&t.delegatesFocus&&delete t.delegatesFocus,e.apply(this,[t])}}},11654:(e,t,r)=>{"use strict";r.d(t,{_l:()=>i,q0:()=>n,Qx:()=>a,e$:()=>s});var o=r(37500);const i={"primary-background-color":"#111111","card-background-color":"#1c1c1c","secondary-background-color":"#202020","primary-text-color":"#e1e1e1","secondary-text-color":"#9b9b9b","disabled-text-color":"#6f6f6f","app-header-text-color":"#e1e1e1","app-header-background-color":"#101e24","switch-unchecked-button-color":"#999999","switch-unchecked-track-color":"#9b9b9b","divider-color":"rgba(225, 225, 225, .12)","mdc-ripple-color":"#AAAAAA","input-idle-line-color":"rgba(255, 255, 255, 0.42)","input-hover-line-color":"rgba(255, 255, 255, 0.87)","input-disabled-line-color":"rgba(255, 255, 255, 0.06)","input-outlined-idle-border-color":"rgba(255, 255, 255, 0.38)","input-outlined-hover-border-color":"rgba(255, 255, 255, 0.87)","input-outlined-disabled-border-color":"rgba(255, 255, 255, 0.06)","input-fill-color":"rgba(255, 255, 255, 0.05)","input-disabled-fill-color":"rgba(255, 255, 255, 0.02)","input-ink-color":"rgba(255, 255, 255, 0.87)","input-label-ink-color":"rgba(255, 255, 255, 0.6)","input-disabled-ink-color":"rgba(255, 255, 255, 0.37)","input-dropdown-icon-color":"rgba(255, 255, 255, 0.54)","codemirror-keyword":"#C792EA","codemirror-operator":"#89DDFF","codemirror-variable":"#f07178","codemirror-variable-2":"#EEFFFF","codemirror-variable-3":"#DECB6B","codemirror-builtin":"#FFCB6B","codemirror-atom":"#F78C6C","codemirror-number":"#FF5370","codemirror-def":"#82AAFF","codemirror-string":"#C3E88D","codemirror-string-2":"#f07178","codemirror-comment":"#545454","codemirror-tag":"#FF5370","codemirror-meta":"#FFCB6B","codemirror-attribute":"#C792EA","codemirror-property":"#C792EA","codemirror-qualifier":"#DECB6B","codemirror-type":"#DECB6B","energy-grid-return-color":"#a280db"},n={"state-icon-error-color":"var(--error-state-color, var(--error-color))","state-unavailable-color":"var(--state-icon-unavailable-color, var(--disabled-text-color))","sidebar-text-color":"var(--primary-text-color)","sidebar-background-color":"var(--card-background-color)","sidebar-selected-text-color":"var(--primary-color)","sidebar-selected-icon-color":"var(--primary-color)","sidebar-icon-color":"rgba(var(--rgb-primary-text-color), 0.6)","switch-checked-color":"var(--primary-color)","switch-checked-button-color":"var(--switch-checked-color, var(--primary-background-color))","switch-checked-track-color":"var(--switch-checked-color, #000000)","switch-unchecked-button-color":"var(--switch-unchecked-color, var(--primary-background-color))","switch-unchecked-track-color":"var(--switch-unchecked-color, #000000)","slider-color":"var(--primary-color)","slider-secondary-color":"var(--light-primary-color)","slider-track-color":"var(--scrollbar-thumb-color)","label-badge-background-color":"var(--card-background-color)","label-badge-text-color":"rgba(var(--rgb-primary-text-color), 0.8)","paper-listbox-background-color":"var(--card-background-color)","paper-item-icon-color":"var(--state-icon-color)","paper-item-icon-active-color":"var(--state-icon-active-color)","table-row-background-color":"var(--primary-background-color)","table-row-alternative-background-color":"var(--secondary-background-color)","paper-slider-knob-color":"var(--slider-color)","paper-slider-knob-start-color":"var(--slider-color)","paper-slider-pin-color":"var(--slider-color)","paper-slider-pin-start-color":"var(--slider-color)","paper-slider-active-color":"var(--slider-color)","paper-slider-secondary-color":"var(--slider-secondary-color)","paper-slider-container-color":"var(--slider-track-color)","data-table-background-color":"var(--card-background-color)","markdown-code-background-color":"var(--primary-background-color)","mdc-theme-primary":"var(--primary-color)","mdc-theme-secondary":"var(--accent-color)","mdc-theme-background":"var(--primary-background-color)","mdc-theme-surface":"var(--card-background-color)","mdc-theme-on-primary":"var(--text-primary-color)","mdc-theme-on-secondary":"var(--text-primary-color)","mdc-theme-on-surface":"var(--primary-text-color)","mdc-theme-text-disabled-on-light":"var(--disabled-text-color)","mdc-theme-text-primary-on-background":"var(--primary-text-color)","mdc-theme-text-secondary-on-background":"var(--secondary-text-color)","mdc-theme-text-hint-on-background":"var(--secondary-text-color)","mdc-theme-text-icon-on-background":"var(--secondary-text-color)","mdc-theme-error":"var(--error-color)","app-header-text-color":"var(--text-primary-color)","app-header-background-color":"var(--primary-color)","mdc-checkbox-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-checkbox-disabled-color":"var(--disabled-text-color)","mdc-radio-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-radio-disabled-color":"var(--disabled-text-color)","mdc-tab-text-label-color-default":"var(--primary-text-color)","mdc-button-disabled-ink-color":"var(--disabled-text-color)","mdc-button-outline-color":"var(--divider-color)","mdc-dialog-scroll-divider-color":"var(--divider-color)","mdc-text-field-idle-line-color":"var(--input-idle-line-color)","mdc-text-field-hover-line-color":"var(--input-hover-line-color)","mdc-text-field-disabled-line-color":"var(--input-disabled-line-color)","mdc-text-field-outlined-idle-border-color":"var(--input-outlined-idle-border-color)","mdc-text-field-outlined-hover-border-color":"var(--input-outlined-hover-border-color)","mdc-text-field-outlined-disabled-border-color":"var(--input-outlined-disabled-border-color)","mdc-text-field-fill-color":"var(--input-fill-color)","mdc-text-field-disabled-fill-color":"var(--input-disabled-fill-color)","mdc-text-field-ink-color":"var(--input-ink-color)","mdc-text-field-label-ink-color":"var(--input-label-ink-color)","mdc-text-field-disabled-ink-color":"var(--input-disabled-ink-color)","mdc-select-idle-line-color":"var(--input-idle-line-color)","mdc-select-hover-line-color":"var(--input-hover-line-color)","mdc-select-outlined-idle-border-color":"var(--input-outlined-idle-border-color)","mdc-select-outlined-hover-border-color":"var(--input-outlined-hover-border-color)","mdc-select-outlined-disabled-border-color":"var(--input-outlined-disabled-border-color)","mdc-select-fill-color":"var(--input-fill-color)","mdc-select-disabled-fill-color":"var(--input-disabled-fill-color)","mdc-select-ink-color":"var(--input-ink-color)","mdc-select-label-ink-color":"var(--input-label-ink-color)","mdc-select-disabled-ink-color":"var(--input-disabled-ink-color)","mdc-select-dropdown-icon-color":"var(--input-dropdown-icon-color)","mdc-select-disabled-dropdown-icon-color":"var(--input-disabled-ink-color)","chip-background-color":"rgba(var(--rgb-primary-text-color), 0.15)","material-body-text-color":"var(--primary-text-color)","material-background-color":"var(--card-background-color)","material-secondary-background-color":"var(--secondary-background-color)","material-secondary-text-color":"var(--secondary-text-color)"},l=o.iv`
  button.link {
    background: none;
    color: inherit;
    border: none;
    padding: 0;
    font: inherit;
    text-align: left;
    text-decoration: underline;
    cursor: pointer;
  }
`,a=o.iv`
  :host {
    font-family: var(--paper-font-body1_-_font-family);
    -webkit-font-smoothing: var(--paper-font-body1_-_-webkit-font-smoothing);
    font-size: var(--paper-font-body1_-_font-size);
    font-weight: var(--paper-font-body1_-_font-weight);
    line-height: var(--paper-font-body1_-_line-height);
  }

  app-header-layout,
  ha-app-layout {
    background-color: var(--primary-background-color);
  }

  app-header,
  app-toolbar {
    background-color: var(--app-header-background-color);
    font-weight: 400;
    color: var(--app-header-text-color, white);
  }

  app-toolbar {
    height: var(--header-height);
    border-bottom: var(--app-header-border-bottom);
    box-sizing: border-box;
  }

  app-header div[sticky] {
    height: 48px;
  }

  app-toolbar [main-title] {
    margin-left: 20px;
  }

  h1 {
    font-family: var(--paper-font-headline_-_font-family);
    -webkit-font-smoothing: var(--paper-font-headline_-_-webkit-font-smoothing);
    white-space: var(--paper-font-headline_-_white-space);
    overflow: var(--paper-font-headline_-_overflow);
    text-overflow: var(--paper-font-headline_-_text-overflow);
    font-size: var(--paper-font-headline_-_font-size);
    font-weight: var(--paper-font-headline_-_font-weight);
    line-height: var(--paper-font-headline_-_line-height);
  }

  h2 {
    font-family: var(--paper-font-title_-_font-family);
    -webkit-font-smoothing: var(--paper-font-title_-_-webkit-font-smoothing);
    white-space: var(--paper-font-title_-_white-space);
    overflow: var(--paper-font-title_-_overflow);
    text-overflow: var(--paper-font-title_-_text-overflow);
    font-size: var(--paper-font-title_-_font-size);
    font-weight: var(--paper-font-title_-_font-weight);
    line-height: var(--paper-font-title_-_line-height);
  }

  h3 {
    font-family: var(--paper-font-subhead_-_font-family);
    -webkit-font-smoothing: var(--paper-font-subhead_-_-webkit-font-smoothing);
    white-space: var(--paper-font-subhead_-_white-space);
    overflow: var(--paper-font-subhead_-_overflow);
    text-overflow: var(--paper-font-subhead_-_text-overflow);
    font-size: var(--paper-font-subhead_-_font-size);
    font-weight: var(--paper-font-subhead_-_font-weight);
    line-height: var(--paper-font-subhead_-_line-height);
  }

  a {
    color: var(--primary-color);
  }

  .secondary {
    color: var(--secondary-text-color);
  }

  .error {
    color: var(--error-color);
  }

  .warning {
    color: var(--error-color);
  }

  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }

  ${l}

  .card-actions a {
    text-decoration: none;
  }

  .card-actions .warning {
    --mdc-theme-primary: var(--error-color);
  }

  .layout.horizontal,
  .layout.vertical {
    display: flex;
  }
  .layout.inline {
    display: inline-flex;
  }
  .layout.horizontal {
    flex-direction: row;
  }
  .layout.vertical {
    flex-direction: column;
  }
  .layout.wrap {
    flex-wrap: wrap;
  }
  .layout.no-wrap {
    flex-wrap: nowrap;
  }
  .layout.center,
  .layout.center-center {
    align-items: center;
  }
  .layout.bottom {
    align-items: flex-end;
  }
  .layout.center-justified,
  .layout.center-center {
    justify-content: center;
  }
  .flex {
    flex: 1;
    flex-basis: 0.000000001px;
  }
  .flex-auto {
    flex: 1 1 auto;
  }
  .flex-none {
    flex: none;
  }
  .layout.justified {
    justify-content: space-between;
  }
`,s=(o.iv`
  /* mwc-dialog (ha-dialog) styles */
  ha-dialog {
    --mdc-dialog-min-width: 400px;
    --mdc-dialog-max-width: 600px;
    --mdc-dialog-heading-ink-color: var(--primary-text-color);
    --mdc-dialog-content-ink-color: var(--primary-text-color);
    --justify-action-buttons: space-between;
  }

  ha-dialog .form {
    padding-bottom: 24px;
    color: var(--primary-text-color);
  }

  a {
    color: var(--primary-color);
  }

  /* make dialog fullscreen on small screens */
  @media all and (max-width: 450px), all and (max-height: 500px) {
    ha-dialog {
      --mdc-dialog-min-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-max-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-min-height: 100%;
      --mdc-dialog-max-height: 100%;
      --vertial-align-dialog: flex-end;
      --ha-dialog-border-radius: 0px;
    }
  }
  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }
  .error {
    color: var(--error-color);
  }
`,o.iv`
  .ha-scrollbar::-webkit-scrollbar {
    width: 0.4rem;
    height: 0.4rem;
  }

  .ha-scrollbar::-webkit-scrollbar-thumb {
    -webkit-border-radius: 4px;
    border-radius: 4px;
    background: var(--scrollbar-thumb-color);
  }

  .ha-scrollbar {
    overflow-y: auto;
    scrollbar-color: var(--scrollbar-thumb-color) transparent;
    scrollbar-width: thin;
  }
`,o.iv`
  body {
    background-color: var(--primary-background-color);
    color: var(--primary-text-color);
    height: calc(100vh - 32px);
    width: 100vw;
  }
`)},15304:(e,t,r)=>{"use strict";var o;r.d(t,{dy:()=>$,Jb:()=>A,Ld:()=>k,sY:()=>S,YP:()=>x});const i=globalThis.trustedTypes,n=i?i.createPolicy("lit-html",{createHTML:e=>e}):void 0,l=`lit$${(Math.random()+"").slice(9)}$`,a="?"+l,s=`<${a}>`,c=document,d=(e="")=>c.createComment(e),h=e=>null===e||"object"!=typeof e&&"function"!=typeof e,p=Array.isArray,u=e=>{var t;return p(e)||"function"==typeof(null===(t=e)||void 0===t?void 0:t[Symbol.iterator])},v=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,m=/-->/g,b=/>/g,f=/>|[ 	\n\r](?:([^\s"'>=/]+)([ 	\n\r]*=[ 	\n\r]*(?:[^ 	\n\r"'`<>=]|("|')|))|$)/g,g=/'/g,y=/"/g,_=/^(?:script|style|textarea)$/i,w=e=>(t,...r)=>({_$litType$:e,strings:t,values:r}),$=w(1),x=w(2),A=Symbol.for("lit-noChange"),k=Symbol.for("lit-nothing"),E=new WeakMap,S=(e,t,r)=>{var o,i;const n=null!==(o=null==r?void 0:r.renderBefore)&&void 0!==o?o:t;let l=n._$litPart$;if(void 0===l){const e=null!==(i=null==r?void 0:r.renderBefore)&&void 0!==i?i:null;n._$litPart$=l=new O(t.insertBefore(d(),e),e,void 0,null!=r?r:{})}return l._$AI(e),l},C=c.createTreeWalker(c,129,null,!1),P=(e,t)=>{const r=e.length-1,o=[];let i,a=2===t?"<svg>":"",c=v;for(let t=0;t<r;t++){const r=e[t];let n,d,h=-1,p=0;for(;p<r.length&&(c.lastIndex=p,d=c.exec(r),null!==d);)p=c.lastIndex,c===v?"!--"===d[1]?c=m:void 0!==d[1]?c=b:void 0!==d[2]?(_.test(d[2])&&(i=RegExp("</"+d[2],"g")),c=f):void 0!==d[3]&&(c=f):c===f?">"===d[0]?(c=null!=i?i:v,h=-1):void 0===d[1]?h=-2:(h=c.lastIndex-d[2].length,n=d[1],c=void 0===d[3]?f:'"'===d[3]?y:g):c===y||c===g?c=f:c===m||c===b?c=v:(c=f,i=void 0);const u=c===f&&e[t+1].startsWith("/>")?" ":"";a+=c===v?r+s:h>=0?(o.push(n),r.slice(0,h)+"$lit$"+r.slice(h)+l+u):r+l+(-2===h?(o.push(void 0),t):u)}const d=a+(e[r]||"<?>")+(2===t?"</svg>":"");if(!Array.isArray(e)||!e.hasOwnProperty("raw"))throw Error("invalid template strings array");return[void 0!==n?n.createHTML(d):d,o]};class U{constructor({strings:e,_$litType$:t},r){let o;this.parts=[];let n=0,s=0;const c=e.length-1,h=this.parts,[p,u]=P(e,t);if(this.el=U.createElement(p,r),C.currentNode=this.el.content,2===t){const e=this.el.content,t=e.firstChild;t.remove(),e.append(...t.childNodes)}for(;null!==(o=C.nextNode())&&h.length<c;){if(1===o.nodeType){if(o.hasAttributes()){const e=[];for(const t of o.getAttributeNames())if(t.endsWith("$lit$")||t.startsWith(l)){const r=u[s++];if(e.push(t),void 0!==r){const e=o.getAttribute(r.toLowerCase()+"$lit$").split(l),t=/([.?@])?(.*)/.exec(r);h.push({type:1,index:n,name:t[2],strings:e,ctor:"."===t[1]?M:"?"===t[1]?B:"@"===t[1]?R:N})}else h.push({type:6,index:n})}for(const t of e)o.removeAttribute(t)}if(_.test(o.tagName)){const e=o.textContent.split(l),t=e.length-1;if(t>0){o.textContent=i?i.emptyScript:"";for(let r=0;r<t;r++)o.append(e[r],d()),C.nextNode(),h.push({type:2,index:++n});o.append(e[t],d())}}}else if(8===o.nodeType)if(o.data===a)h.push({type:2,index:n});else{let e=-1;for(;-1!==(e=o.data.indexOf(l,e+1));)h.push({type:7,index:n}),e+=l.length-1}n++}}static createElement(e,t){const r=c.createElement("template");return r.innerHTML=e,r}}function T(e,t,r=e,o){var i,n,l,a;if(t===A)return t;let s=void 0!==o?null===(i=r._$Cl)||void 0===i?void 0:i[o]:r._$Cu;const c=h(t)?void 0:t._$litDirective$;return(null==s?void 0:s.constructor)!==c&&(null===(n=null==s?void 0:s._$AO)||void 0===n||n.call(s,!1),void 0===c?s=void 0:(s=new c(e),s._$AT(e,r,o)),void 0!==o?(null!==(l=(a=r)._$Cl)&&void 0!==l?l:a._$Cl=[])[o]=s:r._$Cu=s),void 0!==s&&(t=T(e,s._$AS(e,t.values),s,o)),t}class H{constructor(e,t){this.v=[],this._$AN=void 0,this._$AD=e,this._$AM=t}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}p(e){var t;const{el:{content:r},parts:o}=this._$AD,i=(null!==(t=null==e?void 0:e.creationScope)&&void 0!==t?t:c).importNode(r,!0);C.currentNode=i;let n=C.nextNode(),l=0,a=0,s=o[0];for(;void 0!==s;){if(l===s.index){let t;2===s.type?t=new O(n,n.nextSibling,this,e):1===s.type?t=new s.ctor(n,s.name,s.strings,this,e):6===s.type&&(t=new L(n,this,e)),this.v.push(t),s=o[++a]}l!==(null==s?void 0:s.index)&&(n=C.nextNode(),l++)}return i}m(e){let t=0;for(const r of this.v)void 0!==r&&(void 0!==r.strings?(r._$AI(e,r,t),t+=r.strings.length-2):r._$AI(e[t])),t++}}class O{constructor(e,t,r,o){var i;this.type=2,this._$AH=k,this._$AN=void 0,this._$AA=e,this._$AB=t,this._$AM=r,this.options=o,this._$Cg=null===(i=null==o?void 0:o.isConnected)||void 0===i||i}get _$AU(){var e,t;return null!==(t=null===(e=this._$AM)||void 0===e?void 0:e._$AU)&&void 0!==t?t:this._$Cg}get parentNode(){let e=this._$AA.parentNode;const t=this._$AM;return void 0!==t&&11===e.nodeType&&(e=t.parentNode),e}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,t=this){e=T(this,e,t),h(e)?e===k||null==e||""===e?(this._$AH!==k&&this._$AR(),this._$AH=k):e!==this._$AH&&e!==A&&this.$(e):void 0!==e._$litType$?this.T(e):void 0!==e.nodeType?this.S(e):u(e)?this.A(e):this.$(e)}M(e,t=this._$AB){return this._$AA.parentNode.insertBefore(e,t)}S(e){this._$AH!==e&&(this._$AR(),this._$AH=this.M(e))}$(e){this._$AH!==k&&h(this._$AH)?this._$AA.nextSibling.data=e:this.S(c.createTextNode(e)),this._$AH=e}T(e){var t;const{values:r,_$litType$:o}=e,i="number"==typeof o?this._$AC(e):(void 0===o.el&&(o.el=U.createElement(o.h,this.options)),o);if((null===(t=this._$AH)||void 0===t?void 0:t._$AD)===i)this._$AH.m(r);else{const e=new H(i,this),t=e.p(this.options);e.m(r),this.S(t),this._$AH=e}}_$AC(e){let t=E.get(e.strings);return void 0===t&&E.set(e.strings,t=new U(e)),t}A(e){p(this._$AH)||(this._$AH=[],this._$AR());const t=this._$AH;let r,o=0;for(const i of e)o===t.length?t.push(r=new O(this.M(d()),this.M(d()),this,this.options)):r=t[o],r._$AI(i),o++;o<t.length&&(this._$AR(r&&r._$AB.nextSibling,o),t.length=o)}_$AR(e=this._$AA.nextSibling,t){var r;for(null===(r=this._$AP)||void 0===r||r.call(this,!1,!0,t);e&&e!==this._$AB;){const t=e.nextSibling;e.remove(),e=t}}setConnected(e){var t;void 0===this._$AM&&(this._$Cg=e,null===(t=this._$AP)||void 0===t||t.call(this,e))}}class N{constructor(e,t,r,o,i){this.type=1,this._$AH=k,this._$AN=void 0,this.element=e,this.name=t,this._$AM=o,this.options=i,r.length>2||""!==r[0]||""!==r[1]?(this._$AH=Array(r.length-1).fill(new String),this.strings=r):this._$AH=k}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(e,t=this,r,o){const i=this.strings;let n=!1;if(void 0===i)e=T(this,e,t,0),n=!h(e)||e!==this._$AH&&e!==A,n&&(this._$AH=e);else{const o=e;let l,a;for(e=i[0],l=0;l<i.length-1;l++)a=T(this,o[r+l],t,l),a===A&&(a=this._$AH[l]),n||(n=!h(a)||a!==this._$AH[l]),a===k?e=k:e!==k&&(e+=(null!=a?a:"")+i[l+1]),this._$AH[l]=a}n&&!o&&this.k(e)}k(e){e===k?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=e?e:"")}}class M extends N{constructor(){super(...arguments),this.type=3}k(e){this.element[this.name]=e===k?void 0:e}}const j=i?i.emptyScript:"";class B extends N{constructor(){super(...arguments),this.type=4}k(e){e&&e!==k?this.element.setAttribute(this.name,j):this.element.removeAttribute(this.name)}}class R extends N{constructor(e,t,r,o,i){super(e,t,r,o,i),this.type=5}_$AI(e,t=this){var r;if((e=null!==(r=T(this,e,t,0))&&void 0!==r?r:k)===A)return;const o=this._$AH,i=e===k&&o!==k||e.capture!==o.capture||e.once!==o.once||e.passive!==o.passive,n=e!==k&&(o===k||i);i&&this.element.removeEventListener(this.name,this,o),n&&this.element.addEventListener(this.name,this,e),this._$AH=e}handleEvent(e){var t,r;"function"==typeof this._$AH?this._$AH.call(null!==(r=null===(t=this.options)||void 0===t?void 0:t.host)&&void 0!==r?r:this.element,e):this._$AH.handleEvent(e)}}class L{constructor(e,t,r){this.element=e,this.type=6,this._$AN=void 0,this._$AM=t,this.options=r}get _$AU(){return this._$AM._$AU}_$AI(e){T(this,e)}}const z=window.litHtmlPolyfillSupport;null==z||z(U,O),(null!==(o=globalThis.litHtmlVersions)&&void 0!==o?o:globalThis.litHtmlVersions=[]).push("2.1.2")},37500:(e,t,r)=>{"use strict";r.d(t,{oi:()=>w,iv:()=>s,dy:()=>_.dy,YP:()=>_.YP});const o=window.ShadowRoot&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol(),n=new Map;class l{constructor(e,t){if(this._$cssResult$=!0,t!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e}get styleSheet(){let e=n.get(this.cssText);return o&&void 0===e&&(n.set(this.cssText,e=new CSSStyleSheet),e.replaceSync(this.cssText)),e}toString(){return this.cssText}}const a=e=>new l("string"==typeof e?e:e+"",i),s=(e,...t)=>{const r=1===e.length?e[0]:t.reduce(((t,r,o)=>t+(e=>{if(!0===e._$cssResult$)return e.cssText;if("number"==typeof e)return e;throw Error("Value passed to 'css' function must be a 'css' function result: "+e+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(r)+e[o+1]),e[0]);return new l(r,i)},c=o?e=>e:e=>e instanceof CSSStyleSheet?(e=>{let t="";for(const r of e.cssRules)t+=r.cssText;return a(t)})(e):e;var d;const h=window.trustedTypes,p=h?h.emptyScript:"",u=window.reactiveElementPolyfillSupport,v={toAttribute(e,t){switch(t){case Boolean:e=e?p:null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let r=e;switch(t){case Boolean:r=null!==e;break;case Number:r=null===e?null:Number(e);break;case Object:case Array:try{r=JSON.parse(e)}catch(e){r=null}}return r}},m=(e,t)=>t!==e&&(t==t||e==e),b={attribute:!0,type:String,converter:v,reflect:!1,hasChanged:m};class f extends HTMLElement{constructor(){super(),this._$Et=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Ei=null,this.o()}static addInitializer(e){var t;null!==(t=this.l)&&void 0!==t||(this.l=[]),this.l.push(e)}static get observedAttributes(){this.finalize();const e=[];return this.elementProperties.forEach(((t,r)=>{const o=this._$Eh(r,t);void 0!==o&&(this._$Eu.set(o,r),e.push(o))})),e}static createProperty(e,t=b){if(t.state&&(t.attribute=!1),this.finalize(),this.elementProperties.set(e,t),!t.noAccessor&&!this.prototype.hasOwnProperty(e)){const r="symbol"==typeof e?Symbol():"__"+e,o=this.getPropertyDescriptor(e,r,t);void 0!==o&&Object.defineProperty(this.prototype,e,o)}}static getPropertyDescriptor(e,t,r){return{get(){return this[t]},set(o){const i=this[e];this[t]=o,this.requestUpdate(e,i,r)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)||b}static finalize(){if(this.hasOwnProperty("finalized"))return!1;this.finalized=!0;const e=Object.getPrototypeOf(this);if(e.finalize(),this.elementProperties=new Map(e.elementProperties),this._$Eu=new Map,this.hasOwnProperty("properties")){const e=this.properties,t=[...Object.getOwnPropertyNames(e),...Object.getOwnPropertySymbols(e)];for(const r of t)this.createProperty(r,e[r])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(e){const t=[];if(Array.isArray(e)){const r=new Set(e.flat(1/0).reverse());for(const e of r)t.unshift(c(e))}else void 0!==e&&t.push(c(e));return t}static _$Eh(e,t){const r=t.attribute;return!1===r?void 0:"string"==typeof r?r:"string"==typeof e?e.toLowerCase():void 0}o(){var e;this._$Ep=new Promise((e=>this.enableUpdating=e)),this._$AL=new Map,this._$Em(),this.requestUpdate(),null===(e=this.constructor.l)||void 0===e||e.forEach((e=>e(this)))}addController(e){var t,r;(null!==(t=this._$Eg)&&void 0!==t?t:this._$Eg=[]).push(e),void 0!==this.renderRoot&&this.isConnected&&(null===(r=e.hostConnected)||void 0===r||r.call(e))}removeController(e){var t;null===(t=this._$Eg)||void 0===t||t.splice(this._$Eg.indexOf(e)>>>0,1)}_$Em(){this.constructor.elementProperties.forEach(((e,t)=>{this.hasOwnProperty(t)&&(this._$Et.set(t,this[t]),delete this[t])}))}createRenderRoot(){var e;const t=null!==(e=this.shadowRoot)&&void 0!==e?e:this.attachShadow(this.constructor.shadowRootOptions);return((e,t)=>{o?e.adoptedStyleSheets=t.map((e=>e instanceof CSSStyleSheet?e:e.styleSheet)):t.forEach((t=>{const r=document.createElement("style"),o=window.litNonce;void 0!==o&&r.setAttribute("nonce",o),r.textContent=t.cssText,e.appendChild(r)}))})(t,this.constructor.elementStyles),t}connectedCallback(){var e;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(e=this._$Eg)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostConnected)||void 0===t?void 0:t.call(e)}))}enableUpdating(e){}disconnectedCallback(){var e;null===(e=this._$Eg)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostDisconnected)||void 0===t?void 0:t.call(e)}))}attributeChangedCallback(e,t,r){this._$AK(e,r)}_$ES(e,t,r=b){var o,i;const n=this.constructor._$Eh(e,r);if(void 0!==n&&!0===r.reflect){const l=(null!==(i=null===(o=r.converter)||void 0===o?void 0:o.toAttribute)&&void 0!==i?i:v.toAttribute)(t,r.type);this._$Ei=e,null==l?this.removeAttribute(n):this.setAttribute(n,l),this._$Ei=null}}_$AK(e,t){var r,o,i;const n=this.constructor,l=n._$Eu.get(e);if(void 0!==l&&this._$Ei!==l){const e=n.getPropertyOptions(l),a=e.converter,s=null!==(i=null!==(o=null===(r=a)||void 0===r?void 0:r.fromAttribute)&&void 0!==o?o:"function"==typeof a?a:null)&&void 0!==i?i:v.fromAttribute;this._$Ei=l,this[l]=s(t,e.type),this._$Ei=null}}requestUpdate(e,t,r){let o=!0;void 0!==e&&(((r=r||this.constructor.getPropertyOptions(e)).hasChanged||m)(this[e],t)?(this._$AL.has(e)||this._$AL.set(e,t),!0===r.reflect&&this._$Ei!==e&&(void 0===this._$E_&&(this._$E_=new Map),this._$E_.set(e,r))):o=!1),!this.isUpdatePending&&o&&(this._$Ep=this._$EC())}async _$EC(){this.isUpdatePending=!0;try{await this._$Ep}catch(e){Promise.reject(e)}const e=this.scheduleUpdate();return null!=e&&await e,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var e;if(!this.isUpdatePending)return;this.hasUpdated,this._$Et&&(this._$Et.forEach(((e,t)=>this[t]=e)),this._$Et=void 0);let t=!1;const r=this._$AL;try{t=this.shouldUpdate(r),t?(this.willUpdate(r),null===(e=this._$Eg)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostUpdate)||void 0===t?void 0:t.call(e)})),this.update(r)):this._$EU()}catch(e){throw t=!1,this._$EU(),e}t&&this._$AE(r)}willUpdate(e){}_$AE(e){var t;null===(t=this._$Eg)||void 0===t||t.forEach((e=>{var t;return null===(t=e.hostUpdated)||void 0===t?void 0:t.call(e)})),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}_$EU(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$Ep}shouldUpdate(e){return!0}update(e){void 0!==this._$E_&&(this._$E_.forEach(((e,t)=>this._$ES(t,this[t],e))),this._$E_=void 0),this._$EU()}updated(e){}firstUpdated(e){}}f.finalized=!0,f.elementProperties=new Map,f.elementStyles=[],f.shadowRootOptions={mode:"open"},null==u||u({ReactiveElement:f}),(null!==(d=globalThis.reactiveElementVersions)&&void 0!==d?d:globalThis.reactiveElementVersions=[]).push("1.2.1");var g,y,_=r(15304);class w extends f{constructor(){super(...arguments),this.renderOptions={host:this},this._$Dt=void 0}createRenderRoot(){var e,t;const r=super.createRenderRoot();return null!==(e=(t=this.renderOptions).renderBefore)&&void 0!==e||(t.renderBefore=r.firstChild),r}update(e){const t=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(e),this._$Dt=(0,_.sY)(t,this.renderRoot,this.renderOptions)}connectedCallback(){var e;super.connectedCallback(),null===(e=this._$Dt)||void 0===e||e.setConnected(!0)}disconnectedCallback(){var e;super.disconnectedCallback(),null===(e=this._$Dt)||void 0===e||e.setConnected(!1)}render(){return _.Jb}}w.finalized=!0,w._$litElement$=!0,null===(g=globalThis.litElementHydrateSupport)||void 0===g||g.call(globalThis,{LitElement:w});const $=globalThis.litElementPolyfillSupport;null==$||$({LitElement:w});(null!==(y=globalThis.litElementVersions)&&void 0!==y?y:globalThis.litElementVersions=[]).push("3.1.2")}},o={};function i(e){var t=o[e];if(void 0!==t)return t.exports;var n=o[e]={exports:{}};return r[e](n,n.exports,i),n.exports}i.m=r,i.d=(e,t)=>{for(var r in t)i.o(t,r)&&!i.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},i.f={},i.e=e=>Promise.all(Object.keys(i.f).reduce(((t,r)=>(i.f[r](e,t),t)),[])),i.u=e=>({16134:"85840bc7",43835:"401f3e95",48811:"8724b8f7",78309:"9e80d3dc",82678:"1425373e"}[e]+".js"),i.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),e={},t="home-assistant-frontend:",i.l=(r,o,n,l)=>{if(e[r])e[r].push(o);else{var a,s;if(void 0!==n)for(var c=document.getElementsByTagName("script"),d=0;d<c.length;d++){var h=c[d];if(h.getAttribute("src")==r||h.getAttribute("data-webpack")==t+n){a=h;break}}a||(s=!0,(a=document.createElement("script")).charset="utf-8",a.timeout=120,i.nc&&a.setAttribute("nonce",i.nc),a.setAttribute("data-webpack",t+n),a.src=r),e[r]=[o];var p=(t,o)=>{a.onerror=a.onload=null,clearTimeout(u);var i=e[r];if(delete e[r],a.parentNode&&a.parentNode.removeChild(a),i&&i.forEach((e=>e(o))),t)return t(o)},u=setTimeout(p.bind(null,void 0,{type:"timeout",target:a}),12e4);a.onerror=p.bind(null,a.onerror),a.onload=p.bind(null,a.onload),s&&document.head.appendChild(a)}},i.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.p="/frontend_latest/",(()=>{var e={28017:0};i.f.j=(t,r)=>{var o=i.o(e,t)?e[t]:void 0;if(0!==o)if(o)r.push(o[2]);else{var n=new Promise(((r,i)=>o=e[t]=[r,i]));r.push(o[2]=n);var l=i.p+i.u(t),a=new Error;i.l(l,(r=>{if(i.o(e,t)&&(0!==(o=e[t])&&(e[t]=void 0),o)){var n=r&&("load"===r.type?"missing":r.type),l=r&&r.target&&r.target.src;a.message="Loading chunk "+t+" failed.\n("+n+": "+l+")",a.name="ChunkLoadError",a.type=n,a.request=l,o[1](a)}}),"chunk-"+t,t)}};var t=(t,r)=>{var o,n,[l,a,s]=r,c=0;if(l.some((t=>0!==e[t]))){for(o in a)i.o(a,o)&&(i.m[o]=a[o]);if(s)s(i)}for(t&&t(r);c<l.length;c++)n=l[c],i.o(e,n)&&e[n]&&e[n][0](),e[l[c]]=0},r=self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))})(),(()=>{"use strict";i(37846);var e=i(47181);const t=(e,t,r)=>new Promise(((o,i)=>{const n=document.createElement(e);let l="src",a="body";switch(n.onload=()=>o(t),n.onerror=()=>i(t),e){case"script":n.async=!0,r&&(n.type=r);break;case"link":n.type="text/css",n.rel="stylesheet",l="href",a="head"}n[l]=t,document[a].appendChild(n)})),r=e=>t("script",e),o="customElements"in window&&"content"in document.createElement("template"),n="ha-main-window",l=window.name===n?window:parent.name===n?parent:top;let a;const s=(t,r)=>{const o=(null==r?void 0:r.replace)||!1;var i;a?a.then((()=>s(t,r))):(o?l.history.replaceState(null!==(i=l.history.state)&&void 0!==i&&i.root?{root:!0}:null,"",t):l.history.pushState(null,"",t),(0,e.B)(l,"location-changed",{replace:o}))};var c=i(11654);const d={},h=e=>{const o=(e=>e.html_url?{type:"html",url:e.html_url}:e.module_url&&e.js_url||e.module_url?{type:"module",url:e.module_url}:{type:"js",url:e.js_url})(e);return"js"===o.type?(o.url in d||(d[o.url]=r(o.url)),d[o.url]):"module"===o.type?(i=o.url,t("script",i,"module")):Promise.reject("No valid url found in panel config.");var i};let p,u;function v(e){u&&((e,t)=>{"setProperties"in e?e.setProperties(t):Object.keys(t).forEach((r=>{e[r]=t[r]}))})(u,e)}function m(t,n){const l=document.createElement("style");l.innerHTML="body { margin:0; } \n  @media (prefers-color-scheme: dark) {\n    body {\n      background-color: #111111;\n      color: #e1e1e1;\n    }\n  }",document.head.appendChild(l);const a=t.config._panel_custom;let d=Promise.resolve();o||(d=d.then((()=>r("/static/polyfills/webcomponents-bundle.js")))),d.then((()=>h(a))).then((()=>p||Promise.resolve())).then((()=>{u=(e=>{const t="html_url"in e?`ha-panel-${e.name}`:e.name;return document.createElement(t)})(a);u.addEventListener("hass-toggle-menu",(t=>{window.parent.customPanel&&(0,e.B)(window.parent.customPanel,t.type,t.detail)})),window.addEventListener("location-changed",(e=>{window.parent.customPanel&&window.parent.customPanel.navigate(window.location.pathname,e.detail)})),v({panel:t,...n}),document.body.appendChild(u)}),(e=>{let r;console.error(e,t),"hassio"===t.url_path?(Promise.all([i.e(78309),i.e(43835),i.e(16134),i.e(82678)]).then(i.bind(i,82678)),r=document.createElement("supervisor-error-screen")):(Promise.all([i.e(78309),i.e(16134),i.e(48811)]).then(i.bind(i,48811)),r=document.createElement("hass-error-screen"),r.error=`Unable to load the panel source: ${e}.`);const o=document.createElement("style");o.innerHTML=c.e$.cssText,document.body.appendChild(o),r.hass=n.hass,document.body.appendChild(r)})),document.body.addEventListener("click",(e=>{const t=(e=>{if(e.defaultPrevented||0!==e.button||e.metaKey||e.ctrlKey||e.shiftKey)return;const t=e.composedPath().filter((e=>"A"===e.tagName))[0];if(!t||t.target||t.hasAttribute("download")||"external"===t.getAttribute("rel"))return;let r=t.href;if(!r||-1!==r.indexOf("mailto:"))return;const o=window.location,i=o.origin||o.protocol+"//"+o.host;return 0===r.indexOf(i)&&(r=r.substr(i.length),"#"!==r)?(e.preventDefault(),r):void 0})(e);t&&s(t)}))}window.loadES5Adapter=()=>(p||(p=r("/static/polyfills/custom-elements-es5-adapter.js").catch()),p),document.addEventListener("DOMContentLoaded",(()=>window.parent.customPanel.registerIframe(m,v)),{once:!0})})()})();
//# sourceMappingURL=custom-panel.3d66f817.js.map