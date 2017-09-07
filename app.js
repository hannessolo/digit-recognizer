const express = require('express');
const app = express();
const spawn = require('child_process').spawn;
const bodyParser = require('body-parser');

app.use(express.static('public'));
app.use(bodyParser.json());

app.post('/api', (req, res) => {

  pythonChild = spawn('python', ['script.py', req.body.data.toString()]);
  console.log('Child started');

  pythonChild.stdout.on('data', (data) => {
    res.json({
      data: data.toString('utf8')
    });
  });

  pythonChild.stderr.on('data', (data) => {
    console.log(`Err in child: ${data}`);
  });

  pythonChild.on('exit', (code, signal) => {
    console.log('child exited with ' + `code ${code} and signal ${signal}`);
  });

  res.set({
    'Content-Type': 'application/json'
  });
});

app.get('/', (req, res) => {
  res.redirect('/sketch.html');
});

var server = app.listen(3000, () => {
  console.log('Server on port 3000');
});
