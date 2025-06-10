
from pi_home_security.device_monitoring_service import DeviceMonitoringService
from pi_home_security.system_state_controller import SystemStateController


class HomeServices:
    def __init__(self):
        self.dms: DeviceMonitoringService
        self.ssc: SystemStateController


    def load(self):
        self.ssc= SystemStateController()
        # always load this last since it hold onto a thread unless we want to spin up another thread
        self.dms = DeviceMonitoringService()


def main():
    hs: HomeServices = HomeServices()
    hs.load()


if __name__ == "__main__":
    main()