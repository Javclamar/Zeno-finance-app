import cors from 'cors'
import dotenv from 'dotenv'
import express from 'express'
import authRoutes from './routes/authRoutes'
import budgetRoutes from './routes/budgetRoutes'
import transactionsRoutes from './routes/transactionRoutes'
import userRoutes from './routes/userRoutes'

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
app.use('/api/transactions', transactionsRoutes)
app.use('/api/budgets', budgetRoutes)

dotenv.config()

export default app
