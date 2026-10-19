
import csv
import os
import uuid
from datetime import datetime

FILE_NAME = "stadium_tickets.csv"

# تعریف مسابقات
matches = {
    "1": {
        "name": "استقلال - پرسپولیس",
        "date": "2026-11-20"
    },
    "2": {
        "name": "تراکتور - سپاهان",
        "date": "2026-11-25"
    }
}

# قیمت و ظرفیت هر جایگاه
seats = {
    "1": {"name": "جایگاه ویژه", "price": 500000, "capacity": 100},
    "2": {"name": "جایگاه روبه‌رو", "price": 300000, "capacity": 500},
    "3": {"name": "پشت دروازه", "price": 150000, "capacity": 1000}
}

fields = [
    "ticket_id", "buyer", "match", "date",
    "seat", "price", "purchase_time"
]

# ساخت فایل اطلاعات در اولین اجرا
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()


def get_tickets():
    with open(FILE_NAME, "r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def save_ticket(ticket):
    with open(FILE_NAME, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow(ticket)


def show_matches():
    print("\n--- مسابقات ---")
    for key, match in matches.items():
        print(f"{key}. {match['name']} | تاریخ: {match['date']}")


def show_seats():
    print("\n--- جایگاه‌ها ---")
    for key, seat in seats.items():
        print(
            f"{key}. {seat['name']} | "
            f"قیمت: {seat['price']:,} تومان | "
            f"ظرفیت کل: {seat['capacity']}"
        )


def sell_ticket():
    show_matches()
    match_key = input("شماره مسابقه: ").strip()

    if match_key not in matches:
        print("شماره مسابقه معتبر نیست.")
        return

    show_seats()
    seat_key = input("شماره جایگاه: ").strip()

    if seat_key not in seats:
        print("شماره جایگاه معتبر نیست.")
        return

    buyer = input("نام و نام خانوادگی خریدار: ").strip()

    if not buyer:
        print("نام خریدار الزامی است.")
        return

    match = matches[match_key]
    seat = seats[seat_key]
    tickets = get_tickets()

    # شمارش بلیت‌های فروخته‌شده برای همین مسابقه و جایگاه
    sold = sum(
        1 for t in tickets
        if t["match"] == match["name"]
        and t["seat"] == seat["name"]
    )

    if sold >= seat["capacity"]:
        print("ظرفیت این جایگاه تکمیل شده است.")
        return

    ticket = {
        "ticket_id": uuid.uuid4().hex[:10].upper(),
        "buyer": buyer,
        "match": match["name"],
        "date": match["date"],
        "seat": seat["name"],
        "price": seat["price"],
        "purchase_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    save_ticket(ticket)

    print("\n===== بلیت صادر شد =====")
    print("شماره بلیت:", ticket["ticket_id"])
    print("خریدار:", ticket["buyer"])
    print("مسابقه:", ticket["match"])
    print("تاریخ:", ticket["date"])
    print("جایگاه:", ticket["seat"])
    print(f"قیمت: {ticket['price']:,} تومان")
    print("=========================")


def show_report():
    tickets = get_tickets()

    print("\n--- گزارش فروش ---")
    print("تعداد کل بلیت‌های فروخته‌شده:", len(tickets))

    revenue = sum(int(t["price"]) for t in tickets)
    print(f"مجموع فروش: {revenue:,} تومان")

    for ticket in tickets:
        print(
            f"{ticket['ticket_id']} | {ticket['buyer']} | "
            f"{ticket['match']} | {ticket['seat']} | "
            f"{int(ticket['price']):,} تومان"
        )


while True:
    print("\n===== سیستم فروش بلیت ورزشگاه =====")
    print("1. نمایش مسابقات")
    print("2. فروش بلیت")
    print("3. گزارش فروش")
    print("4. خروج")

    choice = input("یک گزینه انتخاب کن: ").strip()

    if choice == "1":
        show_matches()
    elif choice == "2":
        sell_ticket()
    elif choice == "3":
        show_report()
    elif choice == "4":
        print("برنامه پایان یافت.")
        break
    else:
        print("گزینه نامعتبر است. عدد 1 تا 4 را وارد کن.")
