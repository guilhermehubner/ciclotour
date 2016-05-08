angular.module("ciclotourApp").config(function ($stateProvider, $urlRouterProvider, $urlMatcherFactoryProvider) {

    var GUID_REGEXP = /^[a-f\d]{8}-([a-f\d]{4}-){3}[a-f\d]{12}$/i;
    $urlMatcherFactoryProvider.type('guid', {
        encode: angular.identity,
        decode: angular.identity,
        is: function(item) {
            return GUID_REGEXP.test(item);
        }
    });

    $stateProvider
        .state('login', {
            url: "/login",
            templateUrl: "static/js/views/login.html"
        })
        .state('confirmation', {
            url: "/confirmation/{token:guid}",
            templateUrl: "static/js/views/confirmation.html"
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
