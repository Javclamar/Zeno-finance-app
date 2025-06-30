import cors from 'cors'
import express from 'express'
import authRoutes from './routes/authRoutes'
import stockRoutes from './routes/stockRoutes'
import userRoutes from './routes/userRoutes'
import dotenv from 'dotenv'

const app = express()

app.use(
  cors({
    origin: 'http://localhost:5173',
    credentials: true,
  }),
)
app.use(express.json())

app.use('/api/auth', authRoutes)
app.use('/api/user', userRoutes)
app.use('/api/stocks', stockRoutes)

dotenv.config();

export default app
