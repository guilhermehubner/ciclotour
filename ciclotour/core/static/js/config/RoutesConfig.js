angular.module("ciclotourApp").config(function ($stateProvider, $urlRouterProvider) {
    $stateProvider
        .state('login', {
            url: "/login",
            templateUrl: "static/js/views/login.html"
        })
        .state('home', {
            url: "/home",
            templateUrl: "static/js/views/home.html"
        })
        .state('routeCreate',{
            url: "/routeCreate",
            templateUrl: "static/js/views/routes_form.html"
        })
        .state('routeDetail',{
            url: "/routeDetail/{id:[0-9]+}",
            templateUrl: "static/js/views/routes_detail.html"
        })
        .state('routePointCreate',{
            url: "/routePointCreate/{id:[0-9]+}",
            templateUrl: "static/js/views/routes_point_form.html"
        });

    $urlRouterProvider.otherwise("/home");
});
