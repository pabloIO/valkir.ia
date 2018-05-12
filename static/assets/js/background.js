// https://codepen.io/meesrutten/pen/zWybmy

var backgroundAnimation = function backgroundAnimation() {
	/*
 * Creates a background with 5 rectangles that rotate, scale and change in color intensity
 */
	polygonBackground = document.querySelector('.background');

	polygonBackground.insertAdjacentHTML('beforeend', generatePolygonBackground());

	function generatePolygonBackground() {
		var WIDTH = polygonBackground.getBoundingClientRect().width;
		var HEIGHT = polygonBackground.getBoundingClientRect().height;
		var halfWidth = WIDTH / 2;
		var halfHeight = HEIGHT / 2;
		var rectWidth = WIDTH * 1.25;
		var rectHeight = HEIGHT * 1.25;
		return '\n\t\t\t\t<svg id="polygonHolder" viewBox="0 0 ' + WIDTH + ' ' + HEIGHT + '" preserveAspectRatio="xMinYMin meet" xmlns="http://www.w3.org/2000/svg">\n\t\t\t\t\t<rect x="' + -halfWidth + '" y="' + halfWidth + '" width="' + rectWidth + '" height="' + rectHeight + '"/>\n\t\t\t\t\t<rect x="' + halfWidth + '" y="' + -halfWidth + '" width="' + rectWidth + '" height="' + rectHeight + '"/>\n\t\t\t\t\t<rect x="' + -halfHeight + '" y="' + -halfWidth + '" width="' + rectWidth + '" height="' + rectHeight + '"/>\n\t\t\t\t\t<rect x="' + halfHeight + '" y="' + -halfHeight + '" width="' + rectWidth + '" height="' + rectHeight + '"/>\n\t\t\t\t\t<rect x="' + -halfHeight + '" y="' + -halfHeight + '" width="' + rectWidth + '" height="' + rectHeight + '"/>\n\t\t\t\t</svg>\n\t\t';
	}

	var allPolygons = document.querySelectorAll('.background #polygonHolder rect');

	/**
  * Returns a random number between min and max
  * 
  * @param {Number} min 
  * @param {Number} max 
  * @returns {Number}
  */
	function getRandomArbitrary(min, max) {
		return Math.random() * (max - min) + min;
	}

	/**
  * Animate DOM elements to a new rotation and scale.
  * 
  * @param {Number} timestamp 
  */
	var start = null;
	var step = 0;

	function animatePolygonBackground(timestamp) {
		if (!start) start = timestamp;
		var progress = timestamp - start;
		if (progress > step * 5000) {
			for (var i = 0; i < allPolygons.length; i++) {
				allPolygons[i].style = '\n\t\t\t\t\topacity: ' + getRandomArbitrary(0.02, 0.05).toFixed(2) + ';\n\t\t\t\t\ttransform: rotate(' + Math.round(getRandomArbitrary(15, 80)) + 'deg) scale(' + getRandomArbitrary(.75, 1.2).toFixed(2) + ');\n\t\t\t\t\ttransition-duration: ' + getRandomArbitrary(5, 10).toFixed(2) + 's;\n\t\t\t\t\t';
			}
			step++;
		}

		window.requestAnimationFrame(animatePolygonBackground);
	}

	window.requestAnimationFrame(animatePolygonBackground);
	/**
  * Remove the background and re-add
  * 
  * @param {Number} timestamp 
  */

	window.addEventListener('resize', function () {
		polygonBackground.querySelector('#polygonHolder').remove();
		polygonBackground.insertAdjacentHTML('beforeend', generatePolygonBackground());
	});
};

backgroundAnimation();
