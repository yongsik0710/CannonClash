import os
import json


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


option_file = resource_path("options.json")
with open(option_file, 'r') as file:
    option_data = json.load(file)


option = option_data


class Resources:
    class Fonts:
        font = resource_path("Assets/Fonts/LINESeedKR-Bd.ttf")

    class Sounds:
        class Music:
            lobby = resource_path("Assets/Sounds/Background/lobby.wav")
            stage_1 = resource_path("Assets/Sounds/Background/stage_1.wav")
            stage_2 = resource_path("Assets/Sounds/Background/stage_2.wav")
            stage_3 = resource_path("Assets/Sounds/Background/stage_3.wav")
            stage_4 = resource_path("Assets/Sounds/Background/stage_4.wav")

        class Cannon:
            class Basic:
                shoot = resource_path("Assets/Sounds/Cannon/Basic/shoot.wav")
                damage = resource_path("Assets/Sounds/Cannon/Basic/damage.wav")
                barrel_move = resource_path("Assets/Sounds/Cannon/Basic/barrel_move.wav")
                move = resource_path("Assets/Sounds/Cannon/Basic/move.wav")
                burning = resource_path("Assets/Sounds/Cannon/Basic/burning.wav")

            class Ballista:
                shoot = resource_path("Assets/Sounds/Cannon/Ballista/shoot.wav")
                damage = resource_path("Assets/Sounds/Cannon/Ballista/damage.wav")
                barrel_move = resource_path("Assets/Sounds/Cannon/Ballista/barrel_move.wav")
                move = resource_path("Assets/Sounds/Cannon/Ballista/move.wav")
                burning = resource_path("Assets/Sounds/Cannon/Ballista/burning.wav")

            class FlameCannon:
                shoot = resource_path("Assets/Sounds/Cannon/FlameCannon/shoot.wav")
                damage = resource_path("Assets/Sounds/Cannon/FlameCannon/damage.wav")
                barrel_move = resource_path("Assets/Sounds/Cannon/FlameCannon/barrel_move.wav")
                move = resource_path("Assets/Sounds/Cannon/FlameCannon/move.wav")
                burning = resource_path("Assets/Sounds/Cannon/FlameCannon/burning.wav")

            class Catapult:
                shoot = resource_path("Assets/Sounds/Cannon/Catapult/shoot.wav")
                damage = resource_path("Assets/Sounds/Cannon/Catapult/damage.wav")
                barrel_move = resource_path("Assets/Sounds/Cannon/Catapult/barrel_move.wav")
                move = resource_path("Assets/Sounds/Cannon/Catapult/move.wav")
                burning = resource_path("Assets/Sounds/Cannon/Catapult/burning.wav")

            class Tank:
                shoot = resource_path("Assets/Sounds/Cannon/Tank/shoot.wav")
                damage = resource_path("Assets/Sounds/Cannon/Tank/damage.wav")
                barrel_move = resource_path("Assets/Sounds/Cannon/Tank/barrel_move.wav")
                move = resource_path("Assets/Sounds/Cannon/Tank/move.wav")
                burning = resource_path("Assets/Sounds/Cannon/Tank/burning.wav")

        class Shell:
            class Basic:
                explode = resource_path("Assets/Sounds/Shell/Basic/explode.wav")

            class Arrow:
                explode = resource_path("Assets/Sounds/Shell/Arrow/explode.wav")

            class Fireball:
                explode = resource_path("Assets/Sounds/Shell/Fireball/explode.wav")

            class Stone:
                explode = resource_path("Assets/Sounds/Shell/Stone/explode.wav")

            class Missile:
                explode = resource_path("Assets/Sounds/Shell/Missile/explode.wav")

        class Util:
            class Button:
                mouse_on = resource_path("Assets/Sounds/Util/mouse_on.wav")
                click = resource_path("Assets/Sounds/Util/click.wav")

    class Texture:
        class GameExplain:
            page_1 = resource_path("Assets/Images/GameExplain/page_1.png")
            page_2 = resource_path("Assets/Images/GameExplain/page_2.png")
            page_3 = resource_path("Assets/Images/GameExplain/page_3.png")
            page_4 = resource_path("Assets/Images/GameExplain/page_4.png")
            page_5 = resource_path("Assets/Images/GameExplain/page_5.png")

        class Effects:
            nothing_explosion = resource_path("Assets/Images/Effects/nothing_explosion.png")
            explosion_1 = resource_path("Assets/Images/Effects/explosion_1.png")
            explosion_2 = resource_path("Assets/Images/Effects/explosion_2.png")

            fire = resource_path("Assets/Images/Effects/fire.png")

        class Util:
            title = resource_path("Assets/Images/Utilities/title.png")
            current_player = resource_path("Assets/Images/Utilities/current_player.png")

        class Levels:
            class Level1:
                level_image = resource_path("Assets/Images/Levels/level_1.png")
                background_image = resource_path("Assets/Images/Backgrounds/level_1.png")

            class Level2:
                level_image = resource_path("Assets/Images/Levels/level_2.png")
                background_image = resource_path("Assets/Images/Backgrounds/level_2.png")

            class Level3:
                level_image = resource_path("Assets/Images/Levels/level_3.png")
                background_image = resource_path("Assets/Images/Backgrounds/level_3.png")

            class Level4:
                level_image = resource_path("Assets/Images/Levels/level_4.png")
                background_image = resource_path("Assets/Images/Backgrounds/level_4.png")

        class Cannons:
            class Barrel:
                basic_barrel = resource_path("Assets/Images/Cannons/Basic/barrel.png")
                ballista_barrel = resource_path("Assets/Images/Cannons/Ballista/barrel.png")
                flame_cannon_barrel = resource_path("Assets/Images/Cannons/FlameCannon/barrel.png")
                catapult_barrel = resource_path("Assets/Images/Cannons/Catapult/barrel.png")
                tank_barrel = resource_path("Assets/Images/Cannons/Tank/barrel.png")

            class Body:
                catapult_body = resource_path("Assets/Images/Cannons/Catapult/body.png")
                tank_body = resource_path("Assets/Images/Cannons/Tank/body.png")

            class Wheel:
                basic_wheel = resource_path("Assets/Images/Cannons/Basic/wheel.png")
                ballista_wheel = resource_path("Assets/Images/Cannons/Ballista/wheel.png")
                flame_cannon_wheel = resource_path("Assets/Images/Cannons/FlameCannon/wheel.png")
                catapult_wheel = resource_path("Assets/Images/Cannons/Catapult/wheel.png")
                tank_wheel = resource_path("Assets/Images/Cannons/Tank/wheel.png")

        class Shells:
            basic = resource_path("Assets/Images/Shells/basic.png")
            arrow = resource_path("Assets/Images/Shells/arrow.png")
            fireball = resource_path("Assets/Images/Shells/fireball.png")
            stone = resource_path("Assets/Images/Shells/stone.png")
            missile = resource_path("Assets/Images/Shells/missile.png")
