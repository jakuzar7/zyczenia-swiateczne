let y = [];
let x = [];
let fourierY;
let fourierX;
let kolor = 0;
let time = 0;
let path = [];

let time_ruch = true;

function setup() {
  createCanvas(1800, 720);
  frameRate(144)

  skip = 1
  //pierwsza seria kół
  for (let i = 0; i < drawing0.length; i += skip) {

    y.push(drawing0[i].y);
    x.push(drawing0[i].x);
  }


  fourierY = dft(y);
  fourierX = dft(x);

  fourierX.sort((a, b) => b.amp - a.amp)
  fourierY.sort((a, b) => b.amp - a.amp)
}

function epiCycles(x, y, rotation, fourier, CZAS) {

  for (let i = 0; i < fourier.length; i++) {
    let prevx = x;
    let prevy = y;

    let freq = fourier[i].freq;
    let radius = fourier[i].amp;
    let phase = fourier[i].phase;

    x += radius * cos(freq * CZAS + phase + rotation);
    y += radius * sin(freq * CZAS + phase + rotation);
    strokeWeight(1)
    stroke(255, 0, 0);
    noFill();
    ellipse(prevx, prevy, 2 * radius);

    stroke(0, 0, 255);
    line(prevx, prevy, x, y);

  }
  return createVector(x, y)
}

function draw() {
  background(175);

  fill(175)
  //rect(100,50,1600,800)

  //pierwsza seria kół
  if (time_ruch === true) {
    let vx = epiCycles(width / 2, 50, 0, fourierX, time)
    let vy = epiCycles(50, height / 2, HALF_PI, fourierY, time)
    let v = createVector(vx.x, vy.y);
    path.unshift(v);

    stroke(0, 255, 0)
    line(vx.x, vx.y, v.x, v.y)
    line(vy.x, vy.y, v.x, v.y)

  }

  stroke(kolor)
  fill(kolor)
  //beginShape();
  for (let i = 0; i < path.length; i++) {
    circle(path[i].x, path[i].y, 2);
    //vertex(path[i].x,path[i].y);
  }
  //endShape();

  const dt = TWO_PI / fourierY.length;
  time += dt;

  var drawings = [drawing0, drawing1, drawing2, drawing3,
    drawing4, drawing5, drawing6, drawing7,
    drawing8, drawing9, drawing10, drawing11]
  

  for (let j = 0; j < 12; j++) {
    if (time > (j + 1) * TWO_PI) {

      x.splice(0, x.length);
      y.splice(0, y.length);

      for (let i = 0; i < drawings[j + 1].length; i += skip) {

        y.push(drawings[j + 1][i].y);
        x.push(drawings[j + 1][i].x);
      }
      fourierY = dft(y);
      fourierX = dft(x);
    }
  }
}