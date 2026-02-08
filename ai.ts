import Groq from "groq-sdk";
import * as jsonData from './articles.json';
import * as fs from 'node:fs';
import * as dotenv from 'dotenv';
dotenv.config();


const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

const SYSTEM_PROMPT = `You are a concise tech news summarizer. Your job is to:
1. Distill articles into clear, digestible summaries (2-3 sentences max)
2. Extract 3-5 key bullet points from each article
3. Highlight what matters: impact on users, industry trends, or notable figures
4. Skip fluff, marketing speak, and filler content
5. Use plain language - avoid jargon unless necessary

Format your response as JSON with this structure:
{
  "summary": "Brief 2-3 sentence summary",
  "keyPoints": ["point 1", "point 2", "point 3"]
}
  
If the user asks additional questions, you can provide additional information as long as it is relevant to the article.`;

interface Article {
    title: string;
    link: string;
    published: string;
    summary: string;
    text: string | null;
}

interface ArticleSummary {
    title: string;
    link: string;
    summary: string;
    keyPoints: string[];
}

// reading json file
const articles: Article[] = JSON.parse(
    fs.readFileSync('./articles.json', 'utf8')
);      


// summarizing single article
export async function summarizeArticle(article: Article): Promise<ArticleSummary> {
    const content = article.text || article.summary;

    const chat = await groq.chat.completions.create({
        messages: [
            {
                role: "system",
                content: SYSTEM_PROMPT
            },
            {
                role: "user",
                content: `Summarize the following article: ${content}`,
            }

        ],
        model: "llama-3.3-70b-versatile",
        temperature: 0.3,
        response_format: { type: "json_object" },
    })

    const result = JSON.parse(chat.choices[0].message.content || "{}");

    return {
        title: article.title,
        link: article.link,
        summary: result.summary,
        keyPoints: result.keyPoints || []
    }
}

async function main() {
    for (const article of articles) {
        const summary = await summarizeArticle(article);
        console.log(summary);
    }
}

main();