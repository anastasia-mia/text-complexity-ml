interface UploadControlProps {
    fileName: string;
    file: File | null;
    deleteFile: () => void;
    handleFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export const UploadControl = ({fileName, file, deleteFile, handleFileChange}: UploadControlProps) => {

    return(
        <div className="input-file" role="button">
            <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true"
                 xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M4 15v2a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3v-2m-8 1V4m0 12-4-4m4 4 4-4"/>
            </svg>
            <p>{fileName}</p>

            <input type="file" accept=".txt" onChange={handleFileChange}/>

            {file && (
                <svg className="cross-icon" aria-hidden="true"
                     xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
                     viewBox="0 0 24 24"
                     onClick={deleteFile}
                >
                    <path stroke="darkred" stroke-linecap="round" stroke-linejoin="round"
                          stroke-width="2" d="M6 18 17.94 6M18 18 6.06 6"/>
                </svg>


            )}
        </div>
    )
}