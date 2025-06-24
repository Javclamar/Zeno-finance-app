import { Router } from "express";
import { getUserMoney, getUserTransactions } from '../controllers/userController';

const router = Router();

router.get('/transactions', getUserTransactions);
router.get('/money', getUserMoney)

export default router;