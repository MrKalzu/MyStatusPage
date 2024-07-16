import os
import sys
import atexit
import time
from signal import signal, SIGTERM

class Daemon:
    def __init__(self, pid_file, logger, *, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.pid_file = pid_file
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.logger = logger

    def daemonize(self):
        """Deamonize the process."""
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            self.logger.error(f"Fork #1 failed: {e.errno} ({e.strerror})")
            sys.exit(1)

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            self.logger.error(f"Fork #2 failed: {e.errno} ({e.strerror})")
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()

        with open(self.stdin, 'rb', 0) as f:
            os.dup2(f.fileno(), sys.stdin.fileno())
        with open(self.stdout, 'ab', 0) as f:
            os.dup2(f.fileno(), sys.stdout.fileno())
        with open(self.stderr, 'ab', 0) as f:
            os.dup2(f.fileno(), sys.stderr.fileno())

        self.write_pid_file()
        atexit.register(self.delete_pid_file)
        signal(SIGTERM, self.sigterm_handler)

    def start(self):
        """Start the daemon."""
        if self.is_running():
            self.logger.error("Daemon is already running.")
            sys.exit(1)
        self.logger.info("Starting daemon...")
        try:
            self.logger.info("Starting daemon...")
            self.daemonize()
            self.logger.info("Daemon started.")
            self.run()
        except Exception as e:
            self.logger.error(f"Failed to start daemon: {e}")


    def stop(self):
        """Stop the daemon."""
        if not self.is_running():
            self.logger.warning("Daemon is not running.")
            return

        self.logger.info("Stopping daemon...")
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, SIGTERM)
            self.logger.info(f"Daemon with PID {pid} has been terminated.")
        except ProcessLookupError:
            self.logger.warning(f"No process with PID {pid} found. It might have already stopped.")
        except Exception as e:
            self.logger.error(f"An error occurred while stopping the daemon: {e}")

    def restart(self):
        """Restart the daemon."""
        self.stop()
        time.sleep(1)
        self.start()

    def run(self):
        """Override this method when you subclass Daemon.
        It will be called after the process has been daemonized by start() or restart()."""
        raise NotImplementedError("You must implement the run() method.")

    def is_running(self):
        """Check if the daemon is running."""
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            return True
        except (FileNotFoundError, ProcessLookupError):
            return False

    def write_pid_file(self):
        """Write the PID file."""
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))

    def delete_pid_file(self):
        """Delete the PID file."""
        os.remove(self.pid_file)

    def sigterm_handler(self, signum, frame):
        """Handle SIGTERM signal."""
        self.logger.info("Received SIGTERM. Shutting down...")
        sys.exit(0)
