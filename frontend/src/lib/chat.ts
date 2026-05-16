
export type Message = {
  role: "user" | "assistant";
  content: string;
};
export type Conversation = {
  id: number,
  title: string
}

const API_BASE_URL = import.meta.env.VITE_API_URL


export async function get_conversation_list(token: string, pageUrl?: string | null) {
  const fetchUrl = pageUrl || (API_BASE_URL + "/api/ai/conversations/");
  const res = await fetch(fetchUrl, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
  if (!res.ok) {
    throw new Error(`Failed to fetch conversations: ${res.status}`)
  }
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
  })
  if (!res.ok) {
    throw new Error(`Failed to fetch conversations: ${res.status}`)
  }
  const data = await res.json()
  console.log("data from create_conversation", data)
  return data

}


export async function get_report_data(token: string, report_id: string, page_no: string) {
  const fetchUrl = API_BASE_URL + "/api/ai/report/" + report_id + "/" + page_no;
  const res = await fetch(fetchUrl, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
  if (!res.ok) {
    throw new Error(`Failed to fetch report: ${res.status}`)
  }
  const data = await res.json()
  console.log("data from report", data)
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
  if (!res.ok) {
    throw new Error(`Failed to fetch conversations: ${res.status}`)
  }
  const data = await res.json()
  console.log(data)
  return data

}

