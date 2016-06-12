angular.module("ciclotourApp").controller('PointDetailController', function($scope, $stateParams, $state, RoutesAPI, Message) {
    $scope.mapMarkers = [];
    $scope.route = {};
    $scope.point = null;
    $scope.pointkinds = [];
    $scope.comment = "";
    $scope.comments = [];

    /******************************************
     * Responsible method to get server
     * informations and init map
     *******************************************/
    $scope.initMap = function(){
        RoutesAPI.get_route_point($stateParams.id).success(function(data) {
            $scope.point = data;

            RoutesAPI.get_pointkinds().success(function (data) {
                $scope.pointkinds = data;
            });

            RoutesAPI.get_route($scope.point.route).success(function (data) {
                $scope.route = data;
                var map = startMap("map");

                $scope.route.waypoint_set.forEach(function (waypoint, index) {
                    addNumericMarker(getCoordinates(waypoint), map, index);
                });

                $scope.route.polyline_set.forEach(function (polyline) {
                    renderPolyline(
                        google.maps.geometry.encoding.decodePath(
                            polyline.encoded_polyline)
                        , map);
                });

                new google.maps.Marker({
                    position: getCoordinates($scope.point),
                    map: map,
                    icon: $scope.point.kind_info.icon
                });

                setZoom(map);
            });

            $scope.getComments();
        }).error(function(data){
            Message.showWarning('Ponto não encontrado.', 'Ocorreu uma falha ao tentar ' +
                'encontrar o ponto informado. Tente novamente.');

            console.log(data);
            $state.go("home");
        });
    };

    $scope.getComments = function(){
        if($scope.next == null && $scope.comments.length == 0)
            RoutesAPI.get_point_comments($scope.point.id).success(getCommentsSuccess)
                .error(getCommentsFail);
        else if($scope.next && $scope.comments.length > 0)
            RoutesAPI.get_next_point_comments($scope.point.id, $scope.next)
                .success(getCommentsSuccess).error(getCommentsFail);
    };

    $scope.postComment = function(){
        if ($scope.comment == "")
            return;

        RoutesAPI.post_point_comment($scope.point.id, $scope.comment)
            .success(postCommentSuccess).error(postCommentFail);
    };

    function postCommentSuccess(data){
        $scope.comments.unshift(data);
        $scope.comment = "";
    }

    function postCommentFail(data){
        Message.showWarning('Não foi possível postar comentário.', 'Ocorreu uma falha ao tentar ' +
            'postar comentário. Tente novamente.');

        console.log(data);
    }

    function getCommentsSuccess(data){
        $scope.next = data.next;
        $scope.comments = $scope.comments.concat(data.results);
    }

    function getCommentsFail(data){
        Message.showWarning('Não foi possível obter comentários.', 'Ocorreu uma falha ao tentar ' +
            'obter comentários. Tente novamente.');

        console.log(data);
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