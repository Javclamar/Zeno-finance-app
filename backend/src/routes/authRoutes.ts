import { Router } from 'express';
import { loginController, registerController, googleCallbackController } from '../controllers/authController';

const router = Router();

router.post('/register', registerController);
router.post('/login', loginController);
router.get('/google/callback', (req, res, next) => {
  Promise.resolve(googleCallbackController(req, res)).catch(next);
});

export default router;
