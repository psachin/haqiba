/**
   This is a js module for image zoom effect
**/

// Counter for 'mouseenter'  
var count = 0;
var instance;
var ids;
/*
  Get the image link and add,
  'mouserenter': event to start image zooming
  'mouseleave': event to close the zoomed image
*/
function initImageZoom(_options) {
		var options = $extend({
			rel: 'imagezoom'
		}, _options || {});
		var elements = $$(document.getElementById("image_link")).filter(function(el) {
			if ((el.rel) && (el.rel.indexOf(options.rel) != -1)) 
				return true;
			else
				return false;
		});
		
		
		var el = elements[0];
		el.addEvent("mouseenter", function() {
			if(count == 0){
				count++;
				this.blur();
				var sEl = this;
				var imgCap = "";
				if (this.getElements("img").length > 0)
					sEl = this.getElements("img")[0];
				if ((sEl.alt) && (sEl.alt != ""))
					imgCap = sEl.alt;
				else if (sEl.title)
					imgCap = sEl.title;
				else if (sEl.parentNode.title)
					imgCap = sEl.parentNode.title;
				var _options = $extend({
					image: this.href,
					caption: imgCap,
					startElement: sEl
				}, options || {});
			
				_options.image = this.href;
			
				_options.caption = imgCap;
			
				var imagezoom = new Imagezoom(_options);
			
				imagezoom.preloadImage();
				imagezoom.show();
				return false;
			}
		});
			
			
		el.addEvent("mouseleave", function() {
			instance.close();
			return false;
		});
			
	}
	
	/*
	before image zooming do some preloading stuf to give loading like feel
	*/
	var Imagezoom = function(_options) {		
		var options = $extend({
			image: false,
			caption: "",
			enableCaptions: true,
			startElement: false,
			x: 10,
			y: 10,
			initWidth: 50,
			initHeight: 50,
			draggable: true,
			loadImage: "/static/images/loading.gif",
			loadDelay: 150,
			duration: 300,
			closeDuration: 500,
			transition: Fx.Transitions.Cubic.easeOut,
			startOpacity: 0.6,
			closeText: 'Close',
			rel: 'imagezoom',
			showCaptionBar: true,
			overlay: false,
			overlayColor: "#000",
			overlayOpacity: .75
		}, _options || {});
		
		var box = document.createElement("div");
		instance = this;
		
		
		
		this.preloadImage = function() {
			if (options.image != false) {
				var img = new Image();
				img.src = options.image;
				img.style.visibility = "hidden";
				img.style.position = "absolute";
				img.style.top = "-9999999999px";
				img.setAttribute("id", "imagezoom-" + options.image);
			}	
		}
		
		/*
		get the image and set attributes
		*/
		this.getImage = function() {
			if (($$('imagezoom-' + options.image)) && ($$('imagezoom-' + options.image).width != "0")) {
				var img = $$('imagezoom-' + options.image).clone();
				img.setAttribute("id", "");
				img.style.position = "relative";
				img.style.top = "0px";
				img.style.visibility = "visible";
			} else {
				instance.preloadImage();
				window.setTimeout(function() {
					instance.getImage();
				}, 50);
			}
			return img;
		}		
		
		/*
		set the zoomed image container style
		*/
		this.show = function() {
			if (options.image != false) {
				
				box.style.position = "absolute";
				box.style.overflow = "hidden";
				box.setAttribute("id", "imagezoom-open-" + options.image);
				
				if (options.startElement != false)
					options.startElement.blur();
				
				var x = options.x;
				var y = options.y;
				var boxWidth = options.initWidth;
				var boxHeight = options.initHeight;
				if (options.startElement != false) {
					x = options.startElement.getPosition().x;
					y = options.startElement.getPosition().y;
					boxWidth = options.startElement.offsetWidth;
					boxHeight = options.startElement.offsetHeight;
				}
				
				box.style.left = x + "px";
				box.style.top = y + "px";
				box.style.width = boxWidth + "px";
				box.style.height = boxHeight + "px";
				
				var fx = new Fx.Morph(box);
				fx.set({opacity: options.startOpacity});
				
				box.className = "imagezoom";
				$$('body')[0].appendChild(box);
				box.style.cursor = "pointer";
				box.addEvent("click", function() {
					var fx = new Fx.Morph(box, {duration: 200});
					fx.start({opacity: 0}).chain(function() {
						$$('body')[0].removeChild(box);
					});
				});
				
				this.loadImage();
			}
		}
		
		/*
		load image container and call the method for inserting image
		*/
		this.loadImage = function() {
			if (box.getElements(".loading").length == 0) {
				var loading = new Image();
				loading.src = options.loadImage;
				loading.className = "loading";
				box.appendChild(loading);
			}	
			
			if ($$('imagezoom-' + options.image)) {
				var el = $$('imagezoom-' + options.image);
				if (el.width != "0") {
					var newEl = new Image();
					newEl.src = options.image;
					window.setTimeout(function() { instance.insertImage(newEl) }, options.loadDelay);
				} else {
					window.setTimeout(function() { instance.loadImage(); }, 50);
				}
				
			} else {
				instance.preloadImage();
				window.setTimeout(function() { instance.loadImage(); }, 50);
			}
			
		}
		
		/*
		insert image and set image attributes for height, width etc.
		also, insert 'close' button and  call 'click' event for it
		*/
		this.insertImage = function(img) {
			box.removeEvents("click");
			box.style.cursor = "default";
			box.style.overflow = "visible";
			var w = window.innerWidth/1.4;
			var h = window.innerHeight/1.4;
			
			img.style.width = w-10 + "px";
			img.style.height = h-10 + "px";
			img.className = 'image';
			
			var ptop = (window.getSize().y / 2) + window.getScroll().y - (h/2);
			var pleft = (window.getSize().x / 2) + window.getScroll().x - (w/2);
			var fx = new Fx.Morph(box, {duration: options.duration, transition: options.transition});
			fx.start({
				top: ptop,
				left: pleft,
				width: w,
				height: h,
				opacity: 1
			}).chain(function() {
				if (!$$('imagezoom_overlay')) {
					var overlay = (document.createElement("div"));
					overlay.setAttribute("id", "imagezoom_overlay");
					overlay.style.backgroundColor = options.overlayColor;
					overlay.setOpacity(0);
					$$('body')[0].appendChild(overlay);
				} else {
					var overlay = $$('imagezoom_overlay');
				}
				
				
				var close = document.createElement("div");
				
				close.innerHTML = "<span>" + options.closeText + "</span>";
				close.className = "close";
				
				close.addEvent("click", function() {
					instance.close();
				});
				var loading = box.getElements(".loading");
				if (loading.length > 0)
					box.removeChild(loading[0]);
				var elements = [close, img];
				for (var i = 0; i < elements.length; i++) {
					var elFx = new Fx.Morph(elements[i], {duration: 600});
					elFx.set({opacity: 0});
					box.adopt(elements[i]);
					elFx.start({opacity: 1});
				}
			});		
		}
		
		
		/*
		'close' button event to close the zoomed image
		*/
		this.close = function(hideOverlay) {
			var img = box.getElements(".image")[0];
			box.removeChild(img);
			var close = box.getElements(".close")[0];
			box.removeChild(close);
			var caption = box.getElements(".caption");
			if (caption.length > 0)
				box.removeChild(caption[0]);
			var s = box.getElements(".s");
			for (var i = 0; i < s.length; i++)
				box.removeChild(s[i]);
			var x = options.x;
			var y = options.y;
			var boxWidth = options.initWidth;
			var boxHeight = options.initHeight;
			if (options.startElement != false) {
				x = options.startElement.getPosition().x;
				y = options.startElement.getPosition().y;
				boxWidth = options.startElement.offsetWidth;
				boxHeight = options.startElement.offsetHeight;
			}
			if ((hideOverlay == true) && ($$('imagezoom_overlay'))) {
				var oFx = new Fx.Morph($$('imagezoom_overlay'), {duration: options.closeDuration});
				oFx.start({opacity: 0}).chain(function() {
					$$('body')[0].removeChild($$('imagezoom_overlay'));
				});
			}
			var fx = new Fx.Morph(box, {duration: options.closeDuration});
			fx.start({
				left: x,
				top: y,
				width: boxWidth,
				height: boxHeight,
				opacity: options.startOpacity
			}).chain(function() {
				fx.start({
					opacity: 0
				}).chain(function() {
					count = 0;
					$$('body')[0].removeChild(box);
				});
			});
		}	
	}
