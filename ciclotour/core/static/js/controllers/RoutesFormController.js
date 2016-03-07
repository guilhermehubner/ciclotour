angular.module("ciclotourApp").controller('RoutesFormController', function($scope, $http){
    $scope.origin = "";
    $scope.destination = "";

    $scope.originCoordinates = null;
    $scope.destinationCoordinates = null;

    $scope.setOrigin = function (){
            var url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + $scope.origin.toString();
            if($scope.origin != "") {
                $http.get(url).success(function(data){
                    $scope.originCoordinates = {
                        lat: data.results[0].geometry.location.lat,
                        lng: data.results[0].geometry.location.lng
                    };

                    initMap($scope.originCoordinates, $scope.destinationCoordinates, "map");
                });
            }
            else {
                $scope.originCoordinates = null;
                initMap($scope.originCoordinates, $scope.destinationCoordinates, "map");
            }
        };

    $scope.setDestination = function (){
            if($scope.destination) {
                var url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + $scope.destination.toString();
                $http.get(url).success(function(data){
                    $scope.destinationCoordinates = {
                        lat: data.results[0].geometry.location.lat,
                        lng: data.results[0].geometry.location.lng
                    };

                    initMap($scope.originCoordinates, $scope.destinationCoordinates, "map");
                });
            }
            else {
                $scope.destinationCoordinates = null;
                initMap($scope.originCoordinates, $scope.destinationCoordinates, "map");
            }
        };

        function startMap(center, target){
            return map = new google.maps.Map(document.getElementById(target), {
                center: center,
                scrollwheel: true,
                zoom: 10
            });
        }

        function addMarker(map, coordinates, title){
            return new google.maps.Marker({
                map: map,
                position: coordinates,
                title: title
            });
        }

        function setZoom(map, originMarker, destinationMarker){
            var bounds = new google.maps.LatLngBounds();
            bounds.extend(originMarker.position);
            bounds.extend(destinationMarker.position);
            map.fitBounds(bounds);
        }

        function initMap(origin, destination, target) {
            if(origin != null && destination != null){
                map = startMap(origin, target);

                // Create markers and set its position.
                originMarker = addMarker(map, origin, "Origem!");
                destinationMarker = addMarker(map, destination, "Destino!");

                //Fit map
                setZoom(map, originMarker, destinationMarker);
            }
            else if(origin != null)            {
                map = startMap(origin, target);

                // Create a marker and set its position.
                originMarker = addMarker(map, origin, "Origem!");
            }
            else if(destination != null) {
                map = startMap(destination, target);

                // Create a marker and set its position.
                originMarker = addMarker(map, destination, "Destino!");
            }
            else{
                $(target).html("");
                $(target).removeAttr('style');
            }
        }
});