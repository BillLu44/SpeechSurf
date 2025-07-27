export const config = {
  api: {
    bodyParser: false
  }
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({error: 'Method Not Allowed'});
  }

  // Get the audio data from the request body
  const chunks = []
  for await (const chunk of req) {
    chunks.push(chunk);
  }
  const rawBody = Buffer.concat(chunks)

  const response = await fetch("https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.SpeechSurf}`,
      "Content-Type": "audio/flac",
      "x-wait-for-model": "true"
    },
    body: rawBody,
  });

  const transcriptionData = await response.json();
  res.status(200).json(transcriptionData);
}
