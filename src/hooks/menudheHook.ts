import { type Request, type Response } from 'express'
// import { rootPath } from '../config.js'
// import { promisify } from 'util'
// import { exec } from 'child_process'
import runGitCommand from './runGit.js'

// const execAsync = promisify(exec)

export default async (req: Request, res: Response): Promise<any> => {
  const payload = req.body

  // Handle GitHub webhook payload here
  console.log('Received GitHub webhook:', payload)

  //   const folderPath = `${rootPath}/test` // Change this path as needed

  try {
    //     // Get the folder name from the request body
    //     const { folderName } = req.body;

    //     if (!folderName) {
    //       return res.status(400).json({ error: 'Folder name is required' });
    //     }

    // Construct the shell command to create the folder
    // const shellCommand = `mkdir -p ${rootPath}/test`

    // Execute the shell command using the promisified exec function
    // const { stderr: e, stdout: s } = await execAsync(
    //   'cd .. && cd workspace && ls'
    // )

    // console.log(e)
    // console.log(s)

    // const { stdout, stderr } = await execAsync('git clone')

    // Process the command output
    // console.log(`Command output: ${stdout}`)
    // console.error(`Command errors: ${stderr}`)

    await runGitCommand()

    return res.status(200).json({ message: 'Folder created successfully' })
  } catch (err) {
    console.error('Unexpected error:', err)
    res.status(500).json({ error: 'Unexpected error' })
  }

  //   try {
  //     // Check if the folder exists
  //     await fsPromises.access(folderPath)

  //     // If the folder exists, send a message
  //     console.log('Folder already exists')
  //     return res.status(200).send(`Folder already exists ${folderPath}`)
  //   } catch (err) {
  //     // If the folder doesn't exist, create it
  //     try {
  //       await fsPromises.mkdir(folderPath, { recursive: true })
  //       console.log('Folder created successfully')
  //       return res.status(200).send(`Folder created successfully ${folderPath}`)
  //     } catch (error) {
  //       console.error('Error creating folder:', error)
  //       return res.status(500).json({
  //         message: `Error:  ${folderPath}`,
  //         error
  //       })
  //     }
  //   }

  //   return res.status(200).send('Webhook received successfully')
}
