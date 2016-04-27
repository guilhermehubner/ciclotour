angular.module("ciclotourApp").directive("profileInfo",function(){
    return {
        templateUrl: "static/js/views/profile.html",
        restrict: "E",
        controller: function($scope, $cookies, $location, UserProfileInfoAPI){
            $scope.image = "";
            $scope.name = "";
            $scope.lastName = "";

            $scope.load = function(){
                UserProfileInfoAPI.get_info().success(function(data){
                    $scope.name = data.name;
                    $scope.lastName = data.last_name;
                    $scope.image = data.get_profile_pic;
                });
            };

            $scope.logout = function(){
                $cookies.remove("token");
                $location.path("/login");
            }
        },
        link: function(scope){
            scope.load();
        }
    };
});