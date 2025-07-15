import { Category, PrismaClient } from '@prisma/client'
import { Decimal } from '@prisma/client/runtime/library'

const prisma = new PrismaClient()

export async function createTransactionService(
  userId: number,
  name: string,
  description: string,
  category: string,
  amount: Decimal,
  date: Date,
) {
  try {
    const transaction = await prisma.transaction.create({
      data: {
        name,
        description,
        category: category as Category,
        amount,
        date,
        userId,
      },
    })
    await prisma.user.update({
      where: { id: userId },
      data: {
        money: {
          increment: amount,
        },
      },
    })
    return transaction
  } catch (error) {
    throw new Error(`Error creating income transaction: ${error}`)
  } finally {
    await prisma.$disconnect()
  }
}

export async function getDashboardTransactionsByUser(userId: number) {
  try {
    const transactions = await prisma.transaction.findMany({
      where: { userId },
      orderBy: { date: 'desc' },
      take: 5,
    })
    return transactions
  } catch (error) {
    throw new Error(`Error fetching dashboard transactions: ${error}`)
  } finally {
    await prisma.$disconnect()
  }
}

export async function getMonthlyTransactionsByUser(userId: number) {
  try {
    const transactions = await prisma.transaction.findMany({
      where: {
        userId,
        date: {
          gte: new Date(new Date().getFullYear(), new Date().getMonth(), 1),
          lt: new Date(new Date().getFullYear(), new Date().getMonth() + 1, 1),
        },
      },
      orderBy: { date: 'desc' },
    })
    return transactions
  } catch (error) {
    throw new Error(`Error fetching monthly transactions: ${error}`)
  } finally {
    await prisma.$disconnect()
  }
}

export async function searchTransactionsByUser(userId: number, searchTerm: string) {
  const isValidCategory = Object.values(Category).includes(searchTerm as Category)
  try {
    const transactions = await prisma.transaction.findMany({
      where: {
        userId: userId,
        OR: [
          { description: { contains: searchTerm.trim(), mode: 'insensitive' } },
          { name: { contains: searchTerm.trim(), mode: 'insensitive' } },
          ...(isValidCategory ? [{ category: searchTerm.trim() as Category }] : []),
        ],
      },
      orderBy: {
        date: 'desc',
      },
    })

    return transactions
  } catch (error) {
    throw new Error(`Error searching transactions: ${error}`)
  }
}

export async function getPaginatedTransactionsByUser(
  userId: number,
  page: number,
  pageSize: number,
) {
  try {
    const transactions = await prisma.transaction.findMany({
      where: { userId },
      orderBy: { date: 'desc' },
      skip: (page - 1) * pageSize,
      take: pageSize,
    })
    return transactions
  } catch (error) {
    throw new Error(`Error fetching paginated transactions: ${error}`)
  } finally {
    await prisma.$disconnect()
  }
}

export async function getMonthlyIncomeByUser(userId: number) {
  try {
    const transactions = await prisma.transaction.findMany({
      where: {
        userId,
        amount: {
          gt: new Decimal(0),
        },
        date: {
          gte: new Date(new Date().getFullYear(), new Date().getMonth(), 1),
          lt: new Date(new Date().getFullYear(), new Date().getMonth() + 1, 1),
        },
      },
    })
    const totalIncome = transactions.reduce(
      (sum, transaction) => sum.add(transaction.amount),
      new Decimal(0),
    )
    return totalIncome
  } catch (error) {
    throw new Error(`Error fetching monthly income: ${error}`)
  } finally {
    await prisma.$disconnect()
  }
}

export async function getMonthlySpendingByUser(userId: number) {
  try {
    const transactions = await prisma.transaction.findMany({
      where: {
        userId,
        amount: {
          lt: new Decimal(0),
        },
        date: {
          gte: new Date(new Date().getFullYear(), new Date().getMonth(), 1),
          lt: new Date(new Date().getFullYear(), new Date().getMonth() + 1, 1),
        },
      },
    })
    const totalSpending = transactions.reduce(
      (sum, transaction) => sum.add(transaction.amount),
      new Decimal(0),
    )
    return totalSpending
  } catch (error) {
    throw new Error(`Error fetching monthly spending: ${error}`)
  } finally {
    await prisma.$disconnect()
  }
}
