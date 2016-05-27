angular.module("ciclotourApp").factory('RoutesAPI', function($http){
    return{
        get_route: function(id){
            return $http.get("/api/routes/"+id);
        },
        get_routes: function(){
            return $http.get("/api/routes/");
        },
        get_next_routes: function(next){
            return $http.get("/api/routes/?page="+next);
        },
        get_fields: function(){
            return $http.get("/api/fields/");
        },
        get_pointkinds: function(){
            return $http.get("/api/pointkinds/");
        },
        get_route_pictures: function(routeId){
            return $http.get("/api/route/pictures/?route="+routeId);
        },
        get_next_pictures: function(routeId, next){
            return $http.get("/api/route/pictures/?route="+routeId+"&page="+next);
        },
        save_route_point: function(point){
            return $http.post("/api/route/points/", point);
        },
        save_route_picture: function(picture){
            var fd = new FormData();

            for (var key in picture) {
                fd.append(key, picture[key]);
            }

            return $http.post("/api/route/pictures/", fd,{
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            });
        },
        save_route: function(route){
            return $http.post("/api/routes/", route);
        }
    }
});