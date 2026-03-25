
export type Message = {
  role: "user" | "assistant";
  content: string;
};

const API_BASE_URL = import.meta.env.VITE_API_URL

export async function send_messages(messages: Array<Message>) {

  const res = await fetch(API_BASE_URL + "/ai/api/chat/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ "messages": messages }),
  })

  const data = await res.json()
  return data.message




}
