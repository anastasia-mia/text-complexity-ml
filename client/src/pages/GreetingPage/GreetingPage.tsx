import {useNavigate} from "react-router-dom";
import "../../index.css"
import "./GreetingPage.css"

export const GreetingPage = () => {
    const navigate = useNavigate();
    const levels = ["A1", "A2", "B1", "B2", "C1", "C2"];

    return (
        <main className="greeting-page">
                <div className="greeting-page-wrapper">
                    <div className="cefr-bg">
                        {Array.from({ length: 12 }).map((_, i) => (
                            <div className={`cefr-orb orb-${i + 1}`} key={i}>
                                {levels[i % levels.length]}
                            </div>
                        ))}
                    </div>
                    <h1>Вітаємо у системі прогнозування складності текстів!</h1>
                    <p>Цей інструмент допомагає визначити орієнтовний рівень англомовного тексту за міжнародною шкалою CEFR (A1–C2).
                       CEFR — це стандарт, який описує, наскільки складно людині з певним рівнем володіння англійською розуміти текст.
                    </p>
                    <p>Завантажте або вставте текст — і система автоматично проаналізує його за десятками мовних метрик.</p>
                    <p><b>Готові почати?</b></p>
                    <button onClick={() => navigate("/analysis")}>
                        Перейти до аналізу тексту
                    </button>
                </div>
        </main>
    )
}