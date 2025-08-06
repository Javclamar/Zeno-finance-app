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
    const categoryBudget = await prisma.budget.findFirst({
      where: {
        userId: userId,
        category: category,
      },
    })
    if (!categoryBudget) {
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
    } else {
      throw new Error(`There is another budget with the same category`)
    }
  } catch (error) {
    throw new Error(error instanceof Error ? error.message : String(error))
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
    throw new Error(error instanceof Error ? error.message : String(error))
  }
}

export async function getActiveBudgetsByUserService(userId: number) {
  try {
    const today = new Date()
    const activeBudgets = await prisma.budget.findMany({
      where: {
        userId,
        endDate: { gte: today },
      },
      orderBy: { startDate: 'asc' },
    })
    return activeBudgets
  } catch (error) {
    throw new Error(error instanceof Error ? error.message : String(error))
  }
}

export async function deleteBudgetService(budgetId: number) {
  try {
    await prisma.budget.delete({
      where: { id: Number(budgetId) },
    })
  } catch (error) {
    throw new Error(error instanceof Error ? error.message : String(error))
  }
}

export async function updateBudgetService(
  budgetId: number,
  category: Category,
  amount: number,
  startDate: Date,
  endDate: Date,
) {
  try {
    const budget = await prisma.budget.update({
      where: { id: budgetId },
      data: {
        category: category,
        amount: amount,
        startDate: startDate,
        endDate: endDate,
      },
    })
    return budget
  } catch (error) {
   throw new Error(error instanceof Error ? error.message : String(error))
  }
}
