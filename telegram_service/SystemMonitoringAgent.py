import psutil
import time
from TelegramService import TelegramService
from datetime import datetime

class SystemMonitoringAgent:
    def get_disk_usage(self):
        partitions = psutil.disk_partitions(all=True)
        disk_usage = {}

        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                total = round(usage.total / (1024 ** 3), 2)  # Convert to GB
                used = round(usage.used / (1024 ** 3), 2)
                percentage = usage.percent

                disk_usage[partition.device] = {
                    'total': total,
                    'used': used,
                    'percentage': percentage
                }
            except PermissionError:
                # Skip partitions that cannot be accessed due to permission issues
                continue

        return disk_usage

    def monitor_system(self):
        cpu_load = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory()
        network_traffic = psutil.net_io_counters()
        disk_usage = self.get_disk_usage()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        system_report = f"***************************************\n"
        system_report += f"System Health Report {current_time}\n"
        system_report += f"CPU Load: {cpu_load}%\n"
        system_report += f"Memory Usage: {round(memory_usage.used / (1024 ** 3), 2)} GB / {round(memory_usage.total / (1024 ** 3), 2)} GB ({memory_usage.percent}%)\n"
        system_report += f"Network Traffic: Sent = {round(network_traffic.bytes_sent / (1024 ** 2), 2)} MB, Received = {round(network_traffic.bytes_recv / (1024 ** 2), 2)} MB\n"
        system_report += "Disk Usage:\n"
        for partition, usage in disk_usage.items():
            system_report += f"{partition} - Used: {usage['used']} GB / Total: {usage['total']} GB ({usage['percentage']}%)\n"
        system_report += f"***************************************"
        print(system_report)

if __name__ == "__main__":
    system_monitor = SystemMonitoringAgent()
    system_monitor.monitor_system()
