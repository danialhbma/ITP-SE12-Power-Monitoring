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
        system_report = "******************************************************\n"
        system_report += f"System Health Report: {current_time}\n"
        if self.cpu_load > 80:
            # CPU load deemed to be high if > 80%
            system_report += f"({n}) System Detected High CPU load\n"
            system_report += f"\tCPU Load: {self.cpu_load}%\n"
            n+=1
        if self.memory_usage.percent > 80:
            # RAM load deemed to be high > 80%
            system_report += f"({n}) System Detected High RAM usage\n"
            system_report += f"\tMemory Usage: {round(self.memory_usage.used / (1024 ** 3), 2)} GB / {round(self.memory_usage.total / (1024 ** 3), 2)} GB ({self.memory_usage.percent}%)\n"
            n+=1

        if self.network_traffic.bytes_sent / (1024 ** 2) > 16000 or self.network_traffic.bytes_recv / (1024 ** 2) > 16000:
            # Network traffic deemed to be high if 1.6GB i.e., 80% of what E2-medium machines support (2gb)
            system_report += f"({n}) System Detected High Network Traffic usage\n"
            system_report += f"\tNetwork Traffic: Sent = {round(self.network_traffic.bytes_sent / (1024 ** 2), 2)} MB, Received = {round(self.network_traffic.bytes_recv / (1024 ** 2), 2)} MB\n"
            n+=1

        for partition, usage in self.disk_usage.items():
            if usage['percentage'] > 80:
	    # Disk space low if disk usage > 80%
                system_report += f"({n}) Low Disk Space Detected \n"
                system_report += f"\t{partition} - Used: {usage['used']} GB / Total: {usage['total']} GB ({usage['percentage']}%)\n"
                n+=1
        if (n == 1):
            system_report += f"System OK. No abnormal status detected.\n"
        system_report += "******************************************************\n"
        print(system_report)
        return system_report

async def main():
    tele_client = TelegramService()
    tele_client.retrieve_token_from_environment()
    system_monitor = SystemMonitoringAgent()
    message = system_monitor.monitor_system()
    await tele_client.send_telegram_message(message)

if __name__ == "__main__":
    asyncio.run(main())

