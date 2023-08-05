"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[28561],{3176:(t,i,a)=>{a.r(i),a.d(i,{default:()=>s});class s{static hasCamera(){return s.listCameras(!1).then((e=>!!e.length)).catch((()=>!1))}static listCameras(e=!1){if(!navigator.mediaDevices)return Promise.resolve([]);let t=null;return(e?navigator.mediaDevices.getUserMedia({audio:!1,video:!0}).then((e=>t=e)).catch((()=>{})):Promise.resolve()).then((()=>navigator.mediaDevices.enumerateDevices())).then((e=>e.filter((e=>"videoinput"===e.kind)).map(((e,t)=>({id:e.deviceId,label:e.label||(0===t?"Default Camera":`Camera ${t+1}`)}))))).finally((()=>{if(t)for(const e of t.getTracks())e.stop(),t.removeTrack(e)}))}constructor(e,t,i=this._onDecodeError,a=this._calculateScanRegion,r="environment"){this.$video=e,this.$canvas=document.createElement("canvas"),this._onDecode=t,this._legacyCanvasSize=s.DEFAULT_CANVAS_SIZE,this._preferredCamera=r,this._active=!1,this._paused=!1,this._flashOn=!1,"number"==typeof i?(this._legacyCanvasSize=i,console.warn("You're using a deprecated version of the QrScanner constructor which will be removed in the future")):this._onDecodeError=i,"number"==typeof a?(this._legacyCanvasSize=a,console.warn("You're using a deprecated version of the QrScanner constructor which will be removed in the future")):this._calculateScanRegion=a,this._scanRegion=this._calculateScanRegion(e),this._onPlay=this._onPlay.bind(this),this._onLoadedMetaData=this._onLoadedMetaData.bind(this),this._onVisibilityChange=this._onVisibilityChange.bind(this),e.disablePictureInPicture=!0,e.playsInline=!0,e.muted=!0;let n=!1;e.hidden&&(e.hidden=!1,n=!0),document.body.contains(e)||(document.body.appendChild(e),n=!0),requestAnimationFrame((()=>{const t=window.getComputedStyle(e);"none"===t.display&&(e.style.setProperty("display","block","important"),n=!0),"visible"!==t.visibility&&(e.style.setProperty("visibility","visible","important"),n=!0),n&&(console.warn("QrScanner has overwritten the video hiding style to avoid Safari stopping the playback."),e.style.opacity=0,e.style.width=0,e.style.height=0)})),e.addEventListener("play",this._onPlay),e.addEventListener("loadedmetadata",this._onLoadedMetaData),document.addEventListener("visibilitychange",this._onVisibilityChange),this._qrEnginePromise=s.createQrEngine()}hasFlash(){let e=null;return(this.$video.srcObject?Promise.resolve(this.$video.srcObject.getVideoTracks()[0]):this._getCameraStream().then((({stream:t})=>(console.warn("Call hasFlash after successfully starting the scanner to avoid creating a temporary video stream"),e=t,t.getVideoTracks()[0])))).then((e=>"torch"in e.getSettings())).catch((()=>!1)).finally((()=>{if(e)for(const t of e.getTracks())t.stop(),e.removeTrack(t)}))}isFlashOn(){return this._flashOn}toggleFlash(){return this._flashOn?this.turnFlashOff():this.turnFlashOn()}turnFlashOn(){return this._flashOn?Promise.resolve():(this._flashOn=!0,!this._active||this._paused?Promise.resolve():this.hasFlash().then((e=>e?this.$video.srcObject.getVideoTracks()[0].applyConstraints({advanced:[{torch:!0}]}):Promise.reject("No flash available"))).catch((()=>{throw this._flashOn=!1,e})))}turnFlashOff(){if(this._flashOn)return this._flashOn=!1,this._restartVideoStream()}destroy(){this.$video.removeEventListener("loadedmetadata",this._onLoadedMetaData),this.$video.removeEventListener("play",this._onPlay),document.removeEventListener("visibilitychange",this._onVisibilityChange),this.stop(),s._postWorkerMessage(this._qrEnginePromise,"close")}start(){return this._active&&!this._paused?Promise.resolve():("https:"!==window.location.protocol&&console.warn("The camera stream is only accessible if the page is transferred via https."),this._active=!0,document.hidden?Promise.resolve():(this._paused=!1,this.$video.srcObject?(this.$video.play(),Promise.resolve()):this._getCameraStream().then((({stream:e,facingMode:t})=>{this.$video.srcObject=e,this.$video.play(),this._setVideoMirror(t),this._flashOn&&(this._flashOn=!1,this.turnFlashOn().catch((()=>{})))})).catch((e=>{throw this._active=!1,e}))))}stop(){this.pause(),this._active=!1}pause(e=!1){if(this._paused=!0,!this._active)return Promise.resolve(!0);this.$video.pause();const t=()=>{const e=this.$video.srcObject?this.$video.srcObject.getTracks():[];for(const t of e)t.stop(),this.$video.srcObject.removeTrack(t);this.$video.srcObject=null};return e?(t(),Promise.resolve(!0)):new Promise((e=>setTimeout(e,300))).then((()=>!!this._paused&&(t(),!0)))}setCamera(e){return e===this._preferredCamera?Promise.resolve():(this._preferredCamera=e,this._restartVideoStream())}static scanImage(e,t=null,i=null,a=null,r=!1,n=!1){const o=i instanceof Worker;let h=Promise.all([i||s.createQrEngine(),s._loadImage(e)]).then((([e,n])=>{let h;return i=e,[a,h]=this._drawToCanvas(n,t,a,r),i instanceof Worker?(o||i.postMessage({type:"inversionMode",data:"both"}),new Promise(((e,t)=>{let r,n,o;n=a=>{"qrResult"===a.data.type&&(i.removeEventListener("message",n),i.removeEventListener("error",o),clearTimeout(r),null!==a.data.data?e(a.data.data):t(s.NO_QR_CODE_FOUND))},o=e=>{i.removeEventListener("message",n),i.removeEventListener("error",o),clearTimeout(r);const a=e?e.message||e:"Unknown Error";t("Scanner error: "+a)},i.addEventListener("message",n),i.addEventListener("error",o),r=setTimeout((()=>o("timeout")),1e4);const c=h.getImageData(0,0,a.width,a.height);i.postMessage({type:"decode",data:c},[c.data.buffer])}))):new Promise(((e,t)=>{const r=setTimeout((()=>t("Scanner error: timeout")),1e4);i.detect(a).then((i=>{i.length?e(i[0].rawValue):t(s.NO_QR_CODE_FOUND)})).catch((e=>t("Scanner error: "+(e.message||e)))).finally((()=>clearTimeout(r)))}))}));return t&&n&&(h=h.catch((()=>s.scanImage(e,null,i,a,r)))),h=h.finally((()=>{o||s._postWorkerMessage(i,"close")})),h}setGrayscaleWeights(e,t,i,a=!0){s._postWorkerMessage(this._qrEnginePromise,"grayscaleWeights",{red:e,green:t,blue:i,useIntegerApproximation:a})}setInversionMode(e){s._postWorkerMessage(this._qrEnginePromise,"inversionMode",e)}static createQrEngine(e=s.WORKER_PATH){return("BarcodeDetector"in window&&BarcodeDetector.getSupportedFormats?BarcodeDetector.getSupportedFormats():Promise.resolve([])).then((t=>-1!==t.indexOf("qr_code")?new BarcodeDetector({formats:["qr_code"]}):new Worker(e)))}_onPlay(){this._scanRegion=this._calculateScanRegion(this.$video),this._scanFrame()}_onLoadedMetaData(){this._scanRegion=this._calculateScanRegion(this.$video)}_onVisibilityChange(){document.hidden?this.pause():this._active&&this.start()}_calculateScanRegion(e){const t=Math.min(e.videoWidth,e.videoHeight),i=Math.round(2/3*t);return{x:Math.round((e.videoWidth-i)/2),y:Math.round((e.videoHeight-i)/2),width:i,height:i,downScaledWidth:this._legacyCanvasSize,downScaledHeight:this._legacyCanvasSize}}_scanFrame(){if(!this._active||this.$video.paused||this.$video.ended)return!1;requestAnimationFrame((()=>{this.$video.readyState<=1?this._scanFrame():this._qrEnginePromise.then((e=>s.scanImage(this.$video,this._scanRegion,e,this.$canvas))).then(this._onDecode,(e=>{if(!this._active)return;-1!==(e.message||e).indexOf("service unavailable")&&(this._qrEnginePromise=s.createQrEngine()),this._onDecodeError(e)})).then((()=>this._scanFrame()))}))}_onDecodeError(e){e!==s.NO_QR_CODE_FOUND&&console.log(e)}_getCameraStream(){if(!navigator.mediaDevices)return Promise.reject("Camera not found.");const e="environment"===this._preferredCamera||"user"===this._preferredCamera?"facingMode":"deviceId",t=[{width:{min:1024}},{width:{min:768}},{}];return[...t.map((t=>Object.assign({},t,{[e]:{exact:this._preferredCamera}}))),...t].reduceRight(((e,t)=>()=>navigator.mediaDevices.getUserMedia({video:t,audio:!1}).then((e=>({stream:e,facingMode:this._getFacingMode(e)||(t.facingMode?this._preferredCamera:"environment"===this._preferredCamera?"user":"environment")}))).catch(e)),(()=>Promise.reject("Camera not found.")))()}_restartVideoStream(){const e=this._paused;return this.pause(!0).then((t=>{if(t&&!e&&this._active)return this.start()}))}_setVideoMirror(e){const t="user"===e?-1:1;this.$video.style.transform="scaleX("+t+")"}_getFacingMode(e){const t=e.getVideoTracks()[0];return t?/rear|back|environment/i.test(t.label)?"environment":/front|user|face/i.test(t.label)?"user":null:null}static _drawToCanvas(e,t=null,i=null,a=!1){i=i||document.createElement("canvas");const s=t&&t.x?t.x:0,r=t&&t.y?t.y:0,n=t&&t.width?t.width:e.width||e.videoWidth,o=t&&t.height?t.height:e.height||e.videoHeight;if(!a){const e=t&&t.downScaledWidth?t.downScaledWidth:n,a=t&&t.downScaledHeight?t.downScaledHeight:o;i.width!==e&&(i.width=e),i.height!==a&&(i.height=a)}const h=i.getContext("2d",{alpha:!1});return h.imageSmoothingEnabled=!1,h.drawImage(e,s,r,n,o,0,0,i.width,i.height),[i,h]}static _loadImage(e){if(e instanceof HTMLCanvasElement||e instanceof HTMLVideoElement||window.ImageBitmap&&e instanceof window.ImageBitmap||window.OffscreenCanvas&&e instanceof window.OffscreenCanvas)return Promise.resolve(e);if(e instanceof Image)return s._awaitImageLoad(e).then((()=>e));if(e instanceof File||e instanceof Blob||e instanceof URL||"string"==typeof e){const t=new Image;return e instanceof File||e instanceof Blob?t.src=URL.createObjectURL(e):t.src=e,s._awaitImageLoad(t).then((()=>((e instanceof File||e instanceof Blob)&&URL.revokeObjectURL(t.src),t)))}return Promise.reject("Unsupported image type.")}static _awaitImageLoad(e){return new Promise(((t,i)=>{if(e.complete&&0!==e.naturalWidth)t();else{let a,s;a=()=>{e.removeEventListener("load",a),e.removeEventListener("error",s),t()},s=()=>{e.removeEventListener("load",a),e.removeEventListener("error",s),i("Image load error")},e.addEventListener("load",a),e.addEventListener("error",s)}}))}static _postWorkerMessage(e,t,i){return Promise.resolve(e).then((e=>{e instanceof Worker&&e.postMessage({type:t,data:i})}))}}s.DEFAULT_CANVAS_SIZE=400,s.NO_QR_CODE_FOUND="No QR code found",s.WORKER_PATH="qr-scanner-worker.min.js"}}]);