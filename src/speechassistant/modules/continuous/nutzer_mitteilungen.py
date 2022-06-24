import datetime

from core import ModuleWrapper

INTERVALL = 2


def run(core: ModuleWrapper, profile):
    now = datetime.datetime.now()
    users = core.data_base.user_interface.get_users()

    queue_birthdays_of_system_user(core, now, users)

    if now.month == 12 and now.day == 24:
        queue_christmas_wishes(core, now, users)
    elif now.month == 1 and now.day == 1:
        queue_new_years_wishes(core, now, users)


def queue_christmas_wishes(
    core: ModuleWrapper, now: datetime, users: list[dict]
) -> None:
    for user in users:
        expiration_date: str = f"{now.year}.12.26:00:00:00"
        text: str = f'Frohe Weihnachten, {user["name"]}!'
        core.data_base.user_interface.add_user_notification(
            user["id"], text, expiration_date
        )


def queue_new_years_wishes(
    core: ModuleWrapper, now: datetime, users: list[dict]
) -> None:
    for user in users:
        expiration_date: str = f"{now.year}.01.02:00:00:00"
        core.data_base.user_interface.add_user_notification(
            user["id"],
            f'Ein erfolgreiches neues Jahr wünsch ich dir, {user["name"]}!',
            expiration_date,
        )


def queue_birthdays_of_system_user(
    core: ModuleWrapper, now: datetime, users: list[dict]
) -> None:
    for user in users:
        birthdate = user["date_of_birth"]
        if is_today(now, birthdate):
            expiration_date: str = get_expiration_date_of_next_day(now)
            text: str = f'Alles gute zum Geburtstag, {user["name"]}!'
            core.data_base.user_interface.add_user_notification(
                user["id"], text, expiration_date
            )
            queue_birthday_of_system_user_for_other_system_user(
                core, user, expiration_date
            )


def queue_birthday_of_system_user_for_other_system_user(
    core: ModuleWrapper, birthday_user: dict, expiration_date: str
) -> None:
    for other_user in core.data_base.user_interface.get_users():
        if other_user["id"] != birthday_user["id"]:
            text: str = f'Denk dran, {birthday_user["name"]} hat heute Geburtstag!'
            core.data_base.user_interface.add_user_notification(
                other_user["id"], text, expiration_date
            )


def queue_foreign_birthdays(core: ModuleWrapper, user_id: dict, now: datetime) -> None:
    other_birthdays: list[
        dict
    ] = core.data_base.birthday_interface.get_today_birthdays()
    for birthday in other_birthdays:
        text: str = (
            f'{birthday["firstname"]} {birthday["lastname"]} hat heute Geburtstag und wird '
            f'{birthday["year"] - datetime.date.year} Jahre alt.'
        )
        expiration_date: str = get_expiration_date_of_next_day(now)
        core.data_base.user_interface.add_user_notification(
            user_id, text, expiration_date
        )


def get_expiration_date_of_next_day(now: datetime) -> str:
    return f"{now.year}.{now.month}.{now.day + 1}:00:00:00"


def is_today(now: datetime, birthday: dict) -> bool:
    return now.month == birthday["month"] and now.day == birthday["day"]
