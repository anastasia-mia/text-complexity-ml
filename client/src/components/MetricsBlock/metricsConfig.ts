export const Metric_Config = [
    {
        key: "sem_share_rare_zipf_lt_4",
        label: "Рідкісні слова",
        group: "lexical",
        description: "Частка слів, які дуже рідко зустрічаються в англійській мові. \nБільший показник = текст складніший.",
        format: (v: number) => `${(v * 100).toFixed(1)}%`,
    },
    {
        key: "syn_avg_sentence_length",
        label: "Середня довжина речення",
        group: "syntax",
        description: "Скільки слів у середньому міститься в одному реченні. \nДовші речення = вища складність тексту.",
        format: (v: number) => `${v.toFixed(1)} слів`,
    },
    {
        key: "syn_share_complex_sentences",
        label: "Складні речення",
        group: "syntax",
        description: "Частка речень, що містять кілька підрядних або складну структуру.\nБільше складних речень = вищий рівень CEFR. ",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "morph_share_nouns",
        label: "Іменники",
        group: "pos",
        description: "Відсоток іменників у тексті.\nБагато іменників характерно для описових або академічних текстів. ",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "morph_share_verbs",
        label: "Дієслова",
        group: "pos",
        description: "Відсоток дієслів у тексті.\n Високий показник означає активний стиль і дії в тексті.",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "morph_share_adj",
        label: "Прикметники",
        group: "pos",
        description: "Частка прикметників.\nВелика кількість прикметників робить текст більш деталізованим та описовим. ",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "morph_tense_past_share",
        label: "Минулий час",
        group: "tense",
        description: "Частка дієслів у минулому часі.\nХарактерно для наративів та історій. ",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "morph_tense_present_share",
        label: "Теперішній час",
        group: "tense",
        description: "Частка дієслів у теперішньому часі.\nТипово для загальних описів, інструкцій, фактів. ",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "morph_share_perfect",
        label: "Перфектні форми",
        group: "tense",
        description: "Частка конструкцій типу have done, has been.\nЇхня поява частіше свідчить про вищий рівень грамотності. ",
        format: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
    {
        key: "read_fkgl",
        label: "Flesch–Kincaid Grade Level",
        group: "readability",
        description: "Класична метрика читабельності: оцінює, який \"шкільний рівень\" потрібен, щоб зрозуміти текст.\nВищий бал = складніший текст. ",
        format: (v: number) => v.toFixed(1),
    },
    {
        key: "read_fog",
        label: "Gunning Fog Index",
        group: "readability",
        description: "Оцінка складності, що враховує довгі речення та складні слова.\nПоказник понад 12 часто вказує на професійний або академічний стиль. ",
        format: (v: number) => v.toFixed(1),
    },
    {
        key: "read_smog",
        label: "SMOG Index",
        group: "readability",
        description: "Метрика оцінки зрілості читача на основі кількості складних слів.\nДобре працює для коротких текстів. ",
        format: (v: number) => v.toFixed(1),
    }
] as const;

export type MetricKey = (typeof Metric_Config)[number]["key"];