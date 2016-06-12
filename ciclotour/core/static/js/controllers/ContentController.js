angular.module("ciclotourApp").controller('ContentController', function($scope, $http, RoutesAPI, UsersAPI, Message){
    $scope.feed_active = true;
    $scope.routes_active = false;
    $scope.routes = [];

    $scope.origin = "";
    $scope.destination = "";
    $scope.hasSearch = false;

    $scope.originCoordinates = null;
    $scope.destinationCoordinates = null;

    $scope.next = null;

    $scope.feeds = [];

    $scope.select_feed = function(){
        $scope.feed_active = true;
        $scope.routes_active = false;
        $scope.next = null;
        $scope.feeds = [];

        $scope.getFeed();
    };

    $scope.getFeed = function(){
         if($scope.next == null && $scope.feeds.length == 0)
            UsersAPI.get_feed().success(getFeedSuccess)
                .error(getFeedFail);
        else if($scope.next && $scope.feeds.length > 0)
            UsersAPI.get_next_feed($scope.next)
                .success(getFeedSuccess).error(getFeedFail);
    };

    $scope.select_routes = function(){
        $scope.routes_active = true;
        $scope.feed_active = false;
        $scope.next = null;
        $scope.routes = [];
        $scope.origin = "";
        $scope.destination = "";
        $scope.hasSearch = false;

        get_routes();
    };

    $scope.getNext = get_routes;

    $scope.search = function(origin,destination){
        $scope.origin = origin;
        $scope.destination = destination;
        if ($scope.origin == "" || $scope.destination == "") {
            Message.showWarning("Falha ao buscar","É preciso informar origem e destino para " +
                "buscar rotas.");
            return;
        }

        $scope.routes = [];
        $scope.next = null;
        $scope.hasSearch = true;

        var url = "https://maps.googleapis.com/maps/api/geocode/json?address="
            + $scope.origin.toString();
        $http.get(url, { withoutAuthToken: true }).success(function(data) {
            $scope.originCoordinates = {
                lat: data.results[0].geometry.location.lat,
                lng: data.results[0].geometry.location.lng
            };


            url = "https://maps.googleapis.com/maps/api/geocode/json?address="
                + $scope.destination.toString();
            $http.get(url, {withoutAuthToken: true}).success(function (data) {
                $scope.destinationCoordinates = {
                    lat: data.results[0].geometry.location.lat,
                    lng: data.results[0].geometry.location.lng
                };

                RoutesAPI.search($scope.originCoordinates, $scope.destinationCoordinates)
                    .success(getRoutesSuccess).error(getRoutesFail);
            });
        }).error(getRoutesFail);
    };

    function get_routes(){
        if($scope.hasSearch){
            if($scope.next == null)
                return;

            RoutesAPI.search_next($scope.originCoordinates, $scope.destinationCoordinates,
                $scope.next).success(getRoutesSuccess).error(getRoutesFail);
            return;
        }

        if($scope.next == null && $scope.routes.length == 0)
            RoutesAPI.get_routes().success(getRoutesSuccess).error(getRoutesFail);
        else if($scope.next && $scope.routes.length > 0)
            RoutesAPI.get_next_routes($scope.next).success(getRoutesSuccess).error(getRoutesFail);
    }

    function getRoutesSuccess(data){
        $scope.next = data.next;
        $scope.routes = $scope.routes.concat(data.results);
    }

    function getRoutesFail(data){
        Message.showWarning('Não foi possível buscar rotas.', 'Ocorreu uma falha ao buscar rotas. ' +
            'Tente novamente.');

        console.log(data);
    }

    function getFeedSuccess(data){
        $scope.next = data.next;
        $scope.feeds = $scope.feeds.concat(data.results);
    }

    function getFeedFail(data){
        Message.showWarning('Não foi possível obter feeds.', 'Ocorreu uma falha ao tentar ' +
            'obter feeds. Tente novamente.');

        console.log(data);
    }

    angular.element(document).ready(function () {
        resizeMainPanel();
    });
});