angular.module("ciclotourApp").controller('LoginController', function ($scope, $state, $cookies, Auth) {
    $scope.email = "";
    $scope.password = "";

    $scope.errors = {};

    $scope.login = function () {
        $scope.errors = {};
        Auth.authenticate($scope.email, $scope.password, successAuth, errorAuth);
    };

    function successAuth(data){
        var cookieExpire = new Date();
        cookieExpire.setFullYear(cookieExpire.getFullYear() +1);

        $cookies.put("token", data.token, {'expires': cookieExpire});
        $state.go("home");
    }

    function errorAuth(data){
        $scope.errors = data;
    }
});