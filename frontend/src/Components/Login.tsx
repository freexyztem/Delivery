import { useState } from "react";
import type { FormEvent } from "react";
import { API_URL } from "../Services/api";

interface LoginProps {
    onLogin: (accessToken: string, refreshToken: string) => void;
}

export default function Login({ onLogin }: LoginProps) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    async function handleSubmit(e: FormEvent<HTMLFormElement>) {
        e.preventDefault();

        try {
            const response = await fetch(`${API_URL}/token/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username,
                    password,
                }),
            });

            if (!response.ok) {
                throw new Error("Credenciales incorrectas");
            }

            const data = await response.json();

            const { access, refresh } = data;

            onLogin(access, refresh);

        } catch (error) {
            console.error(error);
        }
    }

    return (
        <section>
            <h2>Iniciar Sesión</h2>

            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="username">
                        Nombre de usuario:
                    </label>
                    <br />

                    <input
                        type="text"
                        id="username"
                        name="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>

                <div>
                    <label htmlFor="password">
                        Contraseña:
                    </label>
                    <br />

                    <input
                        type="password"
                        id="password"
                        name="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                <div>
                    <button type="submit">
                        Iniciar Sesión
                    </button>
                </div>
            </form>
        </section>
    );
}