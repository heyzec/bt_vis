import asyncio
import traceback
from bt_vis.driver import Driver
from bt_vis.visualiser import Visualiser

def main():
    visualiser = Visualiser()
    driver = Driver()
    visualiser.set_driver(driver)

    try:
        loop = asyncio.new_event_loop()
        loop.create_task(driver.run())
        loop.run_until_complete(visualiser.run())
    except Exception:
        traceback.print_exc()
    finally:
        pass
        # Kill child processes
        # child_proc.terminate()
