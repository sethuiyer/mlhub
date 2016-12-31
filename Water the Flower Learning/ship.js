function Ship() {
  this.x = width/2;
  this.xdir=1;

  this.show = function() {
    fill(255);
    rectMode(CENTER);
    rect(this.x, height-20, 20, 60);

    
  }

  this.setDir = function(dir) {
    this.xdir = dir;
  }
  this.getDir = function() {

   return this.xdir;
  }

  this.move = function(dir) {
    this.x += this.xdir*5;
  }

this.setcoor = function(dir)
{
  this.x = dir;
}
this.changeDir = function()
{
  this.xdir = -1 * this.xdir;
}
}