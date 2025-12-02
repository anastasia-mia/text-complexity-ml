import {useMemo} from "react";

interface TextStatsProps {
    text: string;
}

export const TextStats = ({text}: TextStatsProps) => {
    const stats = useMemo(() => {
        const trimmed = text.trim();
        const charCount = text.length;
        const wordCount = trimmed
            ? trimmed.split(/\s+/).filter(Boolean).length
            : 0;

        const sentenceMatches = trimmed.match(/[^.!?]+[.!?]+/g);
        const sentenceCount = sentenceMatches
            ? sentenceMatches.length
            : trimmed ? 1 : 0;

        return {charCount, wordCount, sentenceCount}
    }, [text])

    return (
        <div className="text-stats">
            <span><b>Символів:</b> {stats.charCount}</span>
            <span><b>Слів:</b> {stats.wordCount}</span>
            <span><b>Речень:</b> {stats.sentenceCount}</span>
        </div>)
};
