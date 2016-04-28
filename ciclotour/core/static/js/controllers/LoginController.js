angular.module("ciclotourApp").controller('LoginController', function ($scope, $state, $cookies, Auth) {
    $scope.email = "";
    $scope.password = "";

    $scope.login = function () {
        Auth.authenticate($scope.email, $scope.password, successAuth, errorAuth);
    };

    function successAuth(res){
        var cookieExpire = new Date();
        cookieExpire.setFullYear(cookieExpire.getFullYear() +1);

        $cookies.put("token", res.token, {'expires': cookieExpire});
        $state.go("home");
    }

    function errorAuth(res){

    }
});