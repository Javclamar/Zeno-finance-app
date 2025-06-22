import { PrismaClient } from "@prisma/client";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";

const prisma = new PrismaClient();

export const registerUserService = async (name: string, email: string, password: string, repeatPassword: string) => {
    
    if (password !== repeatPassword) {
        throw new Error("Passwords do not match");
    }
   
    const existingUser = await prisma.user.findUnique({
        where: { email }
    });

    if (existingUser) {
        throw new Error("User already exists");
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const user = await prisma.user.create({
        data: {
            name,
            email,
            password : hashedPassword,
        },
    });

    return user;
}

export const loginUserService = async (email: string, password: string) => {

    const user = await prisma.user.findUnique({
        where: { email }
    });

    if (!user) {
        throw new Error("User not found");
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);

    if (!isPasswordValid) {
        throw new Error("Invalid password");
    }

    const token = jwt.sign({ id: user.id, email: user.email }, "clave-secreta", {expiresIn: '1h'});

    return token;
}
