angular.module("ciclotourApp").controller('RoutesFormController', function($scope, $http){
    $scope.origin = "";
    $scope.wayPoints = [];

    $scope.setOrigin = function (){

        $scope.wayPoints = [];

        if($scope.origin != "") {
            var url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + $scope.origin.toString();
            $http.get(url).success(function(data){
                var originCoordinates = {
                    lat: data.results[0].geometry.location.lat,
                    lng: data.results[0].geometry.location.lng
                };

                initMap(originCoordinates, "map");
            });
        }
        else {
            var originCoordinates = null;
            initMap(originCoordinates, "map");
        }
    };

    $scope.undo = function(){
        if($scope.wayPoints.length <= 1)
        {
            $scope.setOrigin();
            $scope.wayPoints = [];
            return;
        }

        $scope.wayPoints.pop();

        var map = startMap($scope.wayPoints[0], "map");
        var oldList = $scope.wayPoints.slice(0);
        $scope.wayPoints = [];

        while(oldList.length > 0)
            addWayPoint(oldList.shift(), map);

        var bounds = new google.maps.LatLngBounds();
            bounds.extend($scope.wayPoints[0]);
            bounds.extend($scope.wayPoints[$scope.wayPoints.length-1]);
            map.fitBounds(bounds);
    };

    function startMap(center, target){
        var mapOptions = {
            center: center,
            scrollwheel: false,
            streetViewControl: false,
            zoom: 12,
            mapTypeId: google.maps.MapTypeId.HYBRID //ROADMAP, SATELLITE, HYBRID, TERRAIN
        };

        var mapDiv = document.getElementById(target);

        var map = new google.maps.Map(mapDiv, mapOptions);

        google.maps.event.addListener(map, "click", function(event) {
            addWayPoint(event.latLng, map);
        });

        return map;
    }

    function addWayPoint(coordinates, map){
        new google.maps.Marker({
            position: coordinates,
            map: map,
            icon: "http://" + window.location.host+"/static/img/mapIcons/marker/black" +
            ($scope.wayPoints.length + 1) + ".png"
        });

        if($scope.wayPoints.length > 0)
            renderRoute($scope.wayPoints[$scope.wayPoints.length-1], coordinates, map);

        $scope.wayPoints.push(coordinates);
    }

    function renderRoute(originCoordinates, destinationCoordinates, map){
        var renderer = new google.maps.DirectionsRenderer({
	            'draggable': false,
	            'suppressMarkers': true,
	            'preserveViewport': true
	        });
	        renderer.setMap(map);
	        renderer.setPanel(document.getElementById("directionsPanel"));
	        var directionsService = new google.maps.DirectionsService();

	        directionsService.route({
	                origin: originCoordinates,
	                destination: destinationCoordinates,
	                travelMode: google.maps.TravelMode.BICYCLING
	            }, function(response, status) {
	                if (status === google.maps.DirectionsStatus.OK) {
	                    renderer.setDirections(response);
	                } else {
	                    console.log('Directions request failed due to ' + status);
	                }
            });
    }

    function initMap(origin, target) {
        if(origin != null)            {
            map = startMap(origin, target);
        }
        else{
            $(target).html("");
            $(target).removeAttr('style');
        }
    }
});