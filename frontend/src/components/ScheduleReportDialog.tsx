import { useState, useActionState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/context/AuthContext";
import { schedule_report_notification } from "@/lib/chat";
import { Mail, Loader2, CheckCircle2 } from "lucide-react";

type ScheduleReportDialogProps = {
  reportId: number;
  reportTitle: string;
};

type ActionState =
  | { status: "idle" }
  | { status: "error"; message: string }
  | { status: "success"; email: string };

export default function ScheduleReportDialog({ reportId, reportTitle }: ScheduleReportDialogProps) {
  const [open, setOpen] = useState(false);
  // Bumped on each open so the inner form (and its useActionState) remounts fresh.
  const [instanceKey, setInstanceKey] = useState(0);

  function handleOpenChange(next: boolean) {
    if (next) setInstanceKey((k) => k + 1);
    setOpen(next);
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm">
          <Mail className="h-4 w-4" />
          Schedule email
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Schedule email delivery</DialogTitle>
          <DialogDescription>
            Send this report as a CSV attachment automatically, every week on the chosen day and time.
          </DialogDescription>
        </DialogHeader>
        <ScheduleForm key={instanceKey} reportId={reportId} reportTitle={reportTitle} />
      </DialogContent>
    </Dialog>
  );
}

function ScheduleForm({ reportId, reportTitle }: ScheduleReportDialogProps) {
  const { token } = useAuth();

  const [state, formAction, isPending] = useActionState<ActionState, FormData>(
    async (_prev, formData) => {
      if (!token) return { status: "error", message: "You are not signed in." };

      const toEmail = String(formData.get("to_email") ?? "").trim();
      const time = String(formData.get("time") ?? "");
      const [hrStr, minStr] = time.split(":");
      const hr = parseInt(hrStr, 10);
      const min = parseInt(minStr, 10);
      if (Number.isNaN(hr) || Number.isNaN(min)) {
        return { status: "error", message: "Please choose a valid time." };
      }

      try {
        await schedule_report_notification(token, {
          to_email: toEmail,
          report_id: reportId,
          subject: String(formData.get("subject") ?? "").trim(),
          message: String(formData.get("message") ?? "").trim(),
          hr,
          min,
          day: parseInt(String(formData.get("day")), 10),
          // PeriodicTask.name must be unique; generate a collision-free value
          task_name: `report-${reportId}-${Date.now()}`,
        });
        return { status: "success", email: toEmail };
      } catch (err) {
        return { status: "error", message: err instanceof Error ? err.message : "Something went wrong." };
      }
    },
    { status: "idle" },
  );

  if (state.status === "success") {
    return (
      <div className="flex flex-col items-center gap-3 py-6 text-center">
        <CheckCircle2 className="h-10 w-10 text-green-600" />
        <p className="text-sm font-medium">Notification scheduled</p>
        <p className="text-sm text-muted-foreground">
          "{reportTitle}" will be emailed to {state.email}.
        </p>
      </div>
    );
  }

  return (
    <form action={formAction} className="flex flex-col gap-4">
      <div className="flex flex-col gap-2">
        <Label htmlFor="to-email">Recipient email</Label>
        <Input id="to-email" name="to_email" type="email" required placeholder="you@example.com" />
      </div>

      <div className="flex flex-col gap-2">
        <Label htmlFor="subject">Subject</Label>
        <Input
          id="subject"
          name="subject"
          required
          maxLength={255}
          defaultValue={`Report: ${reportTitle}`}
          placeholder="Report subject"
        />
      </div>

      <div className="flex flex-col gap-2">
        <Label htmlFor="message">Message</Label>
        <textarea
          id="message"
          name="message"
          required
          maxLength={1000}
          defaultValue={`Please find the latest "${reportTitle}" report attached.`}
          placeholder="Body of the email"
          rows={3}
          className="flex w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring resize-none"
        />
      </div>

      <div className="flex gap-4">
        <div className="flex flex-1 flex-col gap-2">
          <Label htmlFor="day">Day (weekly)</Label>
          <select
            id="day"
            name="day"
            defaultValue={1}
            className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
          >
            <option value={1}>Monday</option>
            <option value={2}>Tuesday</option>
            <option value={3}>Wednesday</option>
            <option value={4}>Thursday</option>
            <option value={5}>Friday</option>
            <option value={6}>Saturday</option>
            <option value={7}>Sunday</option>
          </select>
        </div>
        <div className="flex flex-col gap-2">
          <Label htmlFor="time">Time</Label>
          <Input id="time" name="time" type="time" required defaultValue="09:00" className="w-32" />
        </div>
      </div>

      {state.status === "error" && <p className="text-sm text-destructive">{state.message}</p>}

      <DialogFooter>
        <DialogClose asChild>
          <Button type="button" variant="outline" disabled={isPending}>
            Cancel
          </Button>
        </DialogClose>
        <Button type="submit" disabled={isPending}>
          {isPending && <Loader2 className="h-4 w-4 animate-spin" />}
          {isPending ? "Scheduling..." : "Schedule"}
        </Button>
      </DialogFooter>
    </form>
  );
}
