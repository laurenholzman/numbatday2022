let img;
let img2;
var value = 0;
var dim = 1000;
var value2 = 0;
var rad = 30;
let current;

var places = [[350/600*dim,197/600*dim],[196/600*dim,262/600*dim]];
var descriptions = ['This dude is really having a good time.','It is in fact her 22nd birthday.'];

function preload() {
  img1 = loadImage('IMG_6112.PNG');
  img4 = loadImage('IMG_7607.jpg');
    img3 = loadImage('IMG_9696.jpg');

    img2 = loadImage('numbat.jpg');


  
  


}
function setup() {
  createCanvas(dim,dim);
  imageMode(CENTER);
}
 function keyPressed() {
  if (keyCode === LEFT_ARROW) {
    value=1;
  }else {
    value = 0;
  }
}
function keyReleased() {
  if (keyCode=== LEFT_ARROW) {
    value = 0;
  }
}
function mousePressed() {
  for (let i = 0; i < places.length; i++) {
    current = places[i];
   console.log(mouseX,mouseY)
    var p1 = mouseX<current[0]+rad;
    var p2 = mouseX > current[0]-rad;
    var p3 = mouseY<current[1]+rad ;
    var p4 = mouseY > current[1]-rad;
   // print(p1,p2,p3,p4,'\n')
    
    if ((mouseX<current[0]+rad && mouseX > current[0]-rad) && (mouseY<current[1]+rad && mouseY > current[1]-rad) ) {
      value2 = i+1;
      print(i+1)
    }
}
}
function mouseReleased() {
  value2 = 0;
}

var resize = 2;
function draw() {
  background(50)
  image(img2,dim/3,dim/2.5,119*3/600*dim,159*3/600*dim)
  
  textSize(12/600*dim);
  fill(119,20,50);
 text('(press the left arrow, I dare you. you will NOT be disappointed)',50/600*dim,550/600*dim,500/600*dim,200/600*dim)
   textSize(42/600*dim);

  text('Happy Birthday to the best numbat of them all!',2*dim/3,dim/10-10,dim/3)
  if (value) {
  image(img1, mouseX, mouseY,75*resize,135*resize);
  }
  if (value2 != 0) {
    textSize(18)
    fill(10,10,10)
    rect(2*dim/3-10,6*dim/10-5,dim/3,dim/6-5);
    fill(119,20,50);
    text(descriptions[value2-1],2*dim/3,6*dim/10,dim/3);
   
  }
  
  //text(str(mouseX)+', ' + str(mouseY),2*dim/3,7*dim/10)
  
   


}
