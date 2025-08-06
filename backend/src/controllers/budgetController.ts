import { Category } from '@prisma/client'
import { Decimal } from '@prisma/client/runtime/library'
import { Request, Response } from 'express'
import {
  createBudgetService,
  deleteBudgetService,
  getActiveBudgetsByUserService,
  updateBudgetService,
} from '../services/budgetService'

export const getActiveBudgetsController = async (req: Request, res: Response) => {
  const userId = req.user?.id as unknown as number
  try {
    const activeBudgets = await getActiveBudgetsByUserService(userId)
    res.status(200).json(activeBudgets)
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}

export const createBudgetController = async (req: Request, res: Response) => {
  const { category, amount, startDate, endDate } = req.body
  const userId = req.user?.id as unknown as number
  try {
    const budget = await createBudgetService(
      userId,
      category as Category,
      amount as Decimal,
      new Date(startDate),
      new Date(endDate),
    )
    res.status(200).json({ message: 'Budget created successfully', budget })
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}

export const deleteBudgetController = async (req: Request, res: Response) => {
  const budgetId = req.query.id as unknown as number
  try {
    await deleteBudgetService(budgetId)
    res.status(200).json({ message: 'Budget deleted succesfully' })
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}

export const updateBudgetController = async (req: Request, res: Response) => {
  const { budgetId, category, amount, startDate, endDate } = req.body
  try {
    const budget = await updateBudgetService(
      budgetId as number,
      category as Category,
      amount as number,
      new Date(startDate),
      new Date(endDate),
    )
    res.status(200).json({ message: 'Budget created successfully', budget })
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}
