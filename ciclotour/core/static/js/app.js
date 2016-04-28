angular.module('ciclotourApp', ['ui.router', 'ngCookies']).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});