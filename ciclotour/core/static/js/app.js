angular.module('ciclotourApp', ['ui.router', 'ngCookies']).config(function($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.interceptors.push('authInterceptor');

    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
    })
    .run(function($rootScope, $urlRouter, $state, Auth) {
        $rootScope.$on('$locationChangeSuccess', function(event) {
            event.preventDefault();

            Auth.isLoggedIn().success(
                function(data){
                    if(data.logged){
                        $urlRouter.sync();
                    }
                    else {
                        $state.go("login");
                    }
                }
            ).error(
                function(){
                    $state.go("login");
                }
            );
        });
    });