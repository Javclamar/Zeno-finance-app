import { Decimal } from '@prisma/client/runtime/library'
import { Request, Response } from 'express'
import { createTransactionService } from '../services/transactionService'

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
