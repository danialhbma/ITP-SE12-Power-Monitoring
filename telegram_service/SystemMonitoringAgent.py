import psutil
import time
from TelegramService import TelegramService
from datetime import datetime
import asyncio
from dotenv import load_dotenv
import sys
import os 

class SystemMonitoringAgent:
    """Class that monitors disk usage, cpu load, memory usage (Ram) and network traffic"""
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
    
    def get_cpu_load(self, interval = 1):
        return psutil.cpu_percent(interval)

    def get_memory_usage(self):
        return psutil.virtual_memory()
    
    def get_network_traffic(self):
        return psutil.net_io_counters()

    def monitor_system(self):
        self.cpu_load = self.get_cpu_load()
        self.memory_usage = self.get_memory_usage()
        self.network_traffic = self.get_network_traffic()
        self.disk_usage = self.get_disk_usage()
        return self.generate_system_report()

    def generate_system_report(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        n = 1
        system_report = f"System Health Report: {current_time}\n"
        if self.cpu_load > 5:
            system_report += f"({n}) System Detected High CPU load\n"
            system_report += f"\tCPU Load: {self.cpu_load}%\n"
            n+=1
        if self.memory_usage.percent > 5:
            system_report += f"({n}) System Detected High RAM usage\n"
            system_report += f"\tMemory Usage: {round(self.memory_usage.used / (1024 ** 3), 2)} GB / {round(self.memory_usage.total / (1024 ** 3), 2)} GB ({self.memory_usage.percent}%)\n"
            n+=1
        if self.network_traffic.bytes_sent > 5 or self.network_traffic.bytes_recv > 5:
            system_report += f"({n}) System Detected High Network Traffic usage\n"
            system_report += f"\tNetwork Traffic: Sent = {round(self.network_traffic.bytes_sent / (1024 ** 2), 2)} MB, Received = {round(self.network_traffic.bytes_recv / (1024 ** 2), 2)} MB\n"
            n+=1
    
        for partition, usage in self.disk_usage.items():
            if usage['percentage'] > 5:
                system_report += f"({n}) Low Disk Space Detected \n"
                system_report += f"\t{partition} - Used: {usage['used']} GB / Total: {usage['total']} GB ({usage['percentage']}%)\n"
                n+=1
        print(system_report)
        return system_report

async def main():
    load_dotenv()
    try:
        TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
        CHAT_ID = os.getenv("CHAT_ID")
        if not TELEGRAM_API_TOKEN:
            raise ValueError("TELEGRAM_API_TOKEN environment variable is missing")
        if not CHAT_ID:
            raise ValueError("CHAT_ID environment variable is missing")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    tele_client = TelegramService(TELEGRAM_API_TOKEN, CHAT_ID)
    system_monitor = SystemMonitoringAgent()
    message = system_monitor.monitor_system()
    await tele_client.send_telegram_message(message)

if __name__ == "__main__":
    asyncio.run(main())

