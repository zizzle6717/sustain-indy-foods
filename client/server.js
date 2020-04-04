const path = require('path');
const express = require('express');
const app = express();

app.use(express.static(path.join(__dirname, './build/')));

app.listen(8000, () => console.log('Client app listening on port 8000!'));