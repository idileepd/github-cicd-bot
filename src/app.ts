// import express from "express";
// import bodyParser from "body-parser";

// const app = express();
// const port = 3000;

// // Middleware to parse JSON body
// app.use(bodyParser.json());

// // GitHub webhook endpoint
// app.post("/webhook", (req, res) => {
//   const payload = req.body;

//   // Handle GitHub webhook payload here
//   console.log("Received GitHub webhook:", payload);

//   res.status(200).send("Webhook received successfully");
// });

// // Start the server
// app.listen(port, () => {
//   console.log(`Server is running on http://localhost:${port}`);
// });

import compression from 'compression'
import cookieParser from 'cookie-parser'

import express, { type Application } from 'express'
import helmet from 'helmet'
import morgan from 'morgan'
import runMenudheHook from './hooks/menudheHook.js'
import hello from './hooks/hello.js'

const ExpressConfig = (): Application => {
  const app = express()
  app.use(compression())
  app.use(express.urlencoded({ extended: true }))
  app.use(express.json())

  app.use(helmet())
  app.use(cookieParser())
  app.use(morgan('dev'))

  app.get('/', hello)
  app.get('/menudhe', runMenudheHook)

  return app
}

export default ExpressConfig
