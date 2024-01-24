const express = require("express");
const bodyParser = require("body-parser");

const app = express();
const port = 3000; // You can change this port as needed

// Middleware to parse JSON body
app.use(bodyParser.json());

// GitHub webhook endpoint
app.post("/webhook", (req, res) => {
  const payload = req.body;

  // Handle GitHub webhook payload here
  console.log("Received GitHub webhook:", payload);

  res.status(200).send("Webhook received successfully");
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
