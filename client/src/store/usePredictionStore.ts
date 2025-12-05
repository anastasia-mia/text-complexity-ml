import { create } from "zustand";

export interface PredictionResult {
    level_id: number;
    level_label: string;
    probabilities?: Record<string, number>;
    metrics?: Record<string, number>;
}

interface AnalyzePayload {
    text: string;
    file: File | null;
}

interface PredictionState {
    result: PredictionResult | null;
    loading: boolean;
    error: string | null;

    analyze: (payload: AnalyzePayload) => Promise<void>;
    reset: () => void;
    clearError: () => void;
}

export const usePredictionStore = create<PredictionState>((set) => ({
    result: null,
    loading: false,
    error: null,

    reset: () => set({ result: null, error: null }),
    clearError: () => set({ error: null }),

    analyze: async ({ text, file }: AnalyzePayload) => {
        const trimmed = text.trim();

        if (!trimmed && !file) {
            set({ error: "Будь ласка, введіть текст або завантажте файл." });
            return;
        }

        const MIN_CHARS = 150;
        const MAX_CHARS = 8000;

        if (trimmed) {
            if (trimmed.length < MIN_CHARS) {
                set({
                    error: `Текст занадто короткий. Мінімум ${MIN_CHARS} символів.`,
                    result: null,
                });
                return;
            }
            if (trimmed.length > MAX_CHARS) {
                set({
                    error: `Текст занадто довгий. Максимум ${MAX_CHARS} символів.`,
                    result: null,
                });
                return;
            }
        }

        const formData = new FormData();
        if (trimmed) formData.append("text", trimmed);
        if (file) formData.append("file", file);

        try {
            set({ loading: true, error: null });

            const res = await fetch("http://localhost:8000/api/predict", {
                method: "POST",
                body: formData,
            });

            const data = await res.json();

            if (!res.ok) {
                const msg =
                    (data && (data.detail || data.message)) ||
                    "Сталася помилка на сервері. Спробуйте ще раз.";
                set({ error: msg, result: null });
                return;
            }

            set({ result: data as PredictionResult, error: null });
        } catch (e) {
            console.error(e);
            set({
                error: "Не вдалося зʼєднатись із сервером.",
                result: null,
            });
        } finally {
            set({ loading: false });
        }
    },
}));
