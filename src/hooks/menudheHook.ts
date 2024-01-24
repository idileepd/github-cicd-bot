import { type Request, type Response } from 'express'

export default (req: Request, res: Response): any => {
  const payload = req.body

  // Handle GitHub webhook payload here
  console.log('Received GitHub webhook:', payload)

  return res.status(200).send('Webhook received successfully')
}
