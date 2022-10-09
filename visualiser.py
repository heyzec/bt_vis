from py_scm.director import Director
from bt_vis.game_scene import GameScene



WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

        
class Visualiser:
    def __init__(self):
        self.director = Director()
        self.driver = None
    
    def set_driver(self, driver):
        self.driver = driver
        driver.set_director(self.director)
        
    async def run(self):
        game_scene = GameScene()
        game_scene.set_driver(self.driver)
        self.director.set_scene(game_scene)
        await self.director.loop()
