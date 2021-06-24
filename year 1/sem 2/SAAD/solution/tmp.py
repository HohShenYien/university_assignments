import random

num = 5
with open("tmp.txt", "r") as file:
    for name in file.readlines():
        print(f"""<tr class="one-row">
                        <td>{name.strip()}</td>
                        <td><a href="member_profile_3.html"><i class="fa fa-info-circle"></i></a></td>
                    </tr>""")