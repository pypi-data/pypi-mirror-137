"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[33137],{85415:(e,t,i)=>{i.d(t,{$:()=>r,f:()=>n});const r=(e,t)=>e<t?-1:e>t?1:0,n=(e,t)=>r(e.toLowerCase(),t.toLowerCase())},73728:(e,t,i)=>{i.d(t,{pV:()=>a,P3:()=>s,Ky:()=>c,D4:()=>d,XO:()=>p,zO:()=>f,oi:()=>h,d4:()=>u,D7:()=>m,ZJ:()=>v,V3:()=>g,WW:()=>y});var r=i(97330),n=i(38346),o=i(5986);const a=["usb","unignore","dhcp","homekit","ssdp","zeroconf","discovery","mqtt","hassio"],s=["reauth"],l={"HA-Frontend-Base":`${location.protocol}//${location.host}`},c=(e,t)=>{var i;return e.callApi("POST","config/config_entries/flow",{handler:t,show_advanced_options:Boolean(null===(i=e.userData)||void 0===i?void 0:i.showAdvanced)},l)},d=(e,t)=>e.callApi("GET",`config/config_entries/flow/${t}`,void 0,l),p=(e,t,i)=>e.callApi("POST",`config/config_entries/flow/${t}`,i,l),f=(e,t,i)=>e.callWS({type:"config_entries/ignore_flow",flow_id:t,title:i}),h=(e,t)=>e.callApi("DELETE",`config/config_entries/flow/${t}`),u=e=>e.callApi("GET","config/config_entries/flow_handlers"),m=e=>e.sendMessagePromise({type:"config_entries/flow/progress"}),w=(e,t)=>e.subscribeEvents((0,n.D)((()=>m(e).then((e=>t.setState(e,!0)))),500,!0),"config_entry_discovered"),v=e=>(0,r._)(e,"_configFlowProgress",m,w),g=(e,t)=>v(e.connection).subscribe(t),y=(e,t)=>t.context.title_placeholders&&0!==Object.keys(t.context.title_placeholders).length?e(`component.${t.handler}.config.flow_title`,t.context.title_placeholders)||("name"in t.context.title_placeholders?t.context.title_placeholders.name:(0,o.Lh)(e,t.handler)):(0,o.Lh)(e,t.handler)},2852:(e,t,i)=>{i.d(t,{t:()=>l});var r=i(37500),n=i(85415),o=i(73728),a=i(5986),s=i(52871);const l=(e,t)=>(0,s.w)(e,t,{loadDevicesAndAreas:!0,getFlowHandlers:async e=>{const[t]=await Promise.all([(0,o.d4)(e),e.loadBackendTranslation("title",void 0,!0)]);return t.sort(((t,i)=>(0,n.f)((0,a.Lh)(e.localize,t),(0,a.Lh)(e.localize,i))))},createFlow:async(e,t)=>{const[i]=await Promise.all([(0,o.Ky)(e,t),e.loadBackendTranslation("config",t),e.loadBackendTranslation("title",t)]);return i},fetchFlow:async(e,t)=>{const i=await(0,o.D4)(e,t);return await e.loadBackendTranslation("config",i.handler),i},handleFlowStep:o.XO,deleteFlow:o.oi,renderAbortDescription(e,t){const i=e.localize(`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return i?r.dy`
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
          `:""},renderLoadingDescription(e,t,i,r){if(!["loading_flow","loading_step"].includes(t))return"";const n=(null==r?void 0:r.handler)||i;return e.localize(`ui.panel.config.integrations.config_flow.loading.${t}`,{integration:n?(0,a.Lh)(e.localize,n):e.localize("ui.panel.config.integrations.config_flow.loading.fallback_title")})}})},52871:(e,t,i)=>{i.d(t,{w:()=>o});var r=i(47181);const n=()=>Promise.all([i.e(78161),i.e(75009),i.e(42955),i.e(68200),i.e(30879),i.e(29907),i.e(88985),i.e(28055),i.e(54040),i.e(87502),i.e(1536),i.e(93883),i.e(41248),i.e(46976),i.e(15517),i.e(13529),i.e(46002),i.e(30486),i.e(81480),i.e(78374),i.e(32229),i.e(68331),i.e(68101),i.e(4940),i.e(81836),i.e(23917)]).then(i.bind(i,63118)),o=(e,t,i)=>{(0,r.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:n,dialogParams:{...t,flowConfig:i}})}},33137:(e,t,i)=>{i.r(t);i(53268),i(12730),i(60010),i(38353),i(63081);var r=i(37500),n=i(72367),o=i(2852),a=i(47181),s=i(11654);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=u(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function c(e){var t,i=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=l();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(f(o.descriptor)||f(n.descriptor)){if(p(o)||p(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(p(o)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}d(o,n)}else t.push(o)}return t}(a.d.map(c)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,n.Mo)("ha-config-ais-dom-config-wifi")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"isWide",value:()=>!0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"method",key:"firstUpdated",value:async function(){}},{kind:"method",key:"render",value:function(){return this.hass?r.dy`
      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div .narrow=${this.narrow}>
          <ha-config-section .isWide=${this.isWide}>
            <span slot="header">Połączenie WiFi</span>
            <span slot="introduction"
              >Możesz sprawdzić lub skonfigurować parametry połączenia
              WiFi</span
            >
            <ha-card header="Parametry sieci">
              <div class="card-content" style="display: flex;">
                <div style="text-align: center;">
                  <div class="aisInfoRow">Lokalna nazwa hosta</div>
                  <div class="aisInfoRow">
                    <mwc-button
                      >${this.hass.states["sensor.local_host_name"].state}
                      <ha-icon
                        class="user-button"
                        icon="hass:cog"
                        @click=${this.createFlowHostName}
                      ></ha-icon>
                    </mwc-button>
                  </div>
                </div>
                <div style="text-align: center;" @click=${this.showLocalIpInfo}>
                  <div class="aisInfoRow">Lokalny adres IP</div>
                  <div class="aisInfoRow">
                    <mwc-button
                      >${this.hass.states["sensor.internal_ip_address"].state}</mwc-button
                    >
                  </div>
                </div>
                <div
                  @click=${this.showWiFiSpeedInfo}
                  style="text-align: center;"
                >
                  <div class="aisInfoRow">Prędkość połączenia WiFi</div>
                  <div class="aisInfoRow">
                    <mwc-button
                      >${this.hass.states["sensor.ais_wifi_service_current_network_info"].state}</mwc-button
                    >
                  </div>
                </div>
              </div>
              <div class="card-actions">
                <ha-icon
                  class="user-button"
                  icon="hass:wifi"
                  @click=${this.showWiFiGroup}
                ></ha-icon
                ><mwc-button @click=${this.createFlowWifi}
                  >Konfigurator połączenia z siecą WiFi</mwc-button
                >
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `:r.dy``}},{kind:"get",static:!0,key:"styles",value:function(){return[s.Qx,r.iv`
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
        div.aisInfoRow {
          display: inline-block;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        div.card-actions {
          text-align: center;
        }
      `]}},{kind:"method",key:"showWiFiGroup",value:function(){(0,a.B)(this,"hass-more-info",{entityId:"group.internet_status"})}},{kind:"method",key:"showWiFiSpeedInfo",value:function(){(0,a.B)(this,"hass-more-info",{entityId:"sensor.ais_wifi_service_current_network_info"})}},{kind:"method",key:"showLocalIpInfo",value:function(){(0,a.B)(this,"hass-more-info",{entityId:"sensor.internal_ip_address"})}},{kind:"method",key:"_continueFlow",value:function(e){(0,o.t)(this,{continueFlowId:e,dialogClosedCallback:()=>{console.log("OK")}})}},{kind:"method",key:"createFlowHostName",value:function(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_host"}).then((e=>{this._continueFlow(e.flow_id)}))}},{kind:"method",key:"createFlowWifi",value:function(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_wifi_service"}).then((e=>{console.log(e),this._continueFlow(e.flow_id)}))}}]}}),r.oi)}}]);
//# sourceMappingURL=5f7d4e4b.js.map