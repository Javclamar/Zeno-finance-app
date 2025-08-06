import { PrismaClient} from "@prisma/client";

const prisma = new PrismaClient();

export async function searchStocksService(searchTerm: string) {
  try {
    const stocks = await prisma.stockData.findMany({
      where: {
        ticker: {
          contains: searchTerm,
          mode: 'insensitive',
        },
      },
      take: 10,
      distinct: ['ticker'],
    });
    const tickers = stocks.map(stock => stock.ticker);
    return tickers;
  } catch (error) {
    throw new Error(error instanceof Error ? error.message : String(error));
  }
}
