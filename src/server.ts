// const config =
//   process.env.NODE_ENV !== 'production' ? await import('dotenv') : null

// if (config) config.config()
import ExpressConfig from './app.js'

export const PORT = 3000

const app = ExpressConfig()

app.listen(PORT, () => {
  console.log('Server Running on Port ' + PORT)
})
