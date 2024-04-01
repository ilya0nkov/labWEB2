import requests


def requests():
    while True:
        command = [i for i in input("Введите запрос:\n").split()]
        response = ""
        if command[0].__eq__("create"):
            response = requests.post(f"http://{HOST}:{PORT}/notes/",
                                     params={"note_text": command[1], "token": command[2]})
        if command[0].__eq__("get_note_info"):
            response = requests.get(f"http://{HOST}:{PORT}/notes/{command[1]}/note_info/",
                                    params={"note_id": command[1], "token": command[2]})
        if command[0].__eq__("get_note_text"):
            response = requests.get(f"http://{HOST}:{PORT}/notes/{command[1]}/note_text/",
                                    params={"note_id": command[1], "token": command[2]})
        if command[0].__eq__("get_list_notes"):
            response = requests.get(f"http://{HOST}:{PORT}/notes/",
                                    params={"token": command[1]})
        if command[0].__eq__("edit_note_text"):
            response = requests.put(f"http://{HOST}:{PORT}/notes/{command[1]}/",
                                    params={"note_id": command[1], "text": command[2], "token": command[3]})
        if command[0].__eq__("delete_note"):
            response = requests.delete(f"http://{HOST}:{PORT}/notes/{command[1]}/",
                                       params={"note_id": command[1], "token": command[2]})

        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.text}\n")


# сначала запустить labWEB1/main.py
if __name__ == '__main__':
    HOST = "localhost"
    PORT = 8080

    requests()