var ships = []
var flowers = [];
var score = 0;
var isGameOver = [];
var Neuvol;
var gen;
var alivecount;
var generation = 1;
var nearestflower = 2500;
var minindex = 0;
var a;
var flag;
//create the canvas and initialize the generation consiting of 5 ships.
function setup() {
  createCanvas(610, 600);
    for (var i = 0; i < 6; i++) {
    flowers[i] = new Flower(i*80+80, 60);
  }
setFrameRate(1);
  Neuvol = new Neuroevolution({
            population:1,
            network:[2, [9], 2],
            randomBehaviour:0.1,
            mutationRate:0.5, 
            mutationRange:2, 
        });

    gen = Neuvol.nextGeneration();

for(var i in this.gen){
        var b = new Ship();
        ships.push(b)
        isGameOver.push(false)
    }
    alivecount = ships.length;
}



//function used to draw to the canvas
function draw() 
{

      background(51);
      fill(0, 102, 153);
      text("Score: "+score, width-90, 30);
      text("Generation: "+generation,width-90,60);
    //show the ships
    for (var i in ships)
    {
            ships[i].show();
            if(generation % 2 ==0)
            {
                ships[0].setDir(1);    
    
            }
          else
          {
            ships[0].setDir(-1);
          }
    for(var k in flowers)
    {
        flowers[k].show();
    }
     
     //FIND THE NEAREST FLOWER
        nearestflower = 2500;
     
       
                for (var j in flowers)
                {
                    a = Math.abs(flowers[j].x-ships[i].x);
                    if(a <=nearestflower)
                    {
                        minindex = j;
                        nearestflower = a;
                    }
                }
                
            ///FEED THE INPUT TO THE NEUROEVOLUTION 

                var direction = ships[i].getDir();
                var inputs = [minindex,direction]
                var res = this.gen[i].compute(inputs);


                if(res > 0.5){
                        ships[i].SetDir(-1);
                    }
                    else
                    {
                        ships[i].setDir(1);
                    }
                    ships[i].move();
                flag = false;
                if((((ships[i].x - nearestflower) <=0) && (ships[i].getDir() == 1)) || (((ships[i].x - nearestflower) >=0) &&(ships[i].getDir() == -1)))
                {
                    flag = true;
                }
                    
                   
                    if(!flag)
                    {
                        flag = false;
                        score -=80;
                        ships[i].changeDir();

                    }
                        ships[i].setcoor(ships[i].x+direction*nearestflower);
                        
                        if(flowers[minindex]!=undefined)
                        {
                                flowers[minindex].grow();
                        }
                        flowers.splice(minindex,1);
                        score += 100
                    
                    
                if((ships[i].x <=0) || (ships[i].x >=width))
                {
                    ships[i].setcoor(width/2);
                    
                    

                    
                }

                if(this.gen[i] !=undefined)
                {
                    Neuvol.networkScore(this.gen[i], score);
                }
                

                if(flowers.length == 0)
                {
                    
                    
                    addTable();
                    
                    generation = generation + 1;
                    this.gen = Neuvol.nextGeneration();
                    ships = [];
                    isGameOver = [];

                    for(var i in this.gen){
                        //alert("yolo");
                        var b = new Ship();
                        ships.push(b)
                        isGameOver.push(false)
                        }
                    
                    score = 0;

                    ships[i].setcoor(width/2);
                    for (var i = 0; i < 6; i++) 
                    {
                    flowers[i] = new Flower(i*80+80, 60);
                    }
                    
                }
        }
    }

     
        
          function addTable() 
          {
      
            var myTableDiv = document.getElementById("mytable");
            var tr = document.createElement('TR');
            var td = document.createElement('TD');
            var td2 = document.createElement('TD');
            td.width='75';
            td.appendChild(document.createTextNode(generation));
            td2.appendChild(document.createTextNode(score));
            tr.appendChild(td);
            tr.appendChild(td2);
            myTableDiv.appendChild(tr);
    
}  
    
