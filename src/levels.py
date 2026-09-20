class Level:
    def __init__(self, name, width, height, start_x, start_y, start_dir, goal_x, goal_y, obstacles=None):
        self.name = name
        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.start_dir = start_dir
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.obstacles = obstacles or []

LEVELS = [
    Level(
        name="Level 1: Straight to the Tree!",
        width=5, height=5,
        start_x=0, start_y=2, start_dir=1, # 1 is Right
        goal_x=4, goal_y=2
    ),
    Level(
        name="Level 2: Turn Around!",
        width=5, height=5,
        start_x=1, start_y=1, start_dir=1,
        goal_x=3, goal_y=4,
        obstacles=[(2, 1), (3, 1), (4, 1)]
    ),
    Level(
        name="Level 3: The Maze",
        width=6, height=6,
        start_x=1, start_y=4, start_dir=0, # 0 is Up
        goal_x=4, goal_y=1,
        obstacles=[(1, 3), (2, 3), (3, 3), (3, 2), (3, 1)]
    ),
    Level(
        name="Level 4: Savanna Walk",
        width=4, height=4,
        start_x=0, start_y=3, start_dir=1,
        goal_x=3, goal_y=3,
        obstacles=[]
    ),
    Level(
        name="Level 5: Giraffe Steps",
        width=4, height=4,
        start_x=0, start_y=0, start_dir=1,
        goal_x=3, goal_y=0,
        obstacles=[(1, 3)]
    ),
    Level(
        name="Level 6: Long Neck Journey",
        width=4, height=4,
        start_x=0, start_y=1, start_dir=1,
        goal_x=3, goal_y=0,
        obstacles=[(1, 0)]
    ),
    Level(
        name="Level 7: Acacia Quest",
        width=4, height=4,
        start_x=0, start_y=2, start_dir=1,
        goal_x=3, goal_y=0,
        obstacles=[(2, 2)]
    ),
    Level(
        name="Level 8: Leafy Snack",
        width=4, height=4,
        start_x=0, start_y=0, start_dir=1,
        goal_x=3, goal_y=1,
        obstacles=[(2, 2)]
    ),
    Level(
        name="Level 9: Jungle Path",
        width=4, height=4,
        start_x=0, start_y=0, start_dir=1,
        goal_x=3, goal_y=2,
        obstacles=[(1, 0)]
    ),
    Level(
        name="Level 10: Sunny Trek",
        width=4, height=4,
        start_x=0, start_y=3, start_dir=1,
        goal_x=3, goal_y=1,
        obstacles=[(1, 2), (2, 0)]
    ),
    Level(
        name="Level 11: River Crossing",
        width=4, height=4,
        start_x=0, start_y=0, start_dir=1,
        goal_x=3, goal_y=2,
        obstacles=[(1, 2), (2, 0)]
    ),
    Level(
        name="Level 12: Tall Trees",
        width=4, height=4,
        start_x=0, start_y=0, start_dir=1,
        goal_x=3, goal_y=2,
        obstacles=[(2, 0), (2, 1)]
    ),
    Level(
        name="Level 13: Green Meadows",
        width=4, height=4,
        start_x=0, start_y=1, start_dir=1,
        goal_x=3, goal_y=0,
        obstacles=[(1, 2), (2, 1)]
    ),
    Level(
        name="Level 14: Safari Adventure",
        width=4, height=4,
        start_x=0, start_y=0, start_dir=1,
        goal_x=3, goal_y=3,
        obstacles=[(1, 0), (2, 1)]
    ),
    Level(
        name="Level 15: Sunset Stroll",
        width=4, height=4,
        start_x=0, start_y=3, start_dir=1,
        goal_x=3, goal_y=3,
        obstacles=[(1, 0), (2, 3), (2, 2)]
    ),
    Level(
        name="Level 16: Spotted Friend",
        width=4, height=4,
        start_x=0, start_y=3, start_dir=1,
        goal_x=3, goal_y=0,
        obstacles=[(1, 0), (1, 1), (1, 2)]
    ),
    Level(
        name="Level 17: Wildlife Explorer",
        width=4, height=4,
        start_x=0, start_y=0, start_dir=1,
        goal_x=3, goal_y=2,
        obstacles=[(1, 1), (1, 3), (2, 1)]
    ),
    Level(
        name="Level 18: Nature Walk",
        width=4, height=4,
        start_x=0, start_y=1, start_dir=1,
        goal_x=3, goal_y=2,
        obstacles=[(2, 3), (1, 0), (2, 2)]
    ),
    Level(
        name="Level 19: Hidden Leaves",
        width=4, height=4,
        start_x=0, start_y=2, start_dir=1,
        goal_x=3, goal_y=3,
        obstacles=[(1, 2), (2, 0), (2, 2)]
    ),
    Level(
        name="Level 20: Bumpy Road",
        width=5, height=5,
        start_x=0, start_y=1, start_dir=1,
        goal_x=4, goal_y=4,
        obstacles=[(3, 1), (2, 1), (1, 4), (3, 0)]
    ),
    Level(
        name="Level 21: Monkey Business",
        width=5, height=5,
        start_x=0, start_y=2, start_dir=1,
        goal_x=4, goal_y=1,
        obstacles=[(1, 1), (3, 2), (2, 1), (2, 4)]
    ),
    Level(
        name="Level 22: Elephant Trail",
        width=5, height=5,
        start_x=0, start_y=2, start_dir=1,
        goal_x=4, goal_y=4,
        obstacles=[(2, 3), (3, 3), (2, 2), (3, 0)]
    ),
    Level(
        name="Level 23: Lion's Den",
        width=5, height=5,
        start_x=0, start_y=3, start_dir=1,
        goal_x=4, goal_y=2,
        obstacles=[(1, 1), (2, 0), (2, 1), (3, 0)]
    ),
    Level(
        name="Level 24: Zebra Zigzag",
        width=5, height=5,
        start_x=0, start_y=4, start_dir=1,
        goal_x=4, goal_y=1,
        obstacles=[(2, 3), (2, 4), (1, 3), (1, 4)]
    ),
    Level(
        name="Level 25: Rhino Run",
        width=5, height=5,
        start_x=0, start_y=1, start_dir=1,
        goal_x=4, goal_y=3,
        obstacles=[(2, 1), (1, 4), (3, 0), (2, 3), (1, 0)]
    ),
    Level(
        name="Level 26: Cheetah Sprint",
        width=5, height=5,
        start_x=0, start_y=1, start_dir=1,
        goal_x=4, goal_y=4,
        obstacles=[(2, 4), (1, 2), (2, 0), (3, 0), (2, 2)]
    ),
    Level(
        name="Level 27: Hippo Pool",
        width=5, height=5,
        start_x=0, start_y=3, start_dir=1,
        goal_x=4, goal_y=4,
        obstacles=[(2, 4), (1, 2), (2, 0), (2, 3)]
    ),
    Level(
        name="Level 28: Crocodile Creek",
        width=5, height=5,
        start_x=0, start_y=3, start_dir=1,
        goal_x=4, goal_y=2,
        obstacles=[(2, 4), (1, 2), (3, 4), (3, 1), (2, 0)]
    ),
    Level(
        name="Level 29: Ostrich Dash",
        width=5, height=5,
        start_x=0, start_y=2, start_dir=1,
        goal_x=4, goal_y=3,
        obstacles=[(3, 1), (1, 1), (1, 4), (2, 3), (3, 3)]
    ),
    Level(
        name="Level 30: Flamingo Flock",
        width=5, height=5,
        start_x=0, start_y=0, start_dir=1,
        goal_x=4, goal_y=1,
        obstacles=[(2, 4), (3, 4), (1, 1), (2, 0), (1, 4), (3, 0)]
    ),
    Level(
        name="Level 31: Meerkat Manor",
        width=5, height=5,
        start_x=0, start_y=0, start_dir=1,
        goal_x=4, goal_y=3,
        obstacles=[(1, 2), (3, 1), (2, 0), (2, 3), (3, 3), (1, 3)]
    ),
    Level(
        name="Level 32: Hyena Hideout",
        width=5, height=5,
        start_x=0, start_y=4, start_dir=1,
        goal_x=4, goal_y=1,
        obstacles=[(1, 1), (2, 0), (3, 0), (2, 2), (1, 0), (3, 2)]
    ),
    Level(
        name="Level 33: Baboon Branch",
        width=5, height=5,
        start_x=0, start_y=0, start_dir=1,
        goal_x=4, goal_y=0,
        obstacles=[(2, 1), (3, 4), (3, 1), (2, 0), (3, 0), (3, 2)]
    ),
    Level(
        name="Level 34: Leopard Leap",
        width=5, height=5,
        start_x=0, start_y=4, start_dir=1,
        goal_x=4, goal_y=2,
        obstacles=[(3, 4), (3, 1), (2, 3), (1, 0), (3, 2)]
    ),
    Level(
        name="Level 35: Wildebeest Way",
        width=5, height=5,
        start_x=0, start_y=1, start_dir=1,
        goal_x=4, goal_y=2,
        obstacles=[(1, 2), (2, 0), (2, 2), (1, 0), (3, 2), (1, 3)]
    ),
    Level(
        name="Level 36: Gazelle Gallop",
        width=5, height=5,
        start_x=0, start_y=3, start_dir=1,
        goal_x=4, goal_y=0,
        obstacles=[(1, 2), (1, 1), (3, 3), (2, 2), (1, 0)]
    ),
    Level(
        name="Level 37: Buffalo Roam",
        width=5, height=5,
        start_x=0, start_y=0, start_dir=1,
        goal_x=4, goal_y=4,
        obstacles=[(2, 1), (1, 1), (3, 0), (2, 3), (3, 3), (1, 0)]
    ),
    Level(
        name="Level 38: Warthog Wallow",
        width=5, height=5,
        start_x=0, start_y=4, start_dir=1,
        goal_x=4, goal_y=3,
        obstacles=[(1, 2), (3, 4), (2, 0), (1, 0), (3, 2), (1, 3)]
    ),
    Level(
        name="Level 39: Python Path",
        width=5, height=5,
        start_x=0, start_y=1, start_dir=1,
        goal_x=4, goal_y=1,
        obstacles=[(3, 4), (2, 0), (1, 4), (3, 0), (2, 2), (1, 0)]
    ),
    Level(
        name="Level 40: Tortoise Trail",
        width=6, height=6,
        start_x=0, start_y=5, start_dir=1,
        goal_x=5, goal_y=5,
        obstacles=[(4, 0), (4, 3), (3, 1), (2, 0), (3, 3), (2, 2), (1, 0), (4, 1)]
    ),
    Level(
        name="Level 41: Chameleon Colors",
        width=6, height=6,
        start_x=0, start_y=1, start_dir=1,
        goal_x=5, goal_y=2,
        obstacles=[(2, 4), (3, 4), (3, 1), (1, 1), (4, 2), (3, 0), (4, 5), (4, 1)]
    ),
    Level(
        name="Level 42: Eagle Eye",
        width=6, height=6,
        start_x=0, start_y=0, start_dir=1,
        goal_x=5, goal_y=4,
        obstacles=[(4, 4), (1, 1), (2, 0), (1, 4), (3, 3), (2, 2), (2, 5)]
    ),
    Level(
        name="Level 43: Vulture View",
        width=6, height=6,
        start_x=0, start_y=5, start_dir=1,
        goal_x=5, goal_y=0,
        obstacles=[(1, 2), (3, 1), (1, 1), (2, 3), (4, 5), (3, 3), (2, 2), (1, 3)]
    ),
    Level(
        name="Level 44: Termite Mound",
        width=6, height=6,
        start_x=0, start_y=3, start_dir=1,
        goal_x=5, goal_y=3,
        obstacles=[(4, 4), (1, 5), (3, 1), (4, 3), (4, 2), (2, 2), (3, 2), (3, 5)]
    ),
    Level(
        name="Level 45: Baobab Tree",
        width=6, height=6,
        start_x=0, start_y=2, start_dir=1,
        goal_x=5, goal_y=0,
        obstacles=[(4, 4), (4, 0), (1, 2), (3, 1), (1, 1), (2, 3), (1, 0), (3, 5)]
    ),
    Level(
        name="Level 46: Dry Riverbed",
        width=6, height=6,
        start_x=0, start_y=0, start_dir=1,
        goal_x=5, goal_y=3,
        obstacles=[(2, 4), (2, 1), (3, 4), (3, 1), (2, 3), (4, 5), (3, 3), (2, 5), (3, 5)]
    ),
    Level(
        name="Level 47: Dusty Trail",
        width=6, height=6,
        start_x=0, start_y=5, start_dir=1,
        goal_x=5, goal_y=5,
        obstacles=[(4, 4), (2, 4), (3, 4), (2, 1), (1, 5), (1, 4), (4, 5), (2, 5), (4, 1)]
    ),
    Level(
        name="Level 48: Rocky Ridge",
        width=6, height=6,
        start_x=0, start_y=2, start_dir=1,
        goal_x=5, goal_y=5,
        obstacles=[(4, 4), (2, 4), (1, 2), (1, 5), (1, 1), (1, 4), (4, 5), (3, 3), (3, 2)]
    ),
    Level(
        name="Level 49: Sandy Dunes",
        width=6, height=6,
        start_x=0, start_y=5, start_dir=1,
        goal_x=5, goal_y=5,
        obstacles=[(1, 2), (2, 1), (3, 4), (2, 0), (4, 2), (3, 3), (2, 2), (3, 2), (4, 1)]
    ),
    Level(
        name="Level 50: Oasis Spring",
        width=6, height=6,
        start_x=0, start_y=5, start_dir=1,
        goal_x=5, goal_y=4,
        obstacles=[(2, 4), (4, 0), (1, 5), (2, 0), (2, 3), (2, 2), (2, 5), (4, 1)]
    ),
    Level(
        name="Level 51: Palm Grove",
        width=6, height=6,
        start_x=0, start_y=4, start_dir=1,
        goal_x=5, goal_y=4,
        obstacles=[(2, 4), (2, 0), (1, 4), (4, 2), (2, 2), (1, 0), (2, 5), (1, 3), (3, 5)]
    ),
    Level(
        name="Level 52: Cactus Patch",
        width=6, height=6,
        start_x=0, start_y=3, start_dir=1,
        goal_x=5, goal_y=1,
        obstacles=[(3, 4), (1, 5), (4, 3), (1, 1), (2, 0), (3, 0), (2, 3), (4, 5), (3, 2)]
    ),
    Level(
        name="Level 53: Thorny Bush",
        width=6, height=6,
        start_x=0, start_y=0, start_dir=1,
        goal_x=5, goal_y=5,
        obstacles=[(4, 0), (4, 3), (2, 0), (3, 0), (2, 3), (3, 3), (2, 2), (1, 0), (4, 1)]
    ),
    Level(
        name="Level 54: Giraffe's Secret",
        width=6, height=6,
        start_x=0, start_y=4, start_dir=1,
        goal_x=5, goal_y=3,
        obstacles=[(4, 4), (2, 4), (1, 2), (3, 4), (1, 5), (1, 1), (2, 0), (3, 3), (1, 0)]
    ),
    Level(
        name="Level 55: Tallest View",
        width=6, height=6,
        start_x=0, start_y=5, start_dir=1,
        goal_x=5, goal_y=0,
        obstacles=[(2, 4), (3, 4), (1, 1), (1, 4), (3, 0), (4, 2), (4, 5), (3, 3), (3, 2)]
    ),
    Level(
        name="Level 56: Stretching Up",
        width=6, height=6,
        start_x=0, start_y=4, start_dir=1,
        goal_x=5, goal_y=2,
        obstacles=[(2, 4), (2, 1), (1, 5), (4, 1), (4, 2), (2, 3), (4, 5), (2, 5), (1, 3)]
    ),
    Level(
        name="Level 57: Tippy Toes",
        width=6, height=6,
        start_x=0, start_y=1, start_dir=1,
        goal_x=5, goal_y=1,
        obstacles=[(4, 4), (2, 4), (2, 0), (1, 4), (4, 2), (3, 0), (4, 5), (3, 3), (1, 3)]
    ),
    Level(
        name="Level 58: High Branches",
        width=6, height=6,
        start_x=0, start_y=3, start_dir=1,
        goal_x=5, goal_y=2,
        obstacles=[(1, 2), (3, 1), (1, 4), (3, 0), (4, 5), (3, 3), (3, 2), (1, 3)]
    ),
    Level(
        name="Level 59: Sweet Leaves",
        width=6, height=6,
        start_x=0, start_y=5, start_dir=1,
        goal_x=5, goal_y=3,
        obstacles=[(1, 5), (3, 1), (4, 3), (1, 1), (2, 0), (4, 2), (3, 0), (4, 5), (3, 2)]
    ),
    Level(
        name="Level 60: Munching Time",
        width=7, height=7,
        start_x=0, start_y=1, start_dir=1,
        goal_x=6, goal_y=6,
        obstacles=[(4, 4), (1, 2), (5, 5), (4, 3), (3, 1), (1, 1), (1, 4), (4, 2), (2, 3), (3, 6), (3, 2), (5, 2)]
    ),
    Level(
        name="Level 61: Hungry Giraffe",
        width=7, height=7,
        start_x=0, start_y=3, start_dir=1,
        goal_x=6, goal_y=6,
        obstacles=[(1, 2), (3, 4), (1, 5), (1, 1), (4, 6), (5, 0), (5, 6), (3, 6), (5, 3), (1, 6), (3, 2), (3, 5)]
    ),
    Level(
        name="Level 62: Yummy Snack",
        width=7, height=7,
        start_x=0, start_y=5, start_dir=1,
        goal_x=6, goal_y=6,
        obstacles=[(1, 2), (2, 0), (5, 1), (1, 4), (3, 0), (3, 3), (2, 6), (5, 6), (5, 3), (3, 2), (2, 5), (1, 3)]
    ),
    Level(
        name="Level 63: Green Feast",
        width=7, height=7,
        start_x=0, start_y=6, start_dir=1,
        goal_x=6, goal_y=4,
        obstacles=[(5, 5), (3, 4), (1, 5), (1, 1), (4, 6), (5, 1), (1, 4), (4, 5), (3, 3), (1, 0), (1, 6), (5, 2)]
    ),
    Level(
        name="Level 64: Savanna Breeze",
        width=7, height=7,
        start_x=0, start_y=6, start_dir=1,
        goal_x=6, goal_y=1,
        obstacles=[(4, 4), (2, 4), (4, 0), (4, 2), (3, 0), (4, 5), (3, 6), (1, 0), (1, 6), (2, 5), (1, 3), (5, 2)]
    ),
    Level(
        name="Level 65: Morning Dew",
        width=7, height=7,
        start_x=0, start_y=2, start_dir=1,
        goal_x=6, goal_y=0,
        obstacles=[(4, 4), (4, 0), (5, 5), (1, 2), (4, 2), (1, 4), (2, 6), (5, 6), (5, 0), (3, 6), (1, 6), (5, 2)]
    ),
    Level(
        name="Level 66: Afternoon Sun",
        width=7, height=7,
        start_x=0, start_y=4, start_dir=1,
        goal_x=6, goal_y=5,
        obstacles=[(2, 4), (5, 5), (4, 3), (1, 1), (5, 4), (1, 4), (2, 6), (3, 6), (1, 0), (1, 6), (3, 2), (5, 2)]
    ),
    Level(
        name="Level 67: Evening Shadows",
        width=7, height=7,
        start_x=0, start_y=2, start_dir=1,
        goal_x=6, goal_y=0,
        obstacles=[(2, 4), (2, 1), (1, 5), (1, 1), (4, 6), (5, 1), (4, 2), (4, 5), (2, 6), (5, 3), (3, 2), (4, 1)]
    ),
    Level(
        name="Level 68: Starry Night",
        width=7, height=7,
        start_x=0, start_y=4, start_dir=1,
        goal_x=6, goal_y=2,
        obstacles=[(4, 4), (2, 4), (4, 3), (3, 1), (5, 4), (4, 6), (5, 1), (2, 6), (1, 6), (2, 5), (4, 1), (3, 5)]
    ),
    Level(
        name="Level 69: Moonlight Walk",
        width=7, height=7,
        start_x=0, start_y=3, start_dir=1,
        goal_x=6, goal_y=3,
        obstacles=[(4, 4), (2, 4), (4, 3), (1, 1), (4, 2), (4, 5), (3, 3), (2, 6), (3, 6), (2, 2), (2, 5), (3, 5)]
    ),
    Level(
        name="Level 70: Sunrise Safari",
        width=7, height=7,
        start_x=0, start_y=0, start_dir=1,
        goal_x=6, goal_y=1,
        obstacles=[(4, 4), (2, 4), (1, 2), (4, 0), (3, 4), (4, 3), (2, 0), (3, 3), (2, 2), (1, 6), (4, 1), (5, 2)]
    ),
    Level(
        name="Level 71: Sunset Safari",
        width=7, height=7,
        start_x=0, start_y=5, start_dir=1,
        goal_x=6, goal_y=6,
        obstacles=[(2, 4), (3, 4), (5, 4), (1, 4), (3, 0), (2, 3), (3, 6), (1, 6), (3, 2), (2, 5), (1, 3), (3, 5)]
    ),
    Level(
        name="Level 72: Cloudy Day",
        width=7, height=7,
        start_x=0, start_y=0, start_dir=1,
        goal_x=6, goal_y=3,
        obstacles=[(4, 0), (5, 5), (3, 4), (2, 1), (3, 1), (5, 4), (4, 6), (2, 0), (5, 1), (4, 5), (1, 6), (5, 2)]
    ),
    Level(
        name="Level 73: Rainy Season",
        width=7, height=7,
        start_x=0, start_y=6, start_dir=1,
        goal_x=6, goal_y=2,
        obstacles=[(4, 4), (2, 1), (4, 3), (3, 1), (1, 1), (2, 3), (1, 0), (2, 6), (5, 6), (5, 3), (1, 3), (3, 5)]
    ),
    Level(
        name="Level 74: Muddy Puddles",
        width=7, height=7,
        start_x=0, start_y=5, start_dir=1,
        goal_x=6, goal_y=2,
        obstacles=[(3, 4), (4, 3), (3, 1), (4, 6), (2, 3), (4, 5), (5, 0), (5, 3), (1, 6), (2, 5), (3, 5), (5, 2)]
    ),
    Level(
        name="Level 75: Splash Time",
        width=7, height=7,
        start_x=0, start_y=3, start_dir=1,
        goal_x=6, goal_y=2,
        obstacles=[(3, 4), (1, 5), (5, 1), (4, 2), (1, 0), (4, 5), (2, 6), (5, 3), (1, 6), (2, 5), (4, 1), (3, 5)]
    ),
    Level(
        name="Level 76: Cooling Off",
        width=7, height=7,
        start_x=0, start_y=3, start_dir=1,
        goal_x=6, goal_y=1,
        obstacles=[(2, 4), (1, 2), (2, 1), (1, 5), (5, 4), (5, 1), (2, 3), (5, 0), (5, 6), (3, 6), (4, 1), (5, 2)]
    ),
    Level(
        name="Level 77: Thirsty Work",
        width=7, height=7,
        start_x=0, start_y=3, start_dir=1,
        goal_x=6, goal_y=6,
        obstacles=[(2, 4), (4, 0), (5, 1), (2, 3), (4, 5), (5, 6), (1, 0), (1, 6), (3, 2), (2, 5), (3, 5)]
    ),
    Level(
        name="Level 78: Watering Hole",
        width=7, height=7,
        start_x=0, start_y=5, start_dir=1,
        goal_x=6, goal_y=3,
        obstacles=[(4, 4), (2, 4), (1, 2), (2, 1), (2, 0), (3, 0), (4, 5), (3, 6), (5, 3), (3, 2), (3, 5), (5, 2)]
    ),
    Level(
        name="Level 79: Friendly Faces",
        width=7, height=7,
        start_x=0, start_y=3, start_dir=1,
        goal_x=6, goal_y=0,
        obstacles=[(4, 4), (4, 0), (5, 5), (3, 4), (5, 4), (4, 6), (4, 2), (2, 3), (2, 6), (5, 6), (1, 0), (3, 2)]
    ),
    Level(
        name="Level 80: Meeting Friends",
        width=8, height=8,
        start_x=0, start_y=0, start_dir=1,
        goal_x=7, goal_y=1,
        obstacles=[(4, 4), (1, 2), (4, 0), (3, 4), (1, 5), (2, 0), (6, 6), (4, 2), (1, 4), (3, 3), (6, 0), (1, 0), (1, 6), (2, 5), (4, 1), (5, 2)]
    ),
    Level(
        name="Level 81: Playing Tag",
        width=8, height=8,
        start_x=0, start_y=5, start_dir=1,
        goal_x=7, goal_y=6,
        obstacles=[(4, 4), (1, 2), (4, 0), (1, 5), (4, 3), (4, 6), (6, 7), (4, 5), (1, 7), (2, 6), (3, 6), (2, 2), (3, 2), (2, 5), (4, 7)]
    ),
    Level(
        name="Level 82: Hide and Seek",
        width=8, height=8,
        start_x=0, start_y=5, start_dir=1,
        goal_x=7, goal_y=3,
        obstacles=[(2, 4), (6, 2), (6, 5), (4, 3), (1, 5), (5, 1), (4, 2), (6, 4), (2, 3), (1, 7), (3, 3), (2, 6), (3, 6), (1, 6), (3, 2), (2, 5)]
    ),
    Level(
        name="Level 83: Racing Fun",
        width=8, height=8,
        start_x=0, start_y=5, start_dir=1,
        goal_x=7, goal_y=5,
        obstacles=[(1, 2), (2, 2), (4, 0), (2, 7), (3, 4), (3, 1), (1, 1), (4, 2), (6, 7), (1, 7), (5, 0), (5, 6), (3, 6), (5, 3), (6, 3), (3, 5)]
    ),
    Level(
        name="Level 84: Puzzle Path",
        width=8, height=8,
        start_x=0, start_y=3, start_dir=1,
        goal_x=7, goal_y=2,
        obstacles=[(4, 4), (1, 2), (1, 5), (3, 1), (4, 3), (6, 1), (3, 7), (6, 4), (3, 0), (2, 3), (6, 0), (5, 3), (3, 2), (4, 1), (4, 7), (5, 2)]
    ),
    Level(
        name="Level 85: Tricky Trail",
        width=8, height=8,
        start_x=0, start_y=0, start_dir=1,
        goal_x=7, goal_y=0,
        obstacles=[(4, 4), (2, 4), (3, 1), (4, 6), (6, 4), (4, 2), (3, 0), (6, 7), (2, 5), (2, 6), (5, 0), (1, 6), (3, 2), (6, 3), (4, 7), (3, 5)]
    ),
    Level(
        name="Level 86: Winding Way",
        width=8, height=8,
        start_x=0, start_y=5, start_dir=1,
        goal_x=7, goal_y=0,
        obstacles=[(4, 4), (1, 3), (4, 0), (2, 2), (3, 1), (6, 1), (5, 4), (3, 7), (5, 1), (6, 7), (6, 0), (3, 2), (2, 5), (4, 1), (4, 7), (3, 5)]
    ),
    Level(
        name="Level 87: Zigzag Route",
        width=8, height=8,
        start_x=0, start_y=3, start_dir=1,
        goal_x=7, goal_y=7,
        obstacles=[(6, 2), (4, 0), (5, 5), (2, 1), (4, 3), (3, 1), (4, 6), (2, 0), (6, 4), (1, 4), (1, 7), (3, 3), (5, 0), (3, 6), (6, 6), (6, 3)]
    ),
    Level(
        name="Level 88: Looping Lane",
        width=8, height=8,
        start_x=0, start_y=3, start_dir=1,
        goal_x=7, goal_y=4,
        obstacles=[(6, 2), (5, 5), (3, 4), (1, 5), (3, 7), (6, 1), (4, 6), (4, 2), (2, 3), (3, 3), (2, 6), (5, 6), (5, 0), (2, 2), (5, 3), (6, 3)]
    ),
    Level(
        name="Level 89: Straight Ahead",
        width=8, height=8,
        start_x=0, start_y=5, start_dir=1,
        goal_x=7, goal_y=4,
        obstacles=[(4, 4), (6, 2), (4, 0), (1, 2), (6, 5), (5, 1), (4, 2), (6, 4), (3, 0), (1, 7), (5, 0), (3, 6), (6, 0), (5, 3), (1, 6), (2, 5)]
    ),
    Level(
        name="Level 90: Turn Left",
        width=8, height=8,
        start_x=0, start_y=6, start_dir=1,
        goal_x=7, goal_y=1,
        obstacles=[(6, 2), (6, 0), (4, 0), (2, 1), (1, 2), (3, 7), (1, 1), (6, 1), (6, 4), (3, 0), (6, 7), (1, 7), (6, 3), (2, 2), (3, 2), (2, 5)]
    ),
    Level(
        name="Level 91: Turn Right",
        width=8, height=8,
        start_x=0, start_y=7, start_dir=1,
        goal_x=7, goal_y=3,
        obstacles=[(4, 4), (2, 4), (4, 0), (2, 7), (1, 5), (3, 1), (3, 7), (5, 4), (2, 0), (5, 1), (6, 6), (3, 3), (1, 0), (2, 5), (4, 1), (3, 5)]
    ),
    Level(
        name="Level 92: U-Turn",
        width=8, height=8,
        start_x=0, start_y=5, start_dir=1,
        goal_x=7, goal_y=0,
        obstacles=[(6, 2), (4, 0), (1, 2), (2, 1), (2, 7), (5, 1), (5, 7), (6, 4), (2, 3), (6, 7), (3, 3), (5, 0), (1, 0), (1, 3), (4, 7), (5, 2)]
    ),
    Level(
        name="Level 93: Roundabout",
        width=8, height=8,
        start_x=0, start_y=7, start_dir=1,
        goal_x=7, goal_y=1,
        obstacles=[(6, 2), (6, 0), (2, 2), (2, 4), (2, 7), (1, 1), (4, 6), (2, 0), (1, 4), (4, 2), (1, 7), (4, 5), (3, 6), (6, 3), (3, 5), (5, 2)]
    ),
    Level(
        name="Level 94: Up and Down",
        width=8, height=8,
        start_x=0, start_y=0, start_dir=1,
        goal_x=7, goal_y=0,
        obstacles=[(4, 4), (6, 2), (5, 5), (2, 4), (4, 3), (1, 1), (6, 4), (1, 4), (3, 0), (2, 3), (1, 7), (3, 3), (3, 6), (6, 3), (4, 7), (5, 2)]
    ),
    Level(
        name="Level 95: Over the Hill",
        width=8, height=8,
        start_x=0, start_y=7, start_dir=1,
        goal_x=7, goal_y=2,
        obstacles=[(4, 4), (2, 4), (5, 5), (1, 2), (2, 1), (6, 5), (4, 3), (3, 1), (2, 0), (5, 7), (3, 0), (2, 3), (4, 5), (6, 0), (6, 3), (4, 7)]
    ),
    Level(
        name="Level 96: Through the Valley",
        width=8, height=8,
        start_x=0, start_y=3, start_dir=1,
        goal_x=7, goal_y=6,
        obstacles=[(1, 3), (6, 2), (3, 1), (6, 1), (2, 0), (5, 1), (3, 0), (1, 0), (4, 5), (1, 7), (5, 0), (6, 0), (6, 6), (3, 2), (4, 1), (3, 5)]
    ),
    Level(
        name="Level 97: Across the River",
        width=8, height=8,
        start_x=0, start_y=6, start_dir=1,
        goal_x=7, goal_y=1,
        obstacles=[(4, 4), (6, 2), (2, 1), (2, 7), (1, 5), (6, 1), (1, 1), (5, 7), (3, 3), (5, 0), (5, 6), (2, 6), (1, 0), (4, 7), (3, 5)]
    ),
    Level(
        name="Level 98: Under the Tree",
        width=8, height=8,
        start_x=0, start_y=2, start_dir=1,
        goal_x=7, goal_y=5,
        obstacles=[(2, 4), (4, 0), (3, 4), (2, 7), (6, 5), (6, 1), (5, 4), (1, 4), (6, 7), (4, 5), (5, 6), (2, 2), (5, 3), (4, 7), (3, 5), (5, 2)]
    ),
    Level(
        name="Level 99: Almost There",
        width=8, height=8,
        start_x=0, start_y=0, start_dir=1,
        goal_x=7, goal_y=5,
        obstacles=[(6, 2), (4, 0), (1, 2), (3, 4), (6, 5), (4, 3), (2, 7), (6, 1), (5, 1), (1, 4), (2, 3), (4, 5), (3, 3), (2, 6), (1, 7), (3, 6)]
    ),
    Level(
        name="Level 100: Just a Bit More",
        width=8, height=8,
        start_x=0, start_y=1, start_dir=1,
        goal_x=7, goal_y=2,
        obstacles=[(4, 4), (5, 5), (2, 2), (2, 1), (2, 7), (3, 1), (3, 7), (5, 3), (5, 7), (3, 0), (4, 2), (6, 0), (1, 0), (1, 6), (3, 2), (5, 2)]
    ),

    Level(
        name="Level 101: Gentle Cave",
        width=6, height=9,
        start_x=5, start_y=7, start_dir=3,
        goal_x=0, goal_y=8,
        obstacles=[(4, 4), (0, 7), (2, 4), (1, 2), (2, 1), (3, 4), (5, 8), (0, 3), (2, 0), (0, 2), (1, 7), (2, 6), (3, 6), (5, 3), (1, 6), (5, 2)]
    ),
    Level(
        name="Level 102: Dusty Cave",
        width=8, height=7,
        start_x=1, start_y=3, start_dir=2,
        goal_x=4, goal_y=5,
        obstacles=[(4, 4), (0, 1), (4, 0), (7, 1), (5, 5), (6, 5), (2, 1), (1, 2), (4, 6), (2, 0), (7, 0), (0, 6), (2, 5), (7, 2), (6, 0), (1, 6), (6, 3)]
    ),
    Level(
        name="Level 103: Wild Path",
        width=8, height=7,
        start_x=7, start_y=3, start_dir=1,
        goal_x=4, goal_y=5,
        obstacles=[(7, 4), (4, 0), (1, 1), (2, 0), (0, 6), (2, 3), (0, 2), (0, 5), (3, 2)]
    ),
    Level(
        name="Level 104: Dusty Path",
        width=8, height=9,
        start_x=3, start_y=2, start_dir=1,
        goal_x=5, goal_y=6,
        obstacles=[(4, 0), (3, 4), (3, 7), (5, 1), (1, 3), (7, 4), (6, 2), (3, 0), (3, 3), (5, 3), (2, 4), (2, 1), (2, 7), (1, 5), (6, 1), (6, 4), (6, 7), (7, 6), (4, 1), (4, 7), (5, 2), (5, 5), (0, 0), (0, 3), (1, 4), (2, 3), (6, 0)]
    ),
    Level(
        name="Level 105: Tangled Labyrinth",
        width=6, height=8,
        start_x=4, start_y=5, start_dir=0,
        goal_x=0, goal_y=3,
        obstacles=[(4, 0), (2, 1), (1, 1), (4, 6), (1, 6), (1, 3), (3, 5)]
    ),
    Level(
        name="Level 106: Tall Savanna",
        width=9, height=9,
        start_x=3, start_y=1, start_dir=3,
        goal_x=3, goal_y=8,
        obstacles=[(7, 4), (2, 0), (4, 2), (4, 1), (7, 8)]
    ),
    Level(
        name="Level 107: Dusty Journey",
        width=6, height=7,
        start_x=0, start_y=5, start_dir=3,
        goal_x=1, goal_y=0,
        obstacles=[(2, 4), (5, 5), (3, 0), (5, 6), (2, 2), (5, 3), (5, 2)]
    ),
    Level(
        name="Level 108: Tangled Maze",
        width=7, height=6,
        start_x=0, start_y=2, start_dir=3,
        goal_x=6, goal_y=2,
        obstacles=[(0, 1), (2, 1), (4, 3), (1, 5), (3, 1), (5, 4), (1, 1), (2, 0), (4, 5), (6, 0), (6, 3), (3, 5)]
    ),
    Level(
        name="Level 109: Gentle Maze",
        width=8, height=9,
        start_x=2, start_y=0, start_dir=0,
        goal_x=6, goal_y=2,
        obstacles=[(4, 4), (7, 4), (2, 4), (2, 7), (1, 5), (1, 1), (4, 6), (5, 1), (6, 6), (3, 2), (1, 3), (0, 8)]
    ),
    Level(
        name="Level 110: Perilous Path",
        width=6, height=9,
        start_x=4, start_y=4, start_dir=2,
        goal_x=2, goal_y=1,
        obstacles=[(4, 0), (3, 4), (5, 8), (2, 5), (2, 8)]
    ),
    Level(
        name="Level 111: Wild Crossing",
        width=9, height=8,
        start_x=4, start_y=4, start_dir=1,
        goal_x=5, goal_y=0,
        obstacles=[(0, 1), (2, 4), (5, 4), (4, 2), (6, 7), (5, 6), (7, 2), (7, 5), (2, 5), (4, 7)]
    ),
    Level(
        name="Level 112: Brave Cave",
        width=9, height=7,
        start_x=2, start_y=6, start_dir=3,
        goal_x=4, goal_y=2,
        obstacles=[(4, 6), (5, 1), (8, 6), (0, 5), (1, 3), (7, 4), (6, 5), (8, 2), (8, 5), (1, 5), (6, 4), (8, 4), (0, 0), (8, 1), (1, 1), (0, 3), (2, 0), (1, 4), (6, 0), (6, 6), (7, 5)]
    ),
    Level(
        name="Level 113: Golden Ridge",
        width=6, height=6,
        start_x=0, start_y=4, start_dir=0,
        goal_x=3, goal_y=1,
        obstacles=[(0, 1), (2, 4), (3, 4), (0, 0), (5, 3), (1, 4), (5, 0), (0, 5), (1, 0), (2, 5)]
    ),
    Level(
        name="Level 114: Tricky Dunes",
        width=8, height=7,
        start_x=3, start_y=0, start_dir=1,
        goal_x=7, goal_y=3,
        obstacles=[(4, 4), (7, 4), (6, 2), (3, 4), (1, 1), (4, 2), (2, 3), (5, 3), (1, 6)]
    ),
    Level(
        name="Level 115: Golden Valley",
        width=8, height=7,
        start_x=1, start_y=4, start_dir=0,
        goal_x=6, goal_y=5,
        obstacles=[(7, 4), (6, 2), (1, 2), (0, 4), (4, 0), (7, 1), (3, 1), (7, 0), (4, 2), (7, 3), (1, 0), (4, 5), (7, 6), (2, 6), (5, 3), (2, 5), (4, 1), (3, 5)]
    ),
    Level(
        name="Level 116: Deep Savanna",
        width=8, height=6,
        start_x=0, start_y=4, start_dir=3,
        goal_x=4, goal_y=3,
        obstacles=[(0, 1), (6, 2), (5, 5), (7, 1), (1, 5), (3, 1), (2, 0), (6, 4), (1, 0), (4, 5), (3, 3), (0, 5), (5, 3), (6, 3), (4, 1)]
    ),
    Level(
        name="Level 117: Secret Bush",
        width=7, height=7,
        start_x=5, start_y=4, start_dir=3,
        goal_x=6, goal_y=0,
        obstacles=[(4, 4), (5, 5), (0, 0), (1, 5), (3, 1), (1, 1), (4, 6), (2, 0), (5, 1), (3, 0), (1, 3)]
    ),
    Level(
        name="Level 118: Distant Meadow",
        width=7, height=9,
        start_x=1, start_y=0, start_dir=1,
        goal_x=3, goal_y=4,
        obstacles=[(4, 3), (3, 1), (5, 1), (5, 7), (0, 8), (2, 5), (6, 8), (3, 0), (3, 3), (5, 6), (3, 6), (0, 7), (2, 1), (1, 8), (3, 2), (4, 1), (0, 3), (6, 0), (6, 6)]
    ),
    Level(
        name="Level 119: Ancient Rock",
        width=9, height=7,
        start_x=2, start_y=4, start_dir=0,
        goal_x=0, goal_y=0,
        obstacles=[(1, 3), (2, 1), (0, 3), (5, 1), (0, 6), (8, 6), (4, 1)]
    ),
    Level(
        name="Level 120: Dry Cave",
        width=7, height=7,
        start_x=0, start_y=0, start_dir=1,
        goal_x=6, goal_y=1,
        obstacles=[(4, 4), (0, 1), (6, 5), (1, 1), (3, 0), (3, 6)]
    ),
    Level(
        name="Level 121: Swift Valley",
        width=8, height=7,
        start_x=5, start_y=4, start_dir=2,
        goal_x=2, goal_y=1,
        obstacles=[(3, 4), (5, 1), (2, 2), (2, 5), (7, 4), (6, 2), (4, 5), (5, 0), (5, 6), (3, 6), (5, 3), (2, 4), (7, 0), (3, 5), (5, 5), (0, 0), (1, 1), (1, 4), (2, 3), (2, 6)]
    ),
    Level(
        name="Level 122: Brave Ridge",
        width=8, height=9,
        start_x=4, start_y=4, start_dir=1,
        goal_x=7, goal_y=3,
        obstacles=[(0, 1), (0, 7), (4, 3), (5, 4), (7, 6), (0, 5), (4, 1), (7, 8)]
    ),
    Level(
        name="Level 123: Sunny Crossing",
        width=9, height=8,
        start_x=5, start_y=4, start_dir=3,
        goal_x=8, goal_y=6,
        obstacles=[(8, 4), (6, 5), (1, 5), (8, 1), (0, 0), (6, 1), (2, 0), (5, 1), (6, 7), (1, 7), (3, 3), (0, 5), (6, 6), (4, 1), (4, 7), (3, 5), (5, 2)]
    ),
    Level(
        name="Level 124: Silent Rock",
        width=7, height=7,
        start_x=0, start_y=4, start_dir=1,
        goal_x=6, goal_y=5,
        obstacles=[(4, 4), (2, 4), (4, 0), (5, 1), (5, 2)]
    ),
    Level(
        name="Level 125: Ancient Tree",
        width=7, height=6,
        start_x=6, start_y=3, start_dir=3,
        goal_x=1, goal_y=5,
        obstacles=[(2, 4), (5, 5), (4, 0), (0, 4), (3, 4), (3, 1), (6, 1), (2, 0), (5, 1), (3, 0), (2, 3), (0, 2), (1, 3)]
    ),
    Level(
        name="Level 126: Tricky Rock",
        width=9, height=8,
        start_x=6, start_y=3, start_dir=0,
        goal_x=4, goal_y=6,
        obstacles=[(4, 0), (2, 1), (6, 5), (4, 1), (8, 1), (6, 4), (7, 2), (5, 3), (1, 3)]
    ),
    Level(
        name="Level 127: Wild Cave",
        width=8, height=7,
        start_x=2, start_y=2, start_dir=2,
        goal_x=5, goal_y=5,
        obstacles=[(2, 4), (1, 2), (0, 4), (6, 5), (1, 5), (5, 4), (7, 0), (2, 0), (6, 6), (0, 6), (0, 5), (5, 3)]
    ),
    Level(
        name="Level 128: Tricky Maze",
        width=8, height=6,
        start_x=1, start_y=3, start_dir=2,
        goal_x=2, goal_y=0,
        obstacles=[(4, 4), (2, 4), (2, 2), (2, 1), (0, 4), (4, 3), (1, 5), (5, 4), (1, 1), (6, 4), (4, 2), (5, 1), (6, 0), (3, 5)]
    ),
    Level(
        name="Level 129: Muddy Trail",
        width=7, height=8,
        start_x=1, start_y=4, start_dir=3,
        goal_x=3, goal_y=0,
        obstacles=[(4, 3), (3, 7), (5, 7), (2, 2), (1, 0)]
    ),
    Level(
        name="Level 130: Thirsty Journey",
        width=6, height=8,
        start_x=1, start_y=3, start_dir=3,
        goal_x=4, goal_y=6,
        obstacles=[(5, 5), (1, 2), (1, 5), (5, 4), (2, 0), (5, 1), (4, 2), (0, 6), (1, 4), (0, 2), (5, 6), (3, 2), (5, 2)]
    ),
    Level(
        name="Level 131: Silent Oasis",
        width=8, height=6,
        start_x=5, start_y=3, start_dir=1,
        goal_x=1, goal_y=1,
        obstacles=[(6, 2), (2, 4), (7, 1), (2, 1), (0, 0), (5, 4), (2, 0), (1, 4), (2, 3), (5, 0), (7, 2), (0, 5), (2, 5), (3, 5)]
    ),
    Level(
        name="Level 132: Hidden Tree",
        width=9, height=8,
        start_x=2, start_y=3, start_dir=2,
        goal_x=7, goal_y=2,
        obstacles=[(0, 1), (7, 4), (2, 4), (1, 2), (3, 4), (2, 7), (1, 5), (6, 1), (7, 3), (5, 6), (0, 5), (1, 0), (7, 5)]
    ),
    Level(
        name="Level 133: Distant Rock",
        width=8, height=9,
        start_x=2, start_y=1, start_dir=1,
        goal_x=6, goal_y=4,
        obstacles=[(0, 5), (0, 8), (1, 3), (2, 8), (6, 2), (6, 5), (3, 0), (3, 3), (4, 8), (3, 6), (0, 4), (4, 4), (0, 0), (1, 1), (0, 3), (1, 4), (0, 6), (6, 6), (6, 3)]
    ),
    Level(
        name="Level 134: Golden Path",
        width=9, height=6,
        start_x=5, start_y=3, start_dir=0,
        goal_x=8, goal_y=1,
        obstacles=[(1, 2), (7, 1), (8, 4), (2, 1), (1, 5), (2, 0), (6, 4), (3, 2), (2, 3), (4, 5), (8, 3), (7, 2), (8, 2), (7, 5)]
    ),
    Level(
        name="Level 135: Winding Meadow",
        width=6, height=8,
        start_x=3, start_y=3, start_dir=2,
        goal_x=0, goal_y=5,
        obstacles=[(5, 5), (3, 4), (4, 3), (3, 7), (1, 7), (2, 6), (5, 3), (1, 6), (2, 5), (1, 3), (3, 5)]
    ),
    Level(
        name="Level 136: Fierce Ridge",
        width=8, height=9,
        start_x=5, start_y=6, start_dir=1,
        goal_x=6, goal_y=0,
        obstacles=[(3, 4), (4, 6), (0, 2), (0, 5), (2, 2), (1, 6), (1, 3), (2, 8), (7, 4), (7, 7), (4, 8), (1, 5), (7, 3), (6, 7), (3, 2), (3, 5), (4, 4), (0, 3), (2, 0), (2, 3), (6, 3)]
    ),
    Level(
        name="Level 137: Tricky Journey",
        width=7, height=9,
        start_x=0, start_y=8, start_dir=3,
        goal_x=4, goal_y=5,
        obstacles=[(6, 2), (1, 2), (3, 4), (3, 1), (1, 8), (6, 4), (0, 6), (3, 0), (5, 6), (0, 5), (4, 8), (4, 1)]
    ),
    Level(
        name="Level 138: Deep Journey",
        width=7, height=9,
        start_x=1, start_y=6, start_dir=3,
        goal_x=5, goal_y=3,
        obstacles=[(0, 7), (3, 7), (1, 4), (0, 6), (1, 3)]
    ),
    Level(
        name="Level 139: Rocky Rock",
        width=8, height=7,
        start_x=4, start_y=1, start_dir=1,
        goal_x=7, goal_y=6,
        obstacles=[(3, 1), (0, 2), (0, 5), (1, 6), (7, 4), (7, 1), (6, 5), (3, 0), (3, 3), (5, 0), (3, 6), (1, 2), (0, 4), (6, 4), (3, 5), (1, 1), (2, 0), (0, 6), (2, 6)]
    ),
    Level(
        name="Level 140: Lost Savanna",
        width=9, height=9,
        start_x=0, start_y=1, start_dir=0,
        goal_x=6, goal_y=1,
        obstacles=[(4, 4), (0, 7), (8, 8), (8, 1), (5, 4), (7, 0), (4, 6), (1, 1), (6, 4), (7, 3), (7, 6), (3, 6), (4, 8), (8, 6), (8, 2), (1, 6), (6, 3), (7, 8)]
    ),
    Level(
        name="Level 141: Winding Rock",
        width=7, height=6,
        start_x=5, start_y=2, start_dir=3,
        goal_x=0, goal_y=2,
        obstacles=[(5, 5), (6, 5), (6, 1), (0, 3), (6, 4), (4, 2), (3, 0), (3, 3), (2, 2), (5, 3), (3, 5)]
    ),
    Level(
        name="Level 142: Winding Path",
        width=7, height=6,
        start_x=3, start_y=0, start_dir=3,
        goal_x=5, goal_y=5,
        obstacles=[(3, 4), (0, 0), (3, 1), (0, 2), (4, 5), (0, 5), (6, 3)]
    ),
    Level(
        name="Level 143: Perilous Trail",
        width=7, height=7,
        start_x=1, start_y=1, start_dir=2,
        goal_x=5, goal_y=5,
        obstacles=[(2, 4), (4, 3), (2, 0), (6, 4), (4, 5), (5, 0), (3, 6), (1, 0), (6, 3), (3, 5)]
    ),
    Level(
        name="Level 144: Sunny Dunes",
        width=7, height=6,
        start_x=6, start_y=3, start_dir=1,
        goal_x=1, goal_y=5,
        obstacles=[(1, 2), (4, 0), (4, 2), (3, 0), (5, 0), (4, 1), (3, 5), (5, 2)]
    ),
    Level(
        name="Level 145: Swift Journey",
        width=7, height=8,
        start_x=4, start_y=2, start_dir=1,
        goal_x=4, goal_y=6,
        obstacles=[(4, 4), (4, 1), (5, 4), (2, 0), (5, 1), (0, 6), (2, 3), (6, 7), (2, 6), (1, 3), (5, 2)]
    ),
    Level(
        name="Level 146: Tricky Sprint",
        width=9, height=7,
        start_x=2, start_y=0, start_dir=3,
        goal_x=8, goal_y=2,
        obstacles=[(7, 4), (6, 5), (0, 0), (7, 6), (1, 6)]
    ),
    Level(
        name="Level 147: Tangled Trail",
        width=7, height=7,
        start_x=2, start_y=6, start_dir=2,
        goal_x=0, goal_y=2,
        obstacles=[(4, 4), (2, 4), (6, 5), (6, 1), (5, 4), (4, 6), (2, 0), (1, 1), (1, 4), (0, 6), (6, 6), (2, 5), (3, 5)]
    ),
    Level(
        name="Level 148: Perilous Oasis",
        width=8, height=6,
        start_x=3, start_y=2, start_dir=3,
        goal_x=7, goal_y=1,
        obstacles=[(7, 4), (6, 2), (2, 4), (6, 0), (0, 0), (1, 5), (7, 0), (2, 0), (5, 1), (4, 2), (0, 2), (5, 0), (0, 5), (2, 2), (1, 0), (7, 5), (4, 1)]
    ),
    Level(
        name="Level 149: Tangled Oasis",
        width=6, height=7,
        start_x=2, start_y=1, start_dir=3,
        goal_x=2, goal_y=6,
        obstacles=[(0, 0), (1, 4), (3, 6), (0, 5), (2, 2), (3, 2)]
    ),
    Level(
        name="Level 150: Ancient Dunes",
        width=8, height=9,
        start_x=4, start_y=7, start_dir=2,
        goal_x=5, goal_y=1,
        obstacles=[(0, 4), (7, 7), (5, 3), (6, 8), (2, 0), (3, 0), (6, 7), (0, 2), (1, 0), (3, 2), (1, 3), (3, 5), (5, 2)]
    ),
    Level(
        name="Level 151: Perilous Labyrinth",
        width=7, height=6,
        start_x=0, start_y=0, start_dir=1,
        goal_x=6, goal_y=0,
        obstacles=[(0, 1), (2, 4), (6, 2), (1, 5), (2, 0), (4, 2), (3, 0), (2, 3), (4, 5), (3, 3), (2, 2), (2, 5), (3, 5)]
    ),
    Level(
        name="Level 152: Fierce Bush",
        width=8, height=9,
        start_x=1, start_y=5, start_dir=2,
        goal_x=7, goal_y=8,
        obstacles=[(5, 4), (4, 6), (6, 4), (0, 2), (3, 6), (6, 3), (3, 5), (2, 8)]
    ),
    Level(
        name="Level 153: Tricky Sprint",
        width=6, height=9,
        start_x=5, start_y=8, start_dir=0,
        goal_x=3, goal_y=1,
        obstacles=[(3, 8), (5, 5), (0, 4), (1, 5), (5, 3), (1, 8), (1, 1), (4, 2), (3, 0), (2, 3), (0, 5), (1, 0), (4, 1), (4, 7)]
    ),
    Level(
        name="Level 154: Fierce Labyrinth",
        width=7, height=6,
        start_x=2, start_y=3, start_dir=2,
        goal_x=6, goal_y=3,
        obstacles=[(6, 2), (6, 5), (4, 3), (3, 1), (6, 1), (1, 1), (5, 4), (5, 1), (3, 0)]
    ),
    Level(
        name="Level 155: Tricky Tree",
        width=8, height=7,
        start_x=0, start_y=0, start_dir=0,
        goal_x=4, goal_y=1,
        obstacles=[(2, 1), (5, 4), (6, 4), (3, 0), (2, 6), (3, 6), (5, 3), (1, 6), (5, 2)]
    ),
    Level(
        name="Level 156: Fierce Dunes",
        width=6, height=8,
        start_x=5, start_y=6, start_dir=2,
        goal_x=1, goal_y=2,
        obstacles=[(0, 7), (0, 0), (3, 1), (4, 6), (1, 4), (0, 5), (3, 6), (1, 0), (2, 5)]
    ),
    Level(
        name="Level 157: Silent Path",
        width=9, height=9,
        start_x=3, start_y=1, start_dir=0,
        goal_x=0, goal_y=6,
        obstacles=[(6, 2), (8, 4), (7, 1), (2, 7), (5, 8), (0, 0), (6, 1), (8, 0), (4, 2), (6, 7), (0, 2), (8, 3), (3, 3), (4, 8), (3, 6), (0, 8), (7, 8), (2, 8)]
    ),
    Level(
        name="Level 158: Winding Pond",
        width=6, height=8,
        start_x=4, start_y=6, start_dir=3,
        goal_x=1, goal_y=0,
        obstacles=[(0, 7), (0, 3), (1, 7), (5, 0), (2, 2), (5, 3), (1, 6), (2, 5), (4, 7)]
    ),
    Level(
        name="Level 159: Winding Journey",
        width=9, height=8,
        start_x=2, start_y=6, start_dir=0,
        goal_x=2, goal_y=1,
        obstacles=[(4, 0), (3, 4), (3, 1), (5, 4), (0, 2), (2, 5), (7, 4), (6, 5), (3, 0), (3, 3), (5, 0), (3, 6), (5, 3), (8, 2), (0, 1), (2, 4), (1, 2), (6, 1), (3, 5), (5, 2), (4, 4), (8, 7), (0, 6), (1, 7), (6, 0), (7, 5)]
    ),
    Level(
        name="Level 160: Wild Ridge",
        width=7, height=6,
        start_x=1, start_y=4, start_dir=3,
        goal_x=5, goal_y=0,
        obstacles=[(2, 4), (6, 2), (6, 5), (2, 0), (2, 3), (1, 0), (5, 3), (3, 2), (3, 5)]
    ),
    Level(
        name="Level 161: Muddy Ridge",
        width=6, height=9,
        start_x=1, start_y=2, start_dir=0,
        goal_x=4, goal_y=8,
        obstacles=[(0, 1), (5, 5), (0, 4), (3, 4), (2, 7), (4, 0), (5, 4), (2, 0), (1, 4), (2, 3), (0, 2), (5, 0), (5, 6), (4, 1), (5, 2)]
    ),
    Level(
        name="Level 162: Dry Meadow",
        width=8, height=9,
        start_x=7, start_y=8, start_dir=3,
        goal_x=5, goal_y=1,
        obstacles=[(3, 8), (5, 5), (1, 5), (0, 5), (7, 2), (5, 3)]
    ),
    Level(
        name="Level 163: Sunny Meadow",
        width=6, height=8,
        start_x=2, start_y=2, start_dir=2,
        goal_x=3, goal_y=6,
        obstacles=[(0, 7), (2, 4), (5, 5), (2, 1), (3, 1), (1, 1), (0, 3), (2, 0), (5, 1), (1, 4), (5, 7), (4, 5), (3, 3), (5, 0), (1, 0), (1, 6), (4, 7), (5, 2)]
    ),
    Level(
        name="Level 164: Deep Savanna",
        width=9, height=8,
        start_x=7, start_y=4, start_dir=1,
        goal_x=2, goal_y=7,
        obstacles=[(2, 4), (5, 5), (3, 4), (1, 1), (5, 1), (8, 3), (3, 6), (8, 6), (6, 0), (1, 6), (7, 5)]
    ),
    Level(
        name="Level 165: Swift Sprint",
        width=8, height=9,
        start_x=3, start_y=0, start_dir=3,
        goal_x=7, goal_y=4,
        obstacles=[(3, 8), (7, 7), (4, 3), (3, 1), (7, 0), (4, 6), (5, 1), (6, 7), (3, 3), (6, 0), (1, 3), (3, 5)]
    ),
    Level(
        name="Level 166: Tangled Canyon",
        width=8, height=9,
        start_x=7, start_y=8, start_dir=2,
        goal_x=1, goal_y=8,
        obstacles=[(2, 4), (5, 5), (0, 4), (6, 0), (4, 3), (5, 7), (3, 6), (1, 0), (2, 8)]
    ),
    Level(
        name="Level 167: Golden Savanna",
        width=6, height=8,
        start_x=1, start_y=3, start_dir=0,
        goal_x=5, goal_y=7,
        obstacles=[(0, 1), (0, 7), (2, 4), (4, 3), (0, 0), (0, 3), (2, 0), (5, 1), (0, 6), (3, 0), (1, 7), (3, 3), (5, 0), (0, 5), (3, 6), (4, 1), (4, 7)]
    ),
    Level(
        name="Level 168: Dry Oasis",
        width=6, height=9,
        start_x=0, start_y=1, start_dir=2,
        goal_x=2, goal_y=5,
        obstacles=[(4, 4), (1, 2), (0, 4), (3, 4), (5, 8), (4, 3), (1, 1), (5, 1), (5, 7), (0, 2), (2, 6), (4, 8), (0, 5), (3, 2), (1, 3)]
    ),
    Level(
        name="Level 169: Secret Dunes",
        width=8, height=6,
        start_x=0, start_y=5, start_dir=0,
        goal_x=4, goal_y=0,
        obstacles=[(4, 4), (0, 1), (7, 1), (6, 5), (4, 3), (1, 1), (0, 3), (5, 1), (5, 0), (6, 3), (4, 1), (5, 2)]
    ),
    Level(
        name="Level 170: Swift Bush",
        width=7, height=7,
        start_x=4, start_y=5, start_dir=0,
        goal_x=1, goal_y=2,
        obstacles=[(0, 1), (4, 4), (2, 4), (6, 0), (2, 1), (1, 1), (2, 3), (3, 3), (0, 5), (2, 2), (2, 5), (4, 1), (3, 5), (5, 2)]
    ),
    Level(
        name="Level 171: Dry Journey",
        width=8, height=8,
        start_x=6, start_y=0, start_dir=0,
        goal_x=2, goal_y=6,
        obstacles=[(0, 4), (1, 4), (5, 7), (0, 6), (7, 6), (6, 3)]
    ),
    Level(
        name="Level 172: Silent Meadow",
        width=6, height=9,
        start_x=5, start_y=2, start_dir=2,
        goal_x=1, goal_y=6,
        obstacles=[(2, 4), (5, 5), (1, 2), (3, 4), (2, 2), (5, 4), (1, 8), (2, 0), (0, 3), (1, 7), (5, 0), (5, 6), (4, 8), (3, 6), (5, 3), (3, 5)]
    ),
    Level(
        name="Level 173: Golden Meadow",
        width=6, height=7,
        start_x=0, start_y=6, start_dir=1,
        goal_x=4, goal_y=3,
        obstacles=[(0, 4), (0, 0), (3, 1), (5, 4), (1, 1), (5, 1), (1, 4), (4, 5), (3, 3), (2, 6), (5, 6), (0, 5), (3, 6), (1, 0), (4, 1), (5, 2)]
    ),
    Level(
        name="Level 174: Secret Plains",
        width=8, height=7,
        start_x=6, start_y=2, start_dir=2,
        goal_x=0, goal_y=0,
        obstacles=[(3, 4), (4, 3), (5, 4), (0, 2), (2, 2), (1, 3), (7, 4), (6, 5), (3, 0), (3, 3), (5, 6), (5, 3), (0, 1), (2, 4), (1, 2), (6, 1), (6, 4), (4, 1), (2, 0), (1, 4), (6, 6)]
    ),
    Level(
        name="Level 175: Distant River",
        width=6, height=9,
        start_x=2, start_y=2, start_dir=2,
        goal_x=2, goal_y=6,
        obstacles=[(4, 4), (3, 8), (1, 2), (2, 4), (2, 1), (0, 0), (5, 1), (5, 7), (3, 3), (1, 0), (1, 3), (3, 5)]
    ),
    Level(
        name="Level 176: Perilous Maze",
        width=8, height=8,
        start_x=0, start_y=6, start_dir=1,
        goal_x=6, goal_y=2,
        obstacles=[(7, 4), (2, 1), (7, 7), (3, 4), (5, 4), (1, 4), (5, 6), (6, 0), (4, 7), (3, 5), (5, 2)]
    ),
    Level(
        name="Level 177: Lost Ridge",
        width=9, height=6,
        start_x=2, start_y=1, start_dir=3,
        goal_x=8, goal_y=5,
        obstacles=[(3, 1), (5, 1), (4, 2), (1, 4), (7, 3), (7, 5)]
    ),
    Level(
        name="Level 178: Winding Cave",
        width=8, height=9,
        start_x=1, start_y=7, start_dir=2,
        goal_x=6, goal_y=2,
        obstacles=[(5, 5), (3, 4), (6, 5), (5, 8), (1, 1), (1, 8), (6, 3), (7, 2), (6, 0), (1, 6), (2, 5), (1, 3), (3, 5)]
    ),
    Level(
        name="Level 179: Fierce Canyon",
        width=8, height=9,
        start_x=1, start_y=4, start_dir=3,
        goal_x=5, goal_y=4,
        obstacles=[(3, 4), (4, 6), (5, 7), (0, 2), (1, 0), (0, 8), (2, 5), (7, 4), (4, 2), (4, 5), (3, 3), (2, 7), (1, 5), (1, 8), (6, 4), (6, 7), (4, 7), (6, 0), (6, 6), (7, 5)]
    ),
    Level(
        name="Level 180: Tangled Meadow",
        width=7, height=8,
        start_x=4, start_y=1, start_dir=2,
        goal_x=0, goal_y=7,
        obstacles=[(0, 1), (1, 1), (5, 3), (2, 0), (5, 4), (4, 2), (0, 6), (1, 0), (2, 5)]
    ),
    Level(
        name="Level 181: Dry Crossing",
        width=7, height=8,
        start_x=4, start_y=2, start_dir=1,
        goal_x=2, goal_y=4,
        obstacles=[(0, 7), (1, 2), (6, 5), (4, 3), (3, 1), (1, 5), (1, 4), (5, 7), (2, 3), (3, 0), (3, 3), (6, 0), (1, 6), (5, 2)]
    ),
    Level(
        name="Level 182: Deep Oasis",
        width=9, height=9,
        start_x=8, start_y=7, start_dir=3,
        goal_x=2, goal_y=3,
        obstacles=[(3, 4), (3, 1), (5, 4), (0, 2), (1, 6), (2, 5), (7, 4), (6, 2), (6, 5), (4, 2), (3, 0), (5, 0), (3, 6), (0, 7), (8, 8), (6, 1), (1, 8), (7, 0), (7, 3), (4, 7), (3, 8), (8, 4), (5, 8), (2, 0), (0, 6), (2, 6), (7, 2), (6, 0), (7, 5)]
    ),
    Level(
        name="Level 183: Sunny Meadow",
        width=9, height=7,
        start_x=1, start_y=0, start_dir=0,
        goal_x=8, goal_y=3,
        obstacles=[(6, 2), (8, 0), (0, 6), (7, 3), (0, 2), (5, 3), (7, 5)]
    ),
    Level(
        name="Level 184: Muddy Savanna",
        width=8, height=7,
        start_x=0, start_y=3, start_dir=1,
        goal_x=7, goal_y=5,
        obstacles=[(7, 4), (4, 0), (6, 5), (0, 0), (6, 1), (1, 1), (2, 0), (1, 4), (4, 5), (7, 2), (2, 2), (1, 6), (4, 1)]
    ),
    Level(
        name="Level 185: Rocky Maze",
        width=7, height=9,
        start_x=1, start_y=3, start_dir=0,
        goal_x=6, goal_y=8,
        obstacles=[(0, 1), (4, 3), (1, 5), (5, 1), (2, 3), (2, 6), (4, 1)]
    ),
    Level(
        name="Level 186: Hidden Meadow",
        width=9, height=7,
        start_x=0, start_y=2, start_dir=0,
        goal_x=7, goal_y=6,
        obstacles=[(2, 4), (6, 2), (0, 4), (7, 1), (0, 0), (2, 0), (6, 4), (4, 2), (1, 4), (5, 3), (8, 2), (6, 3), (8, 5)]
    ),
    Level(
        name="Level 187: Muddy Sprint",
        width=6, height=7,
        start_x=5, start_y=2, start_dir=2,
        goal_x=1, goal_y=6,
        obstacles=[(2, 4), (3, 4), (1, 5), (3, 1), (4, 3), (5, 4), (0, 0), (3, 0), (0, 2), (5, 0), (5, 6), (2, 6), (3, 6), (3, 5)]
    ),
    Level(
        name="Level 188: Fierce Journey",
        width=8, height=9,
        start_x=0, start_y=5, start_dir=2,
        goal_x=7, goal_y=0,
        obstacles=[(0, 7), (2, 4), (5, 5), (7, 1), (6, 5), (4, 3), (5, 8), (1, 5), (1, 1), (3, 7), (6, 4), (6, 7), (4, 5), (3, 3), (1, 7), (3, 6), (0, 8)]
    ),
    Level(
        name="Level 189: Dry Cave",
        width=9, height=9,
        start_x=5, start_y=5, start_dir=0,
        goal_x=0, goal_y=3,
        obstacles=[(4, 1), (6, 1), (6, 8), (7, 0), (5, 4), (5, 1), (5, 7), (4, 5), (8, 6), (1, 0), (8, 2), (1, 6), (1, 3), (7, 8), (2, 8)]
    ),
    Level(
        name="Level 190: Dusty Journey",
        width=7, height=9,
        start_x=0, start_y=2, start_dir=2,
        goal_x=2, goal_y=8,
        obstacles=[(3, 4), (5, 7), (0, 8), (6, 5), (6, 8), (3, 0), (5, 6), (4, 8), (0, 4), (2, 7), (1, 5), (3, 2), (4, 1), (4, 7), (5, 2), (4, 4), (3, 8), (5, 5), (0, 0), (5, 8), (0, 6), (6, 0)]
    ),
    Level(
        name="Level 191: Winding Journey",
        width=9, height=8,
        start_x=0, start_y=6, start_dir=3,
        goal_x=8, goal_y=5,
        obstacles=[(4, 3), (4, 6), (5, 1), (5, 7), (2, 2), (1, 6), (2, 5), (6, 2), (4, 2), (3, 3), (2, 7), (1, 5), (6, 1), (7, 0), (7, 6), (3, 2), (4, 1), (4, 4), (8, 4), (0, 0), (1, 1), (1, 7), (2, 6)]
    ),
    Level(
        name="Level 192: Golden River",
        width=6, height=9,
        start_x=0, start_y=8, start_dir=0,
        goal_x=1, goal_y=0,
        obstacles=[(2, 4), (1, 2), (5, 5), (2, 7), (0, 0), (5, 1), (0, 2), (1, 3), (4, 7), (2, 8)]
    ),
    Level(
        name="Level 193: Tricky Valley",
        width=9, height=8,
        start_x=1, start_y=0, start_dir=1,
        goal_x=8, goal_y=6,
        obstacles=[(4, 0), (1, 5), (6, 1), (0, 3), (2, 0), (0, 6), (7, 3), (4, 5), (3, 2)]
    ),
    Level(
        name="Level 194: Thirsty Journey",
        width=9, height=6,
        start_x=2, start_y=2, start_dir=2,
        goal_x=6, goal_y=1,
        obstacles=[(0, 1), (2, 4), (5, 5), (8, 4), (4, 0), (5, 1), (1, 4), (8, 0), (6, 3), (0, 5), (3, 2), (2, 5), (4, 1), (8, 5), (5, 2)]
    ),
    Level(
        name="Level 195: Ancient River",
        width=6, height=7,
        start_x=5, start_y=3, start_dir=0,
        goal_x=2, goal_y=6,
        obstacles=[(4, 0), (2, 1), (3, 4), (4, 3), (1, 5), (5, 4), (4, 6), (2, 0), (2, 2), (1, 0), (2, 5)]
    ),
    Level(
        name="Level 196: Golden River",
        width=8, height=7,
        start_x=0, start_y=0, start_dir=3,
        goal_x=6, goal_y=2,
        obstacles=[(1, 2), (7, 1), (2, 1), (1, 1), (7, 0), (4, 6), (1, 4), (7, 3), (0, 6), (1, 0), (2, 3), (2, 2), (6, 6), (1, 6)]
    ),
    Level(
        name="Level 197: Tricky Savanna",
        width=7, height=8,
        start_x=2, start_y=7, start_dir=2,
        goal_x=1, goal_y=0,
        obstacles=[(0, 7), (1, 3), (1, 5), (3, 7), (6, 4), (2, 3), (0, 2), (1, 7), (3, 3), (0, 5), (6, 0), (2, 5), (4, 1)]
    ),
    Level(
        name="Level 198: Winding Oasis",
        width=7, height=9,
        start_x=4, start_y=1, start_dir=1,
        goal_x=2, goal_y=8,
        obstacles=[(4, 0), (3, 4), (4, 3), (2, 5), (6, 5), (3, 0), (4, 5), (3, 3), (5, 6), (0, 7), (1, 2), (1, 5), (6, 1), (3, 2), (3, 5), (3, 8), (0, 0), (2, 0), (2, 3), (6, 0)]
    ),
    Level(
        name="Level 199: Swift Crossing",
        width=7, height=7,
        start_x=1, start_y=6, start_dir=2,
        goal_x=6, goal_y=0,
        obstacles=[(6, 2), (2, 4), (0, 4), (1, 2), (1, 5), (3, 1), (5, 4), (0, 6), (1, 0), (0, 2), (2, 5), (0, 5), (6, 6), (6, 3), (4, 1), (3, 5), (5, 2)]
    ),
    Level(
        name="Level 200: Tall Crossing",
        width=8, height=8,
        start_x=0, start_y=6, start_dir=1,
        goal_x=5, goal_y=3,
        obstacles=[(4, 3), (5, 4), (4, 6), (0, 2), (1, 0), (1, 6), (2, 5), (4, 2), (3, 0), (5, 0), (5, 6), (3, 6), (2, 4), (2, 1), (7, 0), (7, 3), (6, 7), (3, 5), (5, 2), (0, 0), (2, 0), (2, 3)]
    ),
]


