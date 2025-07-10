import { Category, PrismaClient } from '@prisma/client'
import { Decimal } from '@prisma/client/runtime/library'

export async function createTransactionService(
  userId: number,
  name: string,
  description: string,
  category: string,
  amount: Decimal,
  date: Date,
) {
  const prisma = new PrismaClient()
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
