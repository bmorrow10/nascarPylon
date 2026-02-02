# src/views/cliView.py

def render_live(layout):
    header = layout["header"]
    print("=" * 50)
    print(f"{header['flag']:<10}  Lap {header['lap']}/{header['total']}")
    print("=" * 50)

    def render_row(car):
        # battle indicator for now just a star
        battle = "*" if car.get("battling", False) else " "
        interval = "LEADER" if car.get("interval") is None else f"+{car['interval']:.3f}"
        print(f"{battle} {car['position']:>2}  {car['car']:<3}  {car['driver']:<12}  {interval:>7}")

    for car in layout["fixed"]:
        render_row(car)

    print("-" * 50)

    for car in layout["scrolling"]:
        render_row(car)


def render_points(layout):
    header = layout.get("header", {})
    print("=" * 50)
    title = header.get("title", "NASCAR CUP SERIES POINTS")
    print(f"{title:^50}")
    print("=" * 50)

    for driver in layout["drivers"]:
        interval = "LEADER" if driver.get("pointsBack") == 0 else f"-{driver['pointsBack']}"
        print(f"{driver['position']:>2}  {driver['car']:<3}  {driver['driver']:<12}  {interval:>7}")


def render_schedule(layout):
    print("=" * 50)
    print(layout["header"].center(50))
    print("=" * 50)

    for race in layout["rows"]:
        # Add playoff indicator
        chaseMarker = "🏆" if race.get("isChase", False) else " "
        
        line = (
            f"{chaseMarker} {race['date']}  "
            f"{race['time']:<5}  "
            f"{race['name']:<30}  "
            f"{race['broadcast']:<5}  "
            f"{race['series']}"
        )

        print(line)

