const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function postJSON<T>(url: string, body: unknown): Promise<T> {
    const res = await fetch(`${API_BASE_URL}${url}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });

    if (!res.ok) {
        const text = await res.text();
        throw new Error(`API error ${res.status}: ${text}`);
    }

    return res.json();
}
