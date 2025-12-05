import {usePredictionStore} from "../../store/usePredictionStore.ts";
import {Metric_Config} from "./metricsConfig.ts";
import "./MetricsBlock.css"

export const MetricsBlock = () => {
    const {result} = usePredictionStore();
    const metrics = result?.metrics;

    if (!metrics) {
        return null;
    }

    return (
        <div className="metrics-block">
            {Metric_Config.map((metric) => (
                <div key={metric.key} className="metric">
                    <p className="metric-label">
                        {metric.label}
                        <svg className="metric-svg-i" aria-hidden="true"
                             xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                            <path stroke="gray" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                  d="M10 11h2v5m-2 0h4m-2.592-8.5h.01M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
                        </svg>

                        <span className="metric-tooltip-text">{metric.description}</span>

                    </p>
                    <p className="metric-value">{metric.format(metrics[metric.key])}</p>
                </div>
            ))}
        </div>
    )
}