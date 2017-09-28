let width = 28;
let height = 28;
let scale = 20;

function setup() {
  createCanvas(width * scale, height * scale);
  background(255);
}

function draw() {

}

function mouseDragged() {
  fill(0);
  rect(mouseX, mouseY, 2*scale, 2*scale);
}

function mouseReleased() {
  if(mouseX > 0 && mouseX < width * scale && mouseY > 0 && mouseY < height * scale){
    loadPixels();

    let ary = [];
    for (let i = 0; i < pixels.length; i += 4) {
      ary.push(255 - (pixels[i] + pixels[i+1] + pixels[i+2]) / 3)
    }

    let bry = [];
    for (let h = 0; h < height * scale; h += scale)
      for (let i = 0; i < width * scale; i += scale) {
        let sum = 0;
        for (let j = 0; j < scale; j++) {
          for (let k = 0; k < scale; k++) {
            sum += ary[h * scale * width + i + j + width * scale * k];
          }
        }
        bry.push(sum / (scale * scale));
      }

    document.getElementById("result").innerHTML = 'Loading...';
    fetch('http://hanneshertach.me/digitrecognize/api', {
      headers: {
        'Content-Type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify({
        data: bry
      })
    }).then(res => {
      return res.json();
    }).then(data => {
      document.getElementById("result").innerHTML = 'You drew a ' + data.data + '!';
    }).catch(err => {
      console.log(err);
    });
  }
}

document.getElementById("resetCanvas").addEventListener("click", function(){
  resetCanvas();
})

function resetCanvas() {
  document.getElementById("result").innerHTML = 'Draw a number!';
  fill(255);
  stroke(0);
  rect(0, 0, width * scale, height * scale);
}