# --- Dynamically assigned Cheetah names ---
cheetah_words = [
    "Speedy Sprint", "Gazelle Chase", "Fast Paws", "Golden Coat",
    "Swift Hunter", "Rapid Race", "Cheetah Bound", "Prowling Path",
    "Quick Reflexes", "Turbo Trot", "Feline Flash", "Wind Runner",
    "Spotted Dash", "Savanna Run", "Jungle Sprint", "Sneaky Steps",
    "Quiet Approach", "Sudden Burst", "Running Free", "Lightning Speed",
    "Big Cat Leap", "Furry Friend", "Chase the Target", "Speed Demon",
    "Hunting Grounds", "Dusty Dash", "River Jump", "Mighty Paws",
    "Hidden Spotted", "Fastest Cat", "Racing Heart", "Catch Me!",
    "Cheetah Trail", "Sunny Sprint", "Morning Run", "Twilight Dash",
    "Midnight Prowl", "Starry Sprint", "Speedy Maneuver", "Swift Turn",
    "Agile Escape", "Quick Dodge", "Cheetah's Secret", "Spotted Hero",
    "Golden Speed", "Savanna Dash", "Jungle Hunter", "Lightning Leap",
    "Feline Grace", "Turbo Paws"
]

for i, lvl in enumerate(LEVELS):
    lvl.name_giraffe = lvl.name
    # Keep the 'Level X: ' prefix but use the cheetah words
    prefix = f"Level {i+1}: "
    word = cheetah_words[i % len(cheetah_words)]
    lvl.name_cheetah = prefix + word
