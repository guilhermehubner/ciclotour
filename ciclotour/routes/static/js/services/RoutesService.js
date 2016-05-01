angular.module("ciclotourApp").factory('RoutesAPI', function($http){
    return{
        get_route: function(id){
            return $http.get("/api/routes/"+id);
        },
        get_fields: function(){
            return $http.get("/api/fields/");
        },
        get_pointkinds: function(){
            return $http.get("/api/pointkinds/");
        },
        get_route_points: function(routeId){
            return $http.get("/api/route/points/"+routeId);
        },
        save_route_point: function(point){
            return $http.post("/api/route/points/", point);
        },
        save_route: function(route){
            return $http.post("/api/routes/", route);
        }
    }
});