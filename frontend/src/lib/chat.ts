
export type Message = {
  role: "user" | "assistant";
  content: string;
};
export type Conversation = {
  id: number,
  title: string
}
export type SavedReport = {
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

export async function get_saved_report_data(token: string, report_id: string, page_no: string) {
  const fetchUrl = API_BASE_URL + "/api/ai/saved-report/" + report_id + "/" + page_no;
  const res = await fetch(fetchUrl, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
  if (!res.ok) {
    throw new Error(`Failed to fetch saved report: ${res.status}`)
  }
  const data = await res.json()
  console.log("data from saved report", data)
  return data
}

export async function get_saved_reports_list(token: string, pageUrl?: string | null) {
  const fetchUrl = pageUrl || (API_BASE_URL + "/api/ai/saved-reports/");
  const res = await fetch(fetchUrl, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
  if (!res.ok) {
    throw new Error(`Failed to fetch saved reports: ${res.status}`)
  }
  const data = await res.json()
  console.log("data from get_saved_reports_list", data)
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

export async function save_report(token: string, report_id: string, title?: string) {
  const res = await fetch(API_BASE_URL + "/api/ai/report/save/" + report_id + "/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(title ? { title } : {}),
  })
  if (!res.ok) {
    throw new Error(`Failed to save report: ${res.status}`)
  }
  const data = await res.json()
  console.log(data)
  return data

}

export async function get_saved_report_details(token: string, report_id: string) {
  const res = await fetch(API_BASE_URL + "/api/ai/saved-reports/" + report_id + "/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
  if (!res.ok) {
    throw new Error(`Failed to fetch report details: ${res.status}`)
  }
  return await res.json()
}

export async function delete_saved_report(token: string, report_id: string) {
  const res = await fetch(API_BASE_URL + "/api/ai/saved-reports/" + report_id + "/", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
  if (!res.ok) {
    throw new Error(`Failed to delete report: ${res.status}`)
  }
}

export type ScheduleNotificationPayload = {
  to_email: string;
  report_id: number;
  subject: string;
  message: string;
  hr: number;
  min: number;
  day: number; // 1 = Monday ... 7 = Sunday
  task_name: string; // unique identifier for the scheduled task
};

export async function schedule_report_notification(token: string, payload: ScheduleNotificationPayload) {
  const res = await fetch(API_BASE_URL + "/api/ai/report/schedule/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    let detail = `Failed to schedule notification: ${res.status}`;
    try {
      const errData = await res.json();
      // DRF returns field errors as { field: [msg] } or { detail: msg }
      const firstError = errData?.detail ?? Object.values(errData)?.[0];
      if (firstError) detail = Array.isArray(firstError) ? firstError[0] : String(firstError);
    } catch {
      // response had no JSON body; keep the status-based message
    }
    throw new Error(detail)
  }
  return await res.json()
}

export async function update_saved_report_title(token: string, report_id: string, title: string) {
  const res = await fetch(API_BASE_URL + "/api/ai/saved-reports/" + report_id + "/", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ title }),
  })
  if (!res.ok) {
    throw new Error(`Failed to update report title: ${res.status}`)
  }
  return await res.json()
}
