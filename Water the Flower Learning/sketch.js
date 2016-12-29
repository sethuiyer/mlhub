var ships = []
var flowers = [];
var drops = [];
var score = 0;
var isGameOver = false;
var Neuvol;
var gen;
function setup() {
  createCanvas(600, 400);
    for (var i = 0; i < 6; i++) {
    flowers[i] = new Flower(i*80+80, 60);
  }
  Neuvol = new Neuroevolution({
            population:5,
            network:[2, [2], 1],
        });
    gen = Neuvol.nextGeneration();
for(var i in this.gen){
        var b = new Ship();
        ships.push(b)
    }
}

function draw() {
  background(51);
  fill(0, 102, 153);
    text("Score: "+score, width-70, 30);
  ship.show();
  ship.move();

  for (var i = 0; i < drops.length; i++) {
    drops[i].show();
    drops[i].move();
    for (var j = 0; j < flowers.length; j++) {
      if (drops[i].hits(flowers[j])) {

        score = score + 10;
        flowers[j].grow();
        drops[i].evaporate()
      }
    }
    
  }

  var edge = false;

  for (var i = 0; i < flowers.length; i++) {
    flowers[i].show();
    flowers[i].move();
    if (flowers[i].x > width || flowers[i].x < 0) {
      edge = true;
    }
  }

  if (edge) {
    for (var i = 0; i < flowers.length; i++) {
      flowers[i].shiftDown();
    }
  }

  for (var i = drops.length-1; i >= 0; i--) {
    drops[i].checkDead();
    if (drops[i].toDelete || drops[i].isDead) {
        if(drops[i].isDead)
        {
            isGameOver = true;
        }
      drops.splice(i, 1);

    }

  }

for (var i = flowers.length-1; i >= 0; i--) {
    if (flowers[i].toDelete) {
      flowers.splice(i, 1);
      score = score + 100;
    }
  }
  
  if (flowers.length == 0 || isGameOver)
  {
    background(51);
    fill(0, 102, 153);
    text("Score: "+score, width/2, height/2 - 20);
    fill(255,0,0)
    text("Game over",300,200);
  }
}

function keyReleased() {
  if (key != ' ') {
    ship.setDir(0);
  }
}


function keyPressed() {
  if (key === ' ') {
    var drop = new Drop(ship.x, height);
    drops.push(drop);
  }

  if (keyCode === RIGHT_ARROW) {
    ship.setDir(1);
  } else if (keyCode === LEFT_ARROW) {
    ship.setDir(-1);
  }
}