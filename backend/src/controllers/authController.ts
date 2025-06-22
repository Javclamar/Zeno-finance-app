import { Request, Response } from 'express';
import { loginUserService, registerUserService } from '../services/authService';

export const registerController = async (req: Request, res: Response) => {
    const { name, email, password, repeatPassword } = req.body;

    try {
        const user = await registerUserService(name, email, password, repeatPassword);
        res.status(201).json({ message: 'User registered successfully', user });
    } catch (error) {
        if (error instanceof Error) {
            res.status(400).json({ error: error.message });
        } else {
            res.status(400).json({ error: 'An unknown error occurred' });
        }
    }
};

export const loginController = async (req: Request, res: Response) => {
    const { email, password } = req.body;

    try {
        const token = await loginUserService(email, password);
        res.status(200).json({ message: 'Login successful', token });
    } catch (error) {
        if (error instanceof Error) {
            res.status(401).json({ error: error.message });
        } else {
            res.status(401).json({ error: 'An unknown error occurred' });
        }
    }
};