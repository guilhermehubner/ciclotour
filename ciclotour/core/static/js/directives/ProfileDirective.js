angular.module("ciclotourApp").directive("profileInfo",function(){
    return {
        templateUrl: "static/js/views/profile.html",
        restrict: "E",
        controller: function($scope, $cookies, $state, UsersAPI){
            $scope.image = "";
            $scope.name = "";
            $scope.lastName = "";

            $scope.load = function(){
                UsersAPI.get_info().success(function(data){
                    $scope.name = data.name;
                    $scope.lastName = data.last_name;
                    $scope.image = data.get_profile_pic;
                });
            };

            $scope.logout = function(){
                $cookies.remove("token");
                $state.go("login");
            }
        },
        link: function(scope){
            scope.load();
        }
    };
});