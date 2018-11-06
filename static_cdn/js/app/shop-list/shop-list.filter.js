'use strict';

angular.module('shopList').
	filter('distanceFilter', function() {
  		return function ( dis ) {
    		var finalDistance
    		if(dis < 500)
    			finalDistance = Math.round( dis ) + ' m'
    		else
    			finalDistance = (dis/1000).toFixed(2) + ' km'
    		return finalDistance
	    }
  });
