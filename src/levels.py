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
