(function ($) {
	"use strict";

	/*-------------------------------------
	 // Marker Map
	 -------------------------------------*/
	function renderMap(map_element_id, lat, lon, icon_url, map_type="Styled"){
		if ($("#".concat(map_element_id)).length) {
			window.onload = function () {
				var styles = [
					{
						featureType: 'water',
						elementType: 'geometry.fill',
						stylers: [{
							color: '#b7d0ea'
						}]
					}, 
					{
						featureType: 'road',
						elementType: 'labels.text.fill',
						stylers: [{
							visibility: 'off'
						}]
					}, 
					{
						featureType: 'road',
						elementType: 'geometry.stroke',
						stylers: [{
							visibility: 'off'
						}]
					}, 
					{
						featureType: 'road.highway',
						elementType: 'geometry',
						stylers: [{
							color: '#c2c2aa'
						}]
					}, 
					{
						featureType: 'poi.park',
						elementType: 'geometry',
						stylers: [{
							color: '#b6d1b0'
						}]
					}, 
					{
						featureType: 'poi.park',
						elementType: 'labels.text.fill',
						stylers: [{
							color: '#6b9a76'
						}]
					}
				];
				var options = {
					mapTypeControlOptions: {
						mapTypeIds: [map_type]
					},
					center: new google.maps.LatLng(lat, lon),
					zoom: 10,
					disableDefaultUI: true,
					mapTypeId: map_type
				};
				var div = document.getElementById('markergoogleMap');
				var map = new google.maps.Map(div, options);
				var styledMapType = new google.maps.StyledMapType(styles, {
					name: map_type
				});
				map.mapTypes.set(map_type, styledMapType);
	
				var marker = new google.maps.Marker({
					position: map.getCenter(),
					animation: google.maps.Animation.BOUNCE,
					icon: icon_url,
					map: map
				});
			};
		}
	}

})(jQuery);