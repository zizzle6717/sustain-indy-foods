const path = require('path');
const express = require('express');
const app = express();

app.use(express.static(path.join(__dirname, './carebackend/django-static/')));

app.listen(8009, () => console.log('Client app listening on port 8009!'));