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
        template: "<canvas width='200' height='250'></canvas>",      
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
                 

                 var lookup = []
                 lookup[0] = "1 min"
                 lookup[1] = "1 hr"
                 lookup[2] = "1 day"
                 lookup[3] = "1/2 wk"
                 lookup[4] = "1 wk"
                 lookup[5] = "2 wk"
                 lookup[6] = "1 mon"
                 lookup[7] = "2 mon"
                 lookup[8] = "4 mon"
                 lookup[9] = "8 mon"
                 lookup[10] = "1 yr"

                 var categories = []
                 var chapters = []
                 var maxchapter = 1
                 
                 for (var i = 0; i<$scope.histogram.length; i++) {
                     var elem = $scope.histogram[i]
                        
                     while (elem.score+1 > categories.length) categories.push({"Characters": 0, "Pinyin": 0, "English": 0})
                     while (elem.score+1 > chapters.length) chapters.push([])

                     if (elem.direction[1] == 'C') categories[Math.floor(elem.score)].Characters++
                     if (elem.direction[1] == 'P') categories[Math.floor(elem.score)].Pinyin++
                     if (elem.direction[1] == 'E') categories[Math.floor(elem.score)].English++
                     
                     if (!(Math.floor(elem.chapter) in chapters[Math.floor(elem.score)])) {
                        chapters[Math.floor(elem.score)][Math.floor(elem.chapter)] = 0
                     }     
                     chapters[Math.floor(elem.score)][Math.floor(elem.chapter)]++

                     if (maxchapter < Math.floor(elem.chapter)) maxchapter = Math.floor(elem.chapter)
                }

                 var histlength = 4
                 while (histlength > categories.length) categories.push({"Characters": 0, "Pinyin": 0, "English": 0})
                 if (categories.length > histlength) histlength = categories.length

                
                     
                 var pos = 20 
                 var divide = ($scope.canvas.width - 40)/histlength
                 ctx.font = "10px sans";
         
                 for (var i = 0; i<histlength; i++) {
                    ctx.fillText(lookup[i], pos + divide/2, $scope.canvas.height-5); 
                    pos += divide
                 }


                 var max = 0
                 var chmax = 0
                 for (var i = 0; i<histlength; i++) {
                     var sum = categories[i].Characters + categories[i].Pinyin + categories[i].English
                     if (sum > max) max = sum

                     var chsum = 0
                     for (var j = 1; j<=maxchapter; j++) {
                        if (chapters[i] == undefined) continue
                        if (chapters[i][j] == undefined) continue
                        chsum += chapters[i][j]
                     }
                     if (chsum > chmax) chmax = chsum
                    
                 }
                
                 /*
                 var pos = 20 
                 for (var i = 0; i<histlength; i++) {
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

                 */

                 getColor = function(chapter) {
                    mag = Math.round(200*chapter/maxchapter)
                    return "rgb("+(mag+55)+","+(255-mag)+",255)"
                 }

                 var pos = 20 
                 for (var i = 0; i<histlength; i++) {
                    var height = yoffset
                    
                    
                    for (var j = 1; j<=maxchapter; j++) {
                        if (chapters[i] == undefined) continue
                        if (chapters[i][j] == undefined) continue
                        var delta = (yoffset - 30)*chapters[i][j]/chmax
                        ctx.fillStyle = getColor(j)
                        ctx.fillRect(pos+10,height - delta,divide-20,delta)
                        ctx.strokeRect(pos+10,height - delta,divide-20,delta)

                        if (delta > 15) {
                            ctx.fillStyle ="black"
                            ctx.font = "12px sans bold";
                            ctx.fillText(j, pos+divide/2, height-delta+13); 
                            
                        }
                        height -= delta
                        
                    }

                    var cumulative = 0
                    var total = 0
                    for (var j = i; j < histlength; j++) {
                        for (var k = 1; k<=maxchapter; k++) {
                            if (chapters[j] == undefined) continue
                            if (chapters[j][k] == undefined) continue
                            if (j == i) total += chapters[j][k]
                            cumulative += chapters[j][k]
                        }
                    }

                    ctx.fillStyle ="black"
                    ctx.font = "12px sans bold";
                    ctx.fillText(Math.round(10*total/6)/10, pos+divide/2, height-5); 
                    ctx.font = "9px sans bold";
                    ctx.fillText(Math.round(10*cumulative/6)/10, pos+divide/2, height-18); 
                        
                    pos += divide

                 }


            }
            $scope.draw()

        }
    }
})



