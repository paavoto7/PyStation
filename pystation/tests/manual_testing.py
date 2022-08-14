from pystation.gui import station_gui


"""These are tests to be run manually for the testing of the tkinter features.
These are just some things to run and can be easily modified to the users liking"""
table = [
    [
        "LEGO® Star Wars™:The Skywalker Saga Deluxe Edition PS4 & PS5",
        "€52,46",
        "€69,95",
    ],
    ["WWE 2K22 for PS4™", "€38,47", "€69,95"],
    ["WWE 2K22 for PS5™", "€44,97", "€74,95"],
    ["Call of Duty®: Vanguard - Cross-Gen Bundle", "€39,97", "€79,95"],
    ["God of War™", "€9,97", "€19,95"],
    ["STAR WARS Jedi: Fallen Order™", "€9,99", "€49,95"],
    ["Grand Theft Auto V: Premium Edition", "€14,67", "€34,95"],
    ["The Quarry for PS4™", "€46,86", "€69,95"],
    ["The Quarry for PS5™", "€50,21", "€74,95"],
    ["Red Dead Redemption 2", "€23,98", "€59,95"],
    ["It Takes Two PS4™ & PS5™", "€19,97", "€39,95"],
]
t = [
    "LEGO® Star Wars™:The Skywalker Saga Deluxe Edition PS4 & PS5",
    "€52,46",
    "€69,95",
    "https://image.api.playstation.com/vulcan/ap/rnd/202207/1210/6zhGBKQpPrlLNI2a7EfALNs1.png?w=1920&thumb=true",
], [
    "WWE 2K22 for PS4™",
    "€38,47",
    "€69,95",
    "https://image.api.playstation.com/vulcan/ap/rnd/202205/2800/1inUo7VTdbmAD9c1efdZGB9R.png?w=1920&thumb=false",
]
print(t[0][3], t[0][0], t[0][1])
station_gui.display(t[0][3], t[0][0], t[0][1])
station_gui.multi_display(t)
