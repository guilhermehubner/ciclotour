angular.module("ciclotourApp").controller('ContentController', function($scope){
    $scope.feed_active = true;
    $scope.routes_active = false;

    $scope.select_feed = function(){
        $scope.feed_active = true;
        $scope.routes_active = false;
    };

    $scope.select_routes = function(){
        $scope.routes_active = true;
        $scope.feed_active = false;
    };

    angular.element(document).ready(function () {
        resizeMainPanel();
    });
});