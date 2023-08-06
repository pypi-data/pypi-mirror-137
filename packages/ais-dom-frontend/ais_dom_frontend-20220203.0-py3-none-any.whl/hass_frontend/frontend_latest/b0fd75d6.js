"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[41193],{41193:(e,t,r)=>{r.r(t);r(53268),r(12730),r(60010),r(63081);var i=r(72367),n=r(37500);function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!l(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return u(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?u(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=p(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function a(e){var t,r=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function l(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function u(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}let f=function(e,t,r,i){var n=o();if(i)for(var d=0;d<i.length;d++)n=i[d](n);var p=t((function(e){n.initializeInstanceElements(e,u.elements)}),r),u=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(c(o.descriptor)||c(n.descriptor)){if(l(o)||l(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(l(o)){if(l(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}s(o,n)}else t.push(o)}return t}(p.d.map(a)),e);return n.initializeClassElements(p.F,u.elements),n.runClassFinishers(p.F,u.finishers)}(null,(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"isWide",value:()=>!0},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`
      .content {
        padding-bottom: 32px;
      }
      .border {
        margin: 32px auto 0;
        border-bottom: 1px solid rgba(0, 0, 0, 0.12);
        max-width: 1040px;
      }
      .narrow .border {
        max-width: 640px;
      }
      .center-container {
        @apply --layout-vertical;
        @apply --layout-center-center;
        height: 70px;
      }
      .content {
        padding-bottom: 24px;
        direction: ltr;
      }
      .account-row {
        display: flex;
        padding: 0 16px;
      }
      mwc-button {
        align-self: center;
      }
      .soon {
        font-style: italic;
        margin-top: 24px;
        text-align: center;
      }
      .nowrap {
        white-space: nowrap;
      }
      .wrap {
        white-space: normal;
      }
      .status {
        text-transform: capitalize;
        padding: 16px;
      }
      a {
        color: var(--primary-color);
      }
      .buttons {
        position: relative;
        width: 200px;
        height: 200px;
      }
      .button {
        position: absolute;
        width: 50px;
        height: 50px;
      }
      .arrow {
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
      }
      .arrow-up {
        border-left: 12px solid transparent;
        border-right: 12px solid transparent;
        border-bottom: 16px solid black;
      }
      .arrow-right {
        border-top: 12px solid transparent;
        border-bottom: 12px solid transparent;
        border-left: 16px solid black;
      }
      .arrow-left {
        border-top: 12px solid transparent;
        border-bottom: 12px solid transparent;
        border-right: 16px solid black;
      }
      .arrow-down {
        border-left: 12px solid transparent;
        border-right: 12px solid transparent;
        border-top: 16px solid black;
      }
      .down {
        bottom: 0;
        left: 75px;
      }
      .left {
        top: 75px;
        left: 0;
      }
      .right {
        top: 75px;
        right: 0;
      }
      .up {
        top: 0;
        left: 75px;
      }
      div.card-actions {
        text-align: center;
      }
    `}},{kind:"method",key:"render",value:function(){return n.dy`
      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div>
          <ha-config-section .isWide=${this.isWide}>
            <span slot="header">Ustawienia ekranu</span>
            <span slot="introduction"
              >Jeżeli obraz na monitorze lub telewizorze podłączonym do bramki
              za pomocą złącza HDMI jest ucięty lub przesunięty, to w tym
              miejscu możesz dostosować obraz do rozmiaru ekranu.</span
            >
            <ha-card header="Dostosuj obraz do rozmiaru ekranu">
              <div class="card-content">
                <div class="card-content" style="text-align: center;">
                  <div style="display: inline-block;">
                    <p>Powiększanie</p>
                    <div
                      class="buttons"
                      style="margin: 0 auto; display: table; border:solid 1px;"
                    >
                      <button
                        class="button up"
                        data-value="top"
                        @click=${this.wmOverscan}
                      >
                        <span class="arrow-up arrow"></span>
                      </button>
                      <button
                        class="button down"
                        data-value="bottom"
                        @click=${this.wmOverscan}
                      >
                        <span class="arrow-down arrow"></span>
                      </button>
                      <button
                        class="button right"
                        data-value="right"
                        @click=${this.wmOverscan}
                      >
                        <span class="arrow-right arrow"></span>
                      </button>
                      <button
                        class="button left"
                        data-value="left"
                        @click=${this.wmOverscan}
                      >
                        <span class="arrow-left arrow"></span>
                      </button>
                    </div>
                  </div>
                  <div
                    style="text-align: center; display: inline-block; margin: 30px;"
                  >
                    <p>Zmniejszanie</p>
                    <div
                      class="buttons"
                      style="margin: 0 auto; display: table;"
                    >
                      <button
                        class="button up"
                        data-value="-top"
                        @click=${this.wmOverscan}
                      >
                        <span class="arrow-down arrow"></span>
                      </button>
                      <div
                        style="margin: 0 auto; height: 98px; width:98px; margin-top: 50px; margin-left: 50px; display: flex; border:solid 1px;"
                      ></div>
                      <button
                        class="button down"
                        data-value="-bottom"
                        @click=${this.wmOverscan}
                      >
                        <span class="arrow-up arrow"></span>
                      </button>
                      <button
                        class="button right"
                        data-value="-right"
                        @click=${this.wmOverscan}
                      >
                        <span class="arrow-left arrow"></span>
                      </button>
                      <button
                        class="button left"
                        data-value="-left"
                        @click=${this.wmOverscan}
                      >
                        <span class="arrow-right arrow"></span>
                      </button>
                    </div>
                  </div>
                </div>
                <div class="card-actions" style="margin-top: 30px;">
                  <mwc-button @click=${this.wmOverscan} data-value="reset">
                    <ha-icon class="user-button" icon="mdi:restore"></ha-icon>
                    Reset ekranu do ustawień domyślnych
                  </mwc-button>
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}},{kind:"method",key:"wmOverscan",value:function(e){this.hass.callService("ais_shell_command","change_wm_overscan",{value:e.currentTarget.getAttribute("data-value")})}}]}}),n.oi);customElements.define("ha-config-ais-dom-config-display",f)}}]);
//# sourceMappingURL=b0fd75d6.js.map