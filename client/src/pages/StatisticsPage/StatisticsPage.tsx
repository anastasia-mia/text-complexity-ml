import {Header} from "../../components/Header/Header.tsx";
import "./StatisticsPage.css"
import {useEffect, useState} from "react";

export const StatisticsPage = () => {
    const [logs, setLogs] = useState(null);

    useEffect(() => {
        fetch("http://localhost:8000/api/stats")
            .then(response => response.json())
            .then(data => setLogs(data))
            .catch(error => console.error(error))
    }, []);

    if (!logs) {
        return (
            <>
                <Header />
                <main className="stat">
                    <p>Завантаження статистики...</p>
                </main>
            </>
        );
    }

    return(
        <>
            <Header />
            <main className="stat">
                <p><b>Всього аналізів:</b> {logs.total_count}</p>
                <p><b>Середній розмір тексту:</b> {logs.avg_text_length.toFixed(2)} символів</p>
                <p><b>Розподіл усіх проаналізованих текстів по рівнях:</b></p>
                {logs && (
                    <div className="stat-cards">
                        {logs.levels.sort((a, b) => a.level_id - b.level_id).map(level => (
                            <div className="level-card">
                                <span className={`level-label result-label-${level.level_id}`}>
                                    {level.level_label}
                                </span>
                                <div className="level-details">
                                    <span>{level.count} разів</span>
                                    <span>{(level.share * 100).toFixed(1)} %</span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>

        </>
    )
}