angular.module("ciclotourApp").directive("profileInfo",function(){
    return {
        templateUrl: "static/js/views/profile.html",
        restrict: "E",
        controller: function($scope, $cookies, $state, UsersAPI){
            $scope.image = "";
            $scope.name = "";
            $scope.lastName = "";
            $scope.friends = "";
            $scope.pending_requests_count = "";

            $scope.load = function(){
                UsersAPI.get_info().success(function(data){
                    $scope.name = data.name;
                    $scope.lastName = data.last_name;
                    $scope.image = data.get_profile_pic;
                    $scope.friends = data.get_friends_count;
                    $scope.pending_requests_count = data.get_pending_requests_count;
                    $scope.pending_routes_count = data.pending_routes_count;
                    $scope.performed_routes_count = data.performed_routes_count;
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