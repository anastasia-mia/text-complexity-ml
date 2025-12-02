import {usePredictionStore} from "../../store/usePredictionStore.ts";
import {Metric_Config, type MetricKey} from "./metricsConfig.ts";
import "./MetricsBlock.css"

export const MetricsBlock = () => {
    const {result} = usePredictionStore();
    const metrics = result?.metrics;

    if (!metrics) {
        return null;
    }

    return (
        <div className="metrics-block">
            {Metric_Config.map((metric: MetricKey) => (
                <div key={metric.key} className="metric">
                    <p className="metric-label">{metric.label}</p>
                    <p className="metric-value">{metric.format(metrics[metric.key])}</p>
                </div>
            ))}
        </div>
    )
}