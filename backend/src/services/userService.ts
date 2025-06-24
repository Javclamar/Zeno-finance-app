import { PrismaClient } from '@prisma/client';


const prisma = new PrismaClient();

export async function getAllTransactionsByUser(userId: number) {
  try {
    const transactions = prisma.transaction.findMany({
      where: {
        userId: userId
      }
    });
    return transactions;
  } catch (error) {
    throw new Error('Error fetching transactions')
  }
}

export async function getMoneyByUser(userId: number) {
  try {
    const user = await prisma.user.findFirst({
      where: {
        id: userId
      },
      select: {
        money: true
      }
    });

    return user?.money.toNumber();
  } catch (error) {
    throw new Error(error instanceof Error ? error.message : String(error))
  }
}

