import { exec } from 'child_process'
import { promisify } from 'util'
import { promises as fs } from 'fs'
import { rootPath } from '../config.js'

const execAsync = promisify(exec)

// const hostPath = '/path/on/host' // Replace with the path on your host machine

// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
const runGitCommand = async () => {
  try {
    // Check if the host path exists
    console.log(rootPath)
    await fs.access(rootPath)

    const { stdout: a, stderr: b } = await execAsync('pwd && ls', {
      cwd: rootPath
    })
    console.log(a, b)

    // Run a Git command using the host's Git executable
    const { stdout, stderr } = await execAsync('git status', { cwd: rootPath })

    console.log('Git Status Output:', stdout)
    console.log('Git Status err: ', stderr)
  } catch (err) {
    console.log(err)
    console.error('Host path does not exist or is inaccessible.')
  }
}

export default runGitCommand
