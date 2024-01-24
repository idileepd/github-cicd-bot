import { type Request, type Response } from 'express'

export default (_: Request, res: Response): any => {
  return res
    .status(200)
    .send(
      'Hello My Friend !! I am github-cicd-bot \n\n--- Created by Dileep Nagendra'
    )
}
