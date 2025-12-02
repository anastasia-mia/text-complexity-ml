import "./TextInputForm.css"
import {useState} from "react";
import {TextStats} from "./TextStats.tsx";
import {UploadControl} from "./UploadControl.tsx";
import {usePredictionStore} from "../../store/usePredictionStore.ts";

export const TextInputForm = () => {
    const [fileName, setFileName] = useState<string>("Завантажити текст");
    const [text, setText] = useState("");
    const [file, setFile] = useState<File | null>(null);

    const {analyze, loading, error, clearError, result, reset} = usePredictionStore();
    const isAnalyzed = !!result && !loading && !error;

    const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setText(e.target.value);
        setFileName("Завантажити текст");
        setFile(null)

        clearError();
    }

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0] || null;
        setFile(selectedFile);
        if (selectedFile) {
            setFileName(selectedFile.name);
            setFile(selectedFile);
            setText("");
        } else {
            setFileName("Завантажити текст");
            setFile(null);
        }

        clearError();
    }

    const handleSubmitText = async (e: React.FormEvent) => {
        e.preventDefault();

        await analyze({text, file});
    }

    const deleteFile = () => {
        setFile(null);
        setFileName("Завантажити текст");
    }

    const handleReset = () => {
        setText("");
        setFile(null);
        setFileName("Завантажити текст");
        clearError();
        reset();
    };

    return (
        <form className={`input-container ${isAnalyzed ? "input-container-analyzed" : ""}`}
              onSubmit={handleSubmitText}
        >
            <textarea
                value={text}
                onChange={handleTextChange}
                readOnly={isAnalyzed}
                placeholder={isAnalyzed && file ? `Проведено аналіз з файлом ${fileName}.txt` : "Введіть або завантажте текст для перевірки на рівень CEFR"}
            >
            </textarea>
            <div className="input-bottom">
                {!text ? (
                    <UploadControl
                        fileName={fileName}
                        file={file}
                        deleteFile={deleteFile}
                        handleFileChange={handleFileChange}
                    />
                ) : <TextStats text={text}/>}
                {isAnalyzed
                    ?
                    <span onClick={handleReset} className="reset-button"
                          role="button">
                        Скинути
                    </span>
                    :
                    <button type="submit" className="input-button">
                        {loading ? "Аналізую..." : "Аналізувати"}
                    </button>
                }
            </div>

            {error && <p className="form-error">{error}</p>}
        </form>
    )
}