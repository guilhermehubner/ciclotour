angular.module("ciclotourApp").controller('ContentController', function($scope, RoutesAPI, Message){
    $scope.feed_active = true;
    $scope.routes_active = false;
    $scope.routes = [];

    $scope.next = null;

    $scope.select_feed = function(){
        $scope.feed_active = true;
        $scope.routes_active = false;
    };

    $scope.select_routes = function(){
        $scope.routes_active = true;
        $scope.feed_active = false;
        $scope.next = null;
        $scope.routes = [];

        get_routes();
    };

    $scope.getNext = get_routes;

    function get_routes(){
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
        Message.showWarning('Não foi possível obter rotas.', 'Ocorreu uma falha ao tentar obter rotas. ' +
            'Tente novamente.');

        console.log(data);
    }

    angular.element(document).ready(function () {
        resizeMainPanel();
    });
});