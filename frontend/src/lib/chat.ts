
export type Message = {
  role: "user" | "assistant";
  content: string;
};
export type Conversation = {
  id: number,
  title: string
}

const API_BASE_URL = import.meta.env.VITE_API_URL

// usused function
export async function send_messages(messages: Array<Message>) {

  const res = await fetch(API_BASE_URL + "/api/ai/chat/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ "messages": messages }),
  })

  const data = await res.json()
  return data.message




}

export async function get_conversation_list(token: string, pageUrl?: string | null) {
  const fetchUrl = pageUrl || (API_BASE_URL + "/api/ai/conversations/");
  const res = await fetch(fetchUrl, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
  const data = await res.json()
  console.log("data from get_conversation_list", data)
  return data

}

export async function create_conversation(token: string) {
  const res = await fetch(API_BASE_URL + "/api/ai/conversations/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ "title": "Latest Chat" })
  })
  const data = await res.json()
  console.log("data from create_conversation", data)
  return data

}



export async function get_conversation(token: string, conversation_id: string) {
  const res = await fetch(API_BASE_URL + "/api/ai/conversations/" + conversation_id, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
  const data = await res.json()
  console.log(data)
  return data

}

