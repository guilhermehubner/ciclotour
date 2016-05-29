angular.module("ciclotourApp").controller('RoutesDetailController', function($scope, $stateParams, $state, Message, RoutesAPI) {
    $scope.mapMarkers = [];
    $scope.route = {};
    $scope.show = false;
    $scope.routeId = 0;

    /******************************************
     * Responsible method to get server
     * informations and init map
    *******************************************/
    $scope.initMap = function(){
        $scope.routeId = $stateParams.id;
        RoutesAPI.get_route($scope.routeId).success(function(data){
            $scope.route = data;
            var map = startMap("map");

            $scope.route.waypoint_set.forEach(function(waypoint, index){
                addNumericMarker(getCoordinates(waypoint), map, index);
            });

            $scope.route.polyline_set.forEach(function(polyline){
                renderPolyline(
                    google.maps.geometry.encoding.decodePath(
                        polyline.encoded_polyline)
                    , map);
            });

            setZoom(map);
            addRoutePointMarkers(map);
        }).error(function(){
            Message.showError("Não foi possível encontrar a rota.", "A rota solicitada não foi " +
                "encontrada, tente novamente.");

            $state.go("home");
        });
    };

    /******************************************
     * Responsible method to redirect to add point
     * form
    *******************************************/
    $scope.addPoint = function(){
        $state.go("routePointCreate", {'id': $scope.routeId});
    };

    /******************************************
     * Responsible method to show picture add
     * modal
    *******************************************/
    $scope.showModal = function(){
        $scope.show = true;
    };

    /******************************************
     * Responsible method to refresh list of pictures
    *******************************************/
    $scope.refreshRoutePictures = function(){
        RoutesAPI.get_route_pictures($scope.routeId).success(function(data){
            $scope.route.pictures = data.results;
        });
    };

    /******************************************
     * Responsible method to show picture in modal
    *******************************************/
    $scope.showPicture = function(url, description){
        $('#imagepreview').attr('src', url);
        $('#imagedescription').text(description);
        $('#imagemodal').modal('show');
    };

    /******************************************
     * Responsible method to return coodinates
     * from an waypoint
    *******************************************/
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
     * Responsible method to render all route point
     * markers on map
    *******************************************/
    function addRoutePointMarkers(map){
        $scope.route.points.forEach(function(point) {
            //Create marker and render it on map
            var marker = new google.maps.Marker({
                position: getCoordinates(point),
                map: map,
                icon: point.kind_info.icon
            });
        });
    }

    /******************************************
     * Responsible method to render a polyline(path)
     * on map and add it to polyline's list
    *******************************************/
    function renderPolyline(path, map){
        //Create polyline and render it on map
        new google.maps.Polyline({
            path: path,
            map: map,
            geodesic: true,
            strokeColor: '#000000',
            strokeWeight: 5
        });
    }

    /******************************************
     * Responsible method to render map
    *******************************************/
    function startMap(target){
        return map = new google.maps.Map(document.getElementById(target), {
            center:{lat:-19.9435015,lng:-43.968830108642600},
            zoom:12,
            scrollwheel: true,
            streetViewControl: false,
            mapTypeId: google.maps.MapTypeId.HYBRID //ROADMAP, SATELLITE, HYBRID, TERRAIN
        });
    }

    /******************************************
     * Responsible method to fit map zoom
    *******************************************/
    function setZoom(map){
        var bounds = new google.maps.LatLngBounds();

        $scope.mapMarkers.forEach(function(marker){
            bounds.extend(marker.position);
        });

        map.fitBounds(bounds);
    }

    angular.element(document).ready(function () {
        resizeMainPanel();
    });
});