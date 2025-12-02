import NoDataImg from "../../assets/no-data.png";
import {usePredictionStore} from "../../store/usePredictionStore.ts";
import "./ResultCard.css"

export const ResultCard = () => {
    const {loading, error, result} = usePredictionStore();
    const isAnalyzed = !!result && !loading && !error;

    const descriptions = ["Beginner", "Elementary", "Intermediate", "Upper Intermediate", "Advanced", "Native"];

    return (
        <div className={`result-container ${isAnalyzed ? "result-container-analyzed" : ""}`}>
            {result ? (
                <div className="result">
                    <p className={`result-label result-label-${result.level_id}`}>{result.level_label}</p>
                    <span>{descriptions[result.level_id - 1]}</span>
                </div>
            ) : (
                <div className="no-result">
                    <img src={NoDataImg} alt="No data image"/>
                    <p>Результат відстуній, вставте текст для аналізу!</p>
                </div>
            )
            }
        </div>
    )
}