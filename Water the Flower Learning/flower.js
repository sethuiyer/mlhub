
function Flower(x, y) {
  this.x = x;
  this.y = y;
  this.r = 30;

  this.xdir = 1;
  this.toDelete = false;
  
  this.grow = function() {
    this.r = this.r + 2;
    this.toDelete = true;
  }

  this.show = function() {
    noStroke();
    fill(255, 0, 200, 150);
    ellipse(this.x, this.y, this.r*2, this.r*2);
  }

}