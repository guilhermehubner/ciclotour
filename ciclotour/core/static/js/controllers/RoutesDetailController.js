angular.module("ciclotourApp").controller('RoutesDetailController', function($scope, $interval) {

    var icons = {
        nature: "https://mt.googleapis.com/vt/icon/name=icons/onion/145-tree.png",
        restaurant: "http://awesomeberlin.net/wp-content/uploads/leaflet-maps-marker-icons/restaurant.png",
        hotel: "http://google-maps-icons.googlecode.com/files/hotel.png"
    };

    $scope.mapMarkers = [];
    $scope.mapPolylines = [];
    $scope.wayPoints = [];

    $scope.percentage = 0;
    $scope.loaded = false;

    $scope.initMap = function(){
        var map = startMap("map");

        $scope.wayPoints = JSON.parse($('#wayPoints').val());

        for(var i=0; i< $scope.wayPoints.length; i++){
            if($scope.wayPoints[i].kind == "G"){
                addNumericMarker(getCoordinates($scope.wayPoints[i]), map, i);

                setTimeout(
                    renderRoute, 1000*i, getCoordinates($scope.wayPoints[i - 1]),
                    getCoordinates($scope.wayPoints[i]),
                    map
                );
            }else if($scope.wayPoints[i].kind == "L"){
                addNumericMarker(getCoordinates($scope.wayPoints[i]), map, i);

                renderLinearRoute([getCoordinates($scope.wayPoints[i-1]),
                            getCoordinates($scope.wayPoints[i])],
                            map
                );
            }else{
                addNumericMarker(getCoordinates($scope.wayPoints[i]), map, i);
            }
        }

        var count =0;
        $interval(function(){
            if($scope.percentage<=100)
                $scope.percentage += (1 /$scope.wayPoints.length) * 100;

            $scope.loaded = ++count == $scope.wayPoints.length;
        },1000, $scope.wayPoints.length);

        setZoom(map);
    };

    function getCoordinates(wayPoint){
        return {
            lat: Number(wayPoint.latitude),
            lng: Number(wayPoint.longitude)
        };
    }

    /******************************************
     * Responsible method to render a marker on
     * map and add it to marker's list
    *******************************************/
    function addNumericMarker(coordinates, map, step){
        //Create marker and render it on map
        var marker = new google.maps.Marker({
            position: coordinates,
            map: map,
            icon: "http://" + window.location.host+"/static/img/mapIcons/marker/black" +
            (step + 1) + ".png"
        });

        //Add marker on list
        $scope.mapMarkers.push(marker);
    }

    /******************************************
     * Responsible method to render a polyline(path)
     * on map and add it to polyline's list
    *******************************************/
    function renderLinearRoute(path, map){
        //Create polyline and render it on map
        var polyLine = new google.maps.Polyline({
            path: path,
            map: map,
            geodesic: true,
            strokeColor: '#000000',
            strokeWeight: 5
        });

        //Add polyline on list
        $scope.mapPolylines.push(polyLine);
    }

    /******************************************
     * Responsible method to request a route from
     * google and render it on map
    *******************************************/
    function renderRoute(originCoordinates, destinationCoordinates, map){
        //Starts the google directions service
        var directionsService = new google.maps.DirectionsService();

        //Performs the bicycling route request between the origin and destination
        directionsService.route({
                origin: originCoordinates,
                destination: destinationCoordinates,
                travelMode: google.maps.TravelMode.BICYCLING //BICYCLING, DRIVING, TRANSIT, WALKING
            },
            function(response, status) {
                //If success on request, render the route
                if (status === google.maps.DirectionsStatus.OK) {
                    var path = [];
                    var legs = response.routes[0].legs;

                    //Build the path to render a polyline
                    for (i = 0; i < legs.length; i++) {
                        var steps = legs[i].steps;
                        for (j = 0; j < steps.length; j++) {
                            var nextSegment = steps[j].path;
                            for (k = 0; k < nextSegment.length; k++) {
                                path.push(nextSegment[k]);
                            }
                        }
                    }

                    //Render the polyline with the google path on map
                    renderLinearRoute(path, map);
                }
                else { // If request failed, log it on console
                    console.log('Directions request failed due to ' + status);
                }
            });
    }

    function startMap(target){
        return map = new google.maps.Map(document.getElementById(target), {
            center:{lat:-19.9435015,lng:-43.968830108642600},
            zoom:12,
            scrollwheel: true,
            streetViewControl: false,
            mapTypeId: google.maps.MapTypeId.HYBRID //ROADMAP, SATELLITE, HYBRID, TERRAIN
        });
    }

    function setZoom(map){
        var bounds = new google.maps.LatLngBounds();

        $scope.mapMarkers.forEach(function(marker){
            bounds.extend(marker.position);
        });

        map.fitBounds(bounds);
    }
});