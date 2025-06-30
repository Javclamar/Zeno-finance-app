import { Category, PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export async function getAllTransactionsByUser(userId: number) {
  try {
    const transactions = prisma.transaction.findMany({
      where: {
        userId: userId,
      },
    })
    return transactions
  } catch (error) {
    throw new Error(`Error fetching transactions: ${error}`)
  }
}

export async function getMoneyByUser(userId: number) {
  try {
    const user = await prisma.user.findFirst({
      where: {
        id: userId,
      },
      select: {
        money: true,
      },
    })

    return user?.money.toNumber()
  } catch (error) {
    throw new Error(error instanceof Error ? error.message : String(error))
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
    })
    return transactions
  } catch (error) {
    throw new Error(`Error searching transactions: ${error}`)
  }
}
