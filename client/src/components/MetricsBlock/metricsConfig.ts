export const Metric_Config = [
    {
        key: "sem_share_rare_zipf_lt_4",
        label: "Рідкісні слова",
        group: "lexical",
        format: (v: number) => `${(v * 100).toFixed(1)}%`,
    },
    {
        key: "syn_avg_sentence_length",
        label: "Середня довжина речення",
        group: "syntax",
        format: (v: number) => `${v.toFixed(1)} слів`,
    },
    {
        key: "syn_share_complex_sentences",
        label: "Складні речення",
        group: "syntax",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "morph_share_nouns",
        label: "Іменники",
        group: "pos",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "morph_share_verbs",
        label: "Дієслова",
        group: "pos",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "morph_share_adj",
        label: "Прикметники",
        group: "pos",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "morph_tense_past_share",
        label: "Минулий час",
        group: "tense",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "morph_tense_present_share",
        label: "Теперішній час",
        group: "tense",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "morph_share_perfect",
        label: "Перфектні форми",
        group: "tense",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "read_fkgl",
        label: "Flesch–Kincaid Grade Level",
        group: "readability",
        format: (v: number) => v.toFixed(1),
    },
    {
        key: "read_fog",
        label: "Gunning Fog Index",
        group: "readability",
        format: (v: number) => v.toFixed(1),
    },
    {
        key: "read_smog",
        label: "SMOG Index",
        group: "readability",
        format: (v: number) => v.toFixed(1),
    }
] as const;

export type MetricKey = (typeof Metric_Config)[number]["key"];