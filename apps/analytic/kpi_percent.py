
def kpi_percent(score: int) -> int:
    ranges = (
        ((95, 100), 100),
        ((89, 94), 90),
        ((84, 88), 80),
        ((78, 83), 70),
        ((72, 77), 60),
        ((66, 71), 50),
        ((60, 65), 40),
        ((54, 59), 30),
        ((48, 53), 20),
        ((42, 47), 10),
    )
    for (low, high), percent in ranges:
        if low <= score <= high:
            return percent
    return 0  # agar past bo'lsa