import { Decimal } from '@prisma/client/runtime/library'
import { Request, Response } from 'express'
import {
  createTransactionService,
  getDashboardTransactionsByUser,
  getMonthlyTransactionsByUser,
  getPaginatedTransactionsByUser,
  searchTransactionsByUser,
  getMonthlyIncomeByUser,
  getMonthlySpendingByUser
} from '../services/transactionService'

export const newTransactionController = async (req: Request, res: Response) => {
  const { name, description, category } = req.body
  const userId = req.user?.id as unknown as number
  const amount = req.body.amount
  const date = req.body.date ? new Date(req.body.date) : new Date()
  const type = req.query.type as string

  if (type !== 'income' && type !== 'expense') {
    res.status(400).json({ message: 'Invalid transaction type' })
  }

  const parsedAmount = new Decimal(amount)
  const signedAmount = type === 'expense' ? parsedAmount.abs().neg() : parsedAmount.abs()

  if (!userId) {
    res.status(401).json({ error: 'Unauthorized: User not found' })
  }

  try {
    const transaction = await createTransactionService(
      userId,
      name,
      description,
      category,
      signedAmount,
      date,
    )
    res.status(200).json({ message: 'Transaction created successfully', transaction })
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}

export const getDashboardTransactionsController = async (req: Request, res: Response) => {
  const userId = req.user?.id as unknown as number

  if (!userId) {
    res.status(401).json({ error: 'Unauthorized: User not found' })
  }

  try {
    const transactions = await getDashboardTransactionsByUser(userId)
    res.status(200).json(transactions)
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}

export const getMonthlyTransactionsController = async (req: Request, res: Response) => {
  const userId = req.user?.id as unknown as number

  if (!userId) {
    res.status(401).json({ error: 'Unauthorized: User not found' })
  }

  try {
    const transactions = await getMonthlyTransactionsByUser(userId)
    res.status(200).json(transactions)
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}

export const searchTransactionsController = async (req: Request, res: Response) => {
  try {
    const userId = Number(req.query.id)
    const searchTerm = req.query.search as string
    const transactions = await searchTransactionsByUser(userId, searchTerm)
    res.status(200).json(transactions)
  } catch (error) {
    res.status(500).json({ message: error })
  }
}

export const getPaginatedUserTransactionsController = async (req: Request, res: Response) => {
  const userId = req.user?.id as unknown as number
  const page = Number(req.query.page) || 1
  const pageSize = Number(req.query.pageSize) || 10

  if (!userId) {
    res.status(401).json({ error: 'Unauthorized: User not found' })
  }

  try {
    const transactions = await getPaginatedTransactionsByUser(userId, page, pageSize)
    res.status(200).json(transactions)
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}

export const getMonthlyIncomeByUserController = async (req: Request, res: Response) => {
  const userId = req.user?.id as unknown as number

  if (!userId) {
    res.status(401).json({ error: 'Unauthorized: User not found' })
  }

  try {
    const monthlyIncome = await getMonthlyIncomeByUser(userId)
    res.status(200).json({ monthlyIncome })
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}

export const getMonthlySpendingByUserController = async (req: Request, res: Response) => {
  const userId = req.user?.id as unknown as number

  if (!userId) {
    res.status(401).json({ error: 'Unauthorized: User not found' })
  }

  try {
    const monthlySpending = await getMonthlySpendingByUser(userId)
    res.status(200).json({ monthlySpending })
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}
