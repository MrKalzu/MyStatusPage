#!/usr/bin/python3

import time
import sys
from config import Config
from database import Database
from listener import Api
from statuspage import Statuspage
from logger import setup_logger
from daemonize import Daemon

class StatusMonitor(Daemon):
    def __init__(self, pid_file, logger):
        super().__init__(pid_file, logger)
        self.config = Config('./config.ini')
        self.settings = self.config.get_config()
        self.db = Database(self.settings['database_file'], self.logger)
        self.api = Api(self.config, self.db, self.logger)
        self.statuspage = Statuspage(self.settings, self.db, self.logger)

    def run(self):
        self.logger.info('Starting statuspage update loop')
        self.db.init_db()
        self.api.start()
        try:
            while True:
                self.statuspage.update_status()
                time.sleep(int(self.settings['update_interval']))
        except KeyboardInterrupt:
            self.logger.info("Received keyboard interrupt, shutting down...")
        except Exception as e:
            self.logger.error(f"An error occurred in the main loop: {e}")
        finally:
            self.api.stop()
            self.db.end()
            self.logger.info("Service stopped")

if __name__ == "__main__":
    config = Config('./config.ini')
    settings = config.get_config()

    output = settings['stdout_logs'].lower() == 'true'
    log_level = settings['log_level']
    logger = setup_logger(settings.get('log_file', 'monitor.log'), log_level, output)

    daemon = StatusMonitor(settings['pid_file'], logger)
    if len(sys.argv) == 1:
        logger.info('Starting service in foreground. Use arguments start|stop|restart to manage daemonized service.')
        daemon.run()
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            daemon.start()
        elif sys.argv[1] == 'stop':
            daemon.stop()
        elif sys.argv[1] == 'restart':
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("Usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
