import { Category, PrismaClient } from '@prisma/client'
import { Decimal } from '@prisma/client/runtime/library'

const prisma = new PrismaClient()

export async function createBudgetService(
  userId: number,
  category: Category,
  amount: Decimal,
  startDate: Date,
  endDate: Date,
) {
  try {
    const budget = await prisma.budget.create({
      data: {
        userId,
        category: category,
        amount,
        startDate,
        endDate,
      },
    })
    return budget
  } catch (error) {
    throw new Error(`Error creating budget: ${error}`)
  }
}

export async function getBudgetsByUserService(userId: number) {
  try {
    const budgets = await prisma.budget.findMany({
      where: { userId },
      orderBy: { startDate: 'asc' },
    })
    return budgets
  } catch (error) {
    throw new Error(`Error fetching budgets: ${error}`)
  }
}

export async function getActiveBudgetsByUserService(userId: number) {
  try {
    const today = new Date()
    const activeBudgets = await prisma.budget.findMany({
      where: {
        userId,
        startDate: { lte: today },
        endDate: { gte: today },
      },
      orderBy: { startDate: 'asc' },
    })
    return activeBudgets
  } catch (error) {
    throw new Error(`Error fetching active budgets: ${error}`)
  }
}

export async function deleteBudgetService(budgetId: number) {
  try {
    await prisma.budget.delete({
      where: { id: Number(budgetId) },
    })
  } catch (error) {
    throw new Error(`Error deleting budget: ${error}`)
  }
}
