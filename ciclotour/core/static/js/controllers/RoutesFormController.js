angular.module("ciclotourApp").controller('RoutesFormController', function($scope, $http){
    $scope.origin = ""; //origin name get from user entry
    $scope.wayPoints = []; //the list of points will be sent to server
    $scope.mapMarkers = []; //the list of route markers
    $scope.mapPolylines = []; //the list of routes path's
    $scope.manualMode = false; //boolean which indicates if path should be drawn by google or
    // simple straight line

    /******************************************
     * This method try to find one place through
     * user entry and init one map centralized in
     * this place
    *******************************************/
    $scope.setOrigin = function (){
        $scope.wayPoints = [];
        $scope.mapMarkers = [];
        $scope.mapPolylines = [];

        if($scope.origin != "") {
            //Build the URL to get place from google maps api
            var url = "https://maps.googleapis.com/maps/api/geocode/json?address="
                + $scope.origin.toString();

            //Performs request and get coordinates
            $http.get(url).success(function(data){
                var originCoordinates = {
                    lat: data.results[0].geometry.location.lat,
                    lng: data.results[0].geometry.location.lng
                };

                //Init map
                initMap(originCoordinates, "map");
            });
        }
        else {
            var originCoordinates = null;
            initMap(originCoordinates, "map");
        }
    };

    /******************************************
     * Undo the last change done by user
    *******************************************/
    $scope.undo = function(){
        if($scope.wayPoints.length == 0)
            return;

        $scope.wayPoints.pop();
        $scope.mapMarkers.pop().setMap(null);

        if($scope.mapPolylines.length > 0)
            $scope.mapPolylines.pop().setMap(null);
    };

    /******************************************
     * Responsible method to render map
    *******************************************/
    function startMap(center, target){
        //Set map configurations
        var mapOptions = {
            center: center,
            scrollwheel: false,
            streetViewControl: false,
            zoom: 12,
            draggableCursor: 'default',
            mapTypeId: google.maps.MapTypeId.HYBRID //ROADMAP, SATELLITE, HYBRID, TERRAIN
        };

        //Get map container element
        var mapDiv = document.getElementById(target);

        //Instanciate the map object
        var map = new google.maps.Map(mapDiv, mapOptions);

        //Add click event listener.
        //For each user click on map, get the coordinates, create a marker and
        //trace route between last marker and actual position requested by user
        google.maps.event.addListener(map, "click", function(event) {
            addWayPoint(event.latLng, map);
        });

        return map;
    }

    /******************************************
     * Responsible method to create a marker and
     * trace route between last marker and actual position
     * requested by user
    *******************************************/
    function addWayPoint(coordinates, map){
        if($scope.wayPoints.length > 0) { //Case this is the second way point or above

            if($scope.manualMode){ //If manual, mode must render a linear route
                //Defines the path as the last way point added until the actual informed
                var path = [$scope.wayPoints[$scope.wayPoints.length - 1].coordinates, coordinates];

                //Render the straight line
                renderLinearRoute(path, map);

                //Add marker on map
                addMarker(coordinates, map);

                //Add actual way point
                $scope.wayPoints.push({
                    type: 'L', // LINEAR
                    coordinates: coordinates
                });
            }
            else{ //If not manual mode, must render a route indicated by google
                renderRoute($scope.wayPoints[$scope.wayPoints.length - 1].coordinates,
                    coordinates, map);
            }
        }
        else{ // Case this is the first way point, only add a marker on map
            addMarker(coordinates, map);

            //Add actual way point
            $scope.wayPoints.push({
                type: 'N', //NONE
                coordinates: coordinates
            });
        }
    }

    /******************************************
     * Responsible method to render a marker on
     * map and add it to marker's list
    *******************************************/
    function addMarker(coordinates, map){
        //Create marker and render it on map
        var marker = new google.maps.Marker({
            position: coordinates,
            map: map,
            icon: "http://" + window.location.host+"/static/img/mapIcons/marker/black" +
            ($scope.wayPoints.length + 1) + ".png"
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
            strokeWeight: 6,
            strokeOpacity: 0.6
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

                    var myroute = response.routes[0].legs[0];

                    var originCoordinates = myroute.steps[0].start_point;
                    var destinationCoordinates = myroute.steps[myroute.steps.length - 1].end_point;

                    //Check if google have changed the origin coordinates, case true,
                    //add a path to link the last waypoint to new google route
                    if($scope.wayPoints[$scope.wayPoints.length - 1].coordinates != originCoordinates)
                        path.push($scope.wayPoints[$scope.wayPoints.length - 1].coordinates);

                    //Add marker on list
                    addMarker(destinationCoordinates, map);

                    //Add waypoint on list
                    $scope.wayPoints.push({
                        type: 'G', //GOOGLE
                        coordinates: destinationCoordinates
                    });

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

    /******************************************
     * Responsible method to initiate the map
    *******************************************/
    function initMap(origin, target) {
        if(origin != null){
            map = startMap(origin, target);
        }
        else{
            $(target).html("");
            $(target).removeAttr('style');
        }
    }
});