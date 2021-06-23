import random

num = 5
with open("tmp.txt", "r") as file:
    for name in file.readlines():
        dice = random.randint(0,2)
        if dice <= 1:
            color = "bg-red"
            checked = ""
            active = ""
        else:
            color = "bg-green"
            checked = " checked"
            active = "active"
        print(
            f"""
                            <tr class="{color}">
                                <td></td>
                                <td><a href="member_profile_3.html" class="fs-20">{name.strip()}</a></td>
                                <td>
                                    <label for="defaultCheck{num}" class="{active}"></label>
                                    <input class="form-check-input m-l-20" type="checkbox" value="" id="defaultCheck{num}"{checked}>
                                </td>
                            </tr>"""
        )
        num = num + 1