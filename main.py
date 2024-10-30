from InquirerPy import inquirer
from os import system
import sys
import time
import keyboard

MINIMAL_DELAY = .0001  # 0.1ms


def print_animated(text: str, delay_seconds: float):
    exiting_loop: bool = False

    def exit_loop() -> None:
        nonlocal exiting_loop
        exiting_loop = True

    keyboard.add_hotkey('space', exit_loop, suppress=True)
    keyboard.add_hotkey('enter', exit_loop, suppress=True)
    keyboard.add_hotkey('backspace', exit_loop, suppress=True)

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay_seconds if not exiting_loop else MINIMAL_DELAY)
    sys.stdout.flush()

    keyboard.remove_all_hotkeys()


class Entity:
    def __init__(self, name: str, desc: str, hp: int, atk: int, intl: int, g: int) -> None:
        self.name = name
        self.desc = desc
        self.hp = hp
        self.atk = atk
        self.intl = intl
        self.g = g

    def lvlup(self) -> None:
        pass

    # this violates several principles
    def fight(self, enemy) -> None:
        system("clear")
        print_animated("Fight start!\n", .08)
        while (self.hp > 0 and enemy.hp > 0):
            time.sleep(.1)
            print_animated(f"You attack, {self.atk} damage dealt...\n", .05)
            enemy.hp -= self.atk
            time.sleep(.1)
            print_animated(f"Enemy attacks, \
                           {enemy.atk} damage dealt...\n", .05)
            self.hp -= enemy.atk
        if self.hp > 0:
            print_animated(f"You won, {self.hp} hp left\n", .05)
            self.lvlup()
            return
        print_animated("You loose :(", .1)
        time.sleep(10)
        exit()

    def pay(self, amount: int) -> bool:
        if self.g < amount:
            return False
        self.g -= amount
        return True


# Characters
HUMAN = Entity(name="Human", desc="average human: jack of all trades, master of none",
               hp=100, atk=10, intl=10, g=100)
DWARF = Entity(name="Dwarf", desc="buff and rich, although weaker and less intelligent",
               hp=130, atk=7, intl=7, g=200)
ELF = Entity(name="Elf", desc="fragile, intellegent creature",
             hp=70, atk=10, intl=13, g=70)

# Enemies
SLIME = Entity(name="Slime", desc="", hp=20, atk=1, intl=1, g=10)
GOBLIN = Entity(name="Goblin", desc="", hp=40, atk=3, intl=3, g=20)
SCORPION = Entity(name="Scorpion", desc="", hp=30, atk=9, intl=2, g=30)
WORM = Entity(name="Worm", desc="", hp=70, atk=5, intl=4, g=100)
ANGEL = Entity(name="Angel", desc="", hp=140, atk=15, intl=15, g=200)
DEVIL = Entity(name="Devil", desc="", hp=150, atk=13, intl=13, g=400)


def load_story(path: str) -> list[list[str]]:
    story: str = open(path).read()
    story_blocks: list[str] = story.split("\n</>\n")
    story_choice_blocks: list[(str, str)] = \
        [block.split("\n<ch>\n") for block in story_blocks]
    parts: list[(list[str], list[str])] = \
        [(
         block[0].split("\n"),
         block[1].split("\n")
         )
         for block in story_choice_blocks]
    return parts


# TODO: make all magic numbers into constants


def main() -> None:
    character: Entity = inquirer.select(
        message="Select a character",
        choices=[{"name": HUMAN.name + " - " + HUMAN.desc, "value": HUMAN},
                 {"name": DWARF.name + " - " + DWARF.desc, "value": DWARF},
                 {"name": ELF.name + " - " + ELF.desc, "value": ELF}]
    ).execute()
    system("clear")

    story_blocks: list[(list[str], list[str])] = load_story("story.txt")
    current_block: int = 0

    for part in story_blocks[current_block][0]:
        print_animated(part + "\n", .05)  # 50ms (20ch/s)
        time.sleep(.1)  # 100ms
    choices: list[dict[str: str]] = [
        {"name": choice.split("<->")[1],
         "value": choice.split("<->")[0]}
        for choice in story_blocks[current_block][1]]
    selected_path: str = inquirer.select(message="", choices=choices).execute()
    for i in range(len(choices)):
        if selected_path == choices[i]["value"]:
            current_block += i+1

    for part in story_blocks[current_block][0]:
        print_animated(part + "\n", .05)  # 50ms (20ch/s)
        time.sleep(.1)  # 100ms
    choices = [
        {"name": choice.split("<->")[1],
         "value": choice.split("<->")[0]}
        for choice in story_blocks[current_block][1]]
    selected_path = inquirer.select(message="", choices=choices).execute()
    if selected_path == "fight goblin":
        character.fight(GOBLIN)
    elif selected_path == "fight slime":
        character.fight(SLIME)
    elif selected_path == "pay":
        if not character.pay(5):
            print_animated(
                "Unfortunately, you didn't have enought gold\n", .05)
            character.fight(GOBLIN)
    else:
        if character.intl <= 10:
            print_animated(
                "Unfortunately, you wasn't able to outsmart the slime\n", .05)
            time.sleep(.1)  # 100ms
            character.fight(SLIME)

    current_block = 3
    system("clear")
    print_animated("End of demo\n", .05)
    input("Press any key to win...")


if __name__ == "__main__":
    main()
