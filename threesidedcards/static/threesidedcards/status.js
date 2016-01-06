var FlashcardStatus = angular.module('FlashcardStatus', []);

FlashcardStatus.controller('status', ['$scope','$timeout','$http',function($scope,$timeout,$http) {

    $scope.users = []
    $scope.error = ''
   
    $scope.fetch = function() {
        $http.get('/flashcards/statusData/', {}).then(function(response) {
            $scope.users = response.data
        },function(response) {
            $scope.error = response.statusText
        });
    }
    $scope.fetch()

   
   

}])


FlashcardStatus.directive("histogram", function() {
    return {
        scope: {
            histogram: '='
        },
        template: "<canvas width='200' height='200'></canvas>",      
        link: function($scope, $element, $attrs) {
            $scope.canvas = $element.find('canvas')[0];
            $scope.context = $scope.canvas.getContext('2d');
            
            $scope.canvas.width = $element[0].offsetWidth - 10

            $scope.draw = function() {
                 var ctx = $scope.context
                 ctx.clearRect(0, 0, $scope.canvas.width, $scope.canvas.height);
                 ctx.fillStyle = "black";
                 ctx.font = "15px sans";
                 ctx.textAlign = "center";
                 ctx.fillText("Flashcard Histogram", $scope.canvas.width/2, 15); 

                 var yoffset =$scope.canvas.height - 20
                 ctx.beginPath()
                 ctx.moveTo(20,yoffset)
                 ctx.lineTo($scope.canvas.width - 20,yoffset)
                 ctx.strokeStyle = "black"
                 ctx.lineWidth = "2"
                 ctx.stroke()
                 
                 var categories = []

                 var lookup = []
                 lookup[0] = "1 min"
                 lookup[1] = "1 hr"
                 lookup[2] = "1 day"
                 lookup[3] = "1/2 wk"
                 lookup[4] = "1 wk"
                 lookup[5] = "2 wk"
                 lookup[6] = "1 mon"

                 var pos = 20 
                 var divide = ($scope.canvas.width - 40)/7
                 ctx.font = "10px sans";
                 for (var i = 0; i<=6; i++) {
                    ctx.fillText(lookup[i], pos + divide/2, $scope.canvas.height-5); 
                    pos += divide
                    categories.push({"Characters": 0, "Pinyin": 0, "English": 0})
                 }

                 
                 for (var i = 0; i<$scope.histogram.length; i++) {
                     var elem = $scope.histogram[i]
                     if (elem.direction[1] == 'C') categories[Math.floor(elem.score)].Characters++
                     if (elem.direction[1] == 'P') categories[Math.floor(elem.score)].Pinyin++
                     if (elem.direction[1] == 'E') categories[Math.floor(elem.score)].English++
                }

                 var max = 0
                 for (var i = 0; i<=6; i++) {
                     var sum = categories[i].Characters + categories[i].Pinyin + categories[i].English
                     if (sum > max) max = sum
                 }
                 
                 var pos = 20 
                 for (var i = 0; i<=6; i++) {
                    var height = yoffset
                    ctx.fillStyle = "#F66"
                    var delta = (yoffset - 30)*categories[i].Characters/max
                    ctx.fillRect(pos+10,height - delta,divide-20,delta)
                    ctx.strokeRect(pos+10,height - delta,divide-20,delta)
                    height -= delta

                    ctx.fillStyle = "#AAF"
                    var delta = (yoffset - 30)*categories[i].Pinyin/max
                    ctx.fillRect(pos+10,height - delta,divide-20,delta)
                    ctx.strokeRect(pos+10,height - delta,divide-20,delta)
                    height -= delta


                    ctx.fillStyle = "#FF8"
                    var delta = (yoffset - 30)*categories[i].English/max
                    ctx.fillRect(pos+10,height - delta,divide-20,delta)
                    ctx.strokeRect(pos+10,height - delta,divide-20,delta)


                    pos += divide
                 }




            }
            $scope.draw()

        }
    }
})



