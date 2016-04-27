angular.module('ciclotourApp', ['ngRoute', 'ngCookies']).config(function($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.interceptors.push('authInterceptor');

    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}).run(['$rootScope', '$location', 'Auth', function ($rootScope, $location, Auth) {
    $rootScope.$on('$routeChangeStart', function (event, next) {
        Auth.isLoggedIn().success(
            function(data){
                if(data.logged){
                    if(next && next.$$route.originalPath.indexOf("/login") == -1){
                        console.log(next);
                        $location.path(next.$$route.redirectTo);}
                    else
                        $location.path('/home');
                }
                else {
                    event.preventDefault();
                    $location.path('/login');
                }
            }
        ).error(
            function(data){
                event.preventDefault();
                $location.path('/login');
            }
        );
    });
}]);
