angular.module("ciclotourApp").controller('PointController', function($scope, $stateParams, $state, RoutesAPI) {

    /*********** Point Fields ****************/

    $scope.address = "";
    $scope.pointkind = "";
    $scope.title = "";
    $scope.description = "";
    $scope.longitude = null;
    $scope.latitude = null;

    /******************************************/

    $scope.mapMarkers = [];
    $scope.route = {};
    $scope.point = null;
    $scope.pointkinds = [];

    /******************************************
     * Responsible method to get server
     * informations and init map
    *******************************************/
    $scope.initMap = function(){
        RoutesAPI.get_pointkinds().success(function(data){
            $scope.pointkinds = data;
        });

        RoutesAPI.get_route($stateParams.id).success(function(data){
            $scope.route = data;
            var map = startMap("map");

            //Add click event listener.
            //For each user click on map, get the coordinates, create
            //or update marker position
            google.maps.event.addListener(map, "click", function(event) {
                addOrUpdatePoint(event.latLng, map);
            });

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
        });
    };

    /******************************************
     * Responsible method to refresh point icon
     * when kind change
    *******************************************/
    $scope.changeKind = function(){
        if($scope.point == null)
            return;

        setMarkerIcon();
    };

    /******************************************
     * Submit form data to server
    *******************************************/
    $scope.save = function(){
        var obj = {
            "title": $scope.title,
            "description": $scope.description,
            "kind": $scope.pointkind,
            "address": $scope.address,
            "latitude": $scope.latitude,
            "longitude": $scope.longitude,
            "route": $stateParams.id
        };

        RoutesAPI.save_route_point(obj).success(saveRoutePointSuccess).error(saveRoutePointFail);
    };

    /******************************************
     * Responsible method to alert success to user
     * on saving point
    *******************************************/
    function saveRoutePointSuccess(data){
        $('#myModal .modal-title').text('Ponto cadastrado com sucesso!');
        $('#myModal #modal-content').text('A Ponto foi cadastrado com sucesso.');
        $("#myModal").modal('show');

        $state.go("routeDetail", {id: data.route});
    }

    /******************************************
     * Responsible method to alert errors to user
     * on saving point
    *******************************************/
    function saveRoutePointFail(data){
        $('#myModal .modal-title').text('Falha ao cadastrar Ponto');
        $('#myModal #modal-content').text('Ocorreu uma falha ao tentar cadastrar o ponto.');
        $("#myModal").modal('show');
    }

    /******************************************
     * Responsible method to render a marker on
     * map or update it's position
    *******************************************/
    function addOrUpdatePoint(coordinates, map){
        if(!$scope.point){
            //Create marker and render it on map
            $scope.point = new google.maps.Marker({
                position: coordinates,
                map: map
            });
        }
        else{
            $scope.point.setMap(null);

            $scope.point = new google.maps.Marker({
                position: coordinates,
                map: map
            });
        }

        $scope.latitude = coordinates.lat();
        $scope.longitude = coordinates.lng();

        setMarkerIcon();
        setAddress(coordinates);
    }

    function setAddress(coordinates){
        var geocoder = new google.maps.Geocoder;
        geocoder.geocode({'location': coordinates}, function(results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                if (results[0]) {
                    $scope.address = results[0].formatted_address;
                    $scope.$apply();
                }
            }
        });
    }

    function setMarkerIcon(){
        if($scope.pointkind == "") {
            $scope.point.setIcon(null);
        }
        else{
            $scope.point.setIcon(
                $scope.pointkinds.find(
                    function(x){return x.id == $scope.pointkind;}
                ).icon);
        }
    }

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