angular.module("ciclotourApp").controller('RoutesDetailController', function($scope, $http) {

    var icons = {
        nature: "https://mt.googleapis.com/vt/icon/name=icons/onion/145-tree.png",
        restaurant: "http://awesomeberlin.net/wp-content/uploads/leaflet-maps-marker-icons/restaurant.png",
        hotel: "http://google-maps-icons.googlecode.com/files/hotel.png"
    };

    $scope.initMap = function(){
        initMap({lat: -19.9166813, lng: -43.9344931},
                {lat: -19.3276057, lng: -43.6187198},
                [
                    {coordinates: {lat: -19.5576057, lng: -43.6187198},
                        title:"Natureza Exuberante",
                        icon: icons.nature},
                    {coordinates: {lat: -19.6576057, lng: -43.7287198},
                        title:"Natureza Exuberante",
                        icon: icons.nature},
                    {coordinates: {lat: -19.4576057, lng: -43.9187198},
                        title:"Restaurante",
                        icon: icons.restaurant},
                    {coordinates: {lat: -19.6576057, lng: -44.0187198},
                        title:"Hotel",
                        icon: icons.hotel}
                ],
                "map"
        )
    };

    function initMap(origin, destination, points, target) {
        map = startMap(origin, target);

        // Create markers and set its position.
        originMarker = addMarker(map, origin, "Origem!");
        destinationMarker = addMarker(map, destination, "Destino!");

        //Fit map
        setZoom(map, originMarker, destinationMarker);

        points.forEach(function(point){
            addMarker(map, point.coordinates, point.title, point.icon)
        });
    }

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

    function addMarker(map, coordinates, title, icon){
        return new google.maps.Marker({
            map: map,
            position: coordinates,
            title: title,
            icon: icon
        });
    }

    function setZoom(map, originMarker, destinationMarker){
        var bounds = new google.maps.LatLngBounds();
        bounds.extend(originMarker.position);
        bounds.extend(destinationMarker.position);
        map.fitBounds(bounds);
    }
});