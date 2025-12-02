import {TextInputForm} from "../../components/TextInputForm/TextInputForm.tsx";
import {ResultCard} from "../../components/ResultCard/ResultCard.tsx";
import "./AnalysisPage.css";
import {MetricsBlock} from "../../components/MetricsBlock/MetricsBlock.tsx";
import {usePredictionStore} from "../../store/usePredictionStore.ts";
import {Header} from "../../components/Header/Header.tsx";

export const AnalysisPage = () => {
    const {result} = usePredictionStore();

    return (
        <>
            <Header />
            <main>
                <div className="analysis-page">
                    <div className="analysis-input">
                        <TextInputForm />
                    </div>
                    <div className="analysis-result">
                        <ResultCard />
                    </div>
                </div>
                {result && <MetricsBlock />}
            </main>
        </>

    )
}