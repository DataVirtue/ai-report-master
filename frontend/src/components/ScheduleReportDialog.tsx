import { useState } from "react";
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

export default function ScheduleReportDialog({ reportId, reportTitle }: ScheduleReportDialogProps) {
  const { token } = useAuth();

  const [open, setOpen] = useState(false);
  const [toEmail, setToEmail] = useState("");
  const [subject, setSubject] = useState("");
  const [message, setMessage] = useState("");
  const [day, setDay] = useState(1); // 1 = Monday ... 7 = Sunday
  const [time, setTime] = useState("09:00");

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  function resetForm() {
    setToEmail("");
    setSubject(`Report: ${reportTitle}`);
    setMessage(`Please find the latest "${reportTitle}" report attached.`);
    setDay(1);
    setTime("09:00");
    setError(null);
    setSuccess(false);
  }

  function handleOpenChange(next: boolean) {
    if (next) resetForm();
    setOpen(next);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!token) return;

    const [hrStr, minStr] = time.split(":");
    const hr = parseInt(hrStr, 10);
    const min = parseInt(minStr, 10);

    if (Number.isNaN(hr) || Number.isNaN(min)) {
      setError("Please choose a valid time.");
      return;
    }

    setIsSubmitting(true);
    setError(null);
    try {
      await schedule_report_notification(token, {
        to_email: toEmail.trim(),
        report_id: reportId,
        subject: subject.trim(),
        message: message.trim(),
        hr,
        min,
        day,
        // PeriodicTask.name must be unique; generate a collision-free value
        task_name: `report-${reportId}-${Date.now()}`,
      });
      setSuccess(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsSubmitting(false);
    }
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

        {success ? (
          <div className="flex flex-col items-center gap-3 py-6 text-center">
            <CheckCircle2 className="h-10 w-10 text-green-600" />
            <p className="text-sm font-medium">Notification scheduled</p>
            <p className="text-sm text-muted-foreground">
              "{reportTitle}" will be emailed to {toEmail}.
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div className="flex flex-col gap-2">
              <Label htmlFor="to-email">Recipient email</Label>
              <Input
                id="to-email"
                type="email"
                required
                value={toEmail}
                onChange={(e) => setToEmail(e.target.value)}
                placeholder="you@example.com"
              />
            </div>

            <div className="flex flex-col gap-2">
              <Label htmlFor="subject">Subject</Label>
              <Input
                id="subject"
                required
                maxLength={255}
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="Report subject"
              />
            </div>

            <div className="flex flex-col gap-2">
              <Label htmlFor="message">Message</Label>
              <textarea
                id="message"
                required
                maxLength={1000}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
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
                  value={day}
                  onChange={(e) => setDay(parseInt(e.target.value, 10))}
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
                <Input
                  id="time"
                  type="time"
                  required
                  value={time}
                  onChange={(e) => setTime(e.target.value)}
                  className="w-32"
                />
              </div>
            </div>

            {error && <p className="text-sm text-destructive">{error}</p>}

            <DialogFooter>
              <DialogClose asChild>
                <Button type="button" variant="outline" disabled={isSubmitting}>
                  Cancel
                </Button>
              </DialogClose>
              <Button type="submit" disabled={isSubmitting}>
                {isSubmitting && <Loader2 className="h-4 w-4 animate-spin" />}
                {isSubmitting ? "Scheduling..." : "Schedule"}
              </Button>
            </DialogFooter>
          </form>
        )}
      </DialogContent>
    </Dialog>
  );
}
