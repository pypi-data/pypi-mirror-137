import urllib
import requests


# Helper functions and constants

templateIcons = {
    "-note": "📝 ",
    "-alert": "🚨 ",
    "-caution": "⚠ ",
    "-warning": "💀 ",
    "-update": "✨ ",
    "-important": "❗ ",
    "-finish": "🏁 ",
    "-start": "🔰 ",
    "-done": "✅ ",
    "-bug": "🐞 ",
}


def add_icon_to_text(text):
    for lable in templateIcons.keys():
        if text.lower().startswith(lable):
            return (templateIcons[lable] + text.split(lable)[-1]).title()
    return text


# Main dakia class
class Dakia:
    def __init__(self, token=None, chatId=None, project="GEN") -> None:
        """
        token: Bot token from the newly created bot
        chatId: Chat Id of the group / channel in which you want the alert to be posted
        """
        self.token = token
        self.chatId = chatId
        self.project = project  # if not(project ==None) else ""
        # self.templateIcons = {
        #         '-note':"📝",
        #         '-alert':'🚨',
        #         '-caution':'⚠',
        #         '-warning':'💀',
        #         '-tip':'✨',
        #         '-important':'❗',
        #         '-finish':'🏁',
        #         '-start':'🔰',
        #         '-done':'✅'
        #     }

    def dak(self, msg: str = None, mtype="text", parse_mode="html"):
        """
        Send Message to the Telegram channel
        msg: str
        type: str
            text [Default] - plain text string
            table - Give a pandas DataFrame
            image - give path to image
            audio - give path to mp3 file
        parse_mode: str
            MarkdownV2 - sets parse_mode as markdown
            html [Default] - sets parse_mode as html for formated messages
        channel
            debug [Default] - messages sent to debug channel
        """
        response = False

        ### Various types of messages

        if mtype == "text":
            msg = add_icon_to_text(msg)
            msg = (
                msg + " #" + str(self.project).upper()[:5]
            )  # Force project name upto first 4 letters

            msg = urllib.parse.quote(msg, safe="")
            response = requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chatId}&text={msg}&parse_mode={parse_mode}"
            )

        if mtype == "table":
            # msg = pd.DataFrame(msg).to_string(index=False) #  Not needed as moved to individual jobs function
            msg = f"<pre>{msg}</pre>"
            response = requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chatId}&text={msg}&parse_mode=html"
            )

        if mtype == "image":
            data = {"chat_id": self.chatId}
            url = f"https://api.telegram.org/bot{self.token}/sendPhoto"
            with open(msg, "rb") as image_file:
                response = requests.post(url, data=data, files={"photo": image_file})

        if mtype == "audio":
            with open(msg, "rb") as audio:
                payload = {
                    "chat_id": self.chatId,
                    "title": "Audio Dashboard",
                    "parse_mode": "HTML",
                }
                files = {
                    "audio": audio.read(),
                }
                response = requests.post(
                    f"https://api.telegram.org/bot{self.token}/sendAudio",
                    data=payload,
                    files=files,
                )

        if mtype == "video":
            response = requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chatId}&text={msg}&parse_mode=html"
            )
        if mtype == "file":
            response = requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chatId}&text={msg}&parse_mode=html"
            )

        if response.status_code == 200:
            return True
        else:
            return False


# End of class
def main():
    pass


if __name__ == "__main__":
    main()
