from django.db import models


class Machine(models.Model):
    name = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=17, unique=True)
    location = models.CharField(max_length=100, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class AppUsageLog(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='app_logs')
    app_name = models.CharField(max_length=255)
    window_title = models.CharField(max_length=500)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    duration_seconds = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.machine.name} | {self.app_name} | {self.duration_seconds}s"


class BrowserVisitLog(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='browser_logs')
    browser = models.CharField(max_length=50)
    url = models.TextField()
    page_title = models.CharField(max_length=500, blank=True)
    visited_at = models.DateTimeField()
    visit_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.machine.name} | {self.browser} | {self.url[:60]}"


class PrintLog(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='print_logs')
    printer_name = models.CharField(max_length=255)
    document_name = models.CharField(max_length=500)
    pages = models.PositiveIntegerField()
    printed_at = models.DateTimeField()

    def __str__(self):
        return f"{self.machine.name} | {self.printer_name} | {self.pages} pages"